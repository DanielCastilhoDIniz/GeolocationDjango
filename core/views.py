from django.shortcuts import render
from django.views.generic import View
from .utils import yelp_search, get_client_city_data


class IndexView(View):

    def get(self, request, **args):
        itens = []
        city = None

        """
         depois do front pronto retirar e esse
         laço e mudar a finalidade do app
         para um simples buscador
        """
        while not city:
            ret = get_client_city_data()
            if ret:
                city = ret.get('city')

        q = request.GET.get('key', None)
        loc = request.GET.get('loc', city)

        context = {
            'city': city,
            'busca': False
        }

        if loc:
            location = loc
        if q:
            itens = yelp_search(keyword=q, location=location)
            context = {
                'itens': itens,
                'city': location,
                'busca': True
            }

        return render(request, 'index.html', context)
