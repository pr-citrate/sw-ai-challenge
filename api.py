import requests, json, os
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("KEY")


def get_data() -> dict:
    try:
        response = requests.get(
            f"http://apis.data.go.kr/1741000/HeatWaveShelter3/getHeatWaveShelterList3?ServiceKey={KEY}&year=2024&areaCd=5214040000&type=json&pageNo=1&numOfRows=20",
            headers={
                "Content-Type": "*/*",
                "charset": "UTF-8",
                "Accept": "*/*",
                "User-Agent": "python-requests/2.26.0",
            },
            timeout=10,
        )

        # print(response.status_code)  # Check the status

        response.raise_for_status()  # Check if the request was successful

        data = response.json()
        # print(json.dumps(data, indent=2))

        return data

    except requests.exceptions.SSLError as ssl_err:
        print(f"SSL error: {ssl_err}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request failed: {req_err}")


if __name__ == "__main__":
    data = get_data()
    print(json.dumps(data, indent=2))
