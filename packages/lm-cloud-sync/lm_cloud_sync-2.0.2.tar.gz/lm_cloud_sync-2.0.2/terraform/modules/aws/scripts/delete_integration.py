#!/usr/bin/env python3
"""Delete AWS integration from LogicMonitor.

This script is called by Terraform to delete AWS device groups.
It uses the lm-cloud-sync library to interact with the LogicMonitor API.
"""

import argparse
import os
import sys

# Try to import from installed package first, then fall back to local src
try:
    from lm_cloud_sync.core.lm_client import LogicMonitorClient
    from lm_cloud_sync.providers.aws.groups import delete_aws_group, get_group_by_account_id
except ImportError:
    # Add src to path for local development
    src_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "src")
    sys.path.insert(0, src_path)
    from lm_cloud_sync.core.lm_client import LogicMonitorClient
    from lm_cloud_sync.providers.aws.groups import delete_aws_group, get_group_by_account_id


def main():
    parser = argparse.ArgumentParser(description="Delete AWS integration from LogicMonitor")
    parser.add_argument("--account-id", required=True, help="AWS account ID")
    args = parser.parse_args()

    # Get credentials from environment
    company = os.environ.get("LM_COMPANY")
    bearer_token = os.environ.get("LM_BEARER_TOKEN")

    if not company or not bearer_token:
        print("Error: LM_COMPANY and LM_BEARER_TOKEN must be set", file=sys.stderr)
        sys.exit(1)

    # Create client and find the group
    with LogicMonitorClient(company=company, bearer_token=bearer_token) as client:
        group = get_group_by_account_id(client, args.account_id)

        if not group:
            print(f"No group found for AWS account {args.account_id}")
            return

        if group.id:
            delete_aws_group(client, group.id)
            print(f"Deleted AWS integration for account {args.account_id} (group ID: {group.id})")
        else:
            print(f"Cannot delete: group ID not found for account {args.account_id}")


if __name__ == "__main__":
    main()
