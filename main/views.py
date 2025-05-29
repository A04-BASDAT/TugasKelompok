# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
import uuid
import random
import string
from datetime import datetime
from supabase_client import supabase
from .forms import (
    RoleSelectionForm, VisitorRegistrationForm, VeterinarianRegistrationForm,
    StaffRegistrationForm, UserProfileUpdateForm, VisitorProfileUpdateForm, VeterinarianProfileUpdateForm, PasswordChangeForm
)

def show_main(request):
    return render(request, 'main.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            result = supabase.rpc('verify_login_credentials', {
                'input_username': username,
                'input_password': password
            }).execute()
            
            if result.data and len(result.data) > 0:
                verification = result.data[0]
                
                if verification['is_valid']:
                    # Login berhasil
                    request.session['username'] = username
                    request.session['user_data'] = verification['user_data']
                    
                    # Determine user role
                    role = get_user_role(username)
                    request.session['user_role'] = role
                    
                    return redirect('main:dashboard')
                else:
                    # Login gagal - pesan error dari stored procedure
                    messages.error(request, verification['message'])
            else:
                messages.error(request, 'Terjadi kesalahan sistem')
                
        except Exception as e:
            messages.error(request, f'Error saat login: {str(e)}')
    
    return render(request, 'login.html')

def get_user_role(username):
    """Helper function to determine user role"""
    try:
        # Check if user is pengunjung
        result = supabase.table('pengunjung').select('username_p').eq('username_p', username).execute()
        if result.data and len(result.data) > 0:
            return 'visitor'
            
        # Check if user is dokter hewan
        result = supabase.table('dokter_hewan').select('username_dh').eq('username_dh', username).execute()
        if result.data and len(result.data) > 0:
            return 'veterinarian'
            
        # Check if user is penjaga hewan
        result = supabase.table('penjaga_hewan').select('username_jh').eq('username_jh', username).execute()
        if result.data and len(result.data) > 0:
            return 'animal_keeper'
            
        # Check if user is pelatih hewan
        result = supabase.table('pelatih_hewan').select('username_lh').eq('username_lh', username).execute()
        if result.data and len(result.data) > 0:
            return 'trainer'
            
        # Check if user is staf admin
        result = supabase.table('staf_admin').select('username_sa').eq('username_sa', username).execute()
        if result.data and len(result.data) > 0:
            return 'admin_staff'
            
        return 'unknown'
    except Exception as e:
        return 'unknown'

def logout_view(request):
    request.session.flush()
    return redirect('main:login')

def register_step1(request):
    """First step of registration - select role"""
    if request.method == 'POST':
        form = RoleSelectionForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            request.session['selected_role'] = role
            return redirect('main:register_step2')
    else:
        form = RoleSelectionForm()
    
    return render(request, 'register_role.html', {'form': form})

def register_step2(request):
    """Second step of registration - fill form based on role"""
    role = request.session.get('selected_role')
    
    if not role:
        return redirect('main:register_step1')
    
    if role == 'visitor':
        return register_visitor(request)
    elif role == 'veterinarian':
        return register_veterinarian(request)
    elif role == 'staff':
        return register_staff(request, role)
    else:
        return redirect('main:register_step1')

def register_visitor(request):
    if request.method == 'POST':
        form = VisitorRegistrationForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                
                # Insert into PENGGUNA table
                pengguna_data = {
                    'username': username,
                    'email': form.cleaned_data['email'],
                    'password': password,
                    'nama_depan': form.cleaned_data['first_name'],
                    'nama_tengah': form.cleaned_data.get('middle_name', ''),
                    'nama_belakang': form.cleaned_data['last_name'],
                    'no_telepon': form.cleaned_data['phone_number']
                }
                
                pengguna_result = supabase.table('pengguna').insert(pengguna_data).execute()
                
                # Check if insert was successful
                if not pengguna_result.data:
                    raise Exception("Failed to insert into pengguna table")
                
                # Insert into PENGUNJUNG table
                pengunjung_data = {
                    'username_p': username,
                    'alamat': form.cleaned_data['address'],
                    'tgl_lahir': form.cleaned_data['birth_date'].isoformat()
                }
                
                pengunjung_result = supabase.table('pengunjung').insert(pengunjung_data).execute()
                
                # Check if insert was successful
                if not pengunjung_result.data:
                    raise Exception("Failed to insert into pengunjung table")
                
                messages.success(request, 'Registrasi berhasil! Silakan login.')
                return redirect('main:login')
                
            except Exception as e:
                error_message = e.message
                
                # Cek apakah error duplikasi username
                if 'sudah digunakan' in error_message or 'already exists' in error_message.lower():
                    messages.error(request, error_message)
                else:
                    messages.error(request, f'Error saat registrasi: {error_message}')
                
                try:
                    supabase.table('pengguna').delete().eq('username', username).execute()
                except:
                    pass
    else:
        form = VisitorRegistrationForm()
    
    return render(request, 'register.html', {'form': form, 'role': 'Pengunjung'})

def register_veterinarian(request):
    if request.method == 'POST':
        form = VeterinarianRegistrationForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                
                # Insert into PENGGUNA table
                pengguna_data = {
                    'username': username,
                    'email': form.cleaned_data['email'],
                    'password': password,
                    'nama_depan': form.cleaned_data['first_name'],
                    'nama_tengah': form.cleaned_data.get('middle_name', ''),
                    'nama_belakang': form.cleaned_data['last_name'],
                    'no_telepon': form.cleaned_data['phone_number']
                }
                
                pengguna_result = supabase.table('pengguna').insert(pengguna_data).execute()
                
                if not pengguna_result.data:
                    raise Exception("Failed to insert into pengguna table")
                
                # Insert into DOKTER_HEWAN table
                dokter_data = {
                    'username_dh': username,
                    'no_str': form.cleaned_data['certification_number']
                }
                
                dokter_result = supabase.table('dokter_hewan').insert(dokter_data).execute()
                
                if not dokter_result.data:
                    raise Exception("Failed to insert into dokter_hewan table")
                
                # Insert specializations
                specialization = (
                    form.cleaned_data.get('other_specialization')
                    if form.cleaned_data.get('specialization') == 'other'
                    else form.cleaned_data.get('specialization')
                )
                
                if specialization:
                    spesialisasi_data = {
                        'username_sh': username,
                        'nama_spesialisasi': specialization
                    }
                    
                    try:
                        spesialisasi_result = supabase.table('spesialisasi').insert(spesialisasi_data).execute()
                    except:
                        pass
                
                messages.success(request, 'Registrasi berhasil! Silakan login.')
                return redirect('main:login')
                
            except Exception as e:
                error_message = e.message
                
                # Cek apakah error duplikasi username
                if 'sudah digunakan' in error_message or 'already exists' in error_message.lower():
                    messages.error(request, error_message)
                else:
                    messages.error(request, f'Error saat registrasi: {error_message}')
                
                # Cleanup on error
                try:
                    supabase.table('spesialisasi').delete().eq('username_sh', username).execute()
                    supabase.table('dokter_hewan').delete().eq('username_dh', username).execute()
                    supabase.table('pengguna').delete().eq('username', username).execute()
                except:
                    pass
    else:
        form = VeterinarianRegistrationForm()
    
    return render(request, 'register.html', {'form': form, 'role': 'Dokter Hewan'})

def register_staff(request, staff_role=None):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                staff_role = form.cleaned_data['staff_role']
                                
                # Insert into PENGGUNA table
                pengguna_data = {
                    'username': username,
                    'email': form.cleaned_data['email'],
                    'password': password,
                    'nama_depan': form.cleaned_data['first_name'],
                    'nama_tengah': form.cleaned_data.get('middle_name', ''),
                    'nama_belakang': form.cleaned_data['last_name'],
                    'no_telepon': form.cleaned_data['phone_number']
                }
                
                pengguna_result = supabase.table('pengguna').insert(pengguna_data).execute()
                
                if not pengguna_result.data:
                    raise Exception("Failed to insert into pengguna table")
                
                # Generate UUID for staff ID
                staff_id = str(uuid.uuid4())
                
                if staff_role == 'animal_keeper':
                    staff_data = {
                        'username_jh': username,
                        'id_staf': staff_id
                    }
                    staff_result = supabase.table('penjaga_hewan').insert(staff_data).execute()
                    
                elif staff_role == 'trainer':
                    staff_data = {
                        'username_lh': username,
                        'id_staf': staff_id
                    }
                    staff_result = supabase.table('pelatih_hewan').insert(staff_data).execute()
                    
                elif staff_role == 'admin_staff':
                    staff_data = {
                        'username_sa': username,
                        'id_staf': staff_id
                    }
                    staff_result = supabase.table('staf_admin').insert(staff_data).execute()
                                
                if not staff_result.data:
                    raise Exception(f"Failed to insert into {staff_role} table")
                
                messages.success(request, 'Registrasi berhasil! Silakan login.')
                return redirect('main:login')
                
            except Exception as e:
                error_message = e.message
                
                # Cek apakah error duplikasi username
                if 'sudah digunakan' in error_message or 'already exists' in error_message.lower():
                    messages.error(request, error_message)
                else:
                    messages.error(request, f'Error saat registrasi: {error_message}')
                
                # Cleanup on error
                try:
                    if staff_role == 'animal_keeper':
                        supabase.table('penjaga_hewan').delete().eq('username_jh', username).execute()
                    elif staff_role == 'trainer':
                        supabase.table('pelatih_hewan').delete().eq('username_lh', username).execute()
                    elif staff_role == 'admin_staff':
                        supabase.table('staf_admin').delete().eq('username_sa', username).execute()
                    
                    supabase.table('pengguna').delete().eq('username', username).execute()
                except:
                    pass
    else:
        form = StaffRegistrationForm(initial={'staff_role': staff_role} if staff_role else {})
    
    return render(request, 'register.html', {
        'form': form, 
        'role': 'Staff',
    })

def generate_staff_id(request):
    """AJAX endpoint to generate UUID-based staff ID"""
    staff_id = str(uuid.uuid4())
    return JsonResponse({'staff_id': staff_id})

def login_required_custom(view_func):
    """Custom login required decorator using session"""
    def wrapper(request, *args, **kwargs):
        if 'username' not in request.session:
            return redirect('main:login')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required_custom
def dashboard(request):
    """Dashboard view - displays different content based on user role"""
    try:
        username = request.session.get('username')
        user_data = request.session.get('user_data')
        role = request.session.get('user_role')
        
        # Get role-specific data
        role_data = {}
        visitor_data = {}
        
        if role == 'visitor':
            # Get visitor specific data
            visitor_result = supabase.table('pengunjung').select('*').eq('username_p', username).execute()
            if visitor_result.data:
                visitor_data = visitor_result.data[0]
                role_data = visitor_data
                # Convert tgl_lahir string to date object 
                if role_data.get('tgl_lahir'):
                    try:
                        from datetime import datetime
                        role_data['tgl_lahir'] = datetime.fromisoformat(role_data['tgl_lahir']).date()
                    except:
                        role_data['tgl_lahir'] = None
                        
                # Get visitor's reservations
                reservasi_result = supabase.table('reservasi').select('''
                    *,
                    fasilitas(nama, jadwal, kapasitas_max)
                ''').eq('username_p', username).order('tanggal_kunjungan', desc=True).execute()
                
                completed_visits = []
                all_tickets = [] 
                
                # Counters for statistics
                total_completed_tickets = 0
                total_scheduled_tickets = 0
                total_active_tickets = 0 
                
                if reservasi_result.data:
                    from datetime import datetime, date
                    
                    for reservasi in reservasi_result.data:
                        try:
                            # Parse tanggal kunjungan
                            tanggal_kunjungan = datetime.fromisoformat(reservasi['tanggal_kunjungan']).date()
                            facility_name = reservasi['nama_fasilitas']
                            status = reservasi['status'].lower()
                            jumlah_tiket = reservasi['jumlah_tiket']
                            
                            # Determine facility type (wahana/atraksi)
                            facility_type = "Fasilitas"
                            
                            # Check if it's a wahana
                            wahana_check = supabase.table('wahana').select('nama_wahana').eq('nama_wahana', facility_name).execute()
                            if wahana_check.data:
                                facility_type = "Wahana"
                            else:
                                # Check if it's an atraksi
                                atraksi_check = supabase.table('atraksi').select('nama_atraksi').eq('nama_atraksi', facility_name).execute()
                                if atraksi_check.data:
                                    facility_type = "Atraksi"
                            
                            # Count tickets for statistics
                            if status == 'selesai':
                                total_completed_tickets += jumlah_tiket
                                total_active_tickets += jumlah_tiket
                                
                                # Add to completed visits
                                completed_visits.append({
                                    'tanggal': tanggal_kunjungan,
                                    'tanggal_formatted': tanggal_kunjungan.strftime('%d %B %Y'),
                                    'nama_fasilitas': facility_name,
                                    'jenis_fasilitas': facility_type,
                                    'jumlah_tiket': jumlah_tiket,
                                    'status': reservasi['status']
                                })
                                
                            elif status == 'terjadwal':
                                total_scheduled_tickets += jumlah_tiket
                                total_active_tickets += jumlah_tiket
                            
                            # Add to all tickets
                            if status in ['terjadwal', 'selesai', 'dibatalkan']:
                                all_tickets.append({
                                    'tanggal': tanggal_kunjungan,
                                    'tanggal_formatted': tanggal_kunjungan.strftime('%d %B %Y'),
                                    'nama_fasilitas': facility_name,
                                    'jenis_fasilitas': facility_type,
                                    'jumlah_tiket': jumlah_tiket,
                                    'status': reservasi['status']
                                })
                            
                        except Exception as e:
                            print(f"Error parsing reservation: {str(e)}")
                            continue
                
                role_data['completed_visits'] = completed_visits  
                role_data['all_tickets'] = all_tickets 
                
                # Calculate statistics
                role_data['total_visits'] = total_completed_tickets
                role_data['upcoming_visits'] = total_scheduled_tickets
                role_data['total_tickets'] = total_active_tickets
                        
        elif role == 'veterinarian':
            # Get veterinarian specific data
            dokter_result = supabase.table('dokter_hewan').select('*').eq('username_dh', username).execute()
            if dokter_result.data:
                role_data = dokter_result.data[0]
                
            # Get specializations
            spesialisasi_result = supabase.table('spesialisasi').select('nama_spesialisasi').eq('username_sh', username).execute()
            if spesialisasi_result.data:
                role_data['specializations'] = [s['nama_spesialisasi'] for s in spesialisasi_result.data]
            else:
                role_data['specializations'] = []
            
            # Get medical records handled by this vet
            catatan_result = supabase.table('catatan_medis').select('*').eq('username_dh', username).execute()
            if catatan_result.data:
                medical_records = catatan_result.data
                
                # Count unique animals (total patients)
                unique_animals = len(set(record['id_hewan'] for record in medical_records))
                role_data['total_patients'] = unique_animals
                
                # Count active patients (animals with recent records)
                active_patients = len([r for r in medical_records if r.get('status_kesehatan') in ['Sakit', 'Dalam Perawatan']])
                role_data['active_patients'] = active_patients
                
                # Count recovered patients
                recovered_patients = len([r for r in medical_records if r.get('status_kesehatan') == 'Sehat'])
                role_data['recovered_patients'] = recovered_patients
                
                # Get latest 5 medical records
                latest_records = sorted(medical_records, key=lambda x: x.get('tanggal_pemeriksaan', ''), reverse=True)[:5]
                role_data['latest_records'] = latest_records
            else:
                role_data['total_patients'] = 0
                role_data['active_patients'] = 0
                role_data['recovered_patients'] = 0
                role_data['latest_records'] = []
                
        elif role == 'animal_keeper':
            # Get animal keeper specific data
            keeper_result = supabase.table('penjaga_hewan').select('*').eq('username_jh', username).execute()
            if keeper_result.data:
                role_data = keeper_result.data[0]
            
            # Get feeding records for today
            memberi_result = supabase.table('memberi').select('*').eq('username_jh', username).execute()
            if memberi_result.data:
                feeding_records = memberi_result.data
                
                # Count animals fed today
                today_feeding = []
                for record in feeding_records:
                    jadwal_str = record.get('jadwal')
                    if jadwal_str:
                        try:
                            # Parse the timestamp to check if it's today
                            jadwal_date = datetime.fromisoformat(jadwal_str.replace('Z', '+00:00')).date()
                            if jadwal_date == today:
                                today_feeding.append(record)
                        except:
                            continue
                
                # Count unique animals fed today
                animals_fed_today = len(set(record['id_hewan'] for record in today_feeding))
                role_data['animals_fed_today'] = animals_fed_today
                role_data['feeding_sessions_today'] = len(today_feeding)
            else:
                role_data['animals_fed_today'] = 0
                role_data['feeding_sessions_today'] = 0
                
        elif role == 'trainer':
            # Get trainer specific data
            trainer_result = supabase.table('pelatih_hewan').select('*').eq('username_lh', username).execute()
            if trainer_result.data:
                role_data = trainer_result.data[0]
                
                # Get current date
                from datetime import datetime, date
                today = date.today()
                
                try:
                    # Get scheduled shows for trainer
                    jadwal_result = supabase.table('jadwal_penugasan').select('''
                        tgl_penugasan,
                        nama_atraksi,
                        atraksi(lokasi)
                    ''').eq('username_lh', username).execute()
                    
                    shows = []
                    if jadwal_result.data:
                        for jadwal in jadwal_result.data:
                            try:
                                jadwal_datetime = datetime.fromisoformat(jadwal['tgl_penugasan'].replace('Z', '+00:00'))
                                jadwal_date = jadwal_datetime.date()
                                jadwal_time = jadwal_datetime.time()
                                
                                # Check if it's today's show
                                if jadwal_date == today:
                                    current_time = datetime.now().time()
                                    
                                    # Determine status
                                    if current_time < jadwal_time:
                                        status = 'upcoming'  
                                    elif current_time >= jadwal_time and current_time <= datetime.combine(today, jadwal_time).replace(hour=jadwal_time.hour + 1).time():
                                        status = 'ongoing'  
                                    else:
                                        status = 'completed' 
                                    
                                    shows.append({
                                        'time': jadwal_time.strftime('%H:%M'),
                                        'name': jadwal['nama_atraksi'],
                                        'location': jadwal['atraksi']['lokasi'] if jadwal['atraksi'] else 'Lokasi tidak ditemukan',
                                        'status': status,
                                        'datetime': jadwal_datetime
                                    })
                            except Exception as e:
                                print(f"Error parsing jadwal: {str(e)}")
                                continue
                    
                    # Sort shows by time
                    shows.sort(key=lambda x: x['datetime'])
                    role_data['shows'] = shows
                    
                    # Get animals trained by this trainer
                    trainer_shows = supabase.table('jadwal_penugasan').select('nama_atraksi').eq('username_lh', username).execute()
                    
                    trained_animals = []
                    if trainer_shows.data:
                        show_names = [show['nama_atraksi'] for show in trainer_shows.data]
                        
                        # Get animals participating in these shows
                        for show_name in set(show_names): 
                            animals_result = supabase.table('berpartisipasi').select('''
                                hewan(id, nama, spesies)
                            ''').eq('nama_fasilitas', show_name).execute()
                            
                            if animals_result.data:
                                for animal_data in animals_result.data:
                                    if animal_data['hewan']:
                                        trained_animals.append({
                                            'id': animal_data['hewan']['id'],
                                            'name': animal_data['hewan']['nama'] or 'Nama tidak tersedia',
                                            'species': animal_data['hewan']['spesies'],
                                            'show': show_name
                                        })
                    
                    role_data['trained_animals'] = trained_animals
                    
                    # Calculate statistics
                    role_data['total_shows_today'] = len(shows)
                    role_data['total_animals'] = len(trained_animals)
                    role_data['completed_shows'] = len([s for s in shows if s['status'] == 'completed'])
                    role_data['upcoming_shows'] = len([s for s in shows if s['status'] == 'upcoming'])
                    
                except Exception as e:
                    print(f"Error getting trainer data: {str(e)}")
                    # Set default values if error occurs
                    role_data['shows'] = []
                    role_data['trained_animals'] = []
                    role_data['total_shows_today'] = 0
                    role_data['total_animals'] = 0
                    role_data['completed_shows'] = 0
                    role_data['upcoming_shows'] = 0
                
        elif role == 'admin_staff':
            # Get admin staff specific data
            admin_result = supabase.table('staf_admin').select('*').eq('username_sa', username).execute()
            if admin_result.data:
                role_data = admin_result.data[0]
                
                # Calculate ticket statistics
                try:
                    # Get all reservations
                    reservasi_result = supabase.table('reservasi').select('*').execute()
                    
                    if reservasi_result.data:
                        reservations = reservasi_result.data
                        
                        # Calculate total tickets 
                        total_tickets = sum(
                            r['jumlah_tiket'] for r in reservations 
                            if r['status'].lower() in ['terjadwal', 'selesai']
                        )
                        
                        # Calculate revenue 
                        total_revenue = total_tickets * 100000
                        
                        # Calculate visitors (only completed tickets)
                        total_visitors = sum(
                            r['jumlah_tiket'] for r in reservations 
                            if r['status'].lower() == 'selesai'
                        )
                        
                        # Add calculated data to role_data
                        role_data['ticket_count'] = total_tickets
                        role_data['revenue'] = total_revenue
                        role_data['today_visitor_count'] = total_visitors
                        
                        # Create revenue report by date
                        from collections import defaultdict
                        from datetime import datetime
                        
                        revenue_by_date = defaultdict(lambda: {'tickets': 0, 'revenue': 0, 'visitors': 0})
                        
                        for reservation in reservations:
                            date_str = reservation['tanggal_kunjungan']
                            status = reservation['status'].lower()
                            tickets = reservation['jumlah_tiket']
                            
                            # Add to revenue report if status is terjadwal or selesai
                            if status in ['terjadwal', 'selesai']:
                                revenue_by_date[date_str]['tickets'] += tickets
                                revenue_by_date[date_str]['revenue'] += tickets * 100000
                                
                                # Add visitors only if status is selesai
                                if status == 'selesai':
                                    revenue_by_date[date_str]['visitors'] += tickets
                        
                        # Convert to list and sort by date
                        revenue_report = []
                        for date_str, data in revenue_by_date.items():
                            try:
                                # Parse date for proper sorting
                                date_obj = datetime.fromisoformat(date_str).date()
                                revenue_report.append({
                                    'date': date_str,
                                    'date_obj': date_obj,
                                    'formatted_date': date_obj.strftime('%d %B %Y'),
                                    'tickets': data['tickets'],
                                    'revenue': data['revenue'],
                                })
                            except:
                                revenue_report.append({
                                    'date': date_str,
                                    'date_obj': None,
                                    'formatted_date': date_str,
                                    'tickets': data['tickets'],
                                    'revenue': data['revenue'],
                                })
                        
                        # Sort by date
                        revenue_report.sort(key=lambda x: x['date_obj'] or datetime.min.date(), reverse=True)
                        role_data['revenue_report'] = revenue_report
                        
                    else:
                        # No reservations found
                        role_data['ticket_count'] = 0
                        role_data['revenue'] = 0
                        role_data['today_visitor_count'] = 0
                        role_data['revenue_report'] = []
                        
                except Exception as e:
                    print(f"Error calculating admin statistics: {str(e)}")
                    # Set default values if calculation fails
                    role_data['ticket_count'] = 0
                    role_data['revenue'] = 0
                    role_data['today_visitor_count'] = 0
                    role_data['revenue_report'] = []
        
        context = {
            'role': role,
            'user': user_data,
            'username': username,
            'role_data': role_data,
            'visitor_data': visitor_data,
        }
        
        return render(request, 'dashboard.html', context)
        
    except Exception as e:
        messages.error(request, f'Error mengakses dashboard: {str(e)}')
        return redirect('main:login')


@login_required_custom
def profile_settings(request):
    """View for updating user profile information based on their role"""
    try:
        username = request.session.get('username')
        role = request.session.get('user_role')
        
        # Get current user data
        user_result = supabase.table('pengguna').select('*').eq('username', username).execute()
        if not user_result.data:
            messages.error(request, 'Profil pengguna tidak ditemukan')
            return redirect('main:dashboard')
            
        user_data = user_result.data[0]
        
        if request.method == 'POST':
            try:
                # Update PENGGUNA table
                update_data = {
                    'email': request.POST.get('email'),
                    'nama_depan': request.POST.get('first_name'),
                    'nama_belakang': request.POST.get('last_name'),
                    'nama_tengah': request.POST.get('middle_name', ''),
                    'no_telepon': request.POST.get('phone_number')
                }
                
                supabase.table('pengguna').update(update_data).eq('username', username).execute()
                
                # Update role-specific tables
                if role == 'visitor':
                    visitor_data = {
                        'alamat': request.POST.get('address'),
                        'tgl_lahir': request.POST.get('birth_date')
                    }
                    supabase.table('pengunjung').update(visitor_data).eq('username_p', username).execute()
                
                elif role == 'veterinarian':
                    # Ambil spesialisasi dari form
                    new_specialization = request.POST.get('specialization')
                    other_specialization = request.POST.get('other_specialization')

                    if new_specialization == 'other' and other_specialization:
                        new_specialization = other_specialization

                    if new_specialization:
                        # Hapus spesialisasi lama
                        supabase.table('spesialisasi').delete().eq('username_sh', username).execute()
                        # Simpan spesialisasi baru
                        spesialisasi_data = {
                            'username_sh': username,
                            'nama_spesialisasi': new_specialization
                        }
                        supabase.table('spesialisasi').insert(spesialisasi_data).execute()
                
                # Update session data
                request.session['user_data'] = {**user_data, **update_data}
                
                messages.success(request, 'Profil berhasil diperbarui')
                return redirect('main:dashboard')
                
            except Exception as e:
                messages.error(request, f'Error saat memperbarui profil: {str(e)}')
        
        # Get role-specific data for display
        role_data = {}
        if role == 'visitor':
            visitor_result = supabase.table('pengunjung').select('*').eq('username_p', username).execute()
            if visitor_result.data:
                role_data = visitor_result.data[0]
                
        elif role == 'veterinarian':
            dokter_result = supabase.table('dokter_hewan').select('*').eq('username_dh', username).execute()
            if dokter_result.data:
                role_data = dokter_result.data[0]
                
            # Get specializations
            spesialisasi_result = supabase.table('spesialisasi').select('nama_spesialisasi').eq('username_sh', username).execute()
            role_data['specializations'] = [s['nama_spesialisasi'] for s in spesialisasi_result.data]
        
        elif role == 'animal_keeper':
            keeper_result = supabase.table('penjaga_hewan').select('*').eq('username_jh', username).execute()
            if keeper_result.data:
                role_data = keeper_result.data[0]

        elif role == 'trainer':
            trainer_result = supabase.table('pelatih_hewan').select('*').eq('username_lh', username).execute()
            if trainer_result.data:
                role_data = trainer_result.data[0]

        elif role == 'admin_staff':
            admin_result = supabase.table('staf_admin').select('*').eq('username_sa', username).execute()
            if admin_result.data:
                role_data = admin_result.data[0]
        context = {
            'user_data': user_data,
            'role_data': role_data,
            'role': role,
            'username': username
        }
        
        return render(request, 'profile_settings.html', context)
        
    except Exception as e:
        messages.error(request, f'Error mengakses pengaturan profil: {str(e)}')
        return redirect('main:dashboard')

@login_required_custom
def change_password(request):
    """View for changing user password"""
    try:
        username = request.session.get('username')
        
        if request.method == 'POST':
            form = PasswordChangeForm(request.POST)
            if form.is_valid():
                current_password = form.cleaned_data['current_password']
                new_password = form.cleaned_data['new_password']
                
                try:
                    # Verify current password
                    result = supabase.table('pengguna').select('password').eq('username', username).execute()
                    
                    if not result.data or len(result.data) == 0:
                        messages.error(request, 'Pengguna tidak ditemukan')
                        return render(request, 'change_password.html', {'form': form})
                    
                    current_db_password = result.data[0]['password']
                    
                    if current_password != current_db_password:
                        messages.error(request, 'Password lama tidak benar')
                        return render(request, 'change_password.html', {'form': form})
                    
                    # Update password in Supabase
                    update_result = supabase.table('pengguna').update({
                        'password': new_password
                    }).eq('username', username).execute()
                    
                    if update_result.data:
                        # Update session data
                        user_data = request.session.get('user_data')
                        if user_data:
                            user_data['password'] = new_password
                            request.session['user_data'] = user_data
                        
                        messages.success(request, 'Password berhasil diubah')
                        return redirect('main:dashboard')
                    else:
                        messages.error(request, 'Gagal mengubah password')
                        
                except Exception as e:
                    messages.error(request, f'Error saat mengubah password: {str(e)}')
            else:
                # Display form errors
                for field_name, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field_name}: {error}')
        else:
            form = PasswordChangeForm()
        
        return render(request, 'change_password.html', {'form': form})
        
    except Exception as e:
        messages.error(request, f'Error mengakses halaman ubah password: {str(e)}')
        return redirect('main:dashboard')