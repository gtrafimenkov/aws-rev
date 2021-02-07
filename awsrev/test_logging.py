###############################################################################
# Copyright (c) 2021 Gennady Trafimenkov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
###############################################################################

import unittest

import awsrev.logging


class TestCloudTrailSelectors(unittest.TestCase):
    def test_basic_correct_selectors(self):
        selectors = [
            {
                "ReadWriteType": "All",
                "IncludeManagementEvents": True,
                "DataResources": [],
                "ExcludeManagementEventSources": [],
            }
        ]
        self.assertTrue(
            awsrev.logging.check_selectors_for_all_management_events(selectors)
        )
