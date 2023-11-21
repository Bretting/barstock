from django.urls import path
from .views import (
    search_home_view,
    search_htmx,
)

app_name = 'price_compare'

urlpatterns = [
    path('', search_home_view),
    path('search', search_htmx, name='search')
]

