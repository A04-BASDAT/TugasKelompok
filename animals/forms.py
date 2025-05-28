from django import forms
from supabase_utils import get_all_habitat

class AnimalForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="Nama Individu",
        widget=forms.TextInput(attrs={'placeholder': '[isian] (opsional)'})
    )
    
    species = forms.CharField(
        max_length=100,
        required=True,
        label="Spesies",
        widget=forms.TextInput(attrs={'placeholder': '[isian]'})
    )
    
    origin = forms.CharField(
        max_length=100,
        required=True,
        label="Asal Hewan",
        widget=forms.TextInput(attrs={'placeholder': '[isian]'})
    )
    
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Tanggal Lahir"
    )
    
    health_status = forms.CharField(
        max_length=50,
        required=True,
        label="Status Kesehatan",
        widget=forms.TextInput(attrs={'placeholder': 'Contoh: Sehat, Sakit, Dalam Perawatan'})
    )
    
    habitat = forms.ChoiceField(
        required=False,
        label="Nama Habitat",
        choices=[]
    )
    
    photo_url = forms.URLField(
        required=True,
        label="URL Foto Satwa",
        widget=forms.URLInput(attrs={'placeholder': '[isian]'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get habitat choices from Supabase
        try:
            habitats = get_all_habitat()
            habitat_choices = [('', 'Pilih habitat')]
            habitat_choices.extend([(habitat['nama'], habitat['nama']) for habitat in habitats])
            self.fields['habitat'].choices = habitat_choices
        except Exception as e:
            # If error getting habitats, provide empty choice
            self.fields['habitat'].choices = [('', 'Pilih habitat')]
    
    def clean_species(self):
        species = self.cleaned_data.get('species')
        if species and len(species.strip()) < 2:
            raise forms.ValidationError('Spesies harus minimal 2 karakter.')
        return species.strip() if species else species
    
    def clean_origin(self):
        origin = self.cleaned_data.get('origin')
        if origin and len(origin.strip()) < 2:
            raise forms.ValidationError('Asal hewan harus minimal 2 karakter.')
        return origin.strip() if origin else origin
    
    def clean_health_status(self):
        health_status = self.cleaned_data.get('health_status')
        if health_status and len(health_status.strip()) < 2:
            raise forms.ValidationError('Status kesehatan harus minimal 2 karakter.')
        return health_status.strip() if health_status else health_status