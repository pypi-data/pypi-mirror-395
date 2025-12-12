import stat
import hashlib
import itertools
import logging
import math
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import os
from os import PathLike
import pathlib
from typing import Optional, Union
from urllib.parse import (
    parse_qs,
    quote,
    unquote,
    urlencode,
    urlparse,
    urlunparse,
)

from urllib.request import pathname2url, url2pathname
from tqdm import tqdm
from boto3.s3.transfer import TransferConfig
from s3transfer.utils import (
    ChunksizeAdjuster,
    OSUtils,
)
from botocore.exceptions import (
    ClientError,
)
from botocore.client import BaseClient

s3_transfer_config = TransferConfig()

logger = logging.getLogger(__name__)

MAX_CONCURRENCY = 10

# When uploading files at least this size, compare the ETags first and skip the upload
# if they're equal; copy the remote file onto itself if the metadata changes.
UPLOAD_ETAG_OPTIMIZATION_THRESHOLD = 1024


class URLParseError(ValueError):
    pass


def read_bytes(client: BaseClient, s3_uri: str) -> bytes:
    pk = _PhysicalKey.from_pathlike(s3_uri)
    response = client.get_object(Bucket=pk.bucket, Key=pk.path, VersionId=pk.version_id)
    return response["Body"].read()


def copy_file(
    src_uri: Union[str, PathLike],
    dest_uri: Union[str, PathLike],
    *,
    s3_client: BaseClient,
    disable_tqdm: bool = False,
    tqdm_desc=None,
) -> str:
    """
    Can be used to copy file from
    - local to s3
    - s3 to local
    - s3 to s3

    Implements the following
    - Multithreading
    - Multi-part uploads and downloads depending on size
    - Returns full s3 uri in response, including versionId (unlike `boto3.upload_file`)
    - Skips upload if local file has same md5sum as remote file
    - Tqdm progress bar

    Returns full destination URI
    E.g. 'file:///home/me/file.txt', 's3://path/to/file.txt?versionId=abcd'
    """
    transfer = _FileTransfer(src_uri, dest_uri, s3_client, disable_tqdm, tqdm_desc)
    return transfer.start()


def _fix_url(url):
    """Convert non-URL paths to file:// URLs"""
    # If it has a scheme, we assume it's a URL.
    if not url:
        raise ValueError("Empty URL")

    url = str(url)

    parsed = urlparse(url)
    if parsed.scheme and not os.path.splitdrive(url)[0]:
        return url

    fixed_url = pathlib.Path(url).expanduser().resolve().absolute().as_uri()

    # pathlib likes to remove trailing slashes, so add it back if needed.
    if url[-1:] in (os.sep, os.altsep) and not fixed_url.endswith("/"):
        fixed_url += "/"

    return fixed_url


class _PhysicalKey:
    __slots__ = ("bucket", "path", "version_id")

    def __init__(self, bucket: Optional[str], path: str, version_id: Optional[str]):
        """
        For internal use only; call from_path or from_url instead.
        """
        if bucket is not None and not isinstance(bucket, str):
            raise ValueError("Bucket must be None or a string")
        if not isinstance(path, str):
            raise ValueError("Path must be a string")
        if version_id is not None and not isinstance(version_id, str):
            raise ValueError("Version ID must be None or a string")

        if bucket is None:
            if path is None:
                raise ValueError("Local keys must have a path")
            if version_id is not None:
                raise ValueError("Local keys cannot have a version ID")
            if os.name == "nt":
                if "\\" in path:
                    raise ValueError("Paths must use / as a separator")
        else:
            if path.startswith("/"):
                raise ValueError("S3 paths must not start with '/'")

        self.bucket = bucket
        self.path = path
        self.version_id = version_id

    @classmethod
    def from_pathlike(cls, path: Union[str, PathLike]):
        return cls.from_url(_fix_url(path))

    @classmethod
    def from_url(cls, url):
        parsed = urlparse(url)

        if parsed.scheme == "s3":
            if not parsed.netloc:
                raise URLParseError("Missing bucket")
            bucket = parsed.netloc
            assert not parsed.path or parsed.path.startswith("/")
            path = unquote(parsed.path)[1:]
            # Parse the version ID the way the Java SDK does:
            # https://github.com/aws/aws-sdk-java/blob/master/aws-java-sdk-s3/src/main/java/com/amazonaws/services/s3/AmazonS3URI.java#L192
            query = parse_qs(parsed.query)
            version_id = query.pop("versionId", [None])[0]
            if query:
                raise URLParseError(f"Unexpected S3 query string: {parsed.query!r}")
            return cls(bucket, path, version_id)
        elif parsed.scheme == "file":
            if parsed.netloc not in ("", "localhost"):
                raise URLParseError("Unexpected hostname")
            if not parsed.path:
                raise URLParseError("Missing path")
            if not parsed.path.startswith("/"):
                raise URLParseError("Relative paths are not allowed")
            if parsed.query:
                raise URLParseError("Unexpected query")
            path = url2pathname(parsed.path)
            if parsed.path.endswith("/") and not path.endswith(os.path.sep):
                # On Windows, url2pathname loses the trailing `/`.
                path += os.path.sep
            return cls.from_path(path)
        else:
            raise URLParseError(f"Unexpected scheme: {parsed.scheme!r}")

    @classmethod
    def from_path(cls, path):
        path = os.fspath(path)
        new_path = os.path.realpath(path)
        # Use '/' as the path separator.
        if os.path.sep != "/":
            new_path = new_path.replace(os.path.sep, "/")
        # Add back a trailing '/' if the original path has it.
        if path.endswith(os.path.sep) or (
            os.path.altsep is not None and path.endswith(os.path.altsep)
        ):
            new_path += "/"
        return cls(None, new_path, None)

    def is_local(self):
        return self.bucket is None

    def looks_like_dir(self):
        return self.basename() == ""

    def join(self, rel_path):
        if self.version_id is not None:
            raise ValueError("Cannot append paths to URLs with a version ID")

        if os.name == "nt" and "\\" in rel_path:
            raise ValueError("Paths must use / as a separator")

        if self.path:
            new_path = self.path.rstrip("/") + "/" + rel_path.lstrip("/")
        else:
            new_path = rel_path.lstrip("/")
        return _PhysicalKey(self.bucket, new_path, None)

    def basename(self):
        return self.path.rsplit("/", 1)[-1]

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.bucket == other.bucket
            and self.path == other.path
            and self.version_id == other.version_id
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.bucket!r}, {self.path!r},"
            f" {self.version_id!r})"
        )

    def __str__(self):
        if self.bucket is None:
            return urlunparse(
                (
                    "file",
                    "",
                    pathname2url(self.path.replace("/", os.path.sep)),
                    None,
                    None,
                    None,
                )
            )
        else:
            if self.version_id is None:
                params = {}
            else:
                params = {"versionId": self.version_id}
            return urlunparse(
                (
                    "s3",
                    self.bucket,
                    quote(self.path),
                    None,
                    urlencode(params),
                    None,
                )
            )


class _WorkerContext:
    def __init__(self, progress, done, submit_task, s3_client):
        self.progress = progress
        self.done = done
        self.submit_task = submit_task
        self.s3_client = s3_client


class _FileTransfer:
    def __init__(
        self,
        src: Union[str, PathLike],
        dest: Union[str, PathLike],
        s3_client: BaseClient,
        disable_tqdm: bool = False,
        tqdm_desc: Optional[str] = None,
    ):
        self.src = _PhysicalKey.from_pathlike(src)
        self.dest = _PhysicalKey.from_pathlike(dest)
        self.s3_client = s3_client
        self.tqdm_desc = tqdm_desc
        self.disable_tqdm = disable_tqdm

        if self.src.looks_like_dir():
            raise ValueError(f"Expected file, got a directory: {self.src}")

        size, version_id = _get_size_and_version(self.src, self.s3_client)

        self.transfer_size = size

        if self.dest.looks_like_dir():
            self.dest = self.dest.join(self.src.basename())
        if self.src.version_id is None:
            self.src = _PhysicalKey(self.src.bucket, self.src.path, version_id)
        if self.dest.version_id:
            raise ValueError("Cannot set version_id on destination")

    def start(self) -> str:
        self._initialize()
        try:
            return self._transfer()
        finally:
            self._progress.close()

    def _initialize(self):
        self._lock = Lock()
        self._futures = deque()
        self._stopped = False
        self._progress = tqdm(
            desc=self.tqdm_desc,
            total=self.transfer_size,
            unit="B",
            unit_scale=True,
            disable=self.disable_tqdm,
            smoothing=0.1,
        )
        self._result = None
        self._executor = ThreadPoolExecutor(MAX_CONCURRENCY)

    def _progress_callback(self, bytes_transferred: int):
        if self._stopped:
            raise Exception("Interrupted")
        with self._lock:
            self._progress.update(bytes_transferred)

    def _submit_task(self, func, *args):
        future = self._executor.submit(func, *args)
        self._futures.append(future)

    def _worker(self, src: _PhysicalKey, dest: _PhysicalKey):
        def done_callback(key: _PhysicalKey):
            self._result = key

        ctx = _WorkerContext(
            progress=self._progress_callback,
            done=done_callback,
            submit_task=self._submit_task,
            s3_client=self.s3_client,
        )

        fro = "local" if src.is_local() else "remote"
        to = "local" if dest.is_local() else "remote"
        direction = (fro, to)

        if direction == ("local", "remote"):
            _upload_or_copy_file(
                ctx, self.transfer_size, src.path, dest.bucket, dest.path
            )

        elif direction == ("remote", "local"):
            _download_file(
                ctx, self.transfer_size, src.bucket, src.path, src.version_id, dest.path
            )

        elif direction == ("remote", "remote"):
            _copy_remote_file(
                ctx,
                self.transfer_size,
                src.bucket,
                src.path,
                src.version_id,
                dest.bucket,
                dest.path,
            )
        else:
            raise NotImplementedError(
                "Transfer for this combination of src"
                f" and dest is not implemented, src={src}, dest={dest}"
            )

    def _transfer(self) -> str:
        try:
            self._submit_task(self._worker, self.src, self.dest)

            while True:
                with self._lock:
                    if not self._futures:
                        break
                    future = self._futures.popleft()

                if future.cancelled():
                    continue

                try:
                    future.result()
                except (Exception, KeyboardInterrupt) as e:
                    for f in self._futures:
                        f.cancel()
                    self._futures.clear()
                    raise e
        finally:
            # Make sure all tasks exit quickly if the
            # main thread exits before they're done.
            self._stopped = True

        return str(self._result)


def _get_size_and_version(pk: _PhysicalKey, s3_client: BaseClient):
    """
    Gets size and version for the object at a given URL.

    Returns:
        size, version(str)
    """
    if pk.looks_like_dir():
        raise Exception("Invalid path: %r; cannot be a directory" % pk.path)

    version = None
    if pk.is_local():
        src_file = pathlib.Path(pk.path)
        if not src_file.is_file():
            raise Exception("Not a file: %r" % str(src_file))
        size = src_file.stat().st_size
    else:
        params = dict(Bucket=pk.bucket, Key=pk.path)
        if pk.version_id is not None:
            params.update(VersionId=pk.version_id)
        resp = s3_client.head_object(**params)
        size = resp["ContentLength"]
        version = resp.get("VersionId")
    return size, version


def _read_file_chunks(file, chunksize=s3_transfer_config.io_chunksize):
    return itertools.takewhile(bool, map(file.read, itertools.repeat(chunksize)))


def _calculate_etag(file_path: str) -> str:
    """
    Attempts to calculate a local file's ETag the way S3 does:
    - Normal uploads: MD5 of the file
    - Multi-part uploads: MD5 of the (binary) MD5s of the parts, dash, number of parts

    We can't know how the file was actually uploaded - but we're assuming it was done
    using the default settings, which we get from `s3_transfer_config`.
    """
    size = pathlib.Path(file_path).stat().st_size
    with open(file_path, "rb") as fd:
        if size < s3_transfer_config.multipart_threshold:
            contents = fd.read()
            etag = hashlib.md5(contents).hexdigest()
        else:
            adjuster = ChunksizeAdjuster()
            chunksize = adjuster.adjust_chunksize(
                s3_transfer_config.multipart_chunksize, size
            )

            hashes = []
            for contents in _read_file_chunks(fd, chunksize):
                hashes.append(hashlib.md5(contents).digest())
            etag = "%s-%d" % (hashlib.md5(b"".join(hashes)).hexdigest(), len(hashes))
    return '"%s"' % etag


def _upload_or_copy_file(
    ctx: _WorkerContext, size: int, src_path: str, dest_bucket: str, dest_path: str
):
    # Optimization: check if the remote file already exists and has the right ETag,
    # and skip the upload.
    if size >= UPLOAD_ETAG_OPTIMIZATION_THRESHOLD:
        try:
            params = dict(Bucket=dest_bucket, Key=dest_path)
            resp = ctx.s3_client.head_object(**params)
        except ClientError:
            # Destination doesn't exist, so fall through to the normal upload.
            pass
        else:
            # Check the ETag.
            dest_size = resp["ContentLength"]
            dest_etag = resp["ETag"]
            dest_version_id = resp.get("VersionId")
            if size == dest_size and resp.get("ServerSideEncryption") != "aws:kms":
                src_etag = _calculate_etag(src_path)
                if src_etag == dest_etag:
                    # Nothing more to do. We should not attempt to copy the object because
                    # that would cause the "copy object to itself" error.
                    ctx.progress(size)
                    ctx.done(_PhysicalKey(dest_bucket, dest_path, dest_version_id))
                    return  # Optimization succeeded.

    # If the optimization didn't happen, do the normal upload.
    _upload_file(ctx, size, src_path, dest_bucket, dest_path)


def _upload_file(
    ctx: _WorkerContext, size: int, src_path: str, dest_bucket: str, dest_key: str
):
    """
    For a small file, uploads it to s3 directly

    For a large file, creates multiple smaller tasks and
    submits them using `ctx.submit_task` to parent executor
    """
    if size < s3_transfer_config.multipart_threshold:
        with OSUtils().open_file_chunk_reader(src_path, 0, size, callbacks=[]) as fd:
            resp = ctx.s3_client.put_object(
                Body=fd,
                Bucket=dest_bucket,
                Key=dest_key,
            )

        version_id = resp.get("VersionId")  # Absent in unversioned buckets.
        ctx.progress(size)
        ctx.done(_PhysicalKey(dest_bucket, dest_key, version_id))
    else:
        resp = ctx.s3_client.create_multipart_upload(
            Bucket=dest_bucket,
            Key=dest_key,
        )
        upload_id = resp["UploadId"]

        adjuster = ChunksizeAdjuster()
        chunksize = adjuster.adjust_chunksize(
            s3_transfer_config.multipart_chunksize, size
        )

        chunk_offsets = list(range(0, size, chunksize))

        lock = Lock()
        remaining = len(chunk_offsets)
        parts = [None] * remaining

        def upload_part(i, start, end):
            nonlocal remaining
            part_id = i + 1
            with OSUtils().open_file_chunk_reader(
                src_path, start, end - start, [ctx.progress]
            ) as fd:
                part = ctx.s3_client.upload_part(
                    Body=fd,
                    Bucket=dest_bucket,
                    Key=dest_key,
                    UploadId=upload_id,
                    PartNumber=part_id,
                )
            with lock:
                ctx.progress(end - start)
                parts[i] = {"PartNumber": part_id, "ETag": part["ETag"]}
                remaining -= 1
                done = remaining == 0

            if done:
                resp = ctx.s3_client.complete_multipart_upload(
                    Bucket=dest_bucket,
                    Key=dest_key,
                    UploadId=upload_id,
                    MultipartUpload={"Parts": parts},
                )
                version_id = resp.get("VersionId")  # Absent in unversioned buckets.
                ctx.done(_PhysicalKey(dest_bucket, dest_key, version_id))

        for i, start in enumerate(chunk_offsets):
            end = min(start + chunksize, size)
            ctx.submit_task(upload_part, i, start, end)


def _copy_remote_file(
    ctx: _WorkerContext,
    size: int,
    src_bucket: str,
    src_key: str,
    src_version: str,
    dest_bucket: str,
    dest_key: str,
    extra_args=None,
):
    src_params = dict(Bucket=src_bucket, Key=src_key)
    if src_version is not None:
        src_params.update(VersionId=src_version)

    if size < s3_transfer_config.multipart_threshold:
        params = dict(
            CopySource=src_params,
            Bucket=dest_bucket,
            Key=dest_key,
        )

        if extra_args:
            params.update(extra_args)

        resp = ctx.s3_client.copy_object(**params)
        ctx.progress(size)
        version_id = resp.get("VersionId")  # Absent in unversioned buckets.
        ctx.done(_PhysicalKey(dest_bucket, dest_key, version_id))
    else:
        resp = ctx.s3_client.create_multipart_upload(
            Bucket=dest_bucket,
            Key=dest_key,
        )
        upload_id = resp["UploadId"]

        adjuster = ChunksizeAdjuster()
        chunksize = adjuster.adjust_chunksize(
            s3_transfer_config.multipart_chunksize, size
        )

        chunk_offsets = list(range(0, size, chunksize))

        lock = Lock()
        remaining = len(chunk_offsets)
        parts = [None] * remaining

        def upload_part(i, start, end):
            nonlocal remaining
            part_id = i + 1
            part = ctx.s3_client.upload_part_copy(
                CopySource=src_params,
                CopySourceRange=f"bytes={start}-{end - 1}",
                Bucket=dest_bucket,
                Key=dest_key,
                UploadId=upload_id,
                PartNumber=part_id,
            )
            with lock:
                parts[i] = {
                    "PartNumber": part_id,
                    "ETag": part["CopyPartResult"]["ETag"],
                }
                remaining -= 1
                done = remaining == 0

            ctx.progress(end - start)

            if done:
                resp = ctx.s3_client.complete_multipart_upload(
                    Bucket=dest_bucket,
                    Key=dest_key,
                    UploadId=upload_id,
                    MultipartUpload={"Parts": parts},
                )
                version_id = resp.get("VersionId")  # Absent in unversioned buckets.
                ctx.done(_PhysicalKey(dest_bucket, dest_key, version_id))

        for i, start in enumerate(chunk_offsets):
            end = min(start + chunksize, size)
            ctx.submit_task(upload_part, i, start, end)


def _download_file(
    ctx: _WorkerContext,
    size: int,
    src_bucket: str,
    src_key: str,
    src_version: str,
    dest_path: str,
):
    """
    Downloads S3 file to local
    """
    dest_file = pathlib.Path(dest_path)
    if dest_file.is_reserved():
        raise ValueError("Cannot download to %r: reserved file name" % dest_path)

    params = dict(Bucket=src_bucket, Key=src_key)

    dest_file.parent.mkdir(parents=True, exist_ok=True)

    with dest_file.open("wb") as f:
        fileno = f.fileno()
        is_regular_file = stat.S_ISREG(os.stat(fileno).st_mode)

    if src_version is not None:
        params.update(VersionId=src_version)

    part_size = s3_transfer_config.multipart_chunksize
    is_multi_part = (
        is_regular_file
        and size >= s3_transfer_config.multipart_threshold
        and size > part_size
    )
    part_numbers = range(math.ceil(size / part_size)) if is_multi_part else (None,)
    remaining_counter = len(part_numbers)
    remaining_counter_lock = Lock()

    def download_part(part_number):
        nonlocal remaining_counter

        with dest_file.open("r+b") as chunk_f:
            if part_number is not None:
                start = part_number * part_size
                end = min(start + part_size, size) - 1
                part_params = dict(params, Range=f"bytes={start}-{end}")
                chunk_f.seek(start)
            else:
                part_params = params

            resp = ctx.s3_client.get_object(**part_params)
            body = resp["Body"]
            while True:
                chunk = body.read(s3_transfer_config.io_chunksize)
                if not chunk:
                    break
                ctx.progress(chunk_f.write(chunk))

        with remaining_counter_lock:
            remaining_counter -= 1
            done = remaining_counter == 0
        if done:
            ctx.done(_PhysicalKey.from_path(dest_path))

    for part_number in part_numbers:
        ctx.submit_task(download_part, part_number)
