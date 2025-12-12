#!/usr/bin/env python

"""Update the OpenAPI schema from the Bitly API.

Copyright (c) 2025 Edgar Ramírez-Mondragón
"""

from __future__ import annotations

import http
import json
import logging
import pathlib
import sys
import urllib.request

OPENAPI_URL = "https://dev.bitly.com/v4/v4.json"
PATH = "tap_bitly/openapi/openapi.json"

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger()


def main() -> None:
    """Update the OpenAPI schema from the Bitly API."""
    logger.info("Updating OpenAPI schema from %s", OPENAPI_URL)
    with (
        pathlib.Path(PATH).open("w", encoding="utf-8") as f_out,
        urllib.request.urlopen(OPENAPI_URL) as f_req,
    ):
        if f_req.status != http.HTTPStatus.OK:
            logger.error("Failed to fetch OpenAPI spec: %s", f_req.reason)
            sys.exit()
        spec = json.load(f_req)
        content = json.dumps(spec, indent=2) + "\n"
        f_out.write(content)


if __name__ == "__main__":
    main()
