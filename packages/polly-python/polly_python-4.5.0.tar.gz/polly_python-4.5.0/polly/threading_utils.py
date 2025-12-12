from concurrent.futures import as_completed, ThreadPoolExecutor
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)


class FailureLimitError(Exception):
    pass


def for_each_threaded(
    items, fn, max_workers: int = 10, max_error_perc: float = 0, verbose=False
):
    """
    Runs 'fn' for each of the 'items' in multiple threads

    Any exception raised while calling fn is caught. If more
    than a certain percentage of calls to fn raise an exception then
    execution is terminated.  This percentage is specified by "max_error_perc"
    argument.

    """
    total_items = len(items)
    if total_items == 0:
        return

    total_errors = 0
    with ThreadPoolExecutor(max_workers=max_workers) as exec:
        futures_to_item = {exec.submit(fn, item): item for item in items}

        def cancel_futures():
            print("Cancelling remaining tasks")
            for f in futures_to_item:
                f.cancel()

        try:
            for i, future in tqdm(
                enumerate(as_completed(futures_to_item)),
                total=total_items,
                disable=(not verbose),
            ):
                try:
                    future.result()
                except Exception:
                    err_item = futures_to_item[future]
                    logger.exception(f"Exception occurred for {err_item}")
                    total_errors += 1
                    if total_errors / total_items > max_error_perc:
                        cancel_futures()
                        raise FailureLimitError(
                            f"Too many errors occurred: {total_errors} out of"
                            f" {i + 1} failed"
                        )
        except KeyboardInterrupt as e:
            cancel_futures()
            raise e
