import logging
import re

import requests

from .errors import ApiError, FetchError

SITE = "https://snowfl.com/"
REGEX_FOR_KEY = re.compile(r'findNextItem.*?"(.*?)"')
REGEX_FOR_JS = re.compile(r'((?:b.min.js).*)(?=")')
HEADERS = {"User-Agent": "Mozilla/5.0"}


logger = logging.getLogger(__name__)


def get_api_key() -> str:
    logger.info("Fetching API key")
    """
    Synchronously fetches the API key from the specified site.

    This function fetches the homepage of the site, extracts a JavaScript file link from the homepage,
    then fetches the JavaScript file and extracts the API key from it.

    Returns:
        str: The API key if found.

    Raises:
        FetchError: If there is an issue in fetching the homepage or the JS file.
        ApiError: If the API key cannot be found.
    """
    try:
        home = requests.get(url=SITE, headers=HEADERS)
        if home.status_code != 200:
            raise FetchError(f"Error in fetching homepage: Status {home.status_code}")
        home_text = home.text

        js_file_match = REGEX_FOR_JS.search(home_text)
        if not js_file_match:
            raise ApiError("JS file link not found in homepage")

        js_file_link = f"{SITE}{js_file_match.group(0)}"
        js_res = requests.get(js_file_link)
        if js_res.status_code != 200:
            raise FetchError(f"Error in fetching JS file: Status {js_res.status_code}")
        js_text = js_res.text

        api_key_match = REGEX_FOR_KEY.search(js_text)
        if not api_key_match:
            raise ApiError("API key not found in JS file")

        return api_key_match.group(1)

    except requests.exceptions.RequestException as e:
        logger.error("HTTP error occurred", exc_info=e)
        raise FetchError("Error during HTTP request") from e
    except Exception as e:
        logger.error("Unexpected error occurred", exc_info=e)
        raise
