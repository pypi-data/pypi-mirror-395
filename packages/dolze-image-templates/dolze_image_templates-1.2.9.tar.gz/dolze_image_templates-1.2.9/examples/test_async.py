"""
Async test script demonstrating how to use the Dolze Templates library with async support.

This script shows how to:
1. Load templates from JSON files
2. Render templates with different data using async/await
3. Save the generated images
"""

import os
import sys
import asyncio
from datetime import datetime
from pathlib import Path

# Add parent directory to path so we can import the package
sys.path.append(str(Path(__file__).parent.parent))

from dolze_image_templates import (
    get_template_registry,
    configure,
    get_font_manager,
    render_template,
)

# Initialize font manager to scan for fonts
font_manager = get_font_manager()
print("Font manager initialized. Available fonts:", font_manager.list_fonts())

# Configure the library
configure(
    templates_dir=os.path.join(
        os.path.dirname(__file__), "..", "dolze_image_templates", "html_templates"
    ),
    output_dir=os.path.join(os.path.dirname(__file__), "output"),
)


async def test_render_template_direct():
    """Test the main render_template function directly."""
    print("\n🎨 Testing render_template function directly...")
    
    template_data = {
        "cta_text": "LEARN MORE",
        "logo_url": "https://media-public.canva.com/cOgj8/MAGczGcOgj8/1/s2.png",
        "image_url": "https://media-public.canva.com/cOgj8/MAGczGcOgj8/1/s2.png",
        "cta_image": "https://media-public.canva.com/cOgj8/MAGczGcOgj8/1/s2.png",
        "heading": "plan your day in a snap",
        "subheading": "Driving success",
        "contact_email": "contact@business.com",
        "contact_phone": "+1-800-555-1234",
        "website_url": "dolze.ai /download",
        "quote": "The only way to do great work is to love what you do.",
        "theme_color": "#44EC9D",
        "user_avatar": "https://media-public.canva.com/cOgj8/MAGczGcOgj8/1/s2.png",
        "user_name": "Alex Johnson",
        "user_title": "Marketing Director, TechCorp",
        "testimonial_text": "This product has completely transformed how we works. The intuitive interface and powerful features have saved us countless hours.",
    }
    
    try:
        # Test with return_bytes=True
        print("Testing with return_bytes=True...")
        image_bytes = await render_template(
            template_name="neon_creative_agency",
            variables=template_data,
            return_bytes=True,
            output_format="png"
        )
        print(f"✅ Successfully generated image bytes: {len(image_bytes)} bytes")
        
        # Test with return_bytes=False (save to file)
        print("Testing with return_bytes=False...")
        output_path = os.path.join("output", "test_direct_render.png")
        result_path = await render_template(
            template_name="neon_creative_agency",
            variables=template_data,
            return_bytes=False,
            output_path=output_path,
            output_format="png"
        )
        print(f"✅ Successfully saved image to: {result_path}")
        
        return True
    except Exception as e:
        print(f"❌ Error in direct render test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_registry_render():
    """Test rendering through the template registry."""
    print("\n🎨 Testing template registry render...")
    
    registry = get_template_registry()
    
    template_data = {
        "website_url": "www.reallygreatsite.com",
        "social_handle": "@reallygreatsite",
        "description": "We are a modern creative agency that pushes the boundaries of traditional marketing. Our edgy approach to branding sets us apart, and our team of talented creatives is dedicated to bringing your vision to life. From strategy and identity to motion design and content, we craft bold work that wins attention and drives growth.",
        "studio_name": "Studio Shodwe",
        "address": "123 Anywhere St., Any City, ST 12345",
    }
    
    try:
        output_path = os.path.join("output", "test_registry_render.png")
        rendered_image = await registry.render_template(
            "neon_creative_agency",
            template_data,
            output_path=output_path,
        )
        
        if rendered_image:
            print(f"✅ Successfully rendered image through registry: {output_path}")
            return True
        else:
            print("❌ Registry render returned None")
            return False
            
    except Exception as e:
        print(f"❌ Error in registry render test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_multiple_templates():
    """Test rendering multiple templates concurrently."""
    print("\n🎨 Testing multiple templates concurrently...")
    
    templates_to_test = [
        {
            "name": "neon_creative_agency",
            "data": {
                "website_url": "www.reallygreatsite.com",
                "social_handle": "@reallygreatsite",
                "description": "We are a modern creative agency that pushes the boundaries of traditional marketing.",
                "studio_name": "Studio Shodwe",
                "address": "123 Anywhere St., Any City, ST 12345",
            }
        },
    
        {
            "name": "hiring_post",
            "data": {
                "theme_color": "#ffc524",
                "heading": "Join Our Team",
                "subheading": "Passionate about AI and business? We want you!",
                "job_title": "Social Media Lead",
                "website_url": "dolze.ai/careers",
                "company_name": "Dolze",
                "cta_text": "Apply Now!",
            }
        },
        {
            "name": "product_showcase_3",
            "data": {
                "product_name": "Dolze AI Assistant",
                "product_description": "Start automating your business today for just $15.99/month.",
                "cta_text": "Get Started",
                "product_image": "https://media-public.canva.com/cOgj8/MAGczGcOgj8/1/s2.png",
                "website_url": "dolze.ai/shop",
            }
        },
        {
            "name": "product_sale_2",
            "data": {
                "theme_color": "#fffdf7",
                "product_image": "https://media-public.canva.com/cOgj8/MAGczGcOgj8/1/s2.png",
                "heading": "Digital planner",
                "usp1": "Undated Planner",
                "usp2": "Hyperlinked Pages",
                "cta_text": "Book Now",
                "product_highlights": "300+ pages",
                "social_handle": "@dolze_ai",
                "business_name": "Dolze AI",
            }
        },
        {
            "name": "spotlight_launching",
            "data": {
                "main_title": "Launching Soon",
                "subheading": "Countdown",
                "days": "10",
                "hours": "09", 
                "minutes": "25",
                "cta_text": "Stay Tuned!"
            }
        },
        {
            "name": "coming_soon_post_2",
            "data": {
                "text": "3 days left until Dolze launches to simplify your business!",
                "cta_text": "STAY TUNED",
                "website_url": "dolze.ai/download",
            }
        },
        {
            "name": "faq_template",
            "data": {
                "question1": "How do I start a return or exchange?",
                "answer1": "Email us your order number to initiate the return or exchange process.",
                "question2": "What if I received a damaged item?",
                "answer2": "Send us photos right away. We'll arrange a replacement or full refund.",
                "company_name": "Dolze AI",
                "website_url": "www.dolze.ai",  
                "background_image_url": "https://media-public.canva.com/cOgj8/MAGczGcOgj8/1/s2.png",
            }
        },
        {
            "name": "food_offer_promo",
            "data": {
                "background_image": "https://media-public.canva.com/cOgj8/MAGczGcOgj8/1/s2.png",
                "logo_url": "https://media-public.canva.com/cOgj8/MAGczGcOgj8/1/s2.png",
                "product_image": "https://media-public.canva.com/cOgj8/MAGczGcOgj8/1/s2.png",
                "product_name": "GRILLED CHICKEN",
                "product_description": "Description of the chicken dish and its ingredients",
                "price": "$14",
                "contact_text": "Contact us on ",
                "price_note": "ONLY",
                "contact_number": "987 6543 3210",
                "address_line1": "123 STREET, AREA NAME",
                "address_line2": "YOUR CITY, STATE",
                "username": "@username",
                "theme_color": "#F4A300",
            }
        },
      
        {
            "name": "product_showcase_4",
            "data": {
                "offer_text": "Only with Dolze",
                "product_image": "https://media-public.canva.com/cOgj8/MAGczGcOgj8/1/s2.png",
                "website_url": "dolze.ai/shop",
                "theme_color": "#ffc524",
            }
        },
        {
            "name": "social_media_tips_template",
            "data": {
                "title": "How to Grow Your Brand on Social Media",
                "tip1": "Determine a consistent upload schedule.",
                "tip2": "Understand your target demographic.",
                "tip3": "Keep track of social media analytics.",
                "tip4": "Encourage interaction with your posts.",
                "tip5": "Engage directly with your audience online.",
                "button_text": "Follow @reallygreatsite for more tips",
                "button_url": "#",
                "custom_css": "",
                "custom_html": ""
            }
        }
    ]
    
    try:
        # Create tasks for concurrent execution
        tasks = []
        for i, template in enumerate(templates_to_test):
            task = render_template(
                template_name=template["name"],
                variables=template["data"],
                return_bytes=False,
                output_path=os.path.join("output", f"test_concurrent_{i}.png"),
                output_format="png"
            )
            tasks.append(task)
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        success_count = 0
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"❌ Template {i} ({templates_to_test[i]['name']}) failed: {str(result)}")
            else:
                print(f"✅ Template {i} ({templates_to_test[i]['name']}) succeeded: {result}")
                success_count += 1
        
        print(f"📊 Concurrent test results: {success_count}/{len(templates_to_test)} templates succeeded")
        return success_count == len(templates_to_test)
        
    except Exception as e:
        print(f"❌ Error in concurrent test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all async tests."""
    print("�� Starting Async Dolze Templates Tests")
    print("=" * 50)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    test_results = []
    
    # Run all tests
    # test_results.append(await test_render_template_direct())
    # test_results.append(await test_registry_render())
    test_results.append(await test_multiple_templates())
    
    # Summary
    passed = sum(test_results)
    total = len(test_results)
    
    print(f"\n📊 Test Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All async tests completed successfully!")
        print("�� Check the 'output' directory for generated images")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total


if __name__ == "__main__":
    asyncio.run(main())