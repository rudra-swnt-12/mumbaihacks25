import httpx


class WeatherService:
    def __init__(self):
        self.lat = 19.0760
        self.lon = 72.8777
        self.url = "https://api.open-meteo.com/v1/forecast"

    async def get_current_weather(self):
        params = {
            "latitude": self.lat,
            "longitude": self.lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code",
        }

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(self.url, params=params)
                data = resp.json()

                current = data.get("current", {})
                temp = current.get("temperature_2m", 30)
                feels_like = current.get("apparent_temperature", 32)

                condition = "Pleasant"
                if temp > 35:
                    condition = "Heatwave"
                elif temp > 30:
                    condition = "Hot"

                return {
                    "temp": temp,
                    "feels_like": feels_like,
                    "condition": condition,
                    "location": "Mumbai",
                }
        except Exception as e:
            print(f"Weather Error: {e}")
            return {
                "temp": "--",
                "feels_like": "--",
                "condition": "Unknown",
                "location": "Unknown",
            }
