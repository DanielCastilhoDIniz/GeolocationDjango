import requests
from random import randint
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.geoip2 import GeoIP2Exception


YELP_SEARCH_ENDPOINT = "https://api.yelp.com/v3/businesses/search"


def yelp_search(keyword=None, location=None):
    """Performs a search on the Yelp API using
    the provided keyword and location.
    If no keyword or location is provided,
    defaults to searching for 'Pizzaria' in 'João Pessoa'.
    """

    headers = {"Authorization": "Bearer " + settings.YELP_API_KEY}

    if keyword and location:
        params = {'term': keyword, 'location': location}
    else:
        params = {'term': 'Pizzaria', 'location': 'João Pessoa'}

    response = requests.get(YELP_SEARCH_ENDPOINT,
                            headers=headers, params=params)

    return response.json()


def get_client_city_data():
    g = GeoIP2()
    ip = get_random_ip()
    try:
        return g.city(ip)
    except GeoIP2Exception:
        return {
            "error": "IP não localizado",
            "ip": ip,
        }


def get_random_ip():
    return '.'.join(str(randint(0, 255)) for _ in range(4))
