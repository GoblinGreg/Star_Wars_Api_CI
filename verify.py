#!/usr/bin/env python3
import requests
import sys
import time


def verify_application():
    """Verify that the Flask application is running correctly on port 8085"""
    url = "http://localhost:8085"

    max_retries = 30
    retry_delay = 2

    print(f"Verifying application at {url}...")

    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                print(f"✓ Application is running successfully!")
                print(f"✓ Status Code: {response.status_code}")
                print(f"✓ Response length: {len(response.text)} bytes")

                # Sprawdź czy strona zawiera oczekiwaną zawartość
                if "Star Wars" in response.text or "Characters" in response.text:
                    print("✓ Page content looks correct!")
                    sys.exit(0)
                else:
                    print("✗ Page content doesn't match expected format")
                    sys.exit(1)
            else:
                print(f"✗ Unexpected status code: {response.status_code}")
                sys.exit(1)

        except requests.ConnectionError:
            print(
                f"Attempt {attempt + 1}/{max_retries}: Connection failed, retrying in {retry_delay}s...")
            time.sleep(retry_delay)
        except requests.Timeout:
            print(
                f"Attempt {attempt + 1}/{max_retries}: Request timeout, retrying in {retry_delay}s...")
            time.sleep(retry_delay)
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            sys.exit(1)

    print(f"✗ Failed to connect after {max_retries} attempts")
    sys.exit(1)


if __name__ == "__main__":
    verify_application()
