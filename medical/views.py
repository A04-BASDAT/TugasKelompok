from datetime import datetime, date
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .forms import MedicalRecordForm, EditMedicalRecordForm
from .models import MedicalRecord
from .forms import HealthCheckScheduleForm  
from supabase_utils import (
    get_all_hewan,
    get_all_dokter_hewan,
    get_all_catatan_medis,
    get_catatan_medis_by_id,
    get_catatan_medis_by_key,
    create_catatan_medis,
    update_catatan_medis,
    delete_catatan_medis,
    create_jadwal_pemeriksaan,
    get_jadwal_pemeriksaan_by_id_hewan,
    get_all_jadwal_pemeriksaan,
    update_jadwal_pemeriksaan,
    delete_jadwal_pemeriksaan,
    serialize_dates,
    get_hewan_by_id
    
)

# ==============================
# REKAM MEDIS HEWAN (CRUD)
# ==============================

def record_list(request):
    records = get_all_catatan_medis()
    for record in records:
        if record.get("id_hewan") and record.get("tanggal_pemeriksaan"):
            record["record_id"] = f"{record['id_hewan']}__{record['tanggal_pemeriksaan'][:10]}"
        else:
            record["record_id"] = ""
    return render(request, 'medical_records/record_list.html', {'records': records})

def add_record(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            try:
                raw_data = form.cleaned_data.copy()

                # Hanya izinkan field yang valid untuk Supabase
                allowed_fields = [
                    'id_hewan',
                    'tanggal_pemeriksaan',
                    'username_dh',
                    'status_kesehatan',
                    'diagnosis',
                    'pengobatan'
                ]

                # Filter dan serialize tanggal
                data = {}
                for key in allowed_fields:
                    value = raw_data.get(key)
                    if isinstance(value, (datetime, date)):
                        data[key] = value.isoformat()
                    else:
                        data[key] = value

                # Log debugging (optional)
                print("[DEBUG] Final data dikirim:", data)

                # Insert ke Supabase
                create_catatan_medis(data)

                # Ambil nama hewan untuk ditampilkan di pesan
                hewan = get_hewan_by_id(data['id_hewan'])
                nama_hewan = hewan['nama'] if hewan and 'nama' in hewan else 'Hewan'

                # Tampilkan pesan sesuai status kesehatan
                if data.get('status_kesehatan') == 'Sakit':
                    messages.success(request, f'SUKSES: Jadwal pemeriksaan hewan "{nama_hewan}" telah diperbarui karena status kesehatan "Sakit".')
                else:
                    messages.success(request, 'Rekam medis berhasil ditambahkan!')

                return redirect('medical:record_list')


            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    else:
        form = MedicalRecordForm()

    return render(request, 'medical_records/add_record.html', {'form': form})

def edit_record(request, record_id):
    try:
        id_hewan, tanggal = record_id.split('__')
    except ValueError:
        return redirect('medical:record_list')
    
    record = get_catatan_medis_by_key(id_hewan, tanggal)
    if not record:
        return redirect('medical:record_list')
    
    if request.method == 'POST':
        form = EditMedicalRecordForm(request.POST, initial=record)
        if form.is_valid():
            try:
                update_data = form.cleaned_data.copy()
                update_catatan_medis(id_hewan, tanggal, update_data)
                messages.success(request, 'Rekam medis berhasil diupdate!')
                return redirect('medical:record_list')
            except Exception as e:
                messages.error(request, f'Error saat update: {str(e)}')
    else:
        form = EditMedicalRecordForm(initial=record)
    
    return render(request, 'medical_records/edit_record.html', {'form': form})

def delete_record(request, record_id):
    try:
        id_hewan, tanggal = record_id.split('__')
    except ValueError:
        return redirect('medical:record_list')
    
    record = get_catatan_medis_by_key(id_hewan, tanggal)
    if request.method == 'POST':
        try:
            delete_catatan_medis(id_hewan, tanggal)
            messages.success(request, 'Rekam medis berhasil dihapus!')
            return redirect('medical:record_list')
        except Exception as e:
            messages.error(request, f'Gagal menghapus: {str(e)}')
    
    return render(request, 'medical_records/delete_record.html', {'record': record})

# ==============================
# PENJADWALAN PEMERIKSAAN KESEHATAN
# ==============================

def health_check_schedule(request):
    if request.method == 'POST':
        form = HealthCheckScheduleForm(request.POST)
        if form.is_valid():
            id_hewan = form.cleaned_data.get('id_hewan')
            tanggal_pemeriksaan = form.cleaned_data.get('tanggal_pemeriksaan_selanjutnya')
            username_dh = form.cleaned_data.get('username_dh')

            data = {
                'id_hewan': id_hewan,
                'tanggal_pemeriksaan_selanjutnya': tanggal_pemeriksaan,
                'freq_pemeriksaan_rutin': 3,
                'is_auto_generated': False
            }
            if username_dh:
                data['username_dh'] = username_dh

            data = serialize_dates(data)
            try:
                create_jadwal_pemeriksaan(data)

                # Ambil nama hewan
                hewan = get_hewan_by_id(data['id_hewan'])
                nama_hewan = hewan['nama'] if hewan and 'nama' in hewan else 'Hewan'

                # Tampilkan pesan sukses
                messages.success(request, f'SUKSES: Jadwal pemeriksaan rutin hewan "{nama_hewan}" telah ditambahkan sesuai frekuensi.')
                return redirect('medical:health_check_schedule')

            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    else:
        form = HealthCheckScheduleForm() 

    context = {
        'form': form,  
        'animals': get_all_hewan(),
        'doctors': get_all_dokter_hewan(),
        'schedules': get_all_jadwal_pemeriksaan(),
    }
    return render(request, 'medical_records/health_check_schedule.html', context)


def schedule_list(request):
    schedules = get_all_jadwal_pemeriksaan()
    return render(request, 'medical/schedule_list.html', {'schedules': schedules})
