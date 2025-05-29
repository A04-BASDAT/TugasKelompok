#!/usr/bin/env python
import sys
import os

# Add parent directory to path to import supabase_utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from supabase_utils import (
    analyze_existing_adopter_ids, 
    validate_all_existing_data,
    check_uuid_format_compatibility
)

def test_existing_adopsi_data():
    """Test and analyze existing adopter IDs in adopsi table"""
    print("=== Testing Existing Adopsi Data ===\n")
    
    try:
        analysis = analyze_existing_adopter_ids()
        
        if 'error' in analysis:
            print(f"❌ Error analyzing data: {analysis['error']}")
            return False
        
        total_ids = analysis['total_adopter_ids']
        compatible_count = len(analysis['compatible_ids'])
        incompatible_count = len(analysis['incompatible_ids'])
        
        print(f"📊 Summary:")
        print(f"   Total adopter IDs: {total_ids}")
        print(f"   ✅ Compatible: {compatible_count}")
        print(f"   ❌ Incompatible: {incompatible_count}")
        print(f"   Success rate: {compatible_count/total_ids*100:.1f}%" if total_ids > 0 else "   No data found")
        
        if analysis['compatible_ids']:
            print(f"\n✅ Compatible IDs (showing first 5):")
            for i, uid in enumerate(analysis['compatible_ids'][:5]):
                print(f"   {i+1}. {uid}")
            if len(analysis['compatible_ids']) > 5:
                print(f"   ... and {len(analysis['compatible_ids']) - 5} more")
        
        if analysis['incompatible_ids']:
            print(f"\n❌ Incompatible IDs:")
            for item in analysis['incompatible_ids']:
                print(f"   ID: {item['id']}")
                print(f"   Issue: {item['issues'].get('recommendation', 'Unknown issue')}")
                print()
        
        if analysis['pattern_analysis']:
            print(f"\n📈 Pattern Analysis:")
            for pattern, ids in analysis['pattern_analysis'].items():
                print(f"   {pattern}: {len(ids)} IDs")
                # Show examples
                for id_info in ids[:2]:
                    print(f"      Example: ...{id_info['suffix']} (digits: {id_info['unique_digits']})")
        
        return compatible_count == total_ids  # All should be compatible
        
    except Exception as e:
        print(f"❌ Error in test_existing_adopsi_data: {e}")
        return False

def test_comprehensive_validation():
    """Run comprehensive validation of all adopter data"""
    print("\n=== Comprehensive Data Validation ===\n")
    
    try:
        validation = validate_all_existing_data()
        
        if 'error' in validation:
            print(f"❌ Error in validation: {validation['error']}")
            return False
        
        # Summary
        adopsi_analysis = validation.get('adopsi_analysis', {})
        adopter_analysis = validation.get('adopter_table_analysis', {})
        consistency = validation.get('cross_table_consistency', {})
        recommendations = validation.get('recommendations', [])
        
        print(f"📊 Validation Summary:")
        print(f"   Adopsi table IDs: {adopsi_analysis.get('total_adopter_ids', 0)}")
        print(f"   Adopter table records: {adopter_analysis.get('total_adopters', 0)}")
        print(f"   Cross-table consistency issues: {len(recommendations)}")
        
        if consistency:
            missing_in_adopter = consistency.get('missing_in_adopter_table', [])
            missing_in_adopsi = consistency.get('missing_in_adopsi_table', [])
            
            if missing_in_adopter:
                print(f"\n⚠️  IDs in adopsi but missing from adopter table: {len(missing_in_adopter)}")
                for uid in missing_in_adopter[:3]:
                    print(f"      {uid}")
                if len(missing_in_adopter) > 3:
                    print(f"      ... and {len(missing_in_adopter) - 3} more")
            
            if missing_in_adopsi:
                print(f"\n⚠️  IDs in adopter table but no adoptions: {len(missing_in_adopsi)}")
                for uid in missing_in_adopsi[:3]:
                    print(f"      {uid}")
                if len(missing_in_adopsi) > 3:
                    print(f"      ... and {len(missing_in_adopsi) - 3} more")
        
        if recommendations:
            print(f"\n📋 Recommendations:")
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")
        else:
            print(f"\n✅ No issues found - data is consistent!")
        
        return len(recommendations) == 0  # Success if no recommendations
        
    except Exception as e:
        print(f"❌ Error in test_comprehensive_validation: {e}")
        return False

def test_sample_patterns():
    """Test some sample patterns to understand what works"""
    print("\n=== Testing Sample Patterns ===\n")
    
    sample_patterns = [
        "5a1f43e5-b1e6-4c5c-bc5a-111111111111",  # All same
        "5a1f43e5-b1e6-4c5c-bc5a-121212121212",  # Alternating
        "5a1f43e5-b1e6-4c5c-bc5a-123123123123",  # Repeating triplet
        "5a1f43e5-b1e6-4c5c-bc5a-999999999911",  # Simple variation
        "5a1f43e5-b1e6-4c5c-bc5a-495845998512",  # Random (should fail)
    ]
    
    for pattern in sample_patterns:
        compatibility = check_uuid_format_compatibility(pattern)
        status = "✅" if compatibility['is_compatible'] else "❌"
        print(f"{status} {pattern}")
        if not compatibility['is_compatible']:
            print(f"   Issue: {compatibility.get('recommendation', 'Unknown')}")
    
    return True

if __name__ == "__main__":
    print("🔍 Analyzing Existing Database Data\n")
    
    # Run all tests
    results = []
    
    print("=" * 60)
    results.append(test_existing_adopsi_data())
    
    print("=" * 60)
    results.append(test_comprehensive_validation())
    
    print("=" * 60)
    results.append(test_sample_patterns())
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎯 Final Summary:")
    print(f"   Existing adopsi data test: {'✅ PASS' if results[0] else '❌ FAIL'}")
    print(f"   Comprehensive validation: {'✅ PASS' if results[1] else '❌ FAIL'}")
    print(f"   Sample patterns test: {'✅ PASS' if results[2] else '❌ FAIL'}")
    
    if all(results):
        print(f"\n🎉 All tests passed! Your existing data follows the required patterns.")
    else:
        print(f"\n⚠️  Some issues found. Check the details above.")
    
    print("\n💡 Next steps:")
    print("   1. If there are incompatible IDs, they may need to be updated")
    print("   2. New adoptions will use the corrected pattern generator")
    print("   3. Test the adoption process with the new patterns") 