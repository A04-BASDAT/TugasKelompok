from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import FeedingForm
from supabase_utils import (
    get_all_pakan, get_pakan_by_id,
    create_pakan, update_pakan, delete_pakan, mark_done_pakan
)
from .forms import FeedingForm

from supabase_utils import get_all_pakan
from datetime import datetime

from django.contrib import messages


@login_required
def feeding_list(request):
    feedings = get_all_pakan()

    for feed in feedings:
        # Inject 'id' agar kompatibel dengan {% url 'edit_feeding' feed.id %}
        feed['id'] = feed.get('id_hewan')

        # Konversi jadwal dari ISO string ke datetime object agar bisa diformat
        if 'jadwal' in feed and isinstance(feed['jadwal'], str):
            try:
                feed['jadwal'] = datetime.fromisoformat(feed['jadwal'])
            except ValueError:
                feed['jadwal'] = None

    print("[DEBUG] Data Feedings:")
    for f in feedings:
        print(f)

    return render(request, 'feeding/feeding_list.html', {'feedings': feedings})

@login_required
def add_feeding(request):
    if request.method == 'POST':
        form = FeedingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data["penjaga"] = request.user.username  # Tambahkan penjaga dari session user
            create_pakan(data)
            messages.success(request, "Jadwal pakan berhasil ditambahkan.")
            return redirect('feeding_list')
    else:
        form = FeedingForm()
    return render(request, 'feeding/add_feeding.html', {'form': form})


@login_required
def edit_feeding(request, feeding_id):
    existing = get_pakan_by_id(feeding_id)
    if not existing:
        messages.error(request, "Jadwal tidak ditemukan.")
        return redirect('feeding_list')

    print(request.user.username)
    feeding = existing[0]
    if feeding.get("penjaga") != request.user.username:
        messages.error(request, "Anda tidak memiliki akses.")
        return redirect('feeding_list')

    if request.method == 'POST':
        form = FeedingForm(request.POST)
        if form.is_valid():
            update_pakan(feeding_id, form.cleaned_data)
            messages.success(request, "Jadwal pakan berhasil diperbarui.")
            return redirect('feeding_list')
    else:
        form = FeedingForm(initial=feeding)
    return render(request, 'feeding/edit_feeding.html', {'form': form})


@login_required
def delete_feeding(request, feeding_id):
    existing = get_pakan_by_id(feeding_id)
    if not existing:
        messages.error(request, "Jadwal tidak ditemukan.")
        return redirect('feeding_list')

    print(request.user.username)
    feeding = existing[0]
    if feeding.get("penjaga") != request.user.username:
        messages.error(request, "Anda tidak memiliki akses.")
        return redirect('feeding_list')

    if request.method == 'POST':
        delete_pakan(feeding_id)
        messages.success(request, "Jadwal pakan berhasil dihapus.")
        return redirect('feeding_list')

    return render(request, 'feeding/delete_feeding.html', {'feeding': feeding})


@login_required
def mark_as_done(request, feeding_id):
    existing = get_pakan_by_id(feeding_id)
    if not existing:
        messages.error(request, "Jadwal tidak ditemukan.")
        return redirect('feeding_list')

    feeding = existing[0]
    if feeding.get("penjaga") != request.user.username:
        messages.error(request, "Anda tidak memiliki akses.")
        return redirect('feeding_list')

    mark_done_pakan(feeding_id)
    messages.success(request, "Jadwal pakan ditandai selesai.")
    return redirect('feeding_list')
