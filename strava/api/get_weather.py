import requests


def get_weather(lat, lng, date):
    """
    Fetch the weather data from NCEI API for a specific latitude, longitude, and date.

    Parameters:
    lat (float): Latitude of the location
    lng (float): Longitude of the location
    date (str): Date in 'YYYY-MM-DD' format

    Returns:
    dict: The weather data for the specified location and date
    """

    # NCEI API Token (Replace with your actual API token)
    api_token = "32pretendUEVWnoaa29Skey02"

    # NCEI API Endpoint
    api_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"

    # API parameters
    params = {
        "datasetid": "GHCND",
        "startdate": date,
        "enddate": date,
        "locationid": f"FIPS:{lat:0.6f}:{lng:0.6f}",
        "units": "metric",
        "limit": 1000,
    }

    # Make the API request with the token in the header
    response = requests.get(api_url, params=params, headers={"token": api_token})

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        weather_data = response.json()
        return weather_data
    else:
        # Print an error message if the request was not successful
        print(f"Failed to fetch weather data. HTTP Status Code: {response.status_code}")
        return None


# Example Usage
weather = get_weather(40.7128, -74.0060, "2023-08-17")
print(weather)
