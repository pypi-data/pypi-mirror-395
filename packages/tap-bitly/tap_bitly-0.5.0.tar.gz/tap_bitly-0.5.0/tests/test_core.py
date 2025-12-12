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
"""Tests standard tap features using the built-in SDK tests library."""

from __future__ import annotations

from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_bitly.tap import TapBitly

TestTapBitly = get_tap_test_class(
    TapBitly,
    config={},
    suite_config=SuiteConfig(
        max_records_limit=50,
        ignore_no_records_for_streams=[
            "bsds",
            "campaigns",
            "channels",
        ],
    ),
)
