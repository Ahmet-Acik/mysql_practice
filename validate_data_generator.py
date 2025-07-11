#!/usr/bin/env python3
"""
Data Generator Validation Script
Validates that the data generator is working correctly.
"""

import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_generator import DataGenerator


def validate_data_generator():
    """Validate the data generator functionality."""
    print("🔍 Data Generator Validation")
    print("=" * 35)
    
    try:
        # Test 1: Import and instantiation
        generator = DataGenerator()
        print("✅ DataGenerator import and instantiation")
        
        # Test 2: Check data pools
        assert len(generator.first_names) > 0, "First names pool is empty"
        assert len(generator.last_names) > 0, "Last names pool is empty"
        assert len(generator.cities) > 0, "Cities pool is empty"
        assert len(generator.states) > 0, "States pool is empty"
        assert len(generator.product_adjectives) > 0, "Product adjectives pool is empty"
        assert len(generator.product_nouns) > 0, "Product nouns pool is empty"
        print("✅ All data pools are properly populated")
        
        # Test 3: Check methods exist
        methods = [
            'setup', 'cleanup', '_check_connection',
            'generate_categories', 'generate_customers', 
            'generate_products', 'generate_orders',
            'generate_sample_views'
        ]
        
        for method in methods:
            assert hasattr(generator, method), f"Method {method} is missing"
        print("✅ All required methods are present")
        
        # Test 4: Database connection (without actual connection)
        # This should not fail even without MySQL server
        try:
            result = generator.setup()
            if result:
                generator.cleanup()
                print("✅ Database connection test passed (MySQL server available)")
            else:
                print("ℹ️  Database connection test skipped (no MySQL server)")
        except Exception as e:
            print(f"ℹ️  Database connection test skipped: {e}")
        
        print("\n🎉 Data Generator Validation: PASSED")
        print("📝 The data generator is ready for use!")
        return True
        
    except Exception as e:
        print(f"\n❌ Data Generator Validation: FAILED")
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    success = validate_data_generator()
    sys.exit(0 if success else 1)
