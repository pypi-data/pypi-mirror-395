#!/usr/bin/env python3
"""
Example usage of Notify Africa SMS SDK

This script demonstrates all the key features of the SDK.
Matches the Node.js SDK structure.
"""

import os
from notify_africa import NotifyAfrica
from notify_africa.exceptions import (
    NotifyAfricaException,
    NetworkError
)


def main():
    # Initialize the client (matching Node.js SDK)
    client = NotifyAfrica(
        apiToken=os.getenv("NOTIFY_AFRICA_API_TOKEN", os.getenv("NOTIFY_AFRICA_API_KEY"))
    )
    
    try:
        # Example 1: Send single SMS (matching Node.js SDK)
        print("1. Sending single SMS...")
        response = client.send_single_message(
            phoneNumber="255694192317",
            message="Hello from API Management endpoint!",
            senderId="164"
        )
        print(f"   Message ID: {response.messageId}")
        print(f"   Status: {response.status}")
        print()
        
        # Example 2: Send batch SMS (matching Node.js SDK)
        print("2. Sending batch SMS...")
        phone_numbers = [
            "255694192317",
            "255743517612",
        ]
        response = client.send_batch_messages(
            phoneNumbers=phone_numbers,
            message="This is a batch SMS message sent to multiple recipients.",
            senderId="164"
        )
        print(f"   Message Count: {response.messageCount}")
        print(f"   Credits Deducted: {response.creditsDeducted}")
        print(f"   Remaining Balance: {response.remainingBalance}")
        print()
        
        # Example 3: Check message status (matching Node.js SDK)
        if response.messageCount > 0:
            print("3. Checking message status...")
            # Use the messageId from the first example if available
            # In a real scenario, you'd use the messageId from send_single_message
            # status_response = client.check_message_status("156022")
            # print(f"   Message ID: {status_response.messageId}")
            # print(f"   Status: {status_response.status}")
            # print(f"   Sent At: {status_response.sentAt}")
            # print(f"   Delivered At: {status_response.deliveredAt}")
            print("   (Skipped - need a messageId from a previous send)")
            print()
        
        print("✅ All examples completed successfully!")
        
    except NotifyAfricaException as e:
        print(f"❌ API error: {e}")
        if e.status_code:
            print(f"   Status Code: {e.status_code}")
        
    except NetworkError as e:
        print(f"❌ Network error: {e}")
        print("Please check your internet connection.")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    print("Notify Africa SMS SDK - Example Usage")
    print("=" * 40)
    print()
    
    # Check for required environment variables
    api_token = os.getenv("NOTIFY_AFRICA_API_TOKEN") or os.getenv("NOTIFY_AFRICA_API_KEY")
    if not api_token:
        print("⚠️  Warning: NOTIFY_AFRICA_API_TOKEN environment variable not set.")
        print("   Set it with: export NOTIFY_AFRICA_API_TOKEN='your_api_token'")
        print()
    
    main()