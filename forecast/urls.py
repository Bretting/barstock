from django.urls import path

from .views import (
    #main views
    dashboard_view,
    account_view,
    account_detail_view,
    accounts_by_product_view,
    add_product_view,
    add_account_view,

    #HTMX views
    delete_item,

    #backend views
    import_accounts_view,
    import_categories_view,
    import_product_view,
)

app_name = 'forecast'

urlpatterns = [
    #main views
    path('', dashboard_view, name='home'),
    path('Accounts',account_view, name='accounts'),
    path('Accounts/<str:name>', account_detail_view, name='account_detail'),
    path('Products/<str:product>', accounts_by_product_view, name='account_by_product'),

    #Add items
    path('Add/Product', add_product_view, name='add_product'),
    path('Add/Account', add_account_view, name='add_account'),


    #HTMX views
    path('Partials/delete_item/<int:item>-<int:account>',delete_item,name='delete-item'),

    #Backend views
    path('Admin/import-accounts', import_accounts_view, name='import_accounts'),
    path('Admin/import-categories', import_categories_view, name='import_categories'),
    path('Admin/import-product', import_product_view, name='import_product'),
]