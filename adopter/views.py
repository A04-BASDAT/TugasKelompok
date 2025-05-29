import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.template.defaulttags import register
from django.http import HttpResponseForbidden
from main.views import login_required_custom
from supabase_utils import (
    get_all_adopsi, get_all_hewan, get_all_adopter,
    get_all_individu, get_all_organisasi, get_all_catatan_medis,
    get_hewan_by_id, get_individu_by_id, get_organisasi_by_id,
    get_adopter_by_username,
    get_catatan_medis_by_id
)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def get_adopter_id_from_user(username):
    adopter = get_adopter_by_username(username)
    if adopter:
        return adopter['id_adopter']
    return None

def load_data():
    return {
        'adopters': get_all_adopter(),
        'individus': get_all_individu(),
        'organisasis': get_all_organisasi(),
        'catatan_kesehatans': get_all_catatan_medis(),
        'animals': get_all_hewan(),
        'adoptions': get_all_adopsi()
    }

def get_adopter_info(adopter_id, data):
    for individu in data['individus']:
        if individu['id_adopter'] == adopter_id:
            for adopter in data['adopters']:
                if adopter['id_adopter'] == adopter_id:
                    return {
                        'type': 'individu',
                        'name': individu['nama'],
                        'nik': individu['nik'],
                        'username': adopter['username_adopter'],
                        'total_kontribusi': adopter['total_kontribusi']
                    }

    for organisasi in data['organisasis']:
        if organisasi['id_adopter'] == adopter_id:
            for adopter in data['adopters']:
                if adopter['id_adopter'] == adopter_id:
                    return {
                        'type': 'organisasi',
                        'name': organisasi['nama_organisasi'],
                        'npp': organisasi['npp'],
                        'username': adopter['username_adopter'],
                        'total_kontribusi': adopter['total_kontribusi']
                    }

    return None

def get_animal_info(animal_id, data):
    for animal in data['animals']:
        if animal['id'] == animal_id:
            return animal
    return None

def get_adoption_info(adopter_id, animal_id, data):
    for adoption in data['adoptions']:
        if adoption['id_adopter'] == adopter_id and adoption['id_hewan'] == animal_id:
            return adoption
    return None

def get_health_records(animal_id, data):
    health_records = []
    for record in data['catatan_kesehatans']:
        if record['id_hewan'] == animal_id:
            health_records.append(record)
    return health_records

def get_adopted_animals(adopter_id, data):
    adopted_animals = []
    for adoption in data['adoptions']:
        if adoption['id_adopter'] == adopter_id:
            animal = get_animal_info(adoption['id_hewan'], data)
            if animal:
                adopted_animals.append({
                    'animal': animal,
                    'adoption': adoption
                })
    return adopted_animals

def get_adoptions_by_adopter_id(adopter_id):
    """
    Get all adoptions for a specific adopter directly from Supabase
    """
    all_adoptions = get_all_adopsi()
    return [adoption for adoption in all_adoptions if adoption['id_adopter'] == adopter_id]

@login_required_custom
def adoption_program(request):
    try:
        username = request.session['username']
        print(f"[DEBUG] Processing for username: {username}")
        
        # Step 1: Get adopter from adopter table by username
        adopter = get_adopter_by_username(username)
        if not adopter:
            print("[DEBUG] User is not an adopter")
            return redirect('main:show_main')
        
        adopter_id = adopter['id_adopter']
        print(f"[DEBUG] Found adopter with ID: {adopter_id}")
        
        # Step 2: Check if adopter is organisasi or individu by id_adopter
        adopter_info = None
        
        # Check in individu table first
        all_individu = get_all_individu()
        print(f"[DEBUG] Checking {len(all_individu)} individu records")
        
        for individu in all_individu:
            if str(individu.get('id_adopter', '')).strip() == str(adopter_id).strip():
                adopter_info = {
                    'type': 'individu',
                    'name': individu['nama'],
                    'nik': individu['nik'],
                    'username': adopter['username_adopter'],
                    'total_kontribusi': adopter['total_kontribusi']
                }
                print(f"[DEBUG] Found individu: {individu}")
                break
        
        # If not found in individu, check in organisasi table
        if not adopter_info:
            all_organisasi = get_all_organisasi()
            print(f"[DEBUG] Checking {len(all_organisasi)} organisasi records")
            
            for organisasi in all_organisasi:
                if str(organisasi.get('id_adopter', '')).strip() == str(adopter_id).strip():
                    adopter_info = {
                        'type': 'organisasi',
                        'name': organisasi['nama_organisasi'],
                        'npp': organisasi['npp'],
                        'username': adopter['username_adopter'],
                        'total_kontribusi': adopter['total_kontribusi']
                    }
                    print(f"[DEBUG] Found organisasi: {organisasi}")
                    break
        
        # If still not found, create default
        if not adopter_info:
            print("[DEBUG] No adopter info found, using default")
            adopter_info = {
                'type': 'unknown',
                'name': adopter['username_adopter'],
                'username': adopter['username_adopter'],
                'total_kontribusi': adopter['total_kontribusi']
            }
        
        # Step 3: Get adoptions by id_adopter
        all_adoptions = get_all_adopsi()
        adopter_adoptions = []
        
        for adoption in all_adoptions:
            if str(adoption.get('id_adopter', '')).strip() == str(adopter_id).strip():
                adopter_adoptions.append(adoption)
        
        print(f"[DEBUG] Found {len(adopter_adoptions)} adoptions for adopter {adopter_id}")
        
        # Step 4: Get animals by id_hewan from adoptions
        all_animals = get_all_hewan()
        my_adoptions = []
        
        for adoption in adopter_adoptions:
            id_hewan = adoption.get('id_hewan')
            print(f"[DEBUG] Looking for animal with id: {id_hewan}")
            
            # Find the animal with matching id
            animal = None
            for hewan in all_animals:
                if str(hewan.get('id', '')).strip() == str(id_hewan).strip():
                    animal = hewan
                    break
            
            if animal:
                my_adoptions.append({
                    'animal': animal,
                    'adoption': adoption
                })
                print(f"[DEBUG] Matched adoption with animal: {animal.get('nama', 'No name')}")
            else:
                print(f"[DEBUG] No animal found for id: {id_hewan}")
        
        print(f"[DEBUG] Final result: {len(my_adoptions)} adoptions with animals")
        
        # Step 5: Get medical records for all adopted animals (filtered by adoption start date)
        from datetime import datetime
        all_medical_records = get_all_catatan_medis()
        health_records = []
        payment_issues = []
        
        for item in my_adoptions:
            animal_id = item['animal']['id']
            adoption_start_date = item['adoption']['tgl_mulai_adopsi']
            
            # Convert adoption start date to datetime for comparison
            if isinstance(adoption_start_date, str):
                try:
                    adoption_start = datetime.strptime(adoption_start_date, '%Y-%m-%d').date()
                except ValueError:
                    try:
                        adoption_start = datetime.strptime(adoption_start_date, '%Y-%m-%d %H:%M:%S').date()
                    except ValueError:
                        adoption_start = None
            else:
                adoption_start = adoption_start_date
            
            animal_records = []
            
            for record in all_medical_records:
                if str(record.get('id_hewan', '')).strip() == str(animal_id).strip():
                    # Check if medical record date is after or equal to adoption start date
                    record_date = record.get('tanggal_pemeriksaan')
                    if isinstance(record_date, str):
                        try:
                            record_date = datetime.strptime(record_date, '%Y-%m-%d').date()
                        except ValueError:
                            try:
                                record_date = datetime.strptime(record_date, '%Y-%m-%d %H:%M:%S').date()
                            except ValueError:
                                record_date = None
                    
                    # Only include records from adoption start date onwards
                    if adoption_start and record_date and record_date >= adoption_start:
                        animal_records.append(record)
                        print(f"[DEBUG] Medical record {record_date} included (adoption started {adoption_start})")
                    elif record_date:
                        print(f"[DEBUG] Medical record {record_date} excluded (before adoption start {adoption_start})")
            
            health_records.extend(animal_records)
            print(f"[DEBUG] Found {len(animal_records)} valid medical records for animal {animal_id}")
            
            # Check payment status
            adoption_status = item['adoption'].get('status_pembayaran', 'Tidak diketahui')
            if adoption_status.lower() in ['belum lunas', 'pending', 'unpaid', 'tertunda']:
                payment_issues.append({
                    'animal_name': item['animal'].get('nama', 'Tanpa Nama'),
                    'status': adoption_status,
                    'adoption_date': adoption_start_date
                })
        
        print(f"[DEBUG] Total medical records found: {len(health_records)}")
        print(f"[DEBUG] Payment issues found: {len(payment_issues)}")
        
        context = {
            'adopter': adopter,
            'adopter_info': adopter_info,
            'my_adoptions': my_adoptions,
            'health_records': health_records,
            'payment_issues': payment_issues
        }
        
        return render(request, 'adopter/adoption_program.html', context)
        
    except Exception as e:
        print(f"[ERROR] An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return HttpResponse(f"Terjadi kesalahan: {str(e)}", status=500)

@login_required_custom
def animal_detail(request, animal_id):
    # Check if user is an adopter
    adopter = get_adopter_by_username(request.session['username'])
    if not adopter:
        return redirect('main:show_main')
    
    animal = get_hewan_by_id(animal_id)
    if not animal:
        return HttpResponse("Hewan tidak ditemukan", status=404)
    
    # Get adoption info if exists
    adoptions = get_all_adopsi()
    adoption = None
    for a in adoptions:
        if a['id_hewan'] == animal_id and a['id_adopter'] == adopter['id_adopter']:
            adoption = a
            break
    
    # Get medical records if animal is adopted by this adopter
    medical_records = []
    if adoption:
        medical_records = get_catatan_medis_by_id(animal_id)
    
    context = {
        'animal': animal,
        'adoption': adoption,
        'medical_records': medical_records
    }
    
    return render(request, 'adopter/animal_detail.html', context)

@login_required_custom
def adoption_certificate(request, animal_id):
    # Check if user is an adopter
    adopter = get_adopter_by_username(request.session['username'])
    if not adopter:
        return redirect('main:show_main')
    
    # Get adoption info
    adoptions = get_all_adopsi()
    adoption = None
    for a in adoptions:
        if a['id_hewan'] == animal_id and a['id_adopter'] == adopter['id_adopter']:
            adoption = a
            break
    
    if not adoption:
        return HttpResponse("Sertifikat tidak ditemukan", status=404)
    
    animal = get_hewan_by_id(animal_id)
    
    context = {
        'adopter': adopter,
        'animal': animal,
        'adoption': adoption
    }
    
    return render(request, 'adopter/adoption_certificate.html', context)

@login_required_custom
def animal_health_report(request, animal_id):
    adopter = get_adopter_by_username(request.session['username'])
    if not adopter:
        return redirect('main:show_main')
    
    adoptions = get_all_adopsi()
    is_adopter = False
    for adoption in adoptions:
        if adoption['id_hewan'] == animal_id and adoption['id_adopter'] == adopter['id_adopter']:
            is_adopter = True
            break
    
    if not is_adopter:
        return HttpResponse("Anda tidak memiliki akses ke laporan kesehatan hewan ini", status=403)
    
    animal = get_hewan_by_id(animal_id)
    medical_records = get_catatan_medis_by_id(animal_id)
    
    context = {
        'animal': animal,
        'medical_records': medical_records
    }
    
    return render(request, 'adopter/animal_health_report.html', context)

@login_required_custom
def extend_adoption(request, animal_id):
    adopter = get_adopter_by_username(request.session['username'])
    if not adopter:
        return redirect('main:show_main')

    animal = get_hewan_by_id(animal_id)
    if not animal:
        return HttpResponse("Hewan tidak ditemukan", status=404)

    # Get adoption info
    adoptions = get_all_adopsi()
    adoption = None
    for a in adoptions:
        if a['id_hewan'] == animal_id and a['id_adopter'] == adopter['id_adopter']:
            adoption = a
            break

    if not adoption:
        return HttpResponse("Data adopsi tidak ditemukan", status=404)

    if request.method == 'POST':
        # Handle extension logic here
        return redirect('adopter:adoption_program')

    context = {
        'animal': animal,
        'adoption': adoption,
        'adopter': adopter
    }

    return render(request, 'adopter/extend_adoption.html', context)

@login_required_custom
def stop_adoption(request, animal_id):
    adopter = get_adopter_by_username(request.session['username'])
    if not adopter:
        return redirect('main:show_main')

    animal = get_hewan_by_id(animal_id)
    if not animal:
        return HttpResponse("Hewan tidak ditemukan", status=404)

    # Get adoption info
    adoptions = get_all_adopsi()
    adoption = None
    for a in adoptions:
        if a['id_hewan'] == animal_id and a['id_adopter'] == adopter['id_adopter']:
            adoption = a
            break

    if not adoption:
        return HttpResponse("Data adopsi tidak ditemukan", status=404)

    if request.method == 'POST':
        # Handle stop adoption logic here
        return redirect('adopter:adoption_program')

    context = {
        'animal': animal,
        'adoption': adoption,
        'adopter': adopter
    }

    return render(request, 'adopter/stop_adoption.html', context)
