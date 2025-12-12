from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dolze-image-templates",
    version="1.1.8",
    author="Dolze Team",
    author_email="support@dolze.com",
    description="A package for generating Dolze templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dolze-templates",
    packages=find_packages(),
    package_data={
        "dolze_image_templates": ["templates/*", "fonts/*", "available_templates/*", "html_templates/*", "email_templates/*", "sms_templates/*"],
    },
    install_requires=[
        "Pillow>=9.0.0",
        "requests>=2.25.0",
        "selenium>=4.1.0",
        "webdriver-manager>=3.5.2",
        "playwright>=1.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
