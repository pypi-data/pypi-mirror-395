from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="swagflask",
    version="0.1.0",
    author="Rithwik",
    author_email="rithwik@example.com",
    description="Swagger UI for Flask - Automatically configure Swagger UI for Flask applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rithwiksb/swagflask",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Flask",
    ],
    python_requires=">=3.7",
    install_requires=[
        "Flask>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-flask>=1.2.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
)
