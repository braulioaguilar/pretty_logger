import json
import logging, curlify
from logger import configure_logging
import requests
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter


class APIError(Exception):
    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError status={}".format(self.status)


def make_request(endpoint, logger=None):
    """
      Makes an HTTP request using the requests library and logs details.
      Also converts the request to a cURL command for logging.
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    try:
        logger.info(f"Making API request to: {url}")

        response = requests.get(endpoint)
        curl_command = curlify.to_curl(response.request)
        logger.debug(f"Equivalent cURL command: {curl_command}")

        if response.status_code >= 400:
            raise APIError(response.status_code)

        # Log the HTTP response
        json_object = json.loads(response.text)
        json_formatted_str = json.dumps(json_object, indent=4, sort_keys=True)
        logger.info(f"Response received: {response.status_code}")
        logger.debug(f"Response body: {highlight(json_formatted_str, JsonLexer(), TerminalFormatter())}")

        return response
    except APIError as e:
        logger.error("API request failed, error: {e}")


if __name__ == "__main__":
    url = "https://api.chucknorris.io/jokes/random?category=music"

    # config logging based on env variables
    logger = configure_logging()
    data = make_request(url,logger=logger)
    print(data)
