from .tasks import search_products
from django.shortcuts import render
from .models import Tracked_Products

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


def track_item_view_htmx(request,link,name,supplier,price):
    print('tracking')

    if request.method == 'POST':
        try:
            Tracked_Products.objects.get(link=link,name=name,supplier=supplier,price=price)
            print(f"{name} already exists.")
            return render (request,'price_compare/partials/tracker.html')
        except Tracked_Products.DoesNotExist:
            Tracked_Products.objects.update_or_create(link=link,name=name,supplier=supplier,price=price)
            return render (request,'price_compare/partials/tracker.html')

    return render(request,'price_compare/partials/tracker-none.html')