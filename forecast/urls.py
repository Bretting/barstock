from django.urls import path

from .views import (
    dashboard_view,
    account_view,
    account_detail_view,
    accounts_by_spirit_view,
    delete_item,
    import_accounts_view,
    import_categories_view,
    import_spirits_view,

    testview,
)


app_name = 'forecast'
urlpatterns = [
    path('', dashboard_view, name='home'),
    path('Accounts',account_view, name='accounts'),
    path('Accounts/<str:name>', account_detail_view, name='account_detail'),
    path('Spirits/<str:spirit>', accounts_by_spirit_view, name='account_by_spirit'),
    path('Partials/delete_item/<int:item>-<int:account>',delete_item,name='delete-item'),
    path('Admin/import-accounts', import_accounts_view, name='import_accounts'),
    path('Admin/import-categories', import_categories_view, name='import_categories'),
    path('Admin/import-spirits', import_spirits_view, name='import_spirits'),
    path('test', testview)
]