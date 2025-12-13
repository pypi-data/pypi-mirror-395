from setuptools import setup, find_packages

setup(
    name="nidataset",
    version="0.2.3",
    description="NIfTI dataset management package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Giulio Russo, Ciro Russo",
    author_email="russogiulio1998@icloud.com, ciro.russo2910@gmail.com",
    url="https://github.com/GiulioRusso/Ni-Dataset",
    packages=find_packages(),
    license="MIT License",
    install_requires=[
        "Pillow>=9.4.0",
        "nibabel>=5.1.0",
        "numpy>=1.24.2",
        "torch>=2.2.2",
        "scikit-image>=0.19.3",
        "pandas>=1.5.3",
        "SimpleITK>=2.2.1",
        "scipy>=1.10.0",
        "tqdm>=4.67.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8.0",
)