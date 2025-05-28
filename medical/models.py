from django.db import models

class MedicalRecord(models.Model):
    STATUS_CHOICES = [
        ('Sehat', 'Sehat'),
        ('Sakit', 'Sakit'),
    ]

    id_hewan = models.CharField(max_length=100)
    tanggal_pemeriksaan = models.DateField()
    username_dh = models.CharField(max_length=100)
    status_kesehatan = models.CharField(max_length=10, choices=STATUS_CHOICES)
    diagnosis = models.TextField(blank=True, null=True)
    pengobatan = models.TextField(blank=True, null=True)
    catatan_tindak_lanjut = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.username_dh} - {self.tanggal_pemeriksaan}"

class HealthCheckSchedule(models.Model):
    tanggal_pemeriksaan_selanjutnya = models.DateField()
    freq_pemeriksaan_rutin = models.PositiveIntegerField(default=3)

    def __str__(self):
        return f"Pemeriksaan berikutnya: {self.tanggal_pemeriksaan_selanjutnya} (Setiap {self.freq_pemeriksaan_rutin} bulan)"
