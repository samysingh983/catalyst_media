import math
from django.shortcuts import render
from catalyst_count import settings
from catalyst_count_app.models import CatalystUser
from django.views.decorators.csrf import csrf_exempt  # Only for testing, remove in production
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import FileForm
from .models import File, Data
import os
import pandas as pd

def profile_view(request):
    users = CatalystUser.objects.filter(is_active=True)
    return render(request, 'profile.html', {'users': users})

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = CatalystUser.objects.create_user(username, email, password)
        user.save()
        return profile_view(request)
    else:
        return render(request, 'register.html')

@csrf_exempt
def delete(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        print(user_id)
        user = CatalystUser.objects.get(pk=user_id)  # Get the user instance
        print(user.is_active)
        user.is_active = False  # Set user to inactive
        user.save()
        return profile_view(request)
    

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save()
            return JsonResponse({'file_id': file_instance.id})
    else:
        form = FileForm()
    return render(request, 'upload_data.html', {'form': form})

@login_required
def process_file_chunk(request):
    if request.method == 'POST':
        file_id = request.POST['file_id']
        chunk = request.FILES['file']
        file_instance = File.objects.get(id=file_id)
        file_path = os.path.join(settings.MEDIA_ROOT, file_instance.file.name)
        
        # Append chunk to the file
        with open(file_path, 'ab') as f:
            f.write(chunk.read())
        
        return JsonResponse({'status': 'Chunk uploaded successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_record_value(value):
    if isinstance(value, float) and math.isnan(value):
        return None
    elif isinstance(value, str) and (value.lower() == 'nan' or value.strip() == ''):
        return None
    else:
        return value


# @login_required
def process_file(request, file_id):
    file_instance = File.objects.get(id=file_id)
    file_path = file_instance.file.path

    try:
        chunks = pd.read_csv(file_path, chunksize=90000)

        bulk_data = []

        for chunk in chunks:
            chunk['locality'] = chunk['locality'].apply(get_record_value)
            chunk['year founded'] = chunk['year founded'].apply(lambda x: None if pd.isna(x) else str(int(float(x))) if isinstance(x, (float, int)) else str(x)[:-2])

            # Split locality into city, state, country
            locality_parts = chunk['locality'].str.split(', ', expand=True)
            chunk['city'] = locality_parts[0]
            chunk['state'] = locality_parts[1]
            chunk['country'] = locality_parts[2]

            # Convert chunk to list of Data instances
            chunk_records = chunk.to_dict('records')
            bulk_data.extend([
                Data(
                    name=record.get('name'),
                    domain=record.get('domain'),
                    year_founded=record.get('year founded'),
                    industry=record.get('industry'),
                    size_range=record.get('size range'),
                    locality=record.get('locality'),
                    city=record.get('city'),
                    state=record.get('state'),
                    country=record.get('country'),
                    linkedin_url=record.get('linkedin url'),
                    current_employee_estimate=record.get('current employee estimate'),
                    total_employee_estimate=record.get('total employee estimate')
                )
                for record in chunk_records
            ])

            # Insert records in bulk to the database in chunks
            print(len(bulk_data))
            if len(bulk_data) >= 90000:
                Data.objects.bulk_create(bulk_data)
                bulk_data = []

        # Insert any remaining records
        if bulk_data:
            Data.objects.bulk_create(bulk_data)

        file_instance.status = 'Processed'
        file_instance.save()

        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def query_builder(request):
    industries = Data.objects.values_list('industry', flat=True).distinct()
    years = Data.objects.values_list('year_founded', flat=True).distinct()
    cities = Data.objects.values_list('city', flat=True).distinct()
    states = Data.objects.values_list('state', flat=True).distinct()
    countries = Data.objects.values_list('country', flat=True).distinct()

    context = {
        'industries': industries,
        'years': years,
        'cities': cities,
        'states': states,
        'countries': countries
    }

    return render(request, 'query_builder.html', context)

def query_data(request):
    keyword = request.GET.get('keyword', '')
    industry = request.GET.get('industry', '')
    year_founded = request.GET.get('year_founded', '')
    city = request.GET.get('city', '')
    state = request.GET.get('state', '')
    country = request.GET.get('country', '')
    employees_from = request.GET.get('employees_from', '')
    employees_to = request.GET.get('employees_to', '')
    filters = {}
    if keyword:
        filters['name__icontains'] = keyword
    if industry:
        filters['industry__icontains'] = industry
    if year_founded:
        filters['year_founded'] = year_founded
    if city:
        filters['city__icontains'] = city
    if state:
        filters['state__icontains'] = state
    if country:
        filters['country__icontains'] = country
    if employees_from:
        filters['current_employee_estimate__gte'] = employees_from
    if employees_to:
        filters['current_employee_estimate__lte'] = employees_to

    query = Data.objects.filter(**filters)
    records_found = query.count()

    return JsonResponse({'records_found': records_found})