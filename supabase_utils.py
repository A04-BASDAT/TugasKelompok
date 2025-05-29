from datetime import date
from supabase_client import supabase
from typing import Dict, List, Any, Optional
import uuid
import random
import time

def serialize_dates(data: Dict[str, Any]) -> Dict[str, Any]:
    from datetime import date, datetime
    serialized_data = {}
    
    for key, value in data.items():
        if isinstance(value, (date, datetime)):
            serialized_data[key] = value.isoformat()
        elif isinstance(value, str) and key in ['tanggal_pemeriksaan', 'tgl_pemeriksaan_selanjutnya']:
            # Pastikan format tanggal sudah benar
            serialized_data[key] = value
        else:
            serialized_data[key] = value
    
    return serialized_data


# Adopsi related functions
def get_all_adopsi() -> List[Dict[str, Any]]:
    return supabase.table('adopsi').select('*').execute().data

def get_adopsi_by_id(id_adopsi: str) -> Optional[Dict[str, Any]]:
    result = supabase.table('adopsi').select('*').eq('id_adopsi', id_adopsi).execute().data
    return result[0] if result else None

# Adopter related functions
def get_all_adopter() -> List[Dict[str, Any]]:
    return supabase.table('adopter').select('*').execute().data

def get_adopter_by_id(id_adopter: str) -> Optional[Dict[str, Any]]:
    result = supabase.table('adopter').select('*').eq('id_adopter', id_adopter).execute().data
    return result[0] if result else None

def get_adopter_by_username(username: str) -> Optional[Dict[str, Any]]:
    result = supabase.table('adopter').select('*').eq('username_adopter', username).execute().data
    return result[0] if result else None

# Atraksi related functions
def get_all_atraksi() -> List[Dict[str, Any]]:
    return supabase.table('atraksi').select('*').execute().data

def get_atraksi_by_id(id_atraksi: str) -> Optional[Dict[str, Any]]:
    result = supabase.table('atraksi').select('*').eq('id_atraksi', id_atraksi).execute().data
    return result[0] if result else None

# Berpartisipasi related functions
def get_all_berpartisipasi() -> List[Dict[str, Any]]:
    return supabase.table('berpartisipasi').select('*').execute().data

# Catatan Medis related functions
def get_all_catatan_medis() -> List[Dict[str, Any]]:
    return supabase.table('catatan_medis').select('*').execute().data

def get_catatan_medis_by_id(id_hewan: str) -> List[Dict[str, Any]]:
    return supabase.table('catatan_medis').select('*').eq('id_hewan', id_hewan).execute().data

# Dokter Hewan related functions
def get_all_dokter_hewan() -> List[Dict[str, Any]]:
    return supabase.table('dokter_hewan').select('*').execute().data

def get_dokter_by_id(username_dh: str) -> Optional[Dict[str, Any]]:
    result = supabase.table('dokter_hewan').select('*').eq('username_dh', username_dh).execute().data
    return result[0] if result else None

# Fasilitas related functions
def get_all_fasilitas() -> List[Dict[str, Any]]:
    return supabase.table('fasilitas').select('*').execute().data

# Habitat related functions
def get_all_habitat() -> List[Dict[str, Any]]:
    return supabase.table('habitat').select('*').execute().data

def get_habitat_by_id(nama_habitat: str) -> Optional[Dict[str, Any]]:
    result = supabase.table('habitat').select('*').eq('nama_habitat', nama_habitat).execute().data
    return result[0] if result else None

# Hewan related functions
def get_all_hewan() -> List[Dict[str, Any]]:
    return supabase.table('hewan').select('*').execute().data

def get_hewan_by_id(id_hewan: str) -> Optional[Dict[str, Any]]:
    result = supabase.table('hewan').select('*').eq('id', id_hewan).execute().data
    return result[0] if result else None

# Individu related functions
def get_all_individu() -> List[Dict[str, Any]]:
    return supabase.table('individu').select('*').execute().data

def get_individu_by_id(id_adopter: str) -> Optional[Dict[str, Any]]:
    result = supabase.table('individu').select('*').eq('id_adopter', id_adopter).execute().data
    return result[0] if result else None

# Jadwal Pemeriksaan Kesehatan related functions
def get_all_jadwal_pemeriksaan() -> List[Dict[str, Any]]:
    return supabase.table('jadwal_pemeriksaan_kesehatan').select('*').execute().data

# Jadwal Penugasan related functions
def get_all_jadwal_penugasan() -> List[Dict[str, Any]]:
    return supabase.table('jadwal_penugasan').select('*').execute().data

def get_jadwal_by_username(username_ph: str) -> List[Dict[str, Any]]:
    return supabase.table('jadwal_penugasan').select('*').eq('username_ph', username_ph).execute().data

# Memberi related functions
def get_all_memberi() -> List[Dict[str, Any]]:
    return supabase.table('memberi').select('*').execute().data

# Organisasi related functions
def get_all_organisasi() -> List[Dict[str, Any]]:
    return supabase.table('organisasi').select('*').execute().data

def get_organisasi_by_id(id_adopter: str) -> Optional[Dict[str, Any]]:
    result = supabase.table('organisasi').select('*').eq('id_adopter', id_adopter).execute().data
    return result[0] if result else None

# Pakan related functions
def get_all_pakan() -> List[Dict[str, Any]]:
    return supabase.table('pakan').select('*').execute().data

def get_pakan_by_id(id_hewan: str) -> List[Dict[str, Any]]:
    return supabase.table('pakan').select('*').eq('id_hewan', id_hewan).execute().data

# Pelatih Hewan related functions
def get_all_pelatih_hewan() -> List[Dict[str, Any]]:
    return supabase.table('pelatih_hewan').select('*').execute().data

def get_pelatih_by_username(username_ph: str) -> Optional[Dict[str, Any]]:
    result = supabase.table('pelatih_hewan').select('*').eq('username_ph', username_ph).execute().data
    return result[0] if result else None

# Pengguna related functions
def get_all_pengguna() -> List[Dict[str, Any]]:
    return supabase.table('pengguna').select('*').execute().data

def get_pengguna_by_username(username: str) -> Optional[Dict[str, Any]]:
    result = supabase.table('pengguna').select('*').eq('username', username).execute().data
    return result[0] if result else None

# Pengunjung related functions
def get_all_pengunjung() -> List[Dict[str, Any]]:
    return supabase.table('pengunjung').select('*').execute().data

def get_pengunjung_by_username(username_p: str) -> Optional[Dict[str, Any]]:
    result = supabase.table('pengunjung').select('*').eq('username_p', username_p).execute().data
    return result[0] if result else None

# Penjaga Hewan related functions
def get_all_penjaga_hewan() -> List[Dict[str, Any]]:
    return supabase.table('penjaga_hewan').select('*').execute().data

def get_penjaga_by_username(username_pj: str) -> Optional[Dict[str, Any]]:
    result = supabase.table('penjaga_hewan').select('*').eq('username_pj', username_pj).execute().data
    return result[0] if result else None

# Reservasi related functions
def get_all_reservasi() -> List[Dict[str, Any]]:
    return supabase.table('reservasi').select('*').execute().data

def get_reservasi_by_id(username_p: str) -> List[Dict[str, Any]]:
    return supabase.table('reservasi').select('*').eq('username_p', username_p).execute().data

# Spesialisasi related functions
def get_all_spesialisasi() -> List[Dict[str, Any]]:
    return supabase.table('spesialisasi').select('*').execute().data

# Staff Admin related functions
def get_all_staff_admin() -> List[Dict[str, Any]]:
    return supabase.table('staf_admin').select('*').execute().data

def get_admin_by_username(username_sa: str) -> Optional[Dict[str, Any]]:
    result = supabase.table('staf_admin').select('*').eq('username_sa', username_sa).execute().data
    return result[0] if result else None

# Wahana related functions
def get_all_wahana() -> List[Dict[str, Any]]:
    return supabase.table('wahana').select('*').execute().data

def get_wahana_by_nama(nama_wahana: str) -> Optional[Dict[str, Any]]:
    result = supabase.table('wahana').select('*').eq('nama_wahana', nama_wahana).execute().data
    return result[0] if result else None

# Create/Insert functions
def create_adopsi(data: Dict[str, Any]) -> Dict[str, Any]:
    # **PERBAIKAN: Validasi dan normalisasi UUID yang lebih ketat**
    id_adopter = data.get('id_adopter')
    id_hewan = data.get('id_hewan')
    
    # Validate id_adopter exists in adopter table
    adopter = get_adopter_by_id(id_adopter)
    if not adopter:
        raise ValueError(f"Adopter dengan ID '{id_adopter}' tidak ditemukan dalam tabel adopter")
    
    # Validate id_hewan exists in hewan table
    hewan = get_hewan_by_id(id_hewan)
    if not hewan:
        raise ValueError(f"Hewan dengan ID '{id_hewan}' tidak ditemukan dalam tabel hewan")
    
    # **PERBAIKAN: Gunakan UUID yang sama persis dari database tanpa normalisasi**
    # Ini memastikan tipe data dan format yang konsisten
    validated_id_adopter = adopter['id_adopter']  # Ambil langsung dari database adopter
    validated_id_hewan = hewan['id']              # Ambil langsung dari database hewan
    
    # Check if adoption already exists
    existing_adoption = get_adopsi_by_id(validated_id_adopter, validated_id_hewan)
    if existing_adoption:
        raise ValueError(f"Adopsi sudah ada untuk adopter '{validated_id_adopter}' dan hewan '{validated_id_hewan}'")
    
    # Ensure proper data types with validated UUIDs
    formatted_data = {
        'id_adopter': validated_id_adopter,      # Gunakan langsung dari database adopter
        'id_hewan': validated_id_hewan,          # Gunakan langsung dari database hewan
        'tgl_mulai_adopsi': str(data['tgl_mulai_adopsi']),  # Ensure string format YYYY-MM-DD
        'tgl_berhenti_adopsi': str(data['tgl_berhenti_adopsi']),  # Ensure string format YYYY-MM-DD
        'status_pembayaran': str(data.get('status_pembayaran', 'tertunda')),  # Ensure string
        'kontribusi_finansial': int(data['kontribusi_finansial'])  # Ensure integer
    }
    
    # **TYPE CONSISTENCY CHECK**
    print(f"[TYPE FINAL] id_adopter from adopter table: {type(validated_id_adopter)} = {validated_id_adopter}")
    print(f"[TYPE FINAL] id_hewan from hewan table: {type(validated_id_hewan)} = {validated_id_hewan}")
    
    try:
        result = supabase.table('adopsi').insert(formatted_data).execute()
        return result.data[0]
    except Exception as e:
        print(f"[ERROR] create_adopsi failed: {e}")
        
        # Show type information for debugging
        print(f"[ERROR] Data types being inserted:")
        for key, value in formatted_data.items():
            print(f"[ERROR]   {key}: {type(value)} = {value}")
        
        raise e

def create_adopter(data: Dict[str, Any]) -> Dict[str, Any]:
    # Generate new UUID with compatible format
    new_uuid = generate_adopter_uuid()
    data['id_adopter'] = new_uuid
    print(f"[DEBUG] Generated new adopter UUID with compatible format: '{new_uuid}'")
    
    # Check format compatibility
    compatibility = check_uuid_format_compatibility(new_uuid)
    if not compatibility['is_compatible']:
        print(f"[WARNING] Generated UUID might not be compatible: {compatibility}")
    
    return supabase.table('adopter').insert(data).execute().data[0]

def create_individu(data: Dict[str, Any]) -> Dict[str, Any]:
    return supabase.table('individu').insert(data).execute().data[0]

def create_organisasi(data: Dict[str, Any]) -> Dict[str, Any]:
    return supabase.table('organisasi').insert(data).execute().data[0]

def create_complete_adopter(adopter_data: Dict[str, Any], type_data: Dict[str, Any], is_individual: bool = True) -> Dict[str, Any]:

    adopter = create_adopter(adopter_data)
    
    type_data['id_adopter'] = adopter['id_adopter']
    
    if is_individual:
        individu = create_individu(type_data)
        return {**adopter, 'detail': individu}
    else:
        organisasi = create_organisasi(type_data)
        return {**adopter, 'detail': organisasi}

def create_hewan(data: Dict[str, Any]) -> Dict[str, Any]:
    return supabase.table('hewan').insert(data).execute().data[0]

def create_catatan_medis(data):
    # Pastikan tidak mengirim field yang tidak ada di Supabase
    data.pop('created_at', None)  # Hapus kalau ada
    data.pop('updated_at', None)  # Kalau kamu pernah pakai ini juga

    response = supabase.table("catatan_medis").insert(data).execute()
    print("[DEBUG] Data dikirim ke Supabase (insert):", data)
    return response

def create_reservasi(data: Dict[str, Any]) -> Dict[str, Any]:
    return supabase.table('reservasi').insert(data).execute().data[0]

# Update functions
def update_adopsi(id_adopsi: str, data: Dict[str, Any]) -> Dict[str, Any]:
    return supabase.table('adopsi').update(data).eq('id_adopsi', id_adopsi).execute().data[0]

def update_adopter(id_adopter: str, data: Dict[str, Any]) -> Dict[str, Any]:
    return supabase.table('adopter').update(data).eq('id_adopter', id_adopter).execute().data[0]

def update_hewan(id_hewan: str, data: Dict[str, Any]) -> Dict[str, Any]:
    return supabase.table('hewan').update(data).eq('id', id_hewan).execute().data[0]

def update_catatan_medis(id_hewan: str, tanggal: str, data: Dict[str, Any]) -> Dict[str, Any]:
    return supabase.table('catatan_medis').update(data).eq('id_hewan', id_hewan).eq('tanggal_pemeriksaan', tanggal).execute().data[0]

# Delete functions
def delete_adopsi(id_adopsi: str) -> Dict[str, Any]:
    return supabase.table('adopsi').delete().eq('id_adopsi', id_adopsi).execute().data[0]

def delete_adopter(id_adopter: str) -> None:

    supabase.table('adopsi').delete().eq('id_adopter', id_adopter).execute()
    
    supabase.table('individu').delete().eq('id_adopter', id_adopter).execute()
    supabase.table('organisasi').delete().eq('id_adopter', id_adopter).execute()
    
    supabase.table('adopter').delete().eq('id_adopter', id_adopter).execute()

def delete_reservasi(username_p: str, tanggal: str) -> Dict[str, Any]:
    return supabase.table('reservasi').delete().eq('username_p', username_p).eq('tanggal_kunjungan', tanggal).execute().data[0] 


# punya abby
# Get single medical record by id_hewan and tanggal_pemeriksaan
def get_catatan_medis_by_key(id_hewan: str, tanggal: str) -> Optional[Dict[str, Any]]:
    result = supabase.table('catatan_medis').select('*')\
        .eq('id_hewan', id_hewan).eq('tanggal_pemeriksaan', tanggal).execute().data
    return result[0] if result else None

# Delete catatan medis by id_hewan and tanggal_pemeriksaan
def delete_catatan_medis(id_hewan: str, tanggal: str) -> Dict[str, Any]:
    return supabase.table('catatan_medis').delete()\
        .eq('id_hewan', id_hewan).eq('tanggal_pemeriksaan', tanggal).execute().data[0]

# Create new health check schedule
def create_jadwal_pemeriksaan(data: Dict[str, Any]) -> Dict[str, Any]:
    data = serialize_dates(data)
    return supabase.table('jadwal_pemeriksaan_kesehatan').insert(data).execute().data[0]

# Get all schedules for a specific animal
def get_jadwal_pemeriksaan_by_id_hewan(id_hewan: str) -> List[Dict[str, Any]]:
    return supabase.table('jadwal_pemeriksaan_kesehatan').select('*').eq('id_hewan', id_hewan).execute().data

# Update schedule (by id_hewan and tanggal)
def update_jadwal_pemeriksaan(id_hewan: str, tanggal: str, data: Dict[str, Any]) -> Dict[str, Any]:
    return supabase.table('jadwal_pemeriksaan_kesehatan')\
        .update(data).eq('id_hewan', id_hewan).eq('tgl_pemeriksaan_selanjutnya', tanggal).execute().data[0]

# Delete schedule (by id_hewan and tanggal)
def delete_jadwal_pemeriksaan(id_hewan: str, tanggal: str) -> Dict[str, Any]:
    return supabase.table('jadwal_pemeriksaan_kesehatan')\
        .delete().eq('id_hewan', id_hewan).eq('tgl_pemeriksaan_selanjutnya', tanggal).execute().data[0]

def generate_adopter_uuid() -> str:
    """Generate UUID with the same format as working UUIDs in database"""
    # Based on the pattern from working UUIDs: 5a1f43e5-b1e6-4c5c-bc5a-xxxxxxxxxxxx
    # **PERBAIKAN: Hanya menggunakan angka untuk suffix, tidak campuran huruf**
    prefix = "5a1f43e5-b1e6-4c5c-bc5a-"
    
    # Get existing adopter IDs to avoid duplicates
    existing_ids = set()
    
    try:
        # Get IDs from adopsi table
        all_adopsi = get_all_adopsi()
        for adopsi in all_adopsi:
            adopter_id = adopsi.get('id_adopter')
            if adopter_id:
                existing_ids.add(str(adopter_id).strip().lower())
        
        # Get IDs from adopter table
        all_adopters = get_all_adopter()
        for adopter in all_adopters:
            adopter_id = adopter.get('id_adopter')
            if adopter_id:
                existing_ids.add(str(adopter_id).strip().lower())
        
    except Exception as e:
        existing_ids = set()
    
    # **PERBAIKAN: Hanya menggunakan pola angka sederhana untuk kompatibilitas dengan database**
    pattern_types = [
        # Pattern type 1: All same NUMBER (like 111111111111, 777777777777)
        lambda: random.choice('0123456789') * 12,
        
        # Pattern type 2: Alternating NUMBERS only (like 121212121212, 787878787878)
        lambda: (lambda a, b: (a + b) * 6)(
            random.choice('0123456789'), random.choice('0123456789')
        ),
        
        # Pattern type 3: Numbers only - different combo (like 191919191919, 545454545454)
        lambda: (lambda a, b: (a + b) * 6)(
            random.choice('123456789'), random.choice('123456789')
        ),
        
        # Pattern type 4: Simple number sequences (like 123456789012, 987654321098)
        lambda: ''.join([str(i % 10) for i in range(12)]),
        
        # Pattern type 5: Reverse sequences (like 210987654321, 109876543210)
        lambda: ''.join([str((9-i) % 10) for i in range(12)]),
        
        # Pattern type 6: Random digits with max 4 unique values
        lambda: generate_simple_digit_pattern()
    ]
    
    max_attempts = 50  # Prevent infinite loop
    attempt = 0
    
    while attempt < max_attempts:
        attempt += 1
        
        # Choose random pattern type
        pattern_generator = random.choice(pattern_types)
        suffix = pattern_generator()
        
        # Ensure suffix is exactly 12 characters and digits only
        suffix = str(suffix)[:12].ljust(12, '0')
        if not suffix.isdigit():
            # Force to digits only if somehow non-digit crept in
            suffix = ''.join([c for c in suffix if c.isdigit()])[:12].ljust(12, '0')
        
        new_uuid = prefix + suffix
        
        # Check if this UUID already exists
        if new_uuid.lower() not in existing_ids:
            # Validate it's a proper UUID format
            try:
                uuid_obj = uuid.UUID(new_uuid)
                final_uuid = str(uuid_obj).lower()
                return final_uuid
            except ValueError as e:
                continue
        
    # If we couldn't generate unique UUID after max attempts
    # Fallback with timestamp to ensure uniqueness (digits only)
    timestamp = str(int(time.time() * 1000))[-12:]  # Last 12 digits of timestamp
    fallback_uuid = prefix + timestamp
    
    try:
        uuid_obj = uuid.UUID(fallback_uuid)
        final_fallback = str(uuid_obj).lower()
        return final_fallback
    except ValueError:
        # Ultimate fallback (digits only)
        ultimate_fallback = prefix + '1' * 12
        return ultimate_fallback

def generate_simple_digit_pattern():
    """Generate simple digit pattern with max 4 unique digits"""
    # Choose 2-4 unique digits
    unique_count = random.randint(2, 4)
    digits = random.sample('0123456789', unique_count)
    
    # Create pattern by repeating these digits
    pattern = ''
    for _ in range(12):
        pattern += random.choice(digits)
    
    return pattern

def normalize_uuid(uuid_value: Any) -> str:
    """Normalize UUID to ensure consistent format"""
    if uuid_value is None:
        return None
    
    # Convert to string and clean up
    uuid_str = str(uuid_value).strip().lower()
    
    # Remove any extra characters
    uuid_str = uuid_str.replace('"', '').replace("'", '')
    
    # Validate UUID format
    try:
        # This will raise ValueError if not valid UUID
        uuid_obj = uuid.UUID(uuid_str)
        # Return standardized lowercase format
        normalized = str(uuid_obj).lower()
        print(f"[DEBUG] UUID normalized: '{uuid_value}' -> '{normalized}'")
        return normalized
    except ValueError as e:
        print(f"[ERROR] Invalid UUID format: '{uuid_value}', error: {e}")
        return str(uuid_value)  # Return as-is if can't normalize

def debug_uuid_comparison(uuid1: Any, uuid2: Any):
    """Debug function to compare UUIDs and show differences"""
    print(f"[DEBUG] UUID Comparison:")
    print(f"[DEBUG]   UUID1: '{uuid1}' (type: {type(uuid1)})")
    print(f"[DEBUG]   UUID2: '{uuid2}' (type: {type(uuid2)})")
    
    norm1 = normalize_uuid(uuid1)
    norm2 = normalize_uuid(uuid2)
    
    print(f"[DEBUG]   Normalized UUID1: '{norm1}'")
    print(f"[DEBUG]   Normalized UUID2: '{norm2}'")
    print(f"[DEBUG]   Are equal: {norm1 == norm2}")
    
    if norm1 != norm2:
        print(f"[DEBUG]   Length difference: {len(str(uuid1))} vs {len(str(uuid2))}")
        print(f"[DEBUG]   Byte comparison:")
        for i, (c1, c2) in enumerate(zip(str(uuid1), str(uuid2))):
            if c1 != c2:
                print(f"[DEBUG]     Position {i}: '{c1}' vs '{c2}'")

def check_uuid_format_compatibility(test_uuid: str) -> Dict[str, Any]:
    """Check if UUID format is compatible with database"""
    working_prefix = "5a1f43e5-b1e6-4c5c-bc5a-"
    
    # Extract the suffix (last 12 characters)
    suffix = test_uuid[len(working_prefix):] if len(test_uuid) >= len(working_prefix) else ""
    suffix_is_digits_only = suffix.isdigit() and len(suffix) == 12
    
    # Check if suffix has max 4 unique digits
    unique_digits = set(suffix) if suffix_is_digits_only else set()
    has_max_4_unique = len(unique_digits) <= 4
    
    result = {
        'is_compatible': test_uuid.lower().startswith(working_prefix.lower()) and suffix_is_digits_only and has_max_4_unique,
        'has_correct_prefix': test_uuid.lower().startswith(working_prefix.lower()),
        'suffix_is_digits_only': suffix_is_digits_only,
        'has_max_4_unique_digits': has_max_4_unique,
        'unique_digits_count': len(unique_digits),
        'unique_digits': sorted(list(unique_digits)),
        'suffix': suffix,
        'prefix_used': test_uuid[:len(working_prefix)-1] if len(test_uuid) >= len(working_prefix) else test_uuid,
        'expected_prefix': working_prefix[:-1],
        'expected_format': working_prefix + "XXXXXXXXXXXX (12 digits, max 4 unique)",
        'recommendation': None
    }
    
    if not result['has_correct_prefix']:
        result['recommendation'] = f"Use UUID with prefix: {working_prefix}XXXXXXXXXXXX"
    elif not result['suffix_is_digits_only']:
        result['recommendation'] = f"Last 12 characters must be digits only (0-9), got: '{suffix}'"
    elif not result['has_max_4_unique_digits']:
        result['recommendation'] = f"Last 12 digits must have max 4 unique digits, got {len(unique_digits)}: {sorted(unique_digits)}"
    
    print(f"[DEBUG] UUID compatibility check: {result}")
    return result

def debug_table_structure():
    """Debug function to check the actual table structure"""
    try:
        # Try to get table info using a simple select to see actual columns
        result = supabase.table('adopsi').select('*').limit(1).execute()
        print(f"[DEBUG] Sample adopsi data: {result.data}")
        
        # Try to see what columns exist
        if result.data:
            print(f"[DEBUG] Adopsi table columns: {list(result.data[0].keys())}")
        
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"[ERROR] debug_table_structure failed: {e}")
        return None

def create_adopsi_raw(data: Dict[str, Any]) -> Dict[str, Any]:
    """Alternative approach using raw SQL if needed"""
    print(f"[DEBUG] create_adopsi_raw called with data: {data}")
    
    try:
        # First, let's check the table structure
        sample = debug_table_structure()
        
        # **PERBAIKAN: Normalize UUIDs**
        normalized_id_adopter = normalize_uuid(data.get('id_adopter'))
        normalized_id_hewan = normalize_uuid(data.get('id_hewan'))
        
        print(f"[DEBUG] Raw - Original id_adopter: '{data.get('id_adopter')}'")
        print(f"[DEBUG] Raw - Normalized id_adopter: '{normalized_id_adopter}'")
        print(f"[DEBUG] Raw - Original id_hewan: '{data.get('id_hewan')}'")
        print(f"[DEBUG] Raw - Normalized id_hewan: '{normalized_id_hewan}'")
        
        # Ensure all values are properly formatted
        formatted_data = {}
        
        # Handle each field individually based on what we know works
        if 'id_adopter' in data:
            formatted_data['id_adopter'] = normalized_id_adopter
        if 'id_hewan' in data:
            formatted_data['id_hewan'] = normalized_id_hewan
        if 'tgl_mulai_adopsi' in data:
            formatted_data['tgl_mulai_adopsi'] = str(data['tgl_mulai_adopsi'])
        if 'tgl_berhenti_adopsi' in data:
            formatted_data['tgl_berhenti_adopsi'] = str(data['tgl_berhenti_adopsi'])
        if 'status_pembayaran' in data:
            formatted_data['status_pembayaran'] = str(data.get('status_pembayaran', 'tertunda'))
        if 'kontribusi_finansial' in data:
            # Try to convert to int, but keep as string if conversion fails
            try:
                formatted_data['kontribusi_finansial'] = int(data['kontribusi_finansial'])
            except (ValueError, TypeError):
                formatted_data['kontribusi_finansial'] = str(data['kontribusi_finansial'])
        
        print(f"[DEBUG] Formatted data for raw insert: {formatted_data}")
        print(f"[DEBUG] Formatted data types:")
        for key, value in formatted_data.items():
            print(f"[DEBUG]   {key}: '{value}' (type: {type(value)}, len: {len(str(value))})")
        
        # Try the insert
        result = supabase.table('adopsi').insert(formatted_data).execute()
        print(f"[DEBUG] create_adopsi_raw successful: {result.data[0]}")
        return result.data[0]
        
    except Exception as e:
        print(f"[ERROR] create_adopsi_raw failed: {e}")
        print(f"[ERROR] Error details: {str(e)}")
        
        # Show what exactly failed
        print(f"[DEBUG] Failed data analysis:")
        for key, value in formatted_data.items():
            print(f"[DEBUG]   {key}: '{value}' -> bytes: {str(value).encode('utf-8')}")
        
        raise e

def verify_adopter_id_consistency(adopter_id: str) -> Dict[str, bool]:
    """Verify that adopter ID exists consistently across all related tables"""
    print(f"[DEBUG] Verifying ID consistency for adopter: {adopter_id}")
    
    results = {
        'adopter_exists': False,
        'individu_exists': False,
        'organisasi_exists': False,
        'has_adoptions': False,
        'adopter_type': None
    }
    
    # Check adopter table
    adopter = get_adopter_by_id(adopter_id)
    if adopter:
        results['adopter_exists'] = True
        print(f"[DEBUG] Adopter found: {adopter}")
    
    # Check individu table
    individu = get_individu_by_id(adopter_id)
    if individu:
        results['individu_exists'] = True
        results['adopter_type'] = 'individu'
        print(f"[DEBUG] Individu found: {individu}")
    
    # Check organisasi table
    organisasi = get_organisasi_by_id(adopter_id)
    if organisasi:
        results['organisasi_exists'] = True
        results['adopter_type'] = 'organisasi'
        print(f"[DEBUG] Organisasi found: {organisasi}")
    
    # Check adoptions
    adoptions = get_all_adopsi()
    for adoption in adoptions:
        if str(adoption.get('id_adopter', '')).strip() == str(adopter_id).strip():
            results['has_adoptions'] = True
            break
    
    print(f"[DEBUG] Consistency check results: {results}")
    return results

def analyze_existing_adopter_ids() -> Dict[str, Any]:
    """Analyze existing adopter IDs in adopsi table to check their patterns"""
    print("[DEBUG] Analyzing existing adopter IDs in adopsi table...")
    
    try:
        # Get all adopsi records
        all_adopsi = get_all_adopsi()
        print(f"[DEBUG] Found {len(all_adopsi)} adopsi records")
        
        # Extract unique adopter IDs
        adopter_ids = set()
        for adopsi in all_adopsi:
            adopter_id = adopsi.get('id_adopter')
            if adopter_id:
                adopter_ids.add(str(adopter_id).strip())
        
        print(f"[DEBUG] Found {len(adopter_ids)} unique adopter IDs")
        
        analysis_results = {
            'total_adopter_ids': len(adopter_ids),
            'compatible_ids': [],
            'incompatible_ids': [],
            'pattern_analysis': {}
        }
        
        working_prefix = "5a1f43e5-b1e6-4c5c-bc5a-"
        
        for adopter_id in adopter_ids:
            print(f"[DEBUG] Analyzing adopter ID: {adopter_id}")
            
            # Check compatibility
            compatibility = check_uuid_format_compatibility(adopter_id)
            
            if compatibility['is_compatible']:
                analysis_results['compatible_ids'].append(adopter_id)
                print(f"[DEBUG] ✅ Compatible: {adopter_id}")
            else:
                analysis_results['incompatible_ids'].append({
                    'id': adopter_id,
                    'issues': compatibility
                })
                print(f"[DEBUG] ❌ Incompatible: {adopter_id}")
                print(f"[DEBUG]    Issues: {compatibility.get('recommendation', 'Unknown issue')}")
            
            # Analyze pattern if it has the right prefix
            if adopter_id.lower().startswith(working_prefix.lower()) and len(adopter_id) >= len(working_prefix):
                suffix = adopter_id[len(working_prefix):]
                if suffix.isdigit() and len(suffix) == 12:
                    unique_digits = set(suffix)
                    pattern_key = f"{len(unique_digits)}_digits"
                    
                    if pattern_key not in analysis_results['pattern_analysis']:
                        analysis_results['pattern_analysis'][pattern_key] = []
                    
                    analysis_results['pattern_analysis'][pattern_key].append({
                        'id': adopter_id,
                        'suffix': suffix,
                        'unique_digits': sorted(list(unique_digits))
                    })
        
        # Summary
        print(f"\n[DEBUG] === Analysis Summary ===")
        print(f"[DEBUG] Total adopter IDs: {analysis_results['total_adopter_ids']}")
        print(f"[DEBUG] Compatible IDs: {len(analysis_results['compatible_ids'])}")
        print(f"[DEBUG] Incompatible IDs: {len(analysis_results['incompatible_ids'])}")
        
        print(f"\n[DEBUG] === Pattern Breakdown ===")
        for pattern, ids in analysis_results['pattern_analysis'].items():
            print(f"[DEBUG] {pattern}: {len(ids)} IDs")
            for id_info in ids[:3]:  # Show first 3 examples
                print(f"[DEBUG]   Example: {id_info['suffix']} (digits: {id_info['unique_digits']})")
            if len(ids) > 3:
                print(f"[DEBUG]   ... and {len(ids) - 3} more")
        
        if analysis_results['incompatible_ids']:
            print(f"\n[DEBUG] === Incompatible IDs ===")
            for item in analysis_results['incompatible_ids']:
                print(f"[DEBUG] ID: {item['id']}")
                print(f"[DEBUG]   Issue: {item['issues'].get('recommendation', 'Unknown')}")
        
        return analysis_results
        
    except Exception as e:
        print(f"[ERROR] analyze_existing_adopter_ids failed: {e}")
        return {
            'error': str(e),
            'total_adopter_ids': 0,
            'compatible_ids': [],
            'incompatible_ids': []
        }

def validate_all_existing_data() -> Dict[str, Any]:
    """Comprehensive validation of all existing adopter data across tables"""
    print("[DEBUG] Starting comprehensive validation of existing adopter data...")
    
    validation_results = {
        'adopsi_analysis': None,
        'adopter_table_analysis': None,
        'cross_table_consistency': None,
        'recommendations': []
    }
    
    try:
        # 1. Analyze adopsi table
        validation_results['adopsi_analysis'] = analyze_existing_adopter_ids()
        
        # 2. Analyze adopter table
        print(f"\n[DEBUG] Analyzing adopter table...")
        all_adopters = get_all_adopter()
        adopter_table_ids = []
        
        for adopter in all_adopters:
            adopter_id = adopter.get('id_adopter')
            if adopter_id:
                adopter_table_ids.append(str(adopter_id).strip())
                compatibility = check_uuid_format_compatibility(adopter_id)
                if not compatibility['is_compatible']:
                    print(f"[DEBUG] ❌ Adopter table has incompatible ID: {adopter_id}")
                    print(f"[DEBUG]    Issue: {compatibility.get('recommendation', 'Unknown')}")
        
        validation_results['adopter_table_analysis'] = {
            'total_adopters': len(all_adopters),
            'adopter_ids': adopter_table_ids
        }
        
        # 3. Cross-table consistency check
        adopsi_ids = set(validation_results['adopsi_analysis']['compatible_ids'] + 
                        [item['id'] for item in validation_results['adopsi_analysis']['incompatible_ids']])
        adopter_ids = set(adopter_table_ids)
        
        missing_in_adopter = adopsi_ids - adopter_ids
        missing_in_adopsi = adopter_ids - adopsi_ids
        
        validation_results['cross_table_consistency'] = {
            'adopsi_ids_count': len(adopsi_ids),
            'adopter_ids_count': len(adopter_ids),
            'missing_in_adopter_table': list(missing_in_adopter),
            'missing_in_adopsi_table': list(missing_in_adopsi)
        }
        
        print(f"\n[DEBUG] === Cross-Table Consistency ===")
        print(f"[DEBUG] IDs in adopsi: {len(adopsi_ids)}")
        print(f"[DEBUG] IDs in adopter: {len(adopter_ids)}")
        print(f"[DEBUG] Missing in adopter table: {len(missing_in_adopter)}")
        print(f"[DEBUG] Missing in adopsi table: {len(missing_in_adopsi)}")
        
        if missing_in_adopter:
            print(f"[DEBUG] IDs in adopsi but not in adopter table: {list(missing_in_adopter)[:5]}")
        if missing_in_adopsi:
            print(f"[DEBUG] IDs in adopter but not in adopsi table: {list(missing_in_adopsi)[:5]}")
        
        # 4. Generate recommendations
        recommendations = []
        
        if validation_results['adopsi_analysis']['incompatible_ids']:
            recommendations.append("Some adopter IDs in adopsi table don't follow the required pattern")
        
        if missing_in_adopter:
            recommendations.append("Some adopter IDs in adopsi table don't exist in adopter table")
        
        if missing_in_adopsi:
            recommendations.append("Some adopter IDs in adopter table have no adoptions")
        
        validation_results['recommendations'] = recommendations
        
        print(f"\n[DEBUG] === Recommendations ===")
        for rec in recommendations:
            print(f"[DEBUG] - {rec}")
        
        return validation_results
        
    except Exception as e:
        print(f"[ERROR] validate_all_existing_data failed: {e}")
        validation_results['error'] = str(e)
        return validation_results

def trigger_notify_top_5_adopter() -> Dict[str, Any]:
    """Trigger the notify_top_5_adopter function in database to generate RAISE NOTICE"""
    try:
        # Trigger the function by updating a dummy adopter record (this will fire the trigger)
        # First, get an existing adopter to update
        all_adopters = get_all_adopter()
        
        if not all_adopters:
            return {
                'success': False,
                'message': 'Tidak ada adopter untuk memicu notifikasi'
            }
        
        # Use the first adopter as example to trigger the function
        first_adopter = all_adopters[0]
        adopter_id = first_adopter['id_adopter']
        
        # Update the adopter with the same data to trigger AFTER UPDATE
        # This will fire the notify_top_5_adopter function
        result = supabase.table('adopter').update({
            'total_kontribusi': first_adopter['total_kontribusi']  # Same value to not change data
        }).eq('id_adopter', adopter_id).execute()
        
        if result.data:
            return {
                'success': True,
                'message': 'Trigger notify_top_5_adopter berhasil dipanggil',
                'triggered_by': f"Update adopter {first_adopter.get('username_adopter', adopter_id)}"
            }
        else:
            return {
                'success': False,
                'message': 'Gagal memicu trigger notify_top_5_adopter'
            }
            
    except Exception as e:
        print(f"[ERROR] trigger_notify_top_5_adopter failed: {e}")
        return {
            'success': False,
            'message': f'Error saat memicu trigger: {str(e)}'
        }

def create_update_total_kontribusi_trigger():
    """Create trigger function and trigger to update total kontribusi adopter"""
    try:
        # Create the trigger function
        trigger_function_sql = """
        CREATE OR REPLACE FUNCTION update_total_kontribusi_adopter()
        RETURNS TRIGGER AS $$
        DECLARE
          target_id TEXT;
        BEGIN
          IF TG_OP = 'DELETE' THEN
            target_id := OLD.id_adopter;
          ELSE
            target_id := NEW.id_adopter;
          END IF;

          UPDATE adopter
          SET total_kontribusi = (
            SELECT COALESCE(SUM(kontribusi_finansial), 0)
            FROM adopsi
            WHERE id_adopter = target_id AND status_pembayaran = 'lunas'
          )
          WHERE id_adopter = target_id;

          RAISE NOTICE 'SUKSES: Total kontribusi adopter "%%" telah diperbarui.', 
            (SELECT username_adopter FROM adopter WHERE id_adopter = target_id);

          RETURN COALESCE(NEW, OLD);
        END;
        $$ LANGUAGE plpgsql;
        """
        
        # Execute the function creation
        supabase.rpc('execute_sql', {'sql': trigger_function_sql}).execute()
        
        # Create the trigger
        trigger_sql = """
        DROP TRIGGER IF EXISTS update_total_kontribusi_adopter_trigger ON adopsi;
        
        CREATE TRIGGER update_total_kontribusi_adopter_trigger
        AFTER INSERT OR UPDATE OR DELETE ON adopsi
        FOR EACH ROW
        EXECUTE FUNCTION update_total_kontribusi_adopter();
        """
        
        supabase.rpc('execute_sql', {'sql': trigger_sql}).execute()
        
        return {
            'success': True,
            'message': 'Trigger untuk update total kontribusi berhasil dibuat'
        }
        
    except Exception as e:
        print(f"[ERROR] create_update_total_kontribusi_trigger: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def delete_adopter_with_cascade(adopter_id):
    """Delete adopter and all related adoptions with cascade, return notification messages"""
    try:
        # Get adopter info first for notification
        adopter_result = supabase.table('adopter').select('username_adopter').eq('id_adopter', adopter_id).execute()
        
        if not adopter_result.data:
            return {
                'success': False,
                'error': 'Adopter tidak ditemukan'
            }
        
        adopter_name = adopter_result.data[0]['username_adopter']
        
        # Get adoption count for notification
        adoption_result = supabase.table('adopsi').select('*').eq('id_adopter', adopter_id).execute()
        adoption_count = len(adoption_result.data) if adoption_result.data else 0
        
        # Delete adoptions first (this will trigger the update function)
        if adoption_count > 0:
            supabase.table('adopsi').delete().eq('id_adopter', adopter_id).execute()
        
        # Delete from individu or organisasi table
        try:
            supabase.table('individu').delete().eq('id_adopter', adopter_id).execute()
        except:
            pass  # If not found in individu, try organisasi
        
        try:
            supabase.table('organisasi').delete().eq('id_adopter', adopter_id).execute()
        except:
            pass  # If not found in organisasi, that's okay
        
        # Finally delete from adopter table
        supabase.table('adopter').delete().eq('id_adopter', adopter_id).execute()
        
        # Create notification messages
        messages = []
        if adoption_count > 0:
            messages.append(f'SUKSES: {adoption_count} adopsi terkait adopter "{adopter_name}" telah dihapus.')
        messages.append(f'SUKSES: Adopter "{adopter_name}" telah dihapus dari sistem.')
        
        return {
            'success': True,
            'messages': messages,
            'adopter_name': adopter_name,
            'adoption_count': adoption_count
        }
        
    except Exception as e:
        print(f"[ERROR] delete_adopter_with_cascade: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def execute_with_notices(sql_query, params=None):
    """Execute SQL and capture RAISE NOTICE messages"""
    try:
        # This is a placeholder - in real implementation, you would need to capture
        # PostgreSQL NOTICE messages. For now, we'll return success status.
        result = supabase.rpc('execute_sql', {'sql': sql_query}).execute()
        
        return {
            'success': True,
            'data': result.data,
            'notices': []  # In real implementation, capture RAISE NOTICE here
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'notices': []
        }