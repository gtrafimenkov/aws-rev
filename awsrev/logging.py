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

import logging

import boto3

from awsrev.results import IssuesCollector


def check_logging(ic: IssuesCollector):
    check_global_cloudtrail(ic)


def check_global_cloudtrail(ic: IssuesCollector):
    """Check that there is a global cloudtrail enabled."""
    client = boto3.client("cloudtrail")
    resp = client.describe_trails()
    found = False
    for trail in resp["trailList"]:
        trail_arn = trail["TrailARN"]
        logging.info("checking CloudTrail %s", trail_arn)
        if trail.get("IsMultiRegionTrail", False):
            status = client.get_trail_status(Name=trail_arn)
            # suitable trail, but need additional checks
            if not status.get("IsLogging", False):
                # not currently logging
                continue
            if not does_trail_include_all_management_events(client, trail_arn):
                # not all events are included
                continue
            found = True
    if not found:
        ic.add("no multi-regions CloudTrail configured to log all management events")


def does_trail_include_all_management_events(client, trail_arn):
    """Check if the event selectors for the trail, include all
    management events."""
    resp = client.get_event_selectors(TrailName=trail_arn)
    return check_selectors_for_all_management_events(resp["EventSelectors"])


def check_selectors_for_all_management_events(event_selectors):
    for selector in event_selectors:
        if (
            selector["ReadWriteType"] == "All"
            and selector["IncludeManagementEvents"]
            and len(selector["ExcludeManagementEventSources"]) == 0
        ):
            return True
    return False
