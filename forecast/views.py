from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Sum
from .models import *
from .forms import *
from datetime import date
import csv

#Helper functions:

def current_month_calc():
    return date.today().replace(day=1)

def later_month_calc(month, offset):
    return month.replace(month=month.month % 12 + offset, day=1)



# Create your views here.
@login_required
def dashboard_view(request):

    current_month = current_month_calc()

    # Calculate the first day of the next month
    next_month = later_month_calc(current_month,1)
    month_after = later_month_calc(current_month,2)

    # Use the annotate() method along with Sum() to calculate the sum of amount for each unique product
    # Use F expressions to check if amount is not None
    products_with_total_amount = Product.objects.annotate(total_amount=Sum('volumeitem__amount')).exclude(total_amount=None)

    # Create a list to store product categories, names and total amounts
    product_totals = []
    for product in products_with_total_amount:
        product_name = product.name
        product_category = product.category
        #Calculate total amount for this month and for next month.
        current_month_total_amount = product.volumeitem_set.filter(start_date__lt=next_month).aggregate(Sum('amount'))['amount__sum'] or 0
        next_month_total_amount = product.volumeitem_set.filter(end_date__gte=next_month).aggregate(Sum('amount'))['amount__sum'] or 0
        month_after_amount =product.volumeitem_set.filter(end_date__gte=month_after).aggregate(Sum('amount'))['amount__sum'] or 0

        #Create one itterable item to use in template.
        product_totals.append({'product_name': product_name,'product_category': product_category, 'total_amount': current_month_total_amount, 'next_month_total_amount' : next_month_total_amount, 'month_after_total_amount' : month_after_amount})

        context = {
            'product_totals' : product_totals
        }
    
    return render(request,'forecast/home.html', context)



#Create an overview of all accounts that carry a certain product:
@login_required
def accounts_by_product_view(request, product):
    
    current_month = current_month_calc()

    # Calculate the first day of the next month
    next_month = later_month_calc(current_month,1)
    month_after = later_month_calc(current_month,2)

    #create a list of all accounts that have a record for the selected product
    items = VolumeItem.objects.filter(product__name=product)

    #Create a list of all accounts with the amount field filtered for this month and next month.
    account_totals = []
    for item in items:
        account_name = item.account
        current_month_total = VolumeItem.objects.filter(account=account_name, start_date__lt=next_month,product__name=product, amount__isnull=False).aggregate(Sum('amount'))['amount__sum']
        next_month_total= VolumeItem.objects.filter(account=account_name, start_date__lte=next_month,product__name=product, amount__isnull=False).aggregate(Sum('amount'))['amount__sum']
        month_after_total= VolumeItem.objects.filter(account=account_name, end_date__gte=month_after,product__name=product, amount__isnull=False).aggregate(Sum('amount'))['amount__sum']


        account_totals.append({'account_name' : account_name, 'current_month_total' : current_month_total, 'next_month_total' : next_month_total, 'month_after_total' : month_after_total})


    context = {
        'product': product,
        'account_totals': account_totals
    }

    return render(request,'forecast/account_by_product.html', context)


#create an overview of all accounts in Db and make them searchable
@login_required
def account_view(request):
    context = {
        'accounts' : Account.objects.all()
    }

    return render (request,'forecast/accounts.html', context)


# Show all product forecasted by a selected account and their dates.
@login_required
def account_detail_view(request, name):
    account = get_object_or_404(Account, name=name)
    forecast_items = VolumeItem.objects.filter(account=account.id)
    accountnr = account.pk

    if request.method == 'POST':
        form = VolumeForm(request.POST)
        if form.is_valid():
            # Get the account associated with the form data
            product = form.cleaned_data['product']
            amount = form.cleaned_data['amount']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            try:
                # Try to get the existing record with the specified account, product, and amount
                volume_item = VolumeItem.objects.get(account=account, product=product)

                # If the record exists, add the new amount to the existing amount
                volume_item.amount += amount
                volume_item.end_date = end_date
                volume_item.start_date = start_date
                volume_item.save()
                form = VolumeForm()

            except VolumeItem.DoesNotExist:
                # If no record exists, create a new record with the provided data
                volume_item = VolumeItem.objects.create(account=account, product=product, amount=amount, start_date=start_date, end_date=end_date)

            # Add your success redirect or response logic here

    else:
        form = VolumeForm()

    context = {
        'account': account,
        'forecast_items': forecast_items,
        'form': form,
        'accountnr': accountnr
    }


    return render(request, 'forecast/account_detail.html', context)

#View used in cobination with HTMX to delete a selected product from an account.
@login_required
def delete_item(request, item, account):
    to_delete = VolumeItem.objects.get(pk=item)
    print(account)

    to_delete.delete()

    context = {
        'forecast_items' : VolumeItem.objects.filter(account=account),
        'accountnr' : account
    }

    # return template fragment with all the user's films
    return render(request, 'forecast/partials/accounts_product_list.html', context)

#view used to add products one by one
@login_required
def add_product_view(request):

    if request.method== 'POST':
        form = ProductForm(request.POST)

        print(request.POST)

        if form.is_valid():
            form.save()
            return redirect('forecast:home')
        else:
            form = ProductForm

    form = ProductForm

    context = {
        'form' : form
    }

    return render(request,'forecast/CRUD.html', context)

#View used to add new accounts one by one
@login_required
def add_account_view(request):

    if request.method== 'POST':
        form = AccountForm(request.POST)

        print(request.POST)

        if form.is_valid():
            form.save()
            return redirect('forecast:home')
        else:
            form = AccountForm

    form = AccountForm

    context = {
        'form' : form
    }

    return render(request,'forecast/CRUD.html', context)










#Import .csv for products, categories and accounts:

@login_required
def import_accounts_view(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        characters = ('.','/','"',',',"'")
        
        if not csv_file.name.endswith('.csv'):
            return HttpResponse('Only .csv files are allowed.')

        # Process the CSV file and save Account objects
        try:
            decoded_file = csv_file.read().decode('ISO-8859-1', errors='replace')
            csv_reader = csv.reader(decoded_file.splitlines())

            for row in csv_reader:
                name = str(row[0])
                #delete special characters
                for c in characters:
                    name = str.replace(name,c,'')
                print(name)
                Account.objects.get_or_create(name=name)

            return HttpResponse('CSV file imported successfully.')
        except Exception as e:
            return HttpResponse(f'Error importing CSV file: {str(e)}')
    else:
        return render(request, 'forecast/import_csv.html', {'name':'Accounts'})

@login_required    
def import_categories_view(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        characters = ('.','/','"',',',"'")
        
        if not csv_file.name.endswith('.csv'):
            return HttpResponse('Only .csv files are allowed.')

        # Process the CSV file and save Category objects
        try:
            decoded_file = csv_file.read().decode('ISO-8859-1', errors='replace')
            csv_reader = csv.reader(decoded_file.splitlines())

            for row in csv_reader:
                name = str(row[0])
                #delete special characters
                for c in characters:
                    name = str.replace(name,c,'')
                print(name)
                Category.objects.get_or_create(name=name)

            return HttpResponse('CSV file imported successfully.')
        except Exception as e:
            return HttpResponse(f'Error importing CSV file: {str(e)}')
    else:
        return render(request, 'forecast/import_csv.html',{'name':'Categories'})
    
@login_required
def import_product_view(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        characters = ('.','/','"',',',"'")
        
        if not csv_file.name.endswith('.csv'):
            return HttpResponse('Only .csv files are allowed.')

        # Process the CSV file and save product objects
        try:
            decoded_file = csv_file.read().decode('ISO-8859-1', errors='replace')
            csv_reader = csv.reader(decoded_file.splitlines(), delimiter=';')

            for row in filter(None,csv_reader):
                print(row)
                name = str(row[1]) 
                #delete special characters
                for c in characters:
                    name = str.replace(name,c,'')

                print(str(row[0]))
                try:
                    cat = Category.objects.get(name=str(row[0]))
                    print(cat.id)
  
                    data = {
                        'category' : cat.id,
                        'name' : name
                    }

                    try:
                        Product.objects.get(name=name)
                    except:
                        form = ProductForm(data)
                        if form.is_valid():
                            form.save()
                        else:
                            print(form.errors)
                except:
                    pass
           
            return HttpResponse('CSV file imported successfully.')
        except Exception as e:
            return HttpResponse(f'Error importing CSV file: {str(e)}')
    else:
        return render(request, 'forecast/import_csv.html', {'name':'Products'})


#Not used.
@login_required
def testview(request):
    if request.method== 'POST':
        form = ProductForm(request.POST)

        print(request.POST)

        if form.is_valid():
            print(form)
            form.save()
            return HttpResponse('saved!')
    else:
        form = ProductForm

    context = {
        'form' : form
    }

    return render(request, 'forecast/test.html', context)

