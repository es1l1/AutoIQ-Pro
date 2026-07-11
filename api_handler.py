import requests

def get_car_models(make, year):
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeYear/make/{make}/modelyear/{year}?format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return [item['Model_Name'] for item in response.json()['Results']]
    return []