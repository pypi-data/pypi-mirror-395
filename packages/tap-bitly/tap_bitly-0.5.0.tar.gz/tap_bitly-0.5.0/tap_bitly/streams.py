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
"""Stream type classes for tap-bitly."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override
from urllib.parse import ParseResult, parse_qs

from singer_sdk import typing as th
from singer_sdk.pagination import BaseHATEOASPaginator

from tap_bitly.client import BitlyStream

if TYPE_CHECKING:
    from collections.abc import Iterable

    import requests
    from singer_sdk.helpers.types import Context


class BitlinksPaginator(BaseHATEOASPaginator):
    """Bitlinks paginator."""

    @override
    def get_next_url(self, response: requests.Response) -> str | None:
        return response.json().get("pagination", {}).get("next") or None


class Groups(BitlyStream[Any]):
    """Users stream."""

    name = "groups"
    path = "/v4/groups"
    primary_keys = ("guid",)
    records_jsonpath = "$.groups[*]"
    replication_key = None

    schema = th.PropertiesList(
        th.Property(
            "guid",
            th.StringType,
            description="The group's unique identifier.",
        ),
        th.Property(
            "name",
            th.StringType,
            description="The group's name.",
        ),
        th.Property(
            "references",
            th.ObjectType(
                th.Property("organization", th.StringType),
            ),
            description="Mapping of group references.",
        ),
        th.Property(
            "created",
            th.DateTimeType,
            description="The date and time the group was created.",
        ),
        th.Property(
            "modified",
            th.DateTimeType,
            description="The date and time the group was last modified.",
        ),
        th.Property(
            "bsds",
            th.ArrayType(th.StringType()),
            description="The group's branded short domains.",
        ),
        th.Property(
            "organization_guid",
            th.StringType,
            description="The group's organization's unique identifier.",
        ),
        th.Property(
            "is_active",
            th.BooleanType,
            description="Whether the group is active.",
        ),
        th.Property(
            "role",
            th.StringType,
            description="The group's role.",
        ),
    ).to_dict()

    @override
    def get_child_context(
        self,
        record: dict[str, Any],
        context: Context | None = None,
    ) -> dict[str, Any]:
        """Get child context for a record.

        Args:
            record: The record to get child context for.
            context: The parent context.

        Returns:
            The child context.
        """
        return {"group_guid": record["guid"]}


class Bitlinks(BitlyStream[ParseResult]):
    """Bitlinks stream."""

    name = "bitlinks"
    path = "/v4/groups/{group_guid}/bitlinks"
    primary_keys = ("id",)
    records_jsonpath = "$.links[*]"
    replication_key = None
    parent_stream_type = Groups

    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
            description="The bitlink's unique identifier.",
        ),
        th.Property(
            "created_at",
            th.DateTimeType,
            description="The date and time the bitlink was created.",
        ),
        th.Property("link", th.StringType, description="The bitlink's URL."),
        th.Property(
            "custom_bitlinks",
            th.ArrayType(th.StringType()),
            description="The bitlink's custom bitlinks.",
        ),
        th.Property("long_url", th.StringType, description="The bitlink's URL."),
        th.Property("title", th.StringType, description="The bitlink's title."),
        th.Property(
            "archived",
            th.BooleanType,
            description="Whether the bitlink is archived.",
        ),
        th.Property("created_by", th.StringType, description="The bitlink's creator."),
        th.Property("client_id", th.StringType, description="The bitlink's client ID."),
        th.Property(
            "tags",
            th.ArrayType(th.StringType()),
            description="The bitlink's tags.",
        ),
        th.Property(
            "deeplinks",
            th.ArrayType(th.StringType()),
            description="The bitlink's deeplinks.",
        ),
        th.Property(
            "references",
            th.ObjectType(th.Property("group", th.StringType)),
            description="Mapping of bitlink references.",
        ),
        th.Property("group_guid", th.StringType, description="The bitlink's group."),
    ).to_dict()

    @override
    def get_new_paginator(self) -> BitlinksPaginator:
        return BitlinksPaginator()

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: ParseResult | None,
    ) -> dict[str, Any]:
        """Get URL parameters.

        Args:
            context: The stream sync context.
            next_page_token: The next page token.

        Returns:
            The URL parameters.
        """
        params = {
            "archived": "both",
            "size": self._page_size,
        }
        if next_page_token:
            params.update(parse_qs(next_page_token.query))

        return params

    @override
    def get_child_context(
        self,
        record: dict[str, Any],
        context: Context | None,
    ) -> dict[str, Any]:
        return {"bitlink": record["id"]}


class BrandedShortDomains(BitlyStream[Any]):
    """Branded Short Domains stream."""

    name = "bsds"
    path = "/v4/bsds"
    primary_keys = ("domain",)

    schema = th.PropertiesList(
        th.Property(
            "domain",
            th.StringType,
            description="The branded short domain.",
            required=True,
        ),
    ).to_dict()

    @override
    def parse_response(self, response: requests.Response) -> Iterable[dict[str, Any]]:
        for bsd in response.json()["bsds"]:
            yield {"domain": bsd}


class Campaigns(BitlyStream[Any]):
    """Campaigns stream."""

    name = "campaigns"
    path = "/v4/campaigns"
    primary_keys = ("guid",)
    records_jsonpath = "$.campaigns[*]"

    schema = th.PropertiesList(
        th.Property(
            "guid",
            th.StringType,
            description="The campaign's unique identifier.",
            required=True,
        ),
        th.Property(
            "group_guid",
            th.StringType,
            description="The campaign's group.",
        ),
        th.Property(
            "name",
            th.StringType,
            description="The campaign's name.",
        ),
        th.Property(
            "description",
            th.StringType,
            description="The campaign's description.",
        ),
        th.Property(
            "created",
            th.DateTimeType,
            description="The date and time the campaign was created.",
        ),
        th.Property(
            "modified",
            th.DateTimeType,
            description="The date and time the campaign was last modified.",
        ),
        th.Property(
            "created_by",
            th.StringType,
            description="The campaign's creator.",
        ),
        th.Property(
            "references",
            th.ObjectType(
                # th.Property("group", th.StringType),  # noqa: ERA001
            ),
            description="Mapping of campaign references.",
        ),
    ).to_dict()


class Channels(BitlyStream[Any]):
    """Channels stream."""

    name = "channels"
    path = "/v4/channels"
    primary_keys = ("guid",)
    records_jsonpath = "$.channels[*]"

    schema = th.PropertiesList(
        th.Property(
            "guid",
            th.StringType,
            description="The channel's unique identifier.",
        ),
        th.Property(
            "name",
            th.StringType,
            description="The channel's name.",
        ),
        th.Property(
            "created",
            th.DateTimeType,
            description="The date and time the channel was created.",
        ),
        th.Property(
            "modified",
            th.DateTimeType,
            description="The date and time the channel was last modified.",
        ),
        th.Property(
            "group_guid",
            th.StringType,
            description="The channel's group.",
        ),
        th.Property(
            "references",
            th.ObjectType(),
            description="Mapping of channel references.",
        ),
    ).to_dict()


class Organizations(BitlyStream[Any]):
    """Organizations stream."""

    name = "organizations"
    path = "/v4/organizations"
    primary_keys = ("guid",)
    records_jsonpath = "$.organizations[*]"

    schema = th.PropertiesList(
        th.Property(
            "guid",
            th.StringType,
            description="The organization's unique identifier.",
        ),
        th.Property(
            "references",
            th.ObjectType(
                th.Property(
                    "groups",
                    th.StringType,
                    description="The organization's groups.",
                ),
            ),
            description="Mapping of organization references.",
        ),
        th.Property("name", th.StringType, description="The organization's name."),
        th.Property(
            "is_active",
            th.BooleanType,
            description="Whether the organization is active.",
        ),
        th.Property("tier", th.StringType, description="The organization's tier."),
        th.Property(
            "tier_family",
            th.StringType,
            description="The organization's tier family.",
        ),
        th.Property(
            "tier_display_name",
            th.StringType,
            description="The organization's tier display name.",
        ),
        th.Property(
            "role",
            th.StringType,
            description="The organization's role.",
        ),
        th.Property(
            "created",
            th.DateTimeType,
            description="The date and time the organization was created.",
        ),
        th.Property(
            "modified",
            th.DateTimeType,
            description="The date and time the organization was last modified.",
        ),
        th.Property(
            "bsds",
            th.ArrayType(th.StringType()),
            description="The organization's branded short domains.",
        ),
    ).to_dict()

    @override
    def get_child_context(
        self,
        record: dict[str, Any],
        context: Context | None,
    ) -> dict[str, Any]:
        return {"organization_guid": record["guid"]}


class Webhooks(BitlyStream[Any]):
    """Webhooks stream."""

    name = "webhooks"
    path = "/v4/organizations/{organization_guid}/webhooks"
    primary_keys = ("guid",)
    records_jsonpath = "$.webhooks[*]"
    parent_stream_type = Organizations

    schema = th.PropertiesList(
        th.Property(
            "guid",
            th.StringType,
            description="The webhook's unique identifier.",
        ),
        th.Property(
            "name",
            th.StringType,
            description="The webhook's name.",
        ),
        th.Property(
            "references",
            th.ObjectType(),
            description="Mapping of webhook references.",
        ),
        th.Property(
            "created",
            th.DateTimeType,
            description="The date and time the webhook was created.",
        ),
        th.Property(
            "modified",
            th.DateTimeType,
            description="The date and time the webhook was last modified.",
        ),
        th.Property(
            "modified_by",
            th.StringType,
            description="The webhook's modifier.",
        ),
        th.Property(
            "deactivated",
            th.DateTimeType,
            description="The date and time the webhook was deactivated.",
        ),
        th.Property(
            "is_active",
            th.BooleanType,
            description="Whether the webhook is active.",
        ),
        th.Property(
            "organization_guid",
            th.StringType,
            description="The webhook's organization.",
        ),
        th.Property(
            "group_guid",
            th.StringType,
            description="The webhook's group.",
        ),
        th.Property(
            "event",
            th.StringType,
            description="The webhook's event.",
        ),
        th.Property(
            "url",
            th.StringType,
            description="The webhook's URL.",
        ),
        th.Property(
            "status",
            th.StringType,
            description="The webhook's status.",
        ),
        th.Property(
            "oauth_url",
            th.StringType,
            description="The webhook's OAuth URL.",
        ),
        th.Property(
            "client_id",
            th.StringType,
            description="The webhook's client ID.",
        ),
        th.Property(
            "client_secret",
            th.StringType,
            description="The webhook's client secret.",
        ),
        th.Property(
            "fetch_tags",
            th.BooleanType,
            description="Whether to fetch tags.",
        ),
    ).to_dict()


class DailyBitlinkClicks(BitlyStream[Any]):
    """Daily bitlink clicks."""

    name = "daily_bitlink_clicks"
    path = "/v4/bitlinks/{bitlink}/clicks"
    primary_keys = ("date", "bitlink")
    records_jsonpath = "$.link_clicks[*]"
    parent_stream_type = Bitlinks

    schema = th.PropertiesList(
        th.Property("clicks", th.IntegerType, description="The number of clicks."),
        th.Property("date", th.DateTimeType, description="The date."),
        th.Property("bitlink", th.StringType, description="The bitlink."),
    ).to_dict()


class MonthlyBitlinkClicks(DailyBitlinkClicks):
    """Monthly bitlink clicks."""

    name = "montly_bitlink_clicks"

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        return {"unit": "month"}
