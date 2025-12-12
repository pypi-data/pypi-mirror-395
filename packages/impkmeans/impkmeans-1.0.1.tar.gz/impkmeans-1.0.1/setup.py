from setuptools import setup, find_packages

setup(
    name="impkmeans",
    version="1.0.1",
    author="Ali Şenol",
    author_email="alisenol@tarsus.edu.tr",  # <- replace with your email
    description="ImpKMeans: Improved K-Means initialization using KDE + KD-Tree (based on Senol, 2025)",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/senolali/ImpKMeans",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scikit-learn",
    ],
    python_requires=">=3.8",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
)
