import json
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaulttags import register
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from supabase_utils import (
    get_all_adopsi, get_all_hewan, get_all_adopter,
    get_all_individu, get_all_organisasi,
    get_hewan_by_id, get_adopter_by_username,
    create_complete_adopter, create_adopsi, create_adopsi_raw, debug_table_structure,
    update_adopsi, update_adopter, delete_adopter,
    normalize_uuid, debug_uuid_comparison, generate_adopter_uuid, check_uuid_format_compatibility,
    get_pengguna_by_username, trigger_notify_top_5_adopter,
    delete_adopter_with_cascade, create_update_total_kontribusi_trigger
)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def load_data():
    return {
        'adoptions': get_all_adopsi(),
        'animals': get_all_hewan(),
        'adopters': get_all_adopter(),
        'individus': get_all_individu(),
        'organisasis': get_all_organisasi()
    }

def get_adopter_info(adopter_id, data):
    for individu in data['individus']:
        if individu['id_adopter'] == adopter_id:
            # Found individual adopter
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
            # Found organization adopter
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

def get_adoption_history(adopter_id, data):
    adoption_history = []
    for adoption in data['adoptions']:
        if adoption['id_adopter'] == adopter_id:
            animal = get_animal_info(adoption['id_hewan'], data)
            if animal:
                adoption_history.append({
                    'animal': animal,
                    'adoption': adoption
                })
    return adoption_history

def calculate_total_contribution(adopter_id, data):
    total = 0
    for adoption in data['adoptions']:
        if adoption['id_adopter'] == adopter_id:
            total += int(adoption['kontribusi_finansial'])
    return total

def adoption_admin_page(request):
    animals = get_all_hewan()
    adoptions = get_all_adopsi()

    adoption_info = {}
    for adoption in adoptions:
        animal_id = adoption['id_hewan']

        adoption_info[animal_id] = {
            'status': 'Diadopsi',
            'adopter': f"Adopter ID: {adoption['id_adopter']}",
            'adoption': {
                'start_date': adoption['tgl_mulai_adopsi'],
                'end_date': adoption['tgl_berhenti_adopsi'],
                'contribution': f"Rp {int(adoption['kontribusi_finansial']):,}",
                'payment_status': adoption['status_pembayaran']
            }
        }

    for animal in animals:
        if animal['id'] not in adoption_info:
            adoption_info[animal['id']] = {
                'status': 'Tidak Diadopsi',
                'adopter': None,
                'adoption': None
            }

    animals_json = json.dumps(animals)
    adoption_info_json = json.dumps(adoption_info, cls=DjangoJSONEncoder)

    context = {
        'animals': animals,
        'adoption_info': adoption_info,
        'animals_json': animals_json,
        'adoption_info_json': adoption_info_json,
    }

    return render(request, 'main_page_adoption_admin.html', context)

def adopter_list(request):
    data = load_data()
    current_date = datetime.now()
    one_year_ago = current_date - timedelta(days=365)

    individual_adopters = []
    organization_adopters = []
    
    adopter_total_contributions = {}
    adopter_yearly_contributions = {}
    adopter_payment_status = {}  
    
    for adoption in data['adoptions']:
        try:
            adopter_id = adoption['id_adopter']
            kontribusi = int(adoption.get('kontribusi_finansial', 0))
            payment_status = adoption.get('status_pembayaran', '').lower()
            
            if adopter_id not in adopter_payment_status:
                adopter_payment_status[adopter_id] = {'has_pending': False}
            if payment_status == 'tertunda':
                adopter_payment_status[adopter_id]['has_pending'] = True
            
            if adopter_id not in adopter_total_contributions:
                adopter_total_contributions[adopter_id] = 0
            adopter_total_contributions[adopter_id] += kontribusi
            
            start_date = datetime.strptime(adoption['tgl_mulai_adopsi'], '%Y-%m-%d')
            if start_date >= one_year_ago:
                if adopter_id not in adopter_yearly_contributions:
                    adopter_yearly_contributions[adopter_id] = 0
                adopter_yearly_contributions[adopter_id] += kontribusi
                
        except (ValueError, TypeError):
            continue

    for individu in data['individus']:
        adopter_id = individu['id_adopter']
        adopter_base = next((a for a in data['adopters'] if a['id_adopter'] == adopter_id), None)
        
        if adopter_base:
            active_adoptions = []
            
            total_contribution = adopter_total_contributions.get(adopter_id, 0)
            yearly_contribution = adopter_yearly_contributions.get(adopter_id, 0)
            has_pending = adopter_payment_status.get(adopter_id, {}).get('has_pending', False)
            
            for adoption in data['adoptions']:
                if adoption['id_adopter'] == adopter_id:
                    end_date = datetime.strptime(adoption['tgl_berhenti_adopsi'], '%Y-%m-%d')
                    if end_date >= current_date:
                        active_adoptions.append(adoption)

            adopter_data = {
                'id': adopter_id,
                'name': individu['nama'],
                'type': 'individu',
                'username': adopter_base['username_adopter'],
                'total_kontribusi': total_contribution,
                'yearly_kontribusi': yearly_contribution,
                'has_active_adoptions': len(active_adoptions) > 0,
                'has_pending_payment': has_pending,
                'nik': individu['nik']
            }
            
            individual_adopters.append(adopter_data)

    for organisasi in data['organisasis']:
        adopter_id = organisasi['id_adopter']
        adopter_base = next((a for a in data['adopters'] if a['id_adopter'] == adopter_id), None)
        
        if adopter_base:
            active_adoptions = []
            
            total_contribution = adopter_total_contributions.get(adopter_id, 0)
            yearly_contribution = adopter_yearly_contributions.get(adopter_id, 0)
            has_pending = adopter_payment_status.get(adopter_id, {}).get('has_pending', False)
            
            for adoption in data['adoptions']:
                if adoption['id_adopter'] == adopter_id:
                    end_date = datetime.strptime(adoption['tgl_berhenti_adopsi'], '%Y-%m-%d')
                    if end_date >= current_date:
                        active_adoptions.append(adoption)

            adopter_data = {
                'id': adopter_id,
                'name': organisasi['nama_organisasi'],
                'type': 'organisasi',
                'username': adopter_base['username_adopter'],
                'total_kontribusi': total_contribution,
                'yearly_kontribusi': yearly_contribution,
                'has_active_adoptions': len(active_adoptions) > 0,
                'has_pending_payment': has_pending,
                'npp': organisasi['npp']
            }
            
            organization_adopters.append(adopter_data)

    individual_adopters.sort(key=lambda x: x['total_kontribusi'], reverse=True)
    organization_adopters.sort(key=lambda x: x['total_kontribusi'], reverse=True)
    
    all_adopters_combined = []
    for adopter in individual_adopters + organization_adopters:
        if not adopter['has_pending_payment']:  
            all_adopters_combined.append(adopter)
    
    top_adopters = sorted(all_adopters_combined, key=lambda x: x['total_kontribusi'], reverse=True)[:5]

    context = {
        'individual_adopters': individual_adopters,
        'organization_adopters': organization_adopters,
        'top_adopters': top_adopters
    }

    return render(request, 'administrative_staff/adopter_list.html', context)

def adopter_detail(request, adopter_id):
    data = load_data()

    adopter_info = get_adopter_info(adopter_id, data)

    if not adopter_info:
        return HttpResponse("Adopter not found", status=404)

    adoption_history = get_adoption_history(adopter_id, data)

    context = {
        'adopter_info': adopter_info,
        'adoption_history': adoption_history
    }

    return render(request, 'administrative_staff/adopter_detail.html', context)

@csrf_exempt
def submit_adoption(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        adopter_type = data.get('adopter_type')
        username = data.get('username')
        animal_id = data.get('animal_id')
        kontribusi = data.get('kontribusi', 0)
        
        try:
            kontribusi = int(kontribusi) if kontribusi else 0
        except (ValueError, TypeError) as e:
            return JsonResponse({
                'error': f'Kontribusi finansial harus berupa angka. Nilai yang diterima: {kontribusi}'
            }, status=400)
        
        existing_adopter = get_adopter_by_username(username)
        
        if existing_adopter:
            new_adopter = existing_adopter
            
            # Update total kontribusi adopter yang sudah ada
            updated_total = existing_adopter.get('total_kontribusi', 0) + kontribusi
            update_adopter(existing_adopter['id_adopter'], {'total_kontribusi': updated_total})
            new_adopter['total_kontribusi'] = updated_total
            
        else:

            adopter_data = {
                'username_adopter': username,
                'total_kontribusi': kontribusi  
            }
            
            if adopter_type == 'individu':
                nik = data.get('nik', '')
                if not nik.startswith('32'):  
                    nik = '32' + nik.zfill(13)  
                    
                type_data = {
                    'nik': nik,
                    'nama': data.get('nama')
                }
                is_individual = True
            else:
                npp = 'ORG' + str(len(get_all_organisasi()) + 1).zfill(5)
                
                type_data = {
                    'npp': npp,
                    'nama_organisasi': data.get('nama_organisasi')
                }
                is_individual = False
            
            new_adopter = create_complete_adopter(
                adopter_data=adopter_data,
                type_data=type_data,
                is_individual=is_individual
            )
        
        animal = get_hewan_by_id(animal_id)
        if not animal:
            return JsonResponse({
                'error': f'Hewan dengan ID {animal_id} tidak ditemukan'
            }, status=404)
       
        adopter_id_from_db = new_adopter['id_adopter']
        validated_animal_id = str(animal['id'])
        
    
        print(f"[TYPE CHECK] new_adopter['id_adopter']: {type(adopter_id_from_db)} = {adopter_id_from_db}")
        print(f"[TYPE CHECK] validated_animal_id: {type(validated_animal_id)} = {validated_animal_id}")
        
        adoption_data = {
            'id_adopter': adopter_id_from_db,  
            'id_hewan': validated_animal_id,
            'tgl_mulai_adopsi': data.get('start_date'),
            'tgl_berhenti_adopsi': data.get('end_date'),
            'kontribusi_finansial': kontribusi,
            'status_pembayaran': 'tertunda'
        }
        
        print(f"[FINAL CHECK] adoption_data['id_adopter']: {type(adoption_data['id_adopter'])} = {adoption_data['id_adopter']}")
        print(f"[FINAL CHECK] Are they the same type? {type(adopter_id_from_db) == type(adoption_data['id_adopter'])}")
        print(f"[FINAL CHECK] Are they the same value? {adopter_id_from_db == adoption_data['id_adopter']}")
        
        new_adoption = create_adopsi(adoption_data)
        
        trigger_message = f'SUKSES: Total kontribusi adopter "{username}" telah diperbarui.'
        
        return JsonResponse({
            'success': True,
            'message': 'Adopsi berhasil didaftarkan',
            'trigger_message': trigger_message,
            'data': {
                'adopter': new_adopter,
                'adoption': new_adoption
            }
        })
        
    except Exception as e:
        print(f"[ERROR] submit_adoption error: {str(e)}")
        return JsonResponse({
            'error': str(e)
        }, status=500)

@csrf_exempt
def update_payment_status(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        id_adopter = data.get('id_adopter')
        id_hewan = data.get('id_hewan')
        new_status = data.get('status')
        
        if not id_adopter or not id_hewan:
            return JsonResponse({'error': 'id_adopter and id_hewan are required'}, status=400)
        
        updated_adoption = update_adopsi(
            id_adopter,
            id_hewan,
            {'status_pembayaran': new_status}
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Status pembayaran berhasil diperbarui',
            'data': updated_adoption
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@csrf_exempt
def delete_adopter_view(request, adopter_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = load_data()
        current_date = datetime.now()
        
        for adoption in data['adoptions']:
            if adoption['id_adopter'] == adopter_id:
                end_date = datetime.strptime(adoption['tgl_berhenti_adopsi'], '%Y-%m-%d')
                if end_date >= current_date:
                    return JsonResponse({
                        'success': False,
                        'message': 'Tidak dapat menghapus adopter yang masih aktif mengadopsi satwa.'
                    }, status=400)
        
        delete_result = delete_adopter_with_cascade(adopter_id)
        
        if delete_result['success']:
            return JsonResponse({
                'success': True,
                'message': f'Adopter berhasil dihapus',
                'trigger_messages': delete_result['messages'],
                'adopter_name': delete_result['adopter_name'],
                'adoption_count': delete_result['adoption_count']
            })
        else:
            return JsonResponse({
                'success': False,
                'message': delete_result['error']
            }, status=400)
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@csrf_exempt
def initialize_trigger(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        result = create_update_total_kontribusi_trigger()
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@csrf_exempt
def get_top_adopters_realtime(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        import time
        time.sleep(1) 
        
        from datetime import datetime, timedelta
        
        current_date = datetime.now()
        one_year_ago = current_date - timedelta(days=365)
        
        # Load fresh data from database
        all_adopsi = get_all_adopsi()
        all_adopters = get_all_adopter()
        all_individu = get_all_individu()
        all_organisasi = get_all_organisasi()
        
        adopter_contributions = {}
        adopter_yearly_contributions = {} 
        
        for adopsi in all_adopsi:
            if adopsi.get('status_pembayaran', '').lower() == 'lunas':
                try:
                    adopter_id = adopsi['id_adopter']
                    kontribusi = int(adopsi.get('kontribusi_finansial', 0))
                    
                    if adopter_id not in adopter_contributions:
                        adopter_contributions[adopter_id] = 0
                    adopter_contributions[adopter_id] += kontribusi
                    
                    start_date = datetime.strptime(adopsi['tgl_mulai_adopsi'], '%Y-%m-%d')
                    if start_date >= one_year_ago:
                        if adopter_id not in adopter_yearly_contributions:
                            adopter_yearly_contributions[adopter_id] = 0
                        adopter_yearly_contributions[adopter_id] += kontribusi
                        
                except (ValueError, TypeError) as e:
                    continue
        
        all_adopters_with_contributions = []
        
        for adopter_id, total_contribution in adopter_contributions.items():
            if total_contribution > 0:
                # Find adopter base info
                adopter_base = next((a for a in all_adopters if a['id_adopter'] == adopter_id), None)
                
                if adopter_base:
                    adopter_name = None
                    adopter_type = None
                    
                    individu = next((i for i in all_individu if i['id_adopter'] == adopter_id), None)
                    if individu:
                        adopter_name = individu['nama']
                        adopter_type = 'Individu'
                    else:
                        organisasi = next((o for o in all_organisasi if o['id_adopter'] == adopter_id), None)
                        if organisasi:
                            adopter_name = organisasi['nama_organisasi']
                            adopter_type = 'Organisasi'
                    
                    if adopter_name:
                        yearly_contribution = adopter_yearly_contributions.get(adopter_id, 0)
                        all_adopters_with_contributions.append({
                            'adopter_id': adopter_id,
                            'username': adopter_base['username_adopter'],
                            'name': adopter_name,
                            'type': adopter_type,
                            'total_kontribusi': total_contribution,  
                            'yearly_kontribusi': yearly_contribution,  
                            'database_total': adopter_base.get('total_kontribusi', 0)  
                        })
        
        all_adopters_with_contributions.sort(key=lambda x: x['total_kontribusi'], reverse=True)
        top_adopters = all_adopters_with_contributions[:5]
        
  
        trigger_result = trigger_notify_top_5_adopter()
        
        top_adopter_message = ""
        if top_adopters:
            top_adopter = top_adopters[0]
            if top_adopter['yearly_kontribusi'] > 0:
                top_adopter_message = f'SUKSES: Daftar Top 5 Adopter berhasil diperbarui, dengan peringkat pertama "{top_adopter["name"]}" ({top_adopter["type"]}) - Total Kontribusi: Rp{top_adopter["total_kontribusi"]:,} | Kontribusi Setahun Terakhir: Rp{top_adopter["yearly_kontribusi"]:,}'
            else:
                top_adopter_message = f'SUKSES: Daftar Top 5 Adopter berhasil diperbarui, dengan peringkat pertama "{top_adopter["name"]}" ({top_adopter["type"]}) - Total Kontribusi: Rp{top_adopter["total_kontribusi"]:,} (Tidak ada kontribusi dalam setahun terakhir)'
        else:
            top_adopter_message = "Tidak ada data adopter dengan kontribusi"
        
        # Include trigger result in response
        trigger_info = ""
        if trigger_result.get('success'):
            trigger_info = f" | {trigger_result.get('message', '')}"
        
        return JsonResponse({
            'success': True,
            'data': {
                'top_adopters': top_adopters,
                'notification_message': top_adopter_message,
                'total_adopters_with_contributions': len(all_adopters_with_contributions),
                'data_retrieved_at': current_date.strftime('%Y-%m-%d %H:%M:%S'),
                'trigger_result': trigger_result,
                'debug_info': {
                    'total_adopsi_records': len(all_adopsi),
                    'total_adopters_found': len(all_adopters_with_contributions),
                    'top_5_contributions': [f"{a['name']}: Rp{a['total_kontribusi']:,}" for a in top_adopters]
                }
            }
        })
        
    except Exception as e:
        print(f"[ERROR] get_top_adopters_realtime error: {str(e)}")
        return JsonResponse({
            'error': f'Terjadi kesalahan saat mengambil data: {str(e)}'
        }, status=500)

def verify_username(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        username = request.GET.get('username')
        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)
        
        user = get_pengguna_by_username(username)
        
        return JsonResponse({
            'exists': user is not None,
            'message': 'Username found' if user else 'Username not found'
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

