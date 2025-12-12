from setuptools import setup, find_packages

setup(
    name="model_monitoring",
    version="2.1.0",
    description="Package for Model Monitoring",
    author="DAT Team",
    url="https://dev.azure.com/credem-data/DAT/_git/model_monitoring",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=find_packages(where="src"),
    package_data={
        "model_monitoring": ["config/*.yml"],
    },
    include_package_data=True,
    package_dir={"": "src"},
    # Updated for Python 3.12
    python_requires=">=3.12",
    install_requires=[
        "numpy>=1.26.0",
        "pandas>=2.1.0",
        "scikit-learn>=1.3.0",
        "lightgbm>=4.0.0",
        "scipy>=1.11.0",
        "PyYAML>=6.0.1",
        "shap>=0.44.0",
        "ipython",
        "numba>=0.59.0",
    ],
)
