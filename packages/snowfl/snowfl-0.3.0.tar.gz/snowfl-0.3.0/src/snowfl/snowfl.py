import json
import logging
from typing import Any, Dict, Optional

import requests

from .lib import ApiError, FetchError, get_api_key

BASE_URL = "https://snowfl.com/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Snowfl:
    def __init__(self):
        self.api_key: Optional[str] = None

    def initialize(self):
        """
        Initialize the Snowfl instance by fetching the API key.
        """
        self.api_key = get_api_key()
        if self.api_key is None:
            raise ApiError("Failed to obtain API key.")

    def parse(
        self, query: str, sort: str = "NONE", include_nsfw: bool = False
    ) -> Dict[str, Any]:
        """
        Parse the given query using the Snowfl API.
        """
        if len(query) <= 2:
            raise FetchError("Query should be of length >= 3")

        sort_option = self.get_sort_url_segment(sort)
        include_nsfw_flag = 1 if include_nsfw else 0
        url = f"{BASE_URL}{self.api_key}/{query}{sort_option}{include_nsfw_flag}"
        logger.info(f"URL: {url}")

        res = requests.get(url=url, headers=HEADERS)

        if res.status_code != 200:
            raise FetchError(f"Failed to fetch data, HTTP status: {res.status_code}")

        data = json.loads(res.text)
        return {"status": 200, "message": "OK", "data": data}

    @staticmethod
    def get_sort_url_segment(sort_key: str) -> str:
        """
        Constructs the URL segment for sorting based on the provided sort key.
        """
        sort_options = {
            "MAX_SEED": "SEED",
            "MAX_LEECH": "LEECH",
            "SIZE_ASC": "SIZE_ASC",
            "SIZE_DSC": "SIZE",
            "RECENT": "DATE",
            "NONE": "NONE",
        }
        sort_type = sort_options.get(sort_key, "NONE")
        return f"/DH5kKsJw/0/{sort_type}/NONE/"

    def __str__(self):
        return f"Snowfl API Wrapper"

    def __repr__(self):
        return "Snowfl()"
