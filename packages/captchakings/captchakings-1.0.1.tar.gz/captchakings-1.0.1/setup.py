"""
CaptchaKings Python Library Setup
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="captchakings",
    version="1.0.1",
    author="CaptchaKings",
    author_email="support@captchakings.com",
    description="Official Python client for CaptchaKings API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://captchakings.com",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
    keywords="captcha, ocr, captcha-solver, captchakings, api-client",
    project_urls={
        "Documentation": "https://captchakings.com?section=documentation",
        "Source": "https://captchakings.com",
        "Bug Reports": "https://captchakings.com",
    },
)
