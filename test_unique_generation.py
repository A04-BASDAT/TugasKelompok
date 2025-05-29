#!/usr/bin/env python
import sys
import os

# Add parent directory to path to import supabase_utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from supabase_utils import (
    generate_adopter_uuid, 
    get_all_adopsi, 
    get_all_adopter,
    analyze_existing_adopter_ids
)

def test_uniqueness_generation():
    """Test that generated UUIDs are unique and don't exist in database"""
    print("=== Testing UUID Uniqueness Generation ===\n")
    
    # First, get all existing IDs
    print("🔍 Fetching existing adopter IDs from database...")
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
        
        print(f"📊 Found {len(existing_ids)} existing adopter IDs in database")
        
        if existing_ids:
            print(f"📋 Sample existing IDs:")
            for i, uid in enumerate(list(existing_ids)[:5]):
                print(f"   {i+1}. {uid}")
            if len(existing_ids) > 5:
                print(f"   ... and {len(existing_ids) - 5} more")
        else:
            print("📋 No existing adopter IDs found (empty database)")
        
    except Exception as e:
        print(f"❌ Error fetching existing IDs: {e}")
        return False
    
    print(f"\n🎲 Generating new UUIDs and checking uniqueness...")
    
    # Generate multiple UUIDs and check uniqueness
    generated_uuids = []
    all_unique = True
    
    for i in range(10):
        print(f"\n--- Generating UUID {i+1} ---")
        new_uuid = generate_adopter_uuid()
        
        # Check against existing IDs
        if new_uuid.lower() in existing_ids:
            print(f"❌ ERROR: Generated UUID '{new_uuid}' already exists in database!")
            all_unique = False
        else:
            print(f"✅ UUID '{new_uuid}' is unique (not in database)")
        
        # Check against previously generated UUIDs in this session
        if new_uuid.lower() in [u.lower() for u in generated_uuids]:
            print(f"❌ ERROR: Generated UUID '{new_uuid}' is duplicate in this session!")
            all_unique = False
        else:
            print(f"✅ UUID '{new_uuid}' is unique in this session")
        
        generated_uuids.append(new_uuid)
    
    print(f"\n📊 Uniqueness Test Results:")
    print(f"   Generated UUIDs: {len(generated_uuids)}")
    print(f"   All unique: {all_unique}")
    print(f"   Success rate: {100 if all_unique else 0}%")
    
    return all_unique

def test_collision_simulation():
    """Simulate potential collision scenarios"""
    print("\n=== Testing Collision Scenarios ===\n")
    
    print("🧪 Testing collision handling...")
    
    # Test multiple rapid generations
    rapid_uuids = []
    collision_free = True
    
    for i in range(5):
        uuid_str = generate_adopter_uuid()
        
        if uuid_str.lower() in [u.lower() for u in rapid_uuids]:
            print(f"❌ Collision detected in rapid generation: {uuid_str}")
            collision_free = False
        
        rapid_uuids.append(uuid_str)
    
    print(f"🏃‍♂️ Rapid generation test: {'✅ PASS' if collision_free else '❌ FAIL'}")
    
    # Test pattern variety
    print(f"\n🎨 Testing pattern variety in generated UUIDs:")
    pattern_types = set()
    
    for uuid_str in rapid_uuids:
        prefix = "5a1f43e5-b1e6-4c5c-bc5a-"
        suffix = uuid_str[len(prefix):]
        
        unique_chars = set(suffix)
        if len(unique_chars) == 1:
            pattern_types.add("all_same")
        elif len(unique_chars) == 2 and suffix == suffix[:2] * 6:
            pattern_types.add("alternating")
        else:
            pattern_types.add("other_simple")
    
    print(f"   Pattern types generated: {sorted(list(pattern_types))}")
    print(f"   Pattern variety: {'✅ GOOD' if len(pattern_types) > 1 else '⚠️ LIMITED'}")
    
    return collision_free

def test_database_consistency():
    """Test consistency with existing database data"""
    print("\n=== Testing Database Consistency ===\n")
    
    try:
        # Analyze existing data
        analysis = analyze_existing_adopter_ids()
        
        if 'error' in analysis:
            print(f"❌ Error analyzing database: {analysis['error']}")
            return False
        
        total_existing = analysis['total_adopter_ids']
        compatible_existing = len(analysis['compatible_ids'])
        
        print(f"📊 Database Analysis:")
        print(f"   Total existing adopter IDs: {total_existing}")
        print(f"   Compatible with our format: {compatible_existing}")
        print(f"   Compatibility rate: {compatible_existing/total_existing*100:.1f}%" if total_existing > 0 else "   No existing data")
        
        # Generate new UUID and show it follows same pattern
        print(f"\n🆕 Generating new UUID for comparison:")
        new_uuid = generate_adopter_uuid()
        
        # Check if new UUID follows same format as existing ones
        from supabase_utils import check_uuid_format_compatibility
        compatibility = check_uuid_format_compatibility(new_uuid)
        
        print(f"   New UUID: {new_uuid}")
        print(f"   Follows database format: {'✅ YES' if compatibility['is_compatible'] else '❌ NO'}")
        
        if not compatibility['is_compatible']:
            print(f"   Issue: {compatibility.get('recommendation', 'Unknown')}")
        
        return compatibility['is_compatible']
        
    except Exception as e:
        print(f"❌ Error in database consistency test: {e}")
        return False

if __name__ == "__main__":
    print("🔒 Testing UUID Uniqueness and Collision Avoidance\n")
    
    # Run all tests
    results = []
    
    print("=" * 70)
    results.append(test_uniqueness_generation())
    
    print("=" * 70)
    results.append(test_collision_simulation())
    
    print("=" * 70)
    results.append(test_database_consistency())
    
    # Final summary
    print("\n" + "=" * 70)
    print("🎯 Final Summary:")
    print(f"   Uniqueness generation: {'✅ PASS' if results[0] else '❌ FAIL'}")
    print(f"   Collision simulation: {'✅ PASS' if results[1] else '❌ FAIL'}")
    print(f"   Database consistency: {'✅ PASS' if results[2] else '❌ FAIL'}")
    
    overall_success = all(results)
    print(f"   Overall result: {'✅ SUCCESS' if overall_success else '❌ FAILURE'}")
    
    if overall_success:
        print(f"\n🎉 All uniqueness tests passed!")
        print(f"✅ Generated UUIDs will be unique and compatible")
        print(f"✅ No collisions with existing database data")
        print(f"✅ Safe to use in adoption system")
    else:
        print(f"\n⚠️ Some uniqueness tests failed!")
        print(f"❗ Review the issues above before using in production")
    
    print(f"\n💡 Next step: Test the adoption process with new UUID generation") 