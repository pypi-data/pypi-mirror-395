"""
Test script for template rendering.

This script demonstrates how to render different templates with various configurations.
It supports rendering multiple templates with different data.
"""

import os
import sys
import asyncio
from pathlib import Path

# Add parent directory to path so we can import the package
sys.path.append(str(Path(__file__).parent.parent))

from dolze_image_templates import (
    get_template_registry,
    configure,
    get_font_manager,
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


async def render_template(template_name, template_data):
    """Render a template with the provided data.

    Args:
        template_name (str): Name to use for the output file
        template_data (dict): Template data with custom content

    Returns:
        The rendered image
    """
    # Get the template registry
    registry = get_template_registry()

    # Render the template with the data
    output_path = os.path.join("output", f"{template_name}.png")
    rendered_image = await registry.render_template(
        template_name,  # Use the actual template name
        template_data,
        output_path=output_path,
    )

    print(f"Template saved to {os.path.abspath(output_path)}")
    return rendered_image


def get_faq_template_data():
    """Get sample data for the FAQ template."""
    return {
        "title": "FAQs",
        "question1": "How do I start a return or exchange?",
        "answer1": "Email us your order number to initiate the return or exchange process.",
        "question2": "What if I received a damaged item?",
        "answer2": "Send us photos right away. We'll arrange a replacement or full refund.",
        "question3": "How long does shipping take?",
        "answer3": "Standard shipping takes 3–7 business days. Express options (1–2 days) are available at checkout.",
        "question4": "Do you ship internationally?",
        "answer4": "Yes! We ship to over 40 countries. Duties and taxes may apply depending on your location.",
        "question5": "What is your return window?",
        "answer5": "You have 30 days from delivery to return unused items in original packaging for a full refund.",
        "question6": "How can I track my order?",
        "answer6": "You'll receive a tracking link via email as soon as your order ships. Check your inbox or spam folder.",
        "brand_name": "Dolze AI",
        "background_color": "#f8fbf8",
        "primary_text_color": "#0a3622",
        "title_color": "#0a6b42",
        "card_bg_color": "#0a6b42",
        "card_text_color": "#ffffff",
        "footer_text_color": "#0a3622",
        "brand_color": "#0a6b42",
        "shape_border_color": "rgba(10, 107, 66, 0.12)",
        "custom_css": "",
        "custom_html": ""
    }


def get_qa_template_data():
    """Get sample data for the Q&A template."""
    return {
        "question": "What is renewable energy?",
        "answer": "One wind turbine can power 1,500 homes annually!",
        "username": "@techcorp",
        "website_url": "techcorp.com",
        "theme_color": "#795548",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png"
    }


def get_spotlight_launching_data():
    """Get sample data for the spotlight launching template."""
    return {
        "main_title": "Launching Soon",
        "subheading": "Countdown",
        "days": "15",
        "hours": "08",
        "minutes": "45",
        "cta_text": "Stay Tuned!"
    }


def get_app_promo_2_data():
    """Get sample data for the app promo 2 template."""
    return {
        "bg_image_url": "https://iili.io/fJbl3YJ.png",
        "text_color": "#FFFFFF",
        "subtitle_color": "#FFFFFF",
        "small_text_color": "rgba(255,255,255,0.75)",
        "screen_background_color": "#050505",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "screenshot_url": "https://iili.io/fJDQpPp.png",
        "title_text": "Don’t get left\nbehind.",
        "subtitle_text": "Upgrade your\nworkflow with AI.",
        "small_text": "Try it now at\nwww.reallygreatsite.com",
        "custom_css": "",
        "custom_html": "",
    }
def get_social_media_tips_template_data():
    """Get sample data for the social media tips template."""
    return {
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
def get_food_offer_promo_data():
    """Get sample data for the food offer promo template."""
    return {
        "product_image": "https://i.postimg.cc/PfZqsPcV/image-31.png",
        "product_name": "GRILLED CHICKEN",
        "product_description": "Description of the chicken dish and its ingredients",
        "price": "$14",
        "contact_text": "Contact us on ",
        "contact_number": "987 6543 3210",
        "address_line1": "123 STREET, AREA NAME",
        "address_line2": "YOUR CITY, STATE",
        "username": "@username",
        "theme_color": "#F4A300",
        "custom_css": "",
        "custom_html": ""
    }

def get_product_promotion_v2_data():
    """Get sample data for the product promotion v2 template."""
    return {
        "brand": "Dolze AI",
        "title": "GRILLED CHICKEN",
        "description": "Description of the chicken dish and its ingredients",
        "price": "$14",
        "contact_text": "Contact us on",
        "contact_phone": "987 6543 3210",
        "address_line1": "123 STREET, AREA NAME",
        "address_line2": "YOUR CITY, STATE",
        "product_image_url": "https://i.postimg.cc/PfZqsPcV/image-31.png",
        "background_color": "#ff9800",
        "price_bg_color": "#d60000",
        "price_text_color": "#ffffff",
        "text_color": "#000000",
        "custom_css": "",
        "custom_html": ""
    }

def get_testimonial_card_3_data():
    """Get sample data for the testimonial card 3 template."""
    return {
        "headline": "Testimonial",
        "author_name": "Olivia Wilson",
        "quote": "Social media can also be used to share interesting facts, inspiring true stories, helpful tips, useful knowledge, and other important information.",
        "author_role": "CEO of Ginyard International Co.",
        "company_name": "ReallyGreatCompany"
    }
def get_stocks_dividend_post_2_data():
    """Get sample data for the stocks dividend post 2 template."""
    return {
        "brand_name": "Stock.Academy",
        "title_line1": "What is a",
        "title_line2_accent": "Dividend Stock?",
        "body_text": "A dividend stock gives you regular income from company profits—paid out to shareholders. Think of it as your investment earning you 'rent' every quarter.",
    }

def get_spotlight_launching_text_3_data():
    """Get sample data for the spotlight launching text 3 template."""
    return {
        "main_title": "Launching Soon",
        "subtitle": "Get ready, because something amazing is coming your way!\nOur launch is just around the corner.",
        "website_url": "www.reallygreatsite.com",
        "custom_css": "",
        "custom_html": ""
    }

def get_search_services_listing_data():
    """Get sample data for the search services listing template."""
    return {
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_light_bg.svg",
        "brand_name": "Dolze AI",
        "search_placeholder": "Search our services...",
        "service1": "Online Payment Tracking",
        "service2": "Automatic Bank Feeds",
        "service3": "Collect Digital Payments",
        "service4": "Online Invoices & Quotes",
        "selected_service": "2",
        "hand_image_url": "https://i.ibb.co/example-hand.png",
        "cta_text": "reallygreatsite.com",
        "custom_css": ".service-item.item2 { background: #F3F4F6; }",
        "custom_html": ""
    }

def get_announcement_template_data():
    """Get sample data for the announcement template."""
    return {
        "primary_color": "#0A1D56",
        "header_text": "Official Announcement",
        "main_text": "We are\npartnering\nwith",
        "partner_text": "Rolk Inc.",
        "details_text": "More details on",
        "website_url": "www.reallygreatsite.com",
        "company_name": "WeisenhamTech",
        "custom_css": "",
        "custom_html": ""
    }

def get_customer_retention_strategies_data():
    """Get sample data for the customer retention strategies template."""
    return {
        "logo_letter": "D",
        "brand_name": "Dolze AI",
        "heading": "6 Strategies for",
        "title": "Customer Retention",
        "strategy1": "Make it simple\nand quick for\npeople to buy.",
        "strategy2": "Give good and\nuseful products\nwith help.",
        "strategy3": "Be kind, patient\nand helpful to\npeople.",
        "strategy4": "Make fun reward\nplans for happy\nbuyers.",
        "strategy5": "Always do what\nyou say you will\ndo about it.",
        "strategy6": "Ask happy\npeople to tell\nmore friends.",
        "footer_text": "www.dolze.ai",
        "custom_css": "",
        "custom_html": ""
    }

def get_hiring_minimal_red_data():
    """Get sample data for the hiring minimal red template."""
    return {
        "company_name": "Dolze AI",
        "hiring_title": "We're\nHiring",
        "role_title": "Marketers",
        "bullet1": "Do you have a passion for marketing?",
        "bullet2": "Do you have experience in marketing campaigns?",
        "bullet3": "Do you want to join a dynamic and innovative team?",
        "cta_text": "If yes, then apply now!",
        "apply_instruction": "Send your CV at email us:",
        "apply_email": "hello@reallygreatsite.com",
        "custom_css": "",
        "custom_html": ""
    }

def get_hiring_post_data():
    """Get sample data for the hiring post template."""
    return {
        "main_heading": "Join Our\nTeam",
        "intro_text": "Passionate about AI and business? We want you!",
        "hiring_prefix": "hiring",
        "job_title": "Social Media Lead",
        "company_name": "Dolze",
        "cta_text": "Apply Now!",
        "custom_css": "",
        "custom_html": ""
    }

def get_myth_or_fact_data():
    """Get sample data for the myth or fact template."""
    return {
        "main_title": "Myth or Fact\nSocial Media",
        "subtitle": "LET'S CLEAR UP COMMON SOCIAL MEDIA ASSUMPTIONS",
        "myth_heading": "Myth",
        "myth_item1": "You must post daily",
        "myth_item2": "More hashtags = more views",
        "myth_item3": "You need to go viral",
        "myth_item4": "Strategy = trend following",
        "fact_heading": "Fact",
        "fact_item1": "You must post daily",
        "fact_item2": "More hashtags = more views",
        "fact_item3": "You need to go viral",
        "fact_item4": "Strategy = trend following",
        "footer_text": "Reallygreatsite",   
        "custom_css": "",
        "custom_html": ""
    }

def get_perfect_job_search_data():
    """Get sample data for the perfect job search template."""
    return {
        "image_url": "https://images.pexels.com/photos/7691739/pexels-photo-7691739.jpeg",
        "logo_icon_url": "https://images.pexels.com/photos/2745478/pexels-photo-2745478.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=200",
        "logo_primary_text": "Business",
        "logo_secondary_text": "Agency",
        "headline": "Find The Perfect\nJob That You\nDeserve.",
        "subtitle": "Join thousands of professionals who found their dream career with us",
        "benefit1": "Expert career guidance",
        "benefit2": "Access to top companies",
        "cta_text": "reallygreatsite.com",
        "custom_css": "",
        "custom_html": ""
    }

def get_social_media_data():
    """Get sample data for the social media marketing template."""
    return {
        "brand_name": "Studio Shodwe",
        "main_heading": "Social Media\nMarketing",
        "tagline": "Transform your online presence with expert strategies",
        "benefit1": "Increased Visibility",
        "benefit2": "Better Engagement",
        "benefit3": "Higher Conversion Rates",
        "cta_main_text": "Visit Us For\nMore",
        "website_url": "reallygreatsite.com",
        "photo_url": "https://images.pexels.com/photos/3184418/pexels-photo-3184418.jpeg?auto=compress&cs=tinysrgb&w=800",
        "custom_css": "",
        "custom_html": ""
    }

def get_contact_us_overlay_data():
    """Get sample data for the contact us overlay template."""
    return {
        "background_image_url": "https://images.pexels.com/photos/259588/pexels-photo-259588.jpeg?auto=compress&cs=tinysrgb&w=1080",
        "brand_name": "Dolze AI",
        "main_heading": "Contact Us",
        "tagline": "Feel free to reach out to us!",
        "phone": "123-456-7890",
        "email": "hello@reallygreatsite.com",
        "website_url": "www.reallygreatsite.com",
        "address": "123 Anywhere St., Any City",
        "custom_css": "",
        "custom_html": ""
    }
def get_perfect_job_search_template_data():
    """Get sample data for the perfect job search template."""
    return {
        "image_url": "https://images.pexels.com/photos/7691739/pexels-photo-7691739.jpeg",
        "logo_icon_url": "https://images.pexels.com/photos/2745478/pexels-photo-2745478.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=200",
        "logo_primary_text": "Business",
        "logo_secondary_text": "Agency",
        "headline": "Find The Perfect\nJob That You\nDeserve.",
        "cta_text": "reallygreatsite.com",
        "supporting_text": "We Will Help You to Find The Most Suitable Job for You",
        "custom_css": "",
        "custom_html": ""
    }
def get_business_highlights_2035_html_data():
    """Get sample data for the business highlights 2035 html template."""
    return {
        "heading_word1": "BUSINESS",
        "heading_word2": "HIGHLIGHTS",
        "highlight1": "We are committed to providing the best possible service to our clients.",
        "highlight2": "We are committed to providing the best possible service to our clients.",
    }

def get_why_us_reasons_data():
    """Get sample data for the why us reasons template."""
    return {
        "site_name": "REALLYGREATSITE",
        "title_line1": "REASONS TO",
        "title_line2_part1": "CHOOSE",
        "title_line2_part2": "US:",
        "badge_text": "5 KEY REASONS",
        "reason1_title": "Expertise and Experience",
        "reason1_description": "Our team consists of seasoned professionals with specialized expertise to produce top-quality results.",
        "reason2_title": "Innovative Solutions",
        "reason2_description": "We utilize the latest technologies and creative strategies to deliver innovative and effective outcomes for your projects.",
        "reason3_title": "Customer-Centric Approach",
        "reason3_description": "We prioritize your needs and preferences, providing personalized solutions and exceptional customer service.",
        "reason4_title": "Reliability and Trust",
        "reason4_description": "We are dedicated to transparency, meeting deadlines, and fostering open communication to build a reliable partnership.",
        "reason5_title": "Competitive Pricing",
        "reason5_description": "We offer high-quality services at a competitive price, ensuring you get the best value for your investment.",
        "background_color": "#f8f4f0",
        "container_bg_color": "#fff",
        "primary_text_color": "#333",
        "secondary_text_color": "#666",
        "accent_color": "#ff5722",
        "line_color": "#ffccbc",
        "number_bg_color": "#fff",
        "number_text_color": "#ff5722",
        "custom_css": "",
        "custom_html": ""
    }

def get_smart_investment_data():
    """Get sample data for the smart investment template."""
    return {
        "company_name": "Ginyard International",
        "headline": "Smart Investment Now",
        "body_text": "A wise step to manage your future finances with the right, safe, and targeted strategy. By starting early, you can make your money work harder, build long-term wealth, and achieve financial freedom faster.",
        "sub_headline": "The Best Time to Invest Is Now",
        "cta_text": "More Infromation",
        "website_url": "www.reallygreatsite.com",
        "image_url": "https://images.pexels.com/photos/1181263/pexels-photo-1181263.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
    }

def get_pricing_plans_data():
    """Get sample data for the pricing plans template."""
    return {
        "company_name": "WARDIERE INC.",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "title": "Pricing Plans",
        "subtitle": "No matter your team size or experience level, our pricing adapts to your needs.",
        "starter_title": "Starter",
        "starter_description": "Perfect for individuals",
        "starter_feature1": "Basic features",
        "starter_feature2": "Email support",
        "starter_feature3": "1 user account",
        "starter_feature4": "Mobile app access",
        "starter_price": "$ 49/mo",
        "starter_extra": "Cancel anytime",
        "pro_title": "Pro",
        "pro_description": "Ideal for growing businesses",
        "pro_feature1": "Everything in Starter",
        "pro_feature2": "Priority support",
        "pro_feature3": "Up to 5 users",
        "pro_feature4": "Weekly reports",
        "pro_price": "$ 99/mo",
        "pro_extra": "24/7 customer support",
        "business_title": "Business",
        "business_description": "Tailored for teams with customizations",
        "business_feature1": "All Pro features",
        "business_feature2": "Account manager",
        "business_feature3": "Unlimited users",
        "business_feature4": "Advanced analytics",
        "business_price": "$ 149/mo",
        "business_extra": "7-day free trial",
      "cta_text": "Visit our website to explore the full list of features, detailed FAQs and plan comparisons. Let's take the next step and grow your business!",
      "website_url": "www.reallygreatsite.com",
      "accent_color": "#FFEB00",
      "custom_css": "",
      "custom_html": ""
  }

def get_we_are_hiring_data():
    """Get sample data for the we are hiring template."""
    return {
        "headline_primary": "WE ARE HIRING",
        "subheading_secondary": "Don't miss this opportunity",
        "role_list": "UI DESIGNER / FRONTEND DEVELOPER",
        "contact_email": "hello@reallygreatsite.com",
        "primary_color": "#233B35",
        "secondary_color": "#FFDE59",
        "custom_css": "",
        "custom_html": ""
    }

def get_flash_sale_data():
    """Get sample data for the flash sale template."""
    return {
        "brand_name": "Borcelle",
        "discount_percentage": "70",
        "days": "00",
        "hours": "00",
        "minutes": "00",
        "cta_text": "Shop Now Before It's Too Late!",
        "primary_color": "#d85028",
        "secondary_color": "#FFEB3B",
        "accent_color": "#5D4037",
        "custom_css": "",
        "custom_html": ""
    }


def get_free_resource_data():
    """Get sample data for the free resource template."""
    return {
        "small_heading": "Free Guide:",
        "headline": "How to Grow Your Audience on Social Media",
        "website_url": "REALLYGREATSITE.COM",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTpyqjYg3R7LdfImgyKZGkbNa498Dh6jg4qlw&s",
        "accent_primary_color": "#000000",
        "accent_secondary_color": "#555555",
        "background_color": "#ffffff",
        "text_color": "#555555",
        "resource_container_background": "#e5e5e5",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_light_bg.svg",
        "custom_css": "",
        "custom_html": "",
    }


def get_creative_marketing_agency_data():
    """Get sample data for the creative marketing agency template."""
    return {
        "company_name": "Wardiere Inc.",
        "company_type": "Company",
        "heading_word1": "Creative",
        "heading_word2": "Marketing",
        "heading_word3": "Agency",
        "photo_url": "https://fjord.dropboxstatic.com/warp/conversion/dropbox/warp/en-us/resources/articles/collaborative-real-time-editing/TL_nzd2t5.jpg?id=109125be-848d-45e0-ad43-035e8555e410&width=1024&output_type=webp",
        "service1": "Branding and Identity Design",
        "service2": "Social Media Management",
        "service3": "Content Creation",
        "service4": "Digital Advertising",
        "phone_number": "+123-456-7890",
        "primary_color": "#1e3a52",
        "secondary_color": "#f5e6d3",
        "background_color": "#f9fafa",
        "custom_css": "",
        "custom_html": ""
    }

def get_quiz_2_data():
    """Get sample data for the quiz 2 template."""
    return {
        "background_color": "#1c1a44",
        "text_color": "#ffffff",
        "number_box_color": "#4d82b8",
        "option_background_color": "#c2e8e0",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "left_image_url": "https://www.bigfootdigital.co.uk/wp-content/uploads/2020/07/image-optimisation-scaled.jpg",
        "title_text": "Which financial service do you\nfind most essential for your needs?",
        "option1_label": "Retirement Planning",
        "option2_label": "Investment Management",
        "option3_label": "Debt Consolidation\nSolutions",
        "option4_label": "Financial Advisory\nServices",
        "footer_text": "@reallygreatwebsite",
        "custom_css": "",
        "custom_html": ""
    }

def get_quiz_3_data():
    """Get sample data for the quiz 3 template."""
    return {
        "background_color": "#1f1e1f",
        "text_color": "#ffffff",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "title_text": "WHICH IS MORE\nIMPORTANT FOR YOU?",
        "option1_label": "CONSISTENCY",
        "option2_label": "RELEVANCE",
        "footer_text": "@reallygreatsite",
        "options_box_background": "#2d2d2d",
        "options_box_border": "rgba(255,255,255,0.1)",
        "divider_color": "rgba(255,255,255,0.5)",
        "custom_css": "",
        "custom_html": ""
    }

def get_black_friday_offer_1_data():
    """Get sample data for the black friday offer 1 template."""
    return {
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "brand_name": "Dolze",
        "big_text_top": "BLACK",
        "big_text_bottom": "FRIDAY",
        "ribbon_text": "UP TO 50% OFF",
        "description": "From fashion to electronics, get everything you need at Black Friday prices!",
        "website_url": "www.reallygreatsite.com",
        "accent_primary_color": "#0066ff",
        "accent_secondary_color": "#ffffff",
        "background_color": "#000000",
        "custom_css": "",
        "custom_html": ""
    }

def get_question_1_data():
    """Get sample data for the question 1 template."""
    return {
        "background_color": "#000000",
        "background_image_url": "https://iili.io/fdMrUI1.webp",
        "background_overlay_opacity": "0.35",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "search_text": "How do I cover emergencies?",
        "footer_text": "Get your answer here: dolze.ai",
        "search_bar_background": "#ffffff",
        "search_text_color": "#111111",
        "icon_stroke_color": "#000000",
        "footer_text_color": "#ffffff",
        "custom_css": "",
        "custom_html": ""
    }

def get_text_block_1_data():
    """Get sample data for the text block 1 template."""
    return {
        "accent_primary_color": "#BD6F4B",
        "accent_secondary_color": "#FFFFFF",
        "text_color_primary": "#FFFFFF",
        "text_color_secondary": "rgba(255,255,255,0.45)",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "heading_line1": "How to build",
        "heading_line2": "an email list",
        "heading_accent_text": "from scratch",
        "cta_text": "Read Caption",
        "cta_link": "#",
        "footer_text": "@reallygreatsite",
        "illustration_url": "https://iili.io/fdjJMrJ.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_product_promo_3_data():
    """Get sample data for the Product Promo 3 template."""
    return {
        "background_color": "#ffffff",
        "primary_color": "#6A41C7",
        "title": "New<br>Product",
        "subtitle": "Brightening Serum",
        "product_image_url": "https://iili.io/f3ZyLzu.png",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_light_bg.svg",
        "website_url": "@dolze.ai",
        "custom_css": "",
        "custom_html": ""
    }

def get_product_promo_1_data():
    """Get sample data for the Product Promo 1 (Polaroid Collage) template."""
    return {
        "background_color": "#f57842",
        "primary_color": "#ffffff",
        "title": "Automate<br>Everything!",
        "subtitle": "Automate your business operations with Dolze",
        "image_url_1": "https://d3njjcbhbojbot.cloudfront.net/api/utilities/v1/imageproxy/https://images.ctfassets.net/wp1lcwdav1p1/5w02MCzaAgiHWdpsDC81YI/d2e12e073619958227bfe7e05b797b0c/GettyImages-1374879082.jpg?w=1500&h=680&q=60&fit=fill&f=faces&fm=jpg&fl=progressive&auto=format%2Ccompress&dpr=1&w=1000",
        "image_url_2": "https://eltchalkboard.com/wp-content/uploads/2023/04/dartboard1200.jpg",
        "image_url_3": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgTNP02uSpEk0vHBM4UgU-GDQO7X2DTWYRoK1P1zL7XHRrBm1kA8OhRtZQSS1jLN7zG3A&usqp=CAU",
        "website_url": "@dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_plan_post_1_data():
    """Get sample data for the Plan Post 1 template."""
    return {
        "background_color": "#f7f1df",
        "primary_color": "#4a2f8b",
        "accent_color": "#6941C7",
        "text1": "\"I have a plan\"",
        "text2": "The plan:",
        "image_url": "https://img.freepik.com/premium-photo/shahi-paneer-with-rich-gravy_1179130-91019.jpg",
        "website_url": "@dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_light_bg.svg",
        "custom_css": "",
        "custom_html": ""
    }

def get_indian_constitution_day_data():
    """Get sample data for the Indian Constitution Day template."""
    return {
        "background_image_url": "https://iili.io/fFOnO7I.png",
        "title": "Honouring the spirit that shapes our democracy.",
        "subtitle": "Celebrating India's Constitution and the values it upholds.",
        "preheading": "📅 Nov 26 — Indian Constitution Day",
        "website_url": "@dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_guru_nanak_jayanti_data():
    """Get sample data for the Guru Nanak Jayanti template."""
    return {
        "background_image_url": "https://iili.io/fFOS3q7.png",
        "title": "Let compassion and wisdom guide our path.",
        "subtitle": "Remembering the teachings of Guru Nanak Dev Ji.",
        "preheading": "📅 Nov 15 — Guru Nanak Jayanti",
        "website_url": "@dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_world_aids_day_data():
    """Get sample data for the World AIDS Day template."""
    return {
        "background_image_url": "https://iili.io/fFe91jV.png",
        "title": "Support. Awareness. Hope.",
        "subtitle": "Standing together in the fight against HIV/AIDS.",
        "preheading": "📅 Dec 1 — World AIDS Day",
        "website_url": "@dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_international_day_persons_disabilities_data():
    """Get sample data for the International Day of Persons with Disabilities template."""
    return {
        "background_image_url": "https://iili.io/fFeuAMX.png",
        "title": "Inclusion strengthens communities.",
        "subtitle": "Promoting accessibility, empowerment & equality.",
        "preheading": "📅 Dec 3 — International Day of Persons with Disabilities",
        "website_url": "@dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_new_year_eve_data():
    """Get sample data for the New Year's Eve template."""
    return {
        "background_image_url": "https://iili.io/fFehiNI.png",
        "title": "Wrapping up the year with gratitude.",
        "subtitle": "Cheers to new beginnings and brighter days.",
        "preheading": "📅 Dec 31 — New Year's Eve",
        "website_url": "@dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_national_youth_day_data():
    """Get sample data for the National Youth Day template."""
    return {
        "background_image_url": "https://iili.io/fFkT3Sj.png",
        "title": "Celebrating the energy that transforms tomorrow.",
        "subtitle": "Honouring the vision and ideals of Swami Vivekananda.",
        "preheading": "📅 Jan 12 — National Youth Day",
        "website_url": "@dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_makar_sankranti_data():
    """Get sample data for the Makar Sankranti template."""
    return {
        "background_image_url": "https://iili.io/fFk789s.png",
        "title": "Let the sky fill with colours of celebration.",
        "subtitle": "Wishing you a joyful and vibrant Makar Sankranti.",
        "preheading": "📅 Jan 14 — Makar Sankranti",
        "website_url": "@dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_pongal_data():
    """Get sample data for the Pongal template."""
    return {
        "background_image_url": "https://iili.io/fFkEoWG.png",
        "title": "A harvest of gratitude and abundance.",
        "subtitle": "Warm wishes for a joyful Pongal.",
        "preheading": "📅 Jan 15 — Pongal",
        "website_url": "@dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_lohri_data():
    """Get sample data for the Lohri template."""
    return {
        "background_image_url": "https://iili.io/fFkXqoF.png",
        "title": "May the flame of Lohri bring warmth and prosperity.",
        "subtitle": "Celebrating the joy of new beginnings.",
        "preheading": "📅 Jan 13 — Lohri",
        "website_url": "@dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_bihu_data():
    """Get sample data for the Bihu template."""
    return {
        "background_image_url": "https://iili.io/fFkbS7j.png",
        "title": "Celebrating culture, rhythm and harvest.",
        "subtitle": "Wishing you a festive and joyful Bihu.",
        "preheading": "📅 Jan 14 — Bihu",
        "website_url": "@dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_republic_day_data():
    """Get sample data for the Republic Day template."""
    return {
        "background_image_url": "https://iili.io/fFUC4WP.png",
        "title": "Celebrating unity, progress and pride.",
        "subtitle": "Wishing you a proud and patriotic Republic Day.",
        "preheading": "📅 Jan 26 — Republic Day (India)",
        "website_url": "@dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_world_cancer_day_data():
    """Get sample data for the World Cancer Day template."""
    return {
        "background_image_url": "https://iili.io/fFgrqx9.png",
        "title": "Together, we can inspire hope.",
        "subtitle": "Supporting awareness, care and early detection.",
        "preheading": "📅 Feb 4 — World Cancer Day",
        "website_url": "@dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_new_year_data():
    """Get sample data for the New Year template."""
    return {
        "background_image_url": "https://iili.io/fFrHgFR.png",
        "title": "Hello 2026 — Let's begin again.",
        "subtitle": "A fresh year filled with opportunities and growth.",
        "website_url": "@dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_valentines_day_data():
    """Get sample data for the Valentine's Day template."""
    return {
        "background_image_url": "https://iili.io/fFrYRXn.png",
        "title": "Love adds colour to every moment.",
        "subtitle": "Celebrate affection in every form.",
        "preheading": "📅 Feb 14 — Valentine's Day",
        "website_url": "@dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_product_launch_data():
    """Get sample data for the Product Launch template."""
    return {
        "background_color": "#6941C7",
        "title": "PRODUCT<br>LAUNCH",
        "subtitle": "Check out our website to see what else we have.",
        "image_url": "https://iili.io/fFrZCdX.png",
        "website_url": "www.dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_flash_sale_simple_data():
    """Get sample data for the Flash Sale Simple template."""
    return {
        "primary_color": "#a83232",
        "secondary_color": "#ffffff",
        "title": "FLASH<br>SALE",
        "subtitle": "Get the best deal on stationary products!",
        "discount_text": "Upto 60% OFF!",
        "image_url": "https://iili.io/fF6q12e.png",
        "website_url": "www.dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_clearance_sale_data():
    """Get sample data for the Clearance Sale template."""
    return {
        "primary_color": "#6941C7",
        "secondary_color": "#ffffff",
        "title": "CLEARANCE<br>SALE!",
        "subtitle": "Get the best deal on winter clothes!",
        "discount_text": "Upto 60% OFF!",
        "image_url": "https://www.plasticsoupfoundation.org/Nieuws/Untitled-design-3.png",
        "website_url": "www.dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_preorder_data():
    """Get sample data for the Preorder template."""
    return {
        "primary_color": "#0e1a3a",
        "secondary_color": "#ffffff",
        "website_url": "@dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "subtitle": "NEW PRODUCT COMING THIS MONTH",
        "image_url": "https://iili.io/fFrZCdX.png",
        "cta_text": "PRE-ORDER NOW",
        "custom_css": "",
        "custom_html": ""
    }

def get_myth_or_truth_data():
    """Get sample data for the Myth or Truth template."""
    return {
        "primary_color": "#ece9df",
        "secondary_color": "#6941C7",
        "text_color": "#2b2b2b",
        "website_url": "www.dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_light_bg.svg",
        "heading": "Myth or Truth?<br>Let's Fact Check!",
        "myth_title": "MYTH",
        "myth_desc": "Going green is too expensive<br>and inaccessible.",
        "truth_title": "TRUTH",
        "truth_desc": "Many sustainable practices, like<br>reducing energy use or eating<br>less meat, can save money in<br>the long run.",
        "custom_css": "",
        "custom_html": ""
    }

def get_download_template_data():
    """Get sample data for the Download Template."""
    return {
        "background_image_url": "https://t3.ftcdn.net/jpg/16/81/25/58/360_F_1681255802_3JLKAyEmo93FKXX3rEoIGJ4cHzQkRRFU.jpg",
        "website_url": "@dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "title": "Download",
        "title_span": "Free Guide",
        "subtitle": "Organize your workspace with ease.",
        "cta_text": "www.dolze.ai",
        "bottom_image_url": "https://iili.io/fKd8Was.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_early_bird_offer_data():
    """Get sample data for the Early Bird Offer template."""
    return {
        "primary_color": "#a83232",
        "secondary_color": "#ffffff",
        "title": "EARLY<br>BIRD<br>OFFER!",
        "subtitle": "Get exclusive access before everyone else!",
        "offer_text": "Save 40% OFF!",
        "image_url": "https://iili.io/fF6q12e.png",
        "website_url": "www.dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_buy_one_get_one_data():
    """Get sample data for the Buy One Get One template."""
    return {
        "primary_color": "#ebb734",
        "secondary_color": "#ffffff",
        "title": "BUY ONE<br>GET ONE",
        "subtitle": "Buy any one item and get one FREE",
        "offer_text": "BUY ONE GET ONE",
        "image_url": "https://www.plasticsoupfoundation.org/Nieuws/Untitled-design-3.png",
        "website_url": "www.dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_referral_program_data():
    """Get sample data for the Referral Program template."""
    return {
        "primary_color": "#D2911A",
        "secondary_color": "#ffffff",
        "title": "REFER A FRIEND<br>& GET $50",
        "subtitle": "Refer your friends and family to earn $50",
        "referral_text": "Referral Program",
        "image_url": "https://iili.io/fK2ujGn.png",
        "website_url": "www.dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_challenge_data():
    """Get sample data for the Challenge template."""
    return {
        "primary_color": "#6941C7",
        "title": "JOIN THE<br>30 DAY CHALLENGE!",
        "subtitle": "Are you ready to push yourself?",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTqEyFHvuFMAc-knprFmaQcUBLgB4bTxJwL9Q&s",
        "tag1": "Weekly progress",
        "tag2": "Guided workout plan",
        "tag3": "Before vs after tracking",
        "website_url": "www.dolze.ai",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "custom_css": "",
        "custom_html": ""
    }

def get_3_tips_data():
    """Get sample data for the 3 tips template."""
    return {
        "background_color": "#f6f3f1",
        "canvas_background_color": "#ffffff",
        "hero_text_color": "#111111",
        "title_line1": "3 simple ways to",
        "title_line2": "grow your email list",
        "tip1_title": "Create a Freebie",
        "tip1_body": "Create a free download for your audience which they'll receive when subscribing to your list.",
        "tip2_title": "Start a Blog",
        "tip2_body": "Create lots of high quality, free content to share with your audience to grow your reach.",
        "tip3_title": "Collaborate",
        "tip3_body": "Get in front of new people by collaborating with online businesses in other niches.",
        "footer_handle": "@REALLYGREATSITE",
        "footer_text_color": "#6f655f",
        "accent_color": "#d6a9a9",
        "tip_border_color": "#eaded6",
        "tip_card1_background": "#fdf7f5",
        "tip_card2_background": "#ffffff",
        "tip_card3_background": "#faf1ee",
        "tip_body_color": "#514f4e",
        "hero_image_url": "https://images.unsplash.com/photo-1485965120184-e220f721d03e?auto=format&fit=crop&w=1200&q=80",
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_light_bg.svg",
        "website_url": "www.reallygreatsite.com",
        "custom_css": "",
        "custom_html": ""
    }

def get_email_template_data():
    """Get sample data for the email template."""
    return {
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "primary_color": "#4F46E5",
        "heading": "Welcome to Our Newsletter",
        "body_text": "Thank you for subscribing! We're excited to share the latest updates, tips, and exclusive offers with you. Stay tuned for amazing content delivered straight to your inbox.",
        "cta_text": "Explore Now",
        "cta_url": "https://www.dolze.ai",
        "footer_text": "You're receiving this email because you subscribed to our newsletter. If you have any questions, feel free to reach out to us.",
        "company_name": "Dolze AI",
        "unsubscribe_url": "https://www.dolze.ai/unsubscribe",
        "custom_css": "",
        "custom_html": ""
    }

def get_welcome_email_data():
    """Get sample data for the welcome email template."""
    return {
        "logo_url": "https://dolze-docs-uat.s3.ap-south-1.amazonaws.com/post_templates/dolze_dark_bg.png",
        "company_name": "FinBank",
        "hero_image_url": "https://iili.io/example-hero.png",
        "feature_1_title": "Instant payments",
        "feature_1_description": "anytime, anywhere.",
        "feature_2_title": "Smart budgeting",
        "feature_2_description": "with real-time insights.",
        "feature_3_title": "Bank-level security",
        "feature_3_description": "built in.",
        "main_heading": "Your account is ready",
        "body_text": "Enjoy instant access, smarter insights, and the confidence of bank-level security – anytime, anywhere.",
        "cta_text": "Login",
        "cta_url": "https://www.example.com/login",
        "help_heading": "Need help?",
        "help_text": "Call us at 1-800-123-4567,\nstart a live chat in the app,\nor visit our Help Center anytime.",
        "phone_number": "1-800-123-4567",
        "phone_link": "tel:18001234567",
        "address": "123 Anywhere St., Any City, ST 12345",
        "unsubscribe_url": "https://www.example.com/unsubscribe",
        "primary_color": "#00c4cc",
        "custom_css": "",
        "custom_html": ""
    }

def get_product_intro_data():
    """Get sample data for the product intro email template."""
    return {
        "hero_image_url": "https://iili.io/fFrZCdX.png",
        "learn_more_text": "Learn more",
        "download_app_text": "Download app",
        "download_app_url": "https://www.example.com/download",
        "price_text": "$9.95/month",
        "feature_1_title": "Lightning-fast transfers",
        "feature_1_description": "Send money instantly with ultra-fast processing.",
        "feature_2_title": "One-tap account switching",
        "feature_2_description": "Switch smoothly between accounts.",
        "feature_3_title": "Stunning insights dashboard",
        "feature_3_description": "See your spending\nin vibrant dashboards.",
        "contact_button_text": "Contact us",
        "contact_button_url": "https://www.example.com/contact",
        "footer_link_1_text": "Shop online",
        "footer_link_1_url": "https://www.example.com/shop",
        "footer_link_2_text": "Find a store",
        "footer_link_2_url": "https://www.example.com/stores",
        "footer_link_3_text": "Download app",
        "footer_link_3_url": "https://www.example.com/download",
        "social_icon_1_url": "https://iili.io/fn1yu19.png",
        "social_icon_1_link": "https://www.facebook.com/example",
        "social_icon_2_url": "https://iili.io/fnEHaVV.png",
        "social_icon_2_link": "https://www.twitter.com/example",
        "social_icon_3_url": "https://iili.io/fnEJq5g.png",
        "social_icon_3_link": "https://www.instagram.com/example",
        "social_icon_4_url": "https://iili.io/fnEduZx.png",
        "social_icon_4_link": "https://www.linkedin.com/example",
        "company_name": "agileTech",
        "email": "hello@reallygreatsite.com",
        "website_url": "www.reallygreatsite.com",
        "phone": "123-456-7890",
        "address": "123 Anywhere St., Any City, ST 12345",
        "unsubscribe_url": "https://www.example.com/unsubscribe",
        "primary_color": "#3d6ee0",
        "gradient_start_color": "#3d6ee0",
        "gradient_end_color": "#c59dff",
        "background_color": "#000d25",
        "custom_css": "",
        "custom_html": ""
    }


def get_newsletter_data():
    """Get sample data for the newsletter template."""
    return {
        "company_name": "GLOBAL SOLUTIONS",
        "nav_link_1": "Updates",
        "nav_link_2": "News",
        "nav_link_3": "Events",
        "hero_image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYoVvVRAwgKPcd6s_2wVpfn92JSymqmbPtOQ&s",
        "leadership_image_url": "https://img.freepik.com/free-photo/designer-working-3d-model_23-2149371896.jpg?semt=ais_hybrid&w=740&q=80",
        "leadership_title": "Unlocking Success",
        "leadership_author": "by Duke Waldron",
        "leadership_description": "Leadership insights description text here...",
        "employee_image_url": "https://img.freepik.com/free-photo/designer-working-3d-model_23-2149371896.jpg?semt=ais_hybrid&w=740&q=80",
        "employee_quote": "\"The designs I create serve as powerful ambassadors for the company.\"",
        "employee_name": "Meet Jordan Ellis",
        "employee_description": "In just 18 months, Jordan has reshaped our marketing campaigns and mentored new interns with creativity and passion.",
        "employee_motto": "\"It's about creating experiences, not just messages.\"",
        "project_1_image_url": "images/16d851bc1b23f9bc239a1c68597ee56c.png",
        "project_1_title": "Customer Engage",
        "project_1_description": "The Customer Engage project was launched in response to market trends and customer feedback. The primary goal was to increase engagement and boost sales over the next quarter through a multi-channel approach to promote the latest product line. The efforts of the team resulted in a 20% increase in engagement.",
        "project_2_image_url": "images/b0fdca469c59873738c1457f3ca2aa64.png",
        "project_2_title": "Project Horizon",
        "project_2_description": "Project Horizon aims to modernize our internal tools for faster collaboration. Led by Sarah Kim and David Ortiz, the team is rolling out a new dashboard that simplifies reporting and cuts admin time by 30%. Early feedback has been overwhelmingly positive.",
        "event_1_icon_url": "images/21ede316019b61ae7820c341c4472652.gif",
        "event_1_title": "Networking November",
        "event_1_date": "All Wednesdays of November",
        "event_1_time": "9:00 AM to 3:00 PM",
        "event_1_location": "Level 1, 123 Anywhere St.",
        "event_2_icon_url": "images/30add955cdb7bcacfc329466ddbead27.gif",
        "event_2_title": "Startup Pitch Night",
        "event_2_date": "Thursday, November 16",
        "event_2_time": "6:00 PM – 9:00 PM",
        "event_2_location": "Innovation Hub Auditorium",
        "event_3_icon_url": "images/eb8438d3c875e0e4c575515e7a23808b.gif",
        "event_3_title": "Tech Skills Workshop",
        "event_3_date": "Monday, November 27",
        "event_3_time": "1:00 PM – 4:00 PM",
        "event_3_location": "Room 204, Learning Center",
        "contact_email": "hello@reallygreatsite.com",
        "custom_css": "",
        "custom_html": ""
    }


def get_reactivation_offer_data():
    """Get sample data for the reactivation offer template."""
    return {
        "company_name": "The Daily Beacon",
        "contact_email": "hello@reallygreatsite.com",
        "hero_image_url": "https://www.shutterstock.com/image-photo/stack-books-against-background-library-600nw-2459213053.jpg",
        "recipient_name": "Pete",
        "greeting_message": "We noticed you haven't been with us for a while, and we miss having you in the conversation.",
        "offer_text": "For a limited time, resubscribe and get",
        "discount_percent": "50% off your first 3 months",
        "exclusive_early_access_text": "plus exclusive early access to our upcoming investigative series.",
        "plan_1_name": "Digital Access",
        "plan_1_price": "$5/month",
        "plan_1_period": "(first 3 months)",
        "plan_1_feature_1": "Unlimited articles & episodes",
        "plan_1_feature_2": "Access to archives",
        "plan_1_feature_3": "Early subscriber-only newsletters",
        "plan_2_image_url": "https://www.shutterstock.com/image-photo/stack-books-against-background-library-600nw-2459213053.jpg",
        "plan_2_name": "Print + Digital",
        "plan_2_price": "$12/month",
        "plan_2_period": "(first 3 months)",
        "plan_2_feature_1": "Home delivery of the weekend edition",
        "plan_2_feature_2": "Unlimited digital access",
        "plan_2_feature_3": "Exclusive behind-the-scenes podcast",
        "plan_3_name": "Full Access",
        "plan_3_price": "$20/month",
        "plan_3_period": "(first 3 months)",
        "plan_3_feature_1": "Print + digital + premium podcast",
        "plan_3_feature_2": "Invites to subscriber-only live Q&A events",
        "plan_3_feature_3": "Recognition as a supporting member",
        "plan_3_image_url": "https://www.shutterstock.com/image-photo/stack-books-against-background-library-600nw-2459213053.jpg",
        "cta_text": "Resubscribe today",
        "cta_url": "#",
        "welcome_back_text": "We'd love to have you back",
        "supporting_message_text": "Because journalism worth reading is journalism worth supporting.",
        "address": "123 Anywhere St., Any City, ST 12345",
        "footer_text": "©️ 2025 Email Design Insights. All rights reserved. You're receiving this email because you signed up for updates from The Daily Beacon",
        "custom_css": "",
        "custom_html": ""
    }


def get_ecommerce_data():
    """Get sample data for the ecommerce template."""
    return {
        "hero_image_url": "https://iili.io/fFrZCdX.png",
        "nav_category_1": "TOPS",
        "nav_category_2": "BOTTOMS",
        "nav_category_3": "FOOTWEAR",
        "nav_category_4": "ACCESSORIES",
        "main_heading_text": "Timeless pieces, up to",
        "discount_percent": "25% off",
        "description_text": "From everyday casuals to versatile accessories, enjoy our handpicked curation at a special discount.",
        "discount_code": "25OFF",
        "offer_expiry": "February 28, 2030",
        "product_1_image_url": "https://iili.io/fFrZCdX.png",
        "product_1_name": "Oversized blazer",
        "product_1_price": "$28.00",
        "product_1_url": "#",
        "product_2_image_url": "https://iili.io/fFrZCdX.png",
        "product_2_name": "Classic shoulder bag",
        "product_2_price": "$15.00",
        "product_2_url": "#",
        "product_3_image_url": "https://iili.io/fFrZCdX.png",
        "product_3_name": "Linen set",
        "product_3_price": "$22.00",
        "product_3_url": "#",
        "product_4_image_url": "https://iili.io/fFrZCdX.png",
        "product_4_name": "Ballerina flats",
        "product_4_price": "$30.00",
        "product_4_url": "#",
        "company_name": "Wardrobe Wear Inc.",
        "company_address": "Suite 123, 123 Anywhere St., Any City, ST 12345",
        "contact_url": "#",
        "preferences_url": "#",
        "unsubscribe_url": "#",
        "copyright_year": "2025",
        "copyright_company": "Company Inc",
        "social_icon_1_url": "https://iili.io/fn1yu19.png",
        "social_icon_1_link": "https://www.facebook.com/example",
        "social_icon_2_url": "https://iili.io/fnEHaVV.png",
        "social_icon_2_link": "https://www.twitter.com/example",
        "social_icon_3_url": "https://iili.io/fnEJq5g.png",
        "social_icon_3_link": "https://www.instagram.com/example",
        "social_icon_4_url": "https://iili.io/fnEduZx.png",
        "social_icon_4_link": "https://www.linkedin.com/example",
        "custom_css": "",
        "custom_html": ""
    }


def get_ecommerce_and_retail_email_data():
    """Get sample data for the ecommerce and retail email template."""
    return {
        "company_name": "Stone & Thread Rugs",
        "hero_image_url": "https://iili.io/fFrZCdX.png",
        "recipient_name": "Pat",
        "main_message_text": "You asked, we listened. Our most-loved rugs are finally back in stock. These designs tend to sell out fast, so now's your chance to bring one home.",
        "product_1_image_url": "images/f1652e5dcce0c54f17425b66dbaf711f.png",
        "product_1_name": "The Haven Jute Rug",
        "product_1_description": "Natural texture, timeless appeal. Perfect for grounding any space with laid-back charm.",
        "product_1_url": "#",
        "product_2_image_url": "https://iili.io/fFrZCdX.png",
        "product_2_name": "The Geometric Rug",
        "product_2_description": "Bold lines and modern design. A statement piece that makes every room pop.",
        "product_2_url": "#",
        "product_3_image_url": "https://iili.io/fFrZCdX.png",
        "product_3_name": "The Willow Moroccan Rug",
        "product_3_description": "Soft underfoot, rich in pattern. Crafted to bring warmth and global flair to your home.",
        "product_3_url": "#",
        "product_4_image_url": "https://iili.io/fFrZCdX.png",
        "product_4_name": "The Ember Vintage Rug",
        "product_4_description": "Faded elegance meets everyday durability. The lived-in look you'll love for years.",
        "product_4_url": "#",
        "tagline_text": "Ethics underfoot.",
        "tagline_description": "Our rugs are sustainably crafted and ethically made, bringing beauty to your space and fairness to the artisans who create them.",
        "nav_link_1": "SHOP ALL",
        "nav_link_2": "WHAT'S NEW",
        "nav_link_3": "SALE",
        "unsubscribe_url": "#",
        "custom_css": "",
        "custom_html": ""
    }


async def main():
    """Main async function to render all templates."""
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Define the templates to render
        templates = [
            # {"name": "product_promo_1", "data": get_product_promo_1_data()},
            # {"name": "product_promo_3", "data": get_product_promo_3_data()},
            # {"name": "free_resource", "data": get_free_resource_data()},
            # {"name": "app_promo_2", "data": get_app_promo_2_data()},
            # {"name": "partnership_announcement", "data": get_announcement_template_data()},
            # {"name": "social_media_tips", "data": get_social_media_tips_template_data()},
            # {"name": "testimonial_card", "data": get_testimonial_card_3_data()},
            # {"name": "contact_us", "data": get_contact_us_overlay_data()},
            # {"name": "job_search_promotion", "data": get_perfect_job_search_data()},
            # {"name": "hiring_announcement", "data": get_hiring_minimal_red_data()},
            # {"name": "strategy_cards", "data": get_customer_retention_strategies_data()},
            # {"name": "financial_education", "data": get_stocks_dividend_post_2_data()},
            # {"name": "services_showcase", "data": get_search_services_listing_data()},
            # {"name": "product_promotion", "data": get_food_offer_promo_data()},
            # {"name": "product_promotion_v2", "data": get_product_promotion_v2_data()},
            # {"name": "launch_announcement", "data": get_spotlight_launching_text_3_data()},
            # {"name": "job_opening", "data": get_hiring_post_data()},
            # {"name": "myth_vs_fact", "data": get_myth_or_fact_data()},
            # {"name": "service_promotion", "data": get_social_media_data()},
            # {"name":"annual_report", "data": get_business_highlights_2035_html_data()},
            # {"name": "why_us_reasons", "data": get_why_us_reasons_data()},
            # {"name": "faq_template", "data": get_faq_template_data()},
            # {"name": "smart_investment", "data": get_smart_investment_data()},
            # {"name": "pricing_plans", "data": get_pricing_plans_data()},
            {"name": "we_are_hiring", "data": get_we_are_hiring_data()},
            # {"name": "flash_sale", "data": get_flash_sale_data()},
            # {"name": "creative_marketing_agency", "data": get_creative_marketing_agency_data()},
            # {"name": "quiz_2", "data": get_quiz_2_data()},
            # {"name": "quiz_3", "data": get_quiz_3_data()},
            # {"name": "black_friday_offer_1", "data": get_black_friday_offer_1_data()},
            # {"name": "question_1", "data": get_question_1_data()},
            # {"name": "text_block_1", "data": get_text_block_1_data()},
            # {"name": "plan_post_1", "data": get_plan_post_1_data()},
            # {"name": "indian_constitution_day", "data": get_indian_constitution_day_data()},
            # {"name": "guru_nanak_jayanti", "data": get_guru_nanak_jayanti_data()},
            # {"name": "world_aids_day", "data": get_world_aids_day_data()},
            # {"name": "international_day_persons_disabilities", "data": get_international_day_persons_disabilities_data()},
            # {"name": "new_year_eve", "data": get_new_year_eve_data()},
            # {"name": "national_youth_day", "data": get_national_youth_day_data()},
            # {"name": "makar_sankranti", "data": get_makar_sankranti_data()},
            # {"name": "pongal", "data": get_pongal_data()},
            # {"name": "lohri", "data": get_lohri_data()},
            # {"name": "bihu", "data": get_bihu_data()},
            # {"name": "republic_day", "data": get_republic_day_data()},
            # {"name": "world_cancer_day", "data": get_world_cancer_day_data()},
            # {"name": "new_year", "data": get_new_year_data()},
            # {"name": "valentines_day", "data": get_valentines_day_data()},
            # {"name": "product_launch", "data": get_product_launch_data()},
            # {"name": "flash_sale_simple", "data": get_flash_sale_simple_data()},
            # {"name": "clearance_sale", "data": get_clearance_sale_data()},
            # {"name": "preorder", "data": get_preorder_data()},
            # {"name": "myth_or_truth", "data": get_myth_or_truth_data()},
            # {"name": "download_template", "data": get_download_template_data()},
            # {"name": "early_bird_offer", "data": get_early_bird_offer_data()},
            # {"name": "buy_one_get_one", "data": get_buy_one_get_one_data()},
            # {"name": "referral_program", "data": get_referral_program_data()},
            # {"name": "challenge", "data": get_challenge_data()},
            # {"name": "3_tips", "data": get_3_tips_data()},
            # {"name": "email_template", "data": get_email_template_data()},
            # {"name": "welcome_email", "data": get_welcome_email_data()},
            # {"name": "product_intro", "data": get_product_intro_data()},
            # {"name": "newsletter", "data": get_newsletter_data()},
            # {"name": "reactivation_offer", "data": get_reactivation_offer_data()},
            {"name": "ecommerce", "data": get_ecommerce_data()},
            # {"name": "ecommerce_and_retail_email", "data": get_ecommerce_and_retail_email_data()},
        ]

        # {"name": "coming_soon_post_2", "data": get_coming_soon_post_2_data()},
        # Render each template
        for template in templates:
            await render_template(template["name"], template["data"])

        print("\nAll templates generated successfully!")
    except Exception as e:
        print(f"\nError generating templates: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
