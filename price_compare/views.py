from .tasks import search_products
from django.shortcuts import render

# Create your views here.
def search_home_view(request):
    return render(request,'price_compare/home.html')


def search_htmx(request):
    
    if request.method == 'POST':
        search = request.POST.get('search')
        query = search_products(search)
        right_spirits = query[0]
        anker = query[1]
        henk_smit = query[2]

        context = {
            'right_spirits': right_spirits,
            'anker' : anker,
            'henk_smit' : henk_smit,
        }
    else:
        context = {}

    return render (request,'price_compare/partials/search.html', context)