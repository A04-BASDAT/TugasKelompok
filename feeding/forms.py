from django import forms

class FeedingForm(forms.Form):
    id_hewan = forms.CharField(label='ID Hewan')
    jenis = forms.CharField(label='Jenis Pakan')
    jumlah = forms.IntegerField(label='Jumlah Pakan (g)')
    jadwal = forms.DateTimeField(
        label='Jadwal',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    status = forms.CharField(
        initial='Terjadwal',
        widget=forms.HiddenInput()
    )
