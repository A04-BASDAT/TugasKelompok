import uuid
from datetime import datetime
from decimal import Decimal
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from supabase_client import supabase
from typing import Any, Dict, List, Optional
from .forms import HabitatForm

# Utility functions for Supabase operations
def get_all_habitat() -> List[Dict[str, Any]]:
    """Get all habitats from database"""
    try:
        response = supabase.table('habitat').select('*').execute()
        return response.data
    except Exception as e:
        print(f"Error getting habitats: {e}")
        return []

def get_habitat_by_nama(nama_habitat: str) -> Optional[Dict[str, Any]]:
    """Get habitat by nama"""
    try:
        response = supabase.table('habitat').select('*').eq('nama', nama_habitat).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error getting habitat {nama_habitat}: {e}")
        return None

def get_all_hewan() -> List[Dict[str, Any]]:
    """Get all animals from database"""
    try:
        response = supabase.table('hewan').select('*').execute()
        return response.data
    except Exception as e:
        print(f"Error getting animals: {e}")
        return []

def create_habitat(data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new habitat"""
    try:
        response = supabase.table('habitat').insert(data).execute()
        return response.data[0] if response.data else {}
    except Exception as e:
        raise Exception(f"Failed to create habitat: {str(e)}")

def update_habitat(old_nama: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Update habitat by nama with proper transaction handling"""
    try:
        new_nama = data.get('nama')
        
        # If nama is being changed, we need to handle it carefully
        if old_nama != new_nama:
            # Check if new name already exists
            existing_habitat = get_habitat_by_nama(new_nama)
            if existing_habitat:
                raise Exception(f'Habitat dengan nama "{new_nama}" sudah ada!')
            
            # First, update the habitat record
            response = supabase.table('habitat').update(data).eq('nama', old_nama).execute()
            
            # Then update all animals to use the new habitat name
            animals = get_all_hewan()
            animals_in_habitat = [a for a in animals if a.get('nama_habitat') == old_nama]
            
            if animals_in_habitat:
                for animal in animals_in_habitat:
                    try:
                        supabase.table('hewan').update({
                            'nama_habitat': new_nama
                        }).eq('id', animal['id']).execute()
                    except Exception as e:
                        # If animal update fails, we need to rollback the habitat change
                        # Rollback habitat name change
                        supabase.table('habitat').update({'nama': old_nama}).eq('nama', new_nama).execute()
                        raise Exception(f"Failed to update animal {animal.get('nama', 'Unknown')}: {str(e)}")
            
            return response.data[0] if response.data else {}
        else:
            # If nama is not changing, just update other fields
            response = supabase.table('habitat').update(data).eq('nama', old_nama).execute()
            return response.data[0] if response.data else {}
            
    except Exception as e:
        raise Exception(f"Failed to update habitat: {str(e)}")

def delete_habitat_by_nama(nama_habitat: str) -> None:
    """Delete habitat by nama"""
    try:
        # Check if there are animals in this habitat
        animals = get_all_hewan()
        animals_in_habitat = [a for a in animals if a.get('nama_habitat') == nama_habitat]
        
        if animals_in_habitat:
            raise Exception(f"Tidak dapat menghapus habitat karena masih ada {len(animals_in_habitat)} hewan di dalamnya. Pindahkan atau hapus hewan terlebih dahulu.")
        
        supabase.table('habitat').delete().eq('nama', nama_habitat).execute()
    except Exception as e:
        raise Exception(f"Failed to delete habitat: {str(e)}")

def count_animals_in_habitat(nama_habitat: str) -> int:
    """Count animals in a specific habitat"""
    try:
        animals = get_all_hewan()
        return len([a for a in animals if a.get('nama_habitat') == nama_habitat])
    except Exception as e:
        print(f"Error counting animals in habitat {nama_habitat}: {e}")
        return 0

# Views
def habitat_list(request):
    """List all habitats"""
    try:
        habitats = get_all_habitat()
        return render(request, 'habitats/habitat_list.html', {
            'habitats': habitats
        })
    except Exception as e:
        messages.error(request, f'Error loading habitats: {str(e)}')
        return render(request, 'habitats/habitat_list.html', {'habitats': []})

def habitat_detail(request, nama_habitat):
    """Show habitat detail with animals"""
    try:
        habitat = get_habitat_by_nama(nama_habitat)
        if not habitat:
            raise Http404("Habitat tidak ditemukan")
        
        # Get animals in this habitat
        all_animals = get_all_hewan()
        animals = [animal for animal in all_animals if animal.get('nama_habitat') == nama_habitat]
        
        return render(request, 'habitats/habitat_detail.html', {
            'habitat': habitat,
            'animals': animals
        })
    except Http404:
        messages.error(request, 'Habitat tidak ditemukan')
        return redirect('habitats:habitat_list')
    except Exception as e:
        messages.error(request, f'Error loading habitat detail: {str(e)}')
        return redirect('habitats:habitat_list')

def habitat_add(request):
    """Add new habitat"""
    if request.method == 'POST':
        # Get existing habitats for validation
        existing_habitats = get_all_habitat()
        
        form = HabitatForm(
            request.POST, 
            existing_habitats=existing_habitats,
            current_animal_count=0
        )
        
        if form.is_valid():
            try:
                # Convert Decimal to float for JSON serialization
                habitat_data = {
                    'nama': form.cleaned_data['nama'].strip(),
                    'luas_area': float(form.cleaned_data['luas_area']),
                    'kapasitas': int(form.cleaned_data['kapasitas']),
                    'status': form.cleaned_data['status'].strip()
                }
                
                create_habitat(habitat_data)
                messages.success(request, f'Habitat "{habitat_data["nama"]}" berhasil ditambahkan!')
                return redirect('habitats:habitat_list')
                
            except Exception as e:
                messages.error(request, f'Error creating habitat: {str(e)}')
                return render(request, 'habitats/habitat_form.html', {
                    'form': form,
                    'title': 'FORM TAMBAH HABITAT',
                    'is_add': True
                })
    else:
        # Get existing habitats for validation
        existing_habitats = get_all_habitat()
        form = HabitatForm(existing_habitats=existing_habitats, current_animal_count=0)
    
    return render(request, 'habitats/habitat_form.html', {
        'form': form,
        'title': 'FORM TAMBAH HABITAT',
        'is_add': True
    })

def habitat_edit(request, nama_habitat):
    """Edit existing habitat"""
    try:
        habitat = get_habitat_by_nama(nama_habitat)
        if not habitat:
            messages.error(request, 'Habitat tidak ditemukan')
            return redirect('habitats:habitat_list')
        
        # Count current animals in habitat
        current_animal_count = count_animals_in_habitat(nama_habitat)
        
        if request.method == 'POST':
            # Get existing habitats for validation
            existing_habitats = get_all_habitat()
            
            form = HabitatForm(
                request.POST,
                existing_habitats=existing_habitats,
                current_animal_count=current_animal_count,
                original_nama=nama_habitat
            )
            
            if form.is_valid():
                try:
                    # Convert Decimal to float for JSON serialization
                    habitat_data = {
                        'nama': form.cleaned_data['nama'].strip(),
                        'luas_area': float(form.cleaned_data['luas_area']),
                        'kapasitas': int(form.cleaned_data['kapasitas']),
                        'status': form.cleaned_data['status'].strip()
                    }
                    
                    update_habitat(nama_habitat, habitat_data)
                    messages.success(request, 'Habitat berhasil diperbarui!')
                    return redirect('habitats:habitat_detail', nama_habitat=habitat_data['nama'])
                    
                except Exception as e:
                    messages.error(request, f'Error updating habitat: {str(e)}')
                    return render(request, 'habitats/habitat_form.html', {
                        'form': form,
                        'title': 'FORM EDIT HABITAT',
                        'is_add': False,
                        'habitat': habitat,
                        'current_animal_count': current_animal_count
                    })
        else:
            # Get existing habitats for validation
            existing_habitats = get_all_habitat()
            
            # Pre-populate form with existing data
            form = HabitatForm(
                initial={
                    'nama': habitat['nama'],
                    'luas_area': habitat['luas_area'],
                    'kapasitas': habitat['kapasitas'],
                    'status': habitat['status']
                },
                existing_habitats=existing_habitats,
                current_animal_count=current_animal_count,
                original_nama=nama_habitat
            )
        
        return render(request, 'habitats/habitat_form.html', {
            'form': form,
            'title': 'FORM EDIT HABITAT',
            'is_add': False,
            'habitat': habitat,
            'current_animal_count': current_animal_count
        })
        
    except Exception as e:
        messages.error(request, f'Error loading habitat: {str(e)}')
        return redirect('habitats:habitat_list')

def habitat_delete(request, nama_habitat):
    """Delete habitat with confirmation"""
    try:
        habitat = get_habitat_by_nama(nama_habitat)
        if not habitat:
            messages.error(request, 'Habitat tidak ditemukan')
            return redirect('habitats:habitat_list')
        
        # Get animals count in this habitat
        all_animals = get_all_hewan()
        animals_in_habitat = [animal for animal in all_animals if animal.get('nama_habitat') == nama_habitat]
        
        if request.method == 'POST':
            try:
                delete_habitat_by_nama(nama_habitat)
                messages.success(request, f'Habitat "{nama_habitat}" berhasil dihapus!')
                return redirect('habitats:habitat_list')
            except Exception as e:
                messages.error(request, f'Error deleting habitat: {str(e)}')
                return redirect('habitats:habitat_detail', nama_habitat=nama_habitat)
        
        return render(request, 'habitats/habitat_confirm_delete.html', {
            'habitat': habitat,
            'animals_count': len(animals_in_habitat),
            'animals': animals_in_habitat
        })
        
    except Exception as e:
        messages.error(request, f'Error loading habitat: {str(e)}')
        return redirect('habitats:habitat_list')