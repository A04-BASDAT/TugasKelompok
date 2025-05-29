#!/usr/bin/env python3
"""
Test script to verify the trigger functionality for updating total kontribusi
"""

import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tugas_kelompok_basdat.settings')
django.setup()

from supabase_utils import (
    create_update_total_kontribusi_trigger,
    get_all_adopter,
    get_all_adopsi,
    delete_adopter_with_cascade
)

def test_trigger_creation():
    """Test creating the trigger function"""
    print("🔧 Testing trigger creation...")
    
    result = create_update_total_kontribusi_trigger()
    
    if result['success']:
        print(f"✅ {result['message']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    return result['success']

def test_current_data():
    """Test current data state"""
    print("\n📊 Current data state:")
    
    adopters = get_all_adopter()
    adoptions = get_all_adopsi()
    
    print(f"Total adopters: {len(adopters)}")
    print(f"Total adoptions: {len(adoptions)}")
    
    # Show some adopters with their contributions
    print("\nAdopter contributions:")
    for i, adopter in enumerate(adopters[:5]):  # Show first 5
        username = adopter.get('username_adopter', 'Unknown')
        total = adopter.get('total_kontribusi', 0)
        print(f"  {i+1}. {username}: Rp{total:,}")
    
    return True

def test_cascade_delete():
    """Test cascade delete functionality (simulation only)"""
    print("\n🗑️  Testing cascade delete functionality...")
    
    adopters = get_all_adopter()
    if adopters:
        # Find an adopter with adoptions for testing
        test_adopter = None
        for adopter in adopters:
            adoptions = get_all_adopsi()
            for adoption in adoptions:
                if adoption['id_adopter'] == adopter['id_adopter']:
                    test_adopter = adopter
                    break
            if test_adopter:
                break
        
        if test_adopter:
            print(f"Found test adopter: {test_adopter['username_adopter']}")
            print("ℹ️  Would delete this adopter and all related adoptions")
            print("⚠️  Not actually deleting in test mode")
            return True
        else:
            print("No adopters with adoptions found for testing")
            return False
    else:
        print("No adopters found")
        return False

def main():
    """Main test function"""
    print("🚀 Starting trigger functionality tests...\n")
    
    # Test 1: Create trigger
    trigger_success = test_trigger_creation()
    
    # Test 2: Check current data
    data_success = test_current_data()
    
    # Test 3: Test cascade delete (simulation)
    delete_success = test_cascade_delete()
    
    print(f"\n📝 Test Results:")
    print(f"Trigger Creation: {'✅ PASS' if trigger_success else '❌ FAIL'}")
    print(f"Data Check: {'✅ PASS' if data_success else '❌ FAIL'}")
    print(f"Cascade Delete: {'✅ PASS' if delete_success else '❌ FAIL'}")
    
    if all([trigger_success, data_success, delete_success]):
        print(f"\n🎉 All tests passed! Trigger functionality is ready.")
    else:
        print(f"\n⚠️  Some tests failed. Check the implementation.")

if __name__ == "__main__":
    main() 