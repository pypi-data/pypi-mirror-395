# Copyright 2025 Edgar Ramirez
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Bitly tap class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from singer_sdk import Tap
from singer_sdk import typing as th

from tap_bitly import streams

if TYPE_CHECKING:
    from tap_bitly.client import BitlyStream


class TapBitly(Tap):
    """Singer tap for Bitly."""

    name = "tap-bitly"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "token",
            th.StringType,
            required=True,
            description="API Token for Bitly",
        ),
        th.Property(
            "include_paid_streams",
            th.BooleanType,
            default=False,
            description="Whether to sync paid streams",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Earliest datetime to get data from",
        ),
    ).to_dict()

    @override
    def discover_streams(self) -> list[BitlyStream[Any]]:
        bitly_streams = [
            streams.Groups(self),
            streams.Bitlinks(self),
            streams.BrandedShortDomains(self),
            streams.Campaigns(self),
            streams.Channels(self),
            streams.Organizations(self),
            streams.DailyBitlinkClicks(self),
            streams.MonthlyBitlinkClicks(self),
        ]

        if self.config.get("include_paid_streams"):
            bitly_streams.append(streams.Webhooks(self))

        return bitly_streams
