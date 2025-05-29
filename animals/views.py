from ast import Dict, List
from typing import Any, Optional, List, Dict
import uuid
from datetime import datetime
from supabase_client import supabase
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views import View
from django.contrib import messages
from .forms import AnimalForm
import json
from supabase_utils import (
    get_all_hewan,
    get_hewan_by_id
)

def check_habitat_capacity(nama_habitat: str) -> tuple[bool, str]:
    """
    Cek apakah habitat masih punya kapasitas untuk menampung hewan baru.
    Mengembalikan tuple: (boleh_ditambah, pesan)
    """
    try:
        from habitats.views import get_habitat_by_nama, count_animals_in_habitat
        
        habitat = get_habitat_by_nama(nama_habitat)
        if not habitat:
            return False, "Habitat tidak ditemukan"

        current_count = count_animals_in_habitat(nama_habitat)
        max_capacity = habitat.get('kapasitas', 0)

        if current_count >= max_capacity:
            return False, f"Habitat '{nama_habitat}' sudah penuh ({current_count}/{max_capacity})."
        
        return True, f"Tersisa {max_capacity - current_count} slot dari {max_capacity} kapasitas"
    
    except Exception as e:
        return False, f"Gagal mengecek kapasitas habitat: {str(e)}"

# Updated Animal related functions using stored procedures
# PERBAIKAN untuk views.py - Ganti fungsi create_animal_with_validation dan update_animal_with_logging
# GANTI FUNGSI create_animal_with_validation dan update_animal_with_logging dengan versi ini:

def create_animal_with_validation(data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new animal record using stored procedure with validation - Simplified"""
    try:
        # Generate UUID for new animal
        animal_id = str(uuid.uuid4())
        
        # Call stored procedure (simplified version)
        result = supabase.rpc('create_animal_simple', {
            'p_id': animal_id,
            'p_nama': data.get('nama'),
            'p_spesies': data.get('spesies'),
            'p_asal_hewan': data.get('asal_hewan'),
            'p_tanggal_lahir': data.get('tanggal_lahir'),
            'p_status_kesehatan': data.get('status_kesehatan'),
            'p_nama_habitat': data.get('nama_habitat'),
            'p_url_foto': data.get('url_foto')
        }).execute()
        
        # Handle response - sekarang lebih sederhana karena return TEXT
        if result.data:
            response_text = result.data
            
            # Jika response adalah list, ambil item pertama
            if isinstance(response_text, list) and len(response_text) > 0:
                response_text = response_text[0]
            
            # Check if success or error
            if response_text.startswith('ERROR:'):
                error_message = response_text.replace('ERROR: ', '')
                raise Exception(error_message)
            elif response_text.startswith('SUCCESS:'):
                success_message = response_text.replace('SUCCESS: ', '')
                return {'id': animal_id, 'message': success_message}
            else:
                # Fallback
                return {'id': animal_id, 'message': response_text}
        else:
            raise Exception('No response from stored procedure')
            
    except Exception as e:
        raise Exception(str(e))

def update_animal_with_logging(id_hewan: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Update animal data using stored procedure with logging - Simplified"""
    try:
        # Call stored procedure (simplified version)
        result = supabase.rpc('update_animal_simple', {
            'p_id': id_hewan,
            'p_nama': data.get('nama'),
            'p_spesies': data.get('spesies'),
            'p_asal_hewan': data.get('asal_hewan'),
            'p_tanggal_lahir': data.get('tanggal_lahir'),
            'p_status_kesehatan': data.get('status_kesehatan'),
            'p_nama_habitat': data.get('nama_habitat'),
            'p_url_foto': data.get('url_foto')
        }).execute()
        
        # Handle response - sekarang lebih sederhana karena return TEXT
        if result.data:
            response_text = result.data
            
            # Jika response adalah list, ambil item pertama
            if isinstance(response_text, list) and len(response_text) > 0:
                response_text = response_text[0]
            
            # Check if success or error
            if response_text.startswith('ERROR:'):
                error_message = response_text.replace('ERROR: ', '')
                raise Exception(error_message)
            elif response_text.startswith('SUCCESS:'):
                success_message = response_text.replace('SUCCESS: ', '')
                return {'message': success_message}
            else:
                # Fallback
                return {'message': response_text}
        else:
            raise Exception('No response from stored procedure')
            
    except Exception as e:
        raise Exception(str(e))

def delete_animal(id_hewan: str) -> None:
    """Delete animal and related records"""
    # Delete related records first
    supabase.table('catatan_medis').delete().eq('id_hewan', id_hewan).execute()
    supabase.table('pakan').delete().eq('id_hewan', id_hewan).execute()
    supabase.table('memberi').delete().eq('id_hewan', id_hewan).execute()
    supabase.table('berpartisipasi').delete().eq('id_hewan', id_hewan).execute()
    supabase.table('jadwal_pemeriksaan_kesehatan').delete().eq('id_hewan', id_hewan).execute()
    supabase.table('adopsi').delete().eq('id_hewan', id_hewan).execute()
    supabase.table('riwayat_satwa').delete().eq('id_hewan', id_hewan).execute()
    
    # Finally delete the animal record
    supabase.table('hewan').delete().eq('id', id_hewan).execute()

def get_animals_with_habitat() -> List[Dict[str, Any]]:
    """Get all animals with habitat information"""
    return supabase.table('hewan').select('*, habitat:nama_habitat(*)').execute().data

# Views
class AnimalListView(View):
    template_name = 'animals/animal_list.html'

    def get(self, request):
        try:
            animals = get_animals_with_habitat()
            context = {
                'animals': animals
            }
            return render(request, self.template_name, context)
        except Exception as e:
            messages.error(request, f'Error mengambil data satwa: {str(e)}')
            context = {'animals': []}
            return render(request, self.template_name, context)

class AnimalCreateView(View):
    template_name = 'animals/animal_form.html'

    def get(self, request):
        form = AnimalForm()
        context = {
            'form': form,
            'title': 'FORM TAMBAH DATA SATWA',
            'is_add': True
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = AnimalForm(request.POST)
        if form.is_valid():
            nama_habitat = form.cleaned_data['habitat']

            # Cek kapasitas habitat sebelum menyimpan data
            if nama_habitat:
                has_capacity, message = check_habitat_capacity(nama_habitat)
                if not has_capacity:
                    messages.error(request, message)
                    context = {
                        'form': form,
                        'title': 'FORM TAMBAH DATA SATWA',
                        'is_add': True
                    }
                    return render(request, self.template_name, context)

            try:
                animal_data = {
                    'nama': form.cleaned_data['name'],
                    'spesies': form.cleaned_data['species'],
                    'asal_hewan': form.cleaned_data['origin'],
                    'tanggal_lahir': form.cleaned_data['birth_date'].isoformat() if form.cleaned_data['birth_date'] else None,
                    'status_kesehatan': form.cleaned_data['health_status'],
                    'nama_habitat': nama_habitat,
                    'url_foto': form.cleaned_data['photo_url']
                }

                # Use stored procedure with validation
                result = create_animal_with_validation(animal_data)
                
                # Show message from stored procedure
                if 'message' in result:
                    if 'sudah terdaftar' in result['message']:
                        messages.error(request, result['message'])
                        context = {
                            'form': form,
                            'title': 'FORM TAMBAH DATA SATWA',
                            'is_add': True
                        }
                        return render(request, self.template_name, context)
                    else:
                        messages.success(request, result['message'])
                else:
                    messages.success(request, f'Satwa berhasil ditambahkan ke habitat "{nama_habitat}"!')
                
                return HttpResponseRedirect(reverse_lazy('animals:animal_list'))

            except Exception as e:
                # Display exact error message from trigger/stored procedure
                error_message = str(e)
                messages.error(request, error_message)

        context = {
            'form': form,
            'title': 'FORM TAMBAH DATA SATWA',
            'is_add': True
        }
        return render(request, self.template_name, context)

class AnimalUpdateView(View):
    template_name = 'animals/animal_form.html'

    def get(self, request, pk):
        try:
            # Get animal data from Supabase
            animal_data = get_hewan_by_id(pk)
            
            if not animal_data:
                messages.error(request, 'Data satwa tidak ditemukan!')
                return redirect('animals:animal_list')

            # Prepare initial data for form
            initial_data = {
                'name': animal_data.get('nama'),
                'species': animal_data.get('spesies'),
                'origin': animal_data.get('asal_hewan'),
                'birth_date': animal_data.get('tanggal_lahir'),
                'health_status': animal_data.get('status_kesehatan'),
                'habitat': animal_data.get('nama_habitat'),
                'photo_url': animal_data.get('url_foto')
            }

            form = AnimalForm(initial=initial_data)
            context = {
                'form': form,
                'title': 'FORM EDIT DATA SATWA',
                'is_add': False,
                'animal': animal_data
            }
            return render(request, self.template_name, context)
            
        except Exception as e:
            messages.error(request, f'Error mengambil data satwa: {str(e)}')
            return redirect('animals:animal_list')

    def post(self, request, pk):
        try:
            # Get existing animal data
            animal_data = get_hewan_by_id(pk)
            
            if not animal_data:
                messages.error(request, 'Data satwa tidak ditemukan!')
                return redirect('animals:animal_list')

            form = AnimalForm(request.POST)
            if form.is_valid():
                # Prepare updated data for Supabase
                updated_data = {
                    'nama': form.cleaned_data['name'],
                    'spesies': form.cleaned_data['species'],
                    'asal_hewan': form.cleaned_data['origin'],
                    'tanggal_lahir': form.cleaned_data['birth_date'].isoformat() if form.cleaned_data['birth_date'] else None,
                    'status_kesehatan': form.cleaned_data['health_status'],
                    'nama_habitat': form.cleaned_data['habitat'],
                    'url_foto': form.cleaned_data['photo_url']
                }
                
                # Use stored procedure with logging
                result = update_animal_with_logging(pk, updated_data)
                
                # Show message from stored procedure
                if 'message' in result:
                    if 'SUKSES: Riwayat perubahan' in result['message']:
                        messages.success(request, result['message'])
                    else:
                        messages.success(request, result['message'])
                else:
                    messages.success(request, 'Data satwa berhasil diperbarui!')
                
                return HttpResponseRedirect(reverse_lazy('animals:animal_list'))

            context = {
                'form': form,
                'title': 'FORM EDIT DATA SATWA',
                'is_add': False,
                'animal': animal_data
            }
            return render(request, self.template_name, context)
            
        except Exception as e:
            # Display exact error message from trigger/stored procedure
            error_message = str(e)
            messages.error(request, error_message)
            return redirect('animals:animal_list')

class AnimalDeleteView(View):
    template_name = 'animals/animal_confirm_delete.html'

    def get(self, request, pk):
        try:
            # Get animal data from Supabase
            animal_data = get_hewan_by_id(pk)
            
            if not animal_data:
                messages.error(request, 'Data satwa tidak ditemukan!')
                return redirect('animals:animal_list')
            
            context = {'object': animal_data}
            return render(request, self.template_name, context)
            
        except Exception as e:
            messages.error(request, f'Error mengambil data satwa: {str(e)}')
            return redirect('animals:animal_list')

    def post(self, request, pk):
        try:
            # Check if animal exists
            animal_data = get_hewan_by_id(pk)
            
            if not animal_data:
                messages.error(request, 'Data satwa tidak ditemukan!')
                return redirect('animals:animal_list')
            
            # Delete animal from Supabase
            delete_animal(pk)
            messages.success(request, f'Data satwa "{animal_data.get("nama", "")}" berhasil dihapus!')
            return redirect('animals:animal_list')
            
        except Exception as e:
            messages.error(request, f'Error menghapus data satwa: {str(e)}')
            return redirect('animals:animal_list')