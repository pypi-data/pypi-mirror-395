"""
Setup script for fm-prime Python package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="fm-prime",
    version="1.0.9",
    author="Farid Masjedi",
    author_email="farid.masjedi1985@gmail.com",
    description="Comprehensive prime number utilities with multiple algorithms including the novel Hyperbolic Equation Method with intelligent caching",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/faridmasjedi/fm-prime",
    project_urls={
        "Bug Tracker": "https://github.com/faridmasjedi/fm-prime/issues",
        "Documentation": "https://github.com/faridmasjedi/fm-prime#readme",
        "Source Code": "https://github.com/faridmasjedi/fm-prime",
    },
    packages=["fm_prime"],
    package_dir={"fm_prime": "fm_prime"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    keywords=[
        "prime",
        "prime-numbers",
        "primes",
        "primality-test",
        "sieve",
        "eratosthenes",
        "miller-rabin",
        "wheel-factorization",
        "hyperbolic",
        "number-theory",
        "mathematics",
        "6k±1",
        "wheel-210",
        "cryptography",
        "algorithm",
    ],
    entry_points={
        "console_scripts": [
            "fm-prime=findPrimes:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
