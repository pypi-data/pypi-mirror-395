from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="alphabit",
    version="0.1.0",
    author="Moneshwaran K.M",
    author_email="mone9732@gmail.com",
    description="Hardware-accelerated symbolic stream processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/monemax/alphabit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Hardware",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0",
        "regex>=2021.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-benchmark",
            "black",
            "flake8",
        ],
    },
)
