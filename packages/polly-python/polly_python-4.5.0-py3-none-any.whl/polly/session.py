from requests import Session
import os


def _package_exists(package_name):
    """Check if a package exists without importing it."""
    try:
        # For Python version >= python3.8
        from importlib.metadata import version as get_version

        get_version(package_name)
    except ImportError:
        # For Python version < python3.8
        try:
            import pkg_resources

            pkg_resources.get_distribution(package_name)
        except pkg_resources.DistributionNotFound:
            return False
    except Exception:
        return False

    return True


def _get_package_version(package_name):
    try:
        # for python version >= python3.8
        from importlib.metadata import version

        version = version("polly-python")
    except ImportError:
        # for python version < python3.8
        import pkg_resources

        version = pkg_resources.get_distribution("polly-python").version

    return version


class PollySession(Session):
    """
    This class contain function to create session for
    polly.

    ``Args:``
        |  ``token (str):`` token copy from polly.

    ``Returns:``
        |  None

    To use this function


    .. code::


            from polly.session import PollySession
            session = PollySession(token)

    """

    def __init__(self, TOKEN, env="polly"):
        Session.__init__(self)
        version = (
            _get_package_version("polly-python")
            if _package_exists("polly-python")
            else "dev"
        )
        client = os.getenv("POLLY_SERVICE")
        if client is not None:
            version = version + "/" + client
        else:
            version = version + "/local"

        self.token = TOKEN
        self.headers = {
            "Content-Type": "application/vnd.api+json",
            "x-api-key": f"{TOKEN}",
            "User-Agent": "polly-python/" + version,
        }
        self.env = env
        self.base_url = f"https://apis.{self.env}.elucidata.io"
        self.discover_url = f"https://api.discover.{self.env}.elucidata.io"
        self.atlas_domain_url = f"https://sarovar.{self.env}.elucidata.io"
