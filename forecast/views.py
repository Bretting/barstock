from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Sum
from .models import *
from .forms import *
from datetime import date
import csv

# Create your views here.
@login_required
def dashboard_view(request):

    current_month = date.today()
    current_month = current_month.replace(day=1)
    # Calculate the first day of the next month
    next_month = current_month.replace(month=current_month.month % 12 + 1, day=1)
    month_after = current_month.replace(month=current_month.month % 12 + 2, day=1)

    # Use the annotate() method along with Sum() to calculate the sum of amount for each unique spirit
    # Use F expressions to check if amount is not None
    spirits_with_total_amount = Spirit.objects.annotate(total_amount=Sum('volumeitem__amount')).exclude(total_amount=None)

    # Create a list to store spirit categories, names and total amounts
    spirit_totals = []
    for spirit in spirits_with_total_amount:
        spirit_name = spirit.name
        spirit_category = spirit.category
        #Calculate total amount for this month and for next month.
        current_month_total_amount = spirit.volumeitem_set.filter(start_date__lt=next_month).aggregate(Sum('amount'))['amount__sum'] or 0
        next_month_total_amount = spirit.volumeitem_set.filter(end_date__gte=next_month).aggregate(Sum('amount'))['amount__sum'] or 0
        month_after_amount =spirit.volumeitem_set.filter(end_date__gte=month_after).aggregate(Sum('amount'))['amount__sum'] or 0

        #Create one itterable item to use in template.
        spirit_totals.append({'spirit_name': spirit_name,'spirit_category': spirit_category, 'total_amount': current_month_total_amount, 'next_month_total_amount' : next_month_total_amount, 'month_after_total_amount' : month_after_amount})

        context = {
            'spirit_totals' : spirit_totals
        }
    
    return render(request,'forecast/home.html', context)



#Create an overview of all accounts that carry a certain spirit:
@login_required
def accounts_by_spirit_view(request, spirit):
    
    current_month = date.today()
    current_month = current_month.replace(day=1)
    # Calculate the first day of the next month
    next_month = current_month.replace(month=current_month.month % 12 + 1, day=1)
    month_after = current_month.replace(month=current_month.month % 12 + 2, day=1)

    #create a list of all accounts that have a record for the selected spirit
    items = VolumeItem.objects.filter(spirit__name=spirit)

    #Create a list of all accounts with the amount field filtered for this month and next month.
    account_totals = []
    for item in items:
        account_name = item.account
        current_month_total = VolumeItem.objects.filter(account=account_name, start_date__lt=next_month,spirit__name=spirit, amount__isnull=False).aggregate(Sum('amount'))['amount__sum']
        next_month_total= VolumeItem.objects.filter(account=account_name, start_date__lte=next_month,spirit__name=spirit, amount__isnull=False).aggregate(Sum('amount'))['amount__sum']
        month_after_total= VolumeItem.objects.filter(account=account_name, end_date__gte=month_after,spirit__name=spirit, amount__isnull=False).aggregate(Sum('amount'))['amount__sum']


        account_totals.append({'account_name' : account_name, 'current_month_total' : current_month_total, 'next_month_total' : next_month_total, 'month_after_total' : month_after_total})


    context = {
        'spirit': spirit,
        'account_totals': account_totals
    }

    return render(request,'forecast/account_by_spirit.html', context)


#create an overview of all accounts in Db and make them searchable
@login_required
def account_view(request):
    context = {
        'accounts' : Account.objects.all()
    }

    return render (request,'forecast/accounts.html', context)


# Show all spirits forecasted by a selected account and their dates.
@login_required
def account_detail_view(request, name):
    account = get_object_or_404(Account, name=name)
    forecast_items = VolumeItem.objects.filter(account=account.id)
    accountnr = account.pk

    if request.method == 'POST':
        form = VolumeForm(request.POST)
        if form.is_valid():
            # Get the account associated with the form data
            spirit = form.cleaned_data['spirit']
            amount = form.cleaned_data['amount']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            try:
                # Try to get the existing record with the specified account, spirit, and amount
                volume_item = VolumeItem.objects.get(account=account, spirit=spirit)

                # If the record exists, add the new amount to the existing amount
                volume_item.amount += amount
                volume_item.end_date = end_date
                volume_item.start_date = start_date
                volume_item.save()
                form = VolumeForm()

            except VolumeItem.DoesNotExist:
                # If no record exists, create a new record with the provided data
                volume_item = VolumeItem.objects.create(account=account, spirit=spirit, amount=amount, start_date=start_date, end_date=end_date)

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
    return render(request, 'forecast/partials/accounts_spirits_list.html', context)




#Import .csv for spirits, categories and accounts:

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
def import_spirits_view(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        characters = ('.','/','"',',',"'")
        
        if not csv_file.name.endswith('.csv'):
            return HttpResponse('Only .csv files are allowed.')

        # Process the CSV file and save Spirits objects
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
                        Spirit.objects.get(name=name)
                    except:
                        form = SpiritForm(data)
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
        return render(request, 'forecast/import_csv.html', {'name':'Spirits'})
    
@login_required
def testview(request):
    if request.method== 'POST':
        form = SpiritForm(request.POST)

        print(request.POST)

        if form.is_valid():
            print(form)
            form.save()
            return HttpResponse('saved!')
    else:
        form = SpiritForm

    context = {
        'form' : form
    }

    return render(request, 'forecast/test.html', context)