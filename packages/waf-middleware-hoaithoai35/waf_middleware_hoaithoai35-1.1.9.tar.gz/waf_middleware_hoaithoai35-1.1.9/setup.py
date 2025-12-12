import os
from setuptools import setup, find_packages

setup(
    name="waf_middleware_hoaithoai35",
    version="1.1.9", # Tăng version lên 1.1.9 cho may mắn
    author="Nguyen Hoai Thoai",
    author_email="hoaithoai35@gmail.com",
    description="A powerful WAF Middleware for Flask with SQLi, XSS, and Logic protection",
    long_description=open("README.md", encoding="utf-8").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/HoaiThoai/waf-middleware",
    packages=find_packages(),
    
    package_data={'waf_middleware': ['*.json', '*.txt']},
    include_package_data=True,
    # --------------------------------
    
    install_requires=[
        "Flask>=2.0.0",
        "requests>=2.25.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)