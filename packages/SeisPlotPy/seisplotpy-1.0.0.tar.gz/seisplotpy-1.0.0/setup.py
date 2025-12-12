from setuptools import setup, find_packages

setup(
    name="SeisPlotPy",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["main"],
    include_package_data=True,
    install_requires=[
        "PyQt6>=6.4.0",
        "pyqtgraph>=0.13.0",
        "segyio>=1.9.0",
        "numpy>=1.21.0",
        "matplotlib>=3.5.0",
        "pandas>=1.3.0",
        "scipy>=1.10.0"
    ],
    entry_points={
        "console_scripts": [
            "seisplotpy=main:main" 
        ]
    },
    author="Arjun V H",
    author_email="arjunvelliyidathu@gmail.com",
    description="A high-performance 2D post-stack Interpretation & QC Workstation.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/arjun-vh/SeisPlotPy",
    keywords="seismic, segy, geophysics, visualization",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics"
    ],
    python_requires=">=3.8",

)
