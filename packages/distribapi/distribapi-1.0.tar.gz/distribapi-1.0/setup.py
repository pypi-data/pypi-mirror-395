from setuptools import setup, find_packages

setup(
    name="distribapi",
    version="1.0",
    author="QKing",
    author_email="qking@qking.me",
    description="Intelligent API request distribution based on system resources and latency",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/QKing-Official/distribapi",
    packages=find_packages(),
    python_requires=">=3.8",

    install_requires=[
        "aiohttp>=3.8.0",
        "psutil>=5.9.0",
    ],

    extras_require={
        "gpu": ["gputil>=1.4.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
