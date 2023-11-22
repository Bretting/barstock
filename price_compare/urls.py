from django.urls import path
from .views import (
    search_home_view,
    search_htmx,
    track_item_view_htmx,
)

app_name = 'price_compare'

urlpatterns = [
    path('', search_home_view),
    path('search', search_htmx, name='search'),
    path('add_tracker/<str:name>/<str:supplier>/<str:price>/<str:link>', track_item_view_htmx,name='add_tracker')
]

