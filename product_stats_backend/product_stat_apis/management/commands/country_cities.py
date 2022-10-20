import json

from django.core.management.base import BaseCommand
import requests

from product_stat_apis.models import Country, City


class Command(BaseCommand):
    """
    Command to create countries and cities
    """

    help = "This command is used to create country cities"

    def handle(self, *args, **kwargs):
        """
        This function is used to create countries and cities
        """
        countries = Country.objects.all()
        city = City.objects.all()
        if city or countries:
            print("Country and city already exists")
            return
        print("Creating countries and cities, please wait...")
        try:
            country_cities = requests.get(
                "https://countriesnow.space/api/v0.1/countries"
            )
            for obj in country_cities.json()["data"]:
                country = Country.objects.create(name=obj["country"])
                url = "https://countriesnow.space/api/v0.1/countries/cities"

                payload = json.dumps({"country": obj["country"]})
                headers = {
                    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwi\
                                      ZXhwIjoxNjk3NDgyNzc4LCJqdGkiOiJkNzhkYzJiMjgwODE0NTZiOWVhMjdkZDg0MzczZD\
                                      U0MyIsInVzZXJfaWQiOjN9.pVfsdh1IYyuGfRiS-lIB-5RXQJkDBD9blOQnmApcua8",
                    "Content-Type": "application/json",
                }

                response = requests.request("POST", url, headers=headers, data=payload)
                if response.status_code == 200:
                    cities = response.json()["data"]
                    if len(cities) > 100:
                        cities = cities[100]
                    for city in cities:
                        City.objects.create(name=city, country=country)
            print("Country cities created successfully")
        except Exception as e:
            print(e)
