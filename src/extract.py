import json
import os
import sys
import requests

#FPL general overview endpoint
FPL_BOOTSTRAP_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"

def fetch_fpl_data(url: str = FPL_BOOTSTRAP_URL) -> dict:
    """Fetches raw JSON payload from the Premier League API."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}", file=sys.stderr)
        raise

def save_raw_json(data: dict, output_filepath: str) -> None:
    """Persists raw payload directly to disk without modification."""
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)

    with open(output_filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Successfully saved raw data to {output_filepath}")

def main():
    output_path = os.path.join("data", "raw", "bootstrap_static.json")
    raw_data = fetch_fpl_data()
    save_raw_json(raw_data, output_path)


if __name__ == "__main__":
    main()