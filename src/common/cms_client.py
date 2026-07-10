import requests


def fetch_cms_data(api_url, limit=10, offset=0):
    request_url = f"{api_url}?limit={limit}&offset={offset}"

    response = requests.get(request_url)
    response.raise_for_status()

    data = response.json()
    return data["results"]

def fetch_all_cms_data(api_url, batch_size=500):
    all_records = []
    offset = 0

    while True:
        batch = fetch_cms_data(
            api_url,
            limit=batch_size,
            offset=offset,
        )

        if not batch:
            break

        all_records.extend(batch)
        offset += batch_size

        print(f"Retrieved {len(all_records)} records so far...")

    return all_records