from django import forms
from .models import MedicalRecord
from supabase_utils import get_all_hewan
from .models import MedicalRecord
from .models import HealthCheckSchedule


class MedicalRecordForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(hewan['id'], f"{hewan['nama']} ({hewan['id']})") for hewan in get_all_hewan()]
        self.fields['id_hewan'] = forms.ChoiceField(choices=choices, label="Hewan")

    class Meta:
        model = MedicalRecord
        fields = ['id_hewan', 'tanggal_pemeriksaan', 'username_dh', 'status_kesehatan', 'diagnosis', 'pengobatan']

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status_kesehatan')
        diagnosis = cleaned_data.get('diagnosis')
        pengobatan = cleaned_data.get('pengobatan')

        if status == 'Sakit':
            if not diagnosis:
                self.add_error('diagnosis', 'Diagnosis wajib diisi untuk status Sakit.')
            if not pengobatan:
                self.add_error('pengobatan', 'Pengobatan wajib diisi untuk status Sakit.')

class EditMedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['catatan_tindak_lanjut', 'diagnosis', 'pengobatan']

class HealthCheckScheduleForm(forms.Form):  # ✅ gunakan forms.Form jika bukan dari model
    id_hewan = forms.ChoiceField(label="Pilih Hewan")
    tanggal_pemeriksaan_selanjutnya = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_hewan'].choices = [
            (hewan['id'], f"{hewan['nama']} ({hewan['id']})") for hewan in get_all_hewan()
        ]