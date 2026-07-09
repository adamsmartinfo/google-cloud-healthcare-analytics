import requests


def fetch_cms_data(api_url, limit=10):
    request_url = f"{api_url}?limit={limit}"

    response = requests.get(request_url)
    response.raise_for_status()

    data = response.json()
    return data["results"]