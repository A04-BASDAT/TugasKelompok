from django import forms

class HabitatForm(forms.Form):
    nama = forms.CharField(
        max_length=50,
        label='Nama Habitat',
        widget=forms.TextInput(attrs={
            'placeholder': 'Masukkan nama habitat',
            'class': 'form-control'
        })
    )
    
    luas_area = forms.DecimalField(
        label='Luas Area',
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Masukkan luas area dalam m²',
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    kapasitas = forms.IntegerField(
        label='Kapasitas Maksimal',
        min_value=1,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Masukkan kapasitas maksimal hewan',
            'class': 'form-control'
        })
    )
    
    status = forms.CharField(
        max_length=100,
        label='Status Habitat',
        widget=forms.TextInput(attrs={
            'placeholder': 'Masukkan status habitat (contoh: Baik, Perlu perawatan, dll)',
            'class': 'form-control'
        })
    )
    
    def __init__(self, *args, **kwargs):
        # Extract custom validation parameters
        self.current_animal_count = kwargs.pop('current_animal_count', 0)
        self.original_nama = kwargs.pop('original_nama', None)
        self.existing_habitats = kwargs.pop('existing_habitats', [])
        super().__init__(*args, **kwargs)
    
    def clean_nama(self):
        nama = self.cleaned_data.get('nama', '')
        if not nama.strip():
            raise forms.ValidationError('Nama habitat tidak boleh kosong')
        
        nama = nama.strip()
        
        # Check for duplicate names (excluding current habitat if editing)
        for habitat in self.existing_habitats:
            if habitat['nama'].lower() == nama.lower() and habitat['nama'] != self.original_nama:
                raise forms.ValidationError(f'Habitat dengan nama "{nama}" sudah ada!')
        
        return nama
    
    def clean_luas_area(self):
        luas_area = self.cleaned_data.get('luas_area')
        if luas_area is None:
            raise forms.ValidationError('Luas area harus diisi')
        if luas_area <= 0:
            raise forms.ValidationError('Luas area harus lebih dari 0')
        return luas_area
    
    def clean_kapasitas(self):
        kapasitas = self.cleaned_data.get('kapasitas')
        if kapasitas is None:
            raise forms.ValidationError('Kapasitas harus diisi')
        if kapasitas <= 0:
            raise forms.ValidationError('Kapasitas harus lebih dari 0')
        
        # Check if new capacity is less than current animal count
        if self.current_animal_count > 0 and kapasitas < self.current_animal_count:
            raise forms.ValidationError(
                f'Kapasitas tidak dapat dikurangi menjadi {kapasitas} karena saat ini ada '
                f'{self.current_animal_count} hewan di habitat ini. '
                f'Minimal kapasitas adalah {self.current_animal_count}.'
            )
        
        return kapasitas
    
    def clean_status(self):
        status = self.cleaned_data.get('status', '')
        if not status.strip():
            raise forms.ValidationError('Status habitat tidak boleh kosong')
        return status.strip()