from django.shortcuts import render
from django.views import View
from .utils import yelp_search, get_client_city_data


class IndexView(View):

    def get(self, request, **kwargs):

        # Cidade padrão via IP (1 tentativa)
        city = None
        geo = get_client_city_data()
        if geo:
            city = geo.get('city')

        # Parâmetros do usuário
        keyword = request.GET.get('key')
        location = request.GET.get('loc') or city
        # print(location, keyword)

        itens = {"businesses": []}
        has_error = False
        busca = False

        if keyword and location:
            busca = True
            itens = yelp_search(keyword=keyword, location=location)

            # Padronização das coordenadas
            for biz in itens.get("businesses", []):
                coords = biz.get("coordinates")
                if not coords:
                    continue

                lat = coords.get("latitude")
                lon = coords.get("longitude")
                print(lat, lon)

                try:
                    coords["latitude"] = float(str(lat).replace(",", "."))
                    coords["longitude"] = float(str(lon).replace(",", "."))
                except (TypeError, ValueError):
                    coords["latitude"] = None
                    coords["longitude"] = None

            if not itens.get("businesses"):
                has_error = True

        context = {
            "city": location,
            "itens": itens,
            "busca": busca,
            "has_error": has_error,
        }

        return render(request, "index.html", context)
