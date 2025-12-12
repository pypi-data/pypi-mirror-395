from typing import Optional

import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

CHROME_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"


def configure_requests_session(
    retries: int = 5,
    backoff_factor: float = 0.3,
    status_forcelist: tuple[int] = (429, 500, 502, 503, 504),
    allowed_methods: tuple[str] = ("HEAD", "GET", "OPTIONS"),
    session: Optional[requests.Session] = None,
    session_headers: Optional[dict] = None,
) -> requests.Session:
    """
    Create or update a requests session with retry parameters. For a request to be retried, it must be in the
    statuc_forcelist and the method_whitelist

    :param retries: The max number of retries to perform
    :param backoff_factor: Amount of time to sleep between reties. URLLib uses the following algorithm
        {backoff factor} * (2 ** ({number of total retries} - 1))
    :param status_forcelist: List of http error codes to automatically retry
    :param allowed_methods: List of http methods to retry
    :param session: An optional pre-existing session to update instead of creating a new one.
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=allowed_methods,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    if not session.headers:
        session.headers = {"User-Agent": CHROME_USER_AGENT}
    if session_headers is not None:
        session.headers.update(session_headers)
    return session
