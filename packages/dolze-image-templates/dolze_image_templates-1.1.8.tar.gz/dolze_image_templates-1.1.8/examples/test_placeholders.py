#!/usr/bin/env python3
"""
Simple test file for placeholder functionality in Dolze Templates

This file tests all available templates with placeholders only.
It generates images showing the default placeholder values for each template.

Usage:
    python test_placeholders.py
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import dolze_image_templates
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dolze_image_templates import render_template

def test_all_templates_with_placeholders():
    """Test all available templates with no variables to show placeholders"""
    
    print("🎨 Testing All Templates with Placeholders Only")
    print("=" * 60)
    
    # Create output directory
    output_dir = "test_placeholder_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # All available templates
    all_templates = [
        "coming_soon_post_2",
        "food_offer_promo", 
        "hiring_post",
       
        "product_sale_2",
        "product_showcase_3",
        "product_showcase_4",
     
    ]
    
    success_count = 0
    total_count = len(all_templates)
    
    for template_name in all_templates:
        print(f"\n📋 Testing: {template_name}")
        
        try:
            output_path = f"{output_dir}/{template_name}_placeholders.png"
            result = render_template(
                template_name=template_name,
                variables=None,  # No variables - should use all placeholders
                return_bytes=False,
                output_path=output_path
            )
            
            if result and os.path.exists(result):
                print(f"   ✅ SUCCESS: Image saved to {result}")
                success_count += 1
            else:
                print(f"   ❌ FAILED: No image generated")
                
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
    
    print(f"\n📊 Results: {success_count}/{total_count} templates generated successfully")
    return success_count == total_count

def main():
    """Main test function"""
    print("🚀 Starting Placeholder Test")
    print("=" * 40)
    
    try:
        success = test_all_templates_with_placeholders()
        
        if success:
            print(f"\n🎉 All tests completed successfully!")
            print(f"📁 Check the 'test_placeholder_output' directory for generated images")
            print(f"🔍 Each image shows the template with placeholder values")
        else:
            print(f"\n⚠️  Some tests failed. Check the output above for details.")
        
    except Exception as e:
        print(f"❌ Test suite failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
