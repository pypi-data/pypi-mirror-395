import logging
import socket
import time
import urllib.request
from urllib.error import URLError

logger = logging.getLogger(__name__)


def download_with_retry(url, timeout=10, retries=5):
    for attempt in range(retries):
        try:
            logger.info(f"Downloading {url} (Attempt {attempt + 1}/{retries})")
            with urllib.request.urlopen(url, timeout=timeout) as response:  # nosec
                return response.read()
        except (URLError, socket.timeout) as e:
            logger.warning(f"Download failed: {e}. Retrying in 2 seconds...")
            if attempt == retries - 1:
                raise
            time.sleep(2)
    return None
