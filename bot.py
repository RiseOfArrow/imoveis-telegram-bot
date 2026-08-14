import requests

url = "https://glue-api.zapimoveis.com.br/v2/listings"

params = {
    "business": "RENTAL",
    "addressCity": "Rio de Janeiro",
    "bedrooms": "2,3,4",
    "parkingSpaces": "1,2,3,4",
    "usableAreasMin": 60,
    "rentalTotalPriceMax": 3500,
    "size": 5,
    "page": 1
}

r = requests.get(url, params=params)

print(r.status_code)
print(r.text[:1000])
