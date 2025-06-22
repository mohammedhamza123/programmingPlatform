import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()

API_KEY = "8e53ad1e9bb0d3b8639f15bbf8b0be20"  # ضع مفتاحك هنا
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@router.get("/weather/")
def get_weather(city: str):
    params = {
        "q": city + ",LY",  # يجبر البحث على ليبيا فقط
        "appid": API_KEY,
        "units": "metric",
        "lang": "ar"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="City not found")
    data = response.json()
    # تحقق أن الدولة ليبيا فقط
    if data.get("sys", {}).get("country") != "LY":
        raise HTTPException(status_code=404, detail="City not in Libya")
    return data
