from setuptools import setup, find_packages

# Leer el archivo README si existe
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Librería de estadística descriptiva e inferencial para Python"

setup(
    name="statslibx",
    version="0.1.6",
    author="Emmanuel Ascendra Perez",
    author_email="ascendraemmanuel@gmail.com",
    description="Librería de estadística descriptiva e inferencial para Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Immanuel3008/StatsLibX",  # Opcional
    packages=find_packages(),  # Encuentra automáticamente todos los paquetes
    include_package_data=True,
    package_data={
        "statslibx": ["datasets/*.csv"]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
    ],
    extras_require={
        "viz": ["seaborn>=0.11.0", "plotly>=5.0.0"],
        "advanced": ["scikit-learn>=1.0.0", "statsmodels>=0.13.0"],
        "all": [
            "seaborn>=0.11.0",
            "plotly>=5.0.0",
            "scikit-learn>=1.0.0",
            "statsmodels>=0.13.0",
        ],
    },
)