import logging
import sys
from pathlib import Path

LOG_FILE = Path("search.log")

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
    ],
)

logger = logging.getLogger(__name__)


class GitHubAPIError(Exception):
    pass


class RateLimitError(GitHubAPIError):
    pass


class NetworkError(Exception):
    pass


class EmptyResponseError(Exception):
    pass


def handle(exc: Exception, context: str = "") -> None:
    msg = f"{context}: {exc}" if context else str(exc)
    logger.error(msg)