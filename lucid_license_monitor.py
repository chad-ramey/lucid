### Lucid License Monitor Script
# This script monitors Lucid Suite licenses by comparing the number of used licenses
# to the total licenses allocated. If the number of used licenses exceeds the total,
# it sends an alert to a configured Slack channel via an Incoming Webhook.
#
# The script uses Lucid's SCIM API to fetch user data and calculate license usage.
# The total licenses are manually configured.
#
# Required Environment Variables:
#   LUCID_TOKEN        - Bearer token for Lucid SCIM API access.
#   SLACK_WEBHOOK_URL  - Webhook URL to send Slack alerts.
#
# Total licenses must be manually configured in the script.
#
# Author: Chad Ramey
# Last Updated: December 10, 2024

import os
import requests

# Lucid SCIM API URL
lucid_api_url = "https://users.lucid.app/scim/v2/Users"

# Load secrets from environment variables
lucid_token = os.getenv("LUCID_TOKEN")
slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")

# Total licenses (manually set based on your Lucid Suite plan)
total_licenses = 657

# Function to fetch used licenses
def get_used_licenses():
    headers = {"Authorization": f"Bearer {lucid_token}", "Content-Type": "application/json"}
    users = []
    start_index = 1
    items_per_page = 100

    while True:
        params = {"startIndex": start_index, "count": items_per_page}
        response = requests.get(lucid_api_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            users.extend(data.get("Resources", []))
            total_results = data.get("totalResults", 0)

            if start_index + items_per_page > total_results:
                break

            start_index += items_per_page
        else:
            print(f"Error fetching user data: {response.status_code} - {response.text}")
            return None

    used_licenses = sum(
        1 for user in users
        if user.get("urn:ietf:params:scim:schemas:extension:lucid:1.0:User", {}).get("productLicenses", {}).get("Lucidchart", False) or
           user.get("urn:ietf:params:scim:schemas:extension:lucid:1.0:User", {}).get("productLicenses", {}).get("Lucidspark", False) or
           user.get("urn:ietf:params:scim:schemas:extension:lucid:1.0:User", {}).get("productLicenses", {}).get("LucidscaleCreator", False) or
           user.get("urn:ietf:params:scim:schemas:extension:lucid:1.0:User", {}).get("productLicenses", {}).get("LucidscaleExplorer", False)
    )
    return used_licenses

# Function to send a Slack alert
def send_slack_alert(message):
    payload = {"text": message}
    response = requests.post(slack_webhook_url, json=payload)
    if response.status_code == 200:
        print("Slack alert sent successfully.")
    else:
        print(f"Failed to send Slack alert: {response.status_code}, {response.text}")

# Main function
def main():
    used_licenses = get_used_licenses()
    if used_licenses is not None:
        print(f"Used Licenses: {used_licenses}")
        available_licenses = total_licenses - used_licenses
        print(f"Total Licenses: {total_licenses}")
        print(f"Available Licenses: {available_licenses}")

        if used_licenses > total_licenses:
            alert_message = (
                f":rotating_light::lucid: *Lucid License Alert* :lucid::rotating_light:\n"
                f"Used Licenses: {used_licenses}\n"
                f"Total Licenses: {total_licenses}\n"
                f"Overage: {used_licenses - total_licenses}\n"
                f"*Immediate action required to resolve the overage.*"
            )
            send_slack_alert(alert_message)
        else:
            alert_message = (
                f":lucid: *Lucid License Report* :lucid:\n"
                f"Used Licenses: {used_licenses}\n"
                f"Total Licenses: {total_licenses}\n"
                f"Available Licenses: {available_licenses}\n"
                f"*All licenses are within the allocated limit.*"
            )
            send_slack_alert(alert_message)
    else:
        print("Could not retrieve used licenses due to errors.")

if __name__ == "__main__":
    main()
