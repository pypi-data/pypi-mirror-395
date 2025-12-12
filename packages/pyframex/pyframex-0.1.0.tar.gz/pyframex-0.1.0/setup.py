from setuptools import setup, find_packages

setup(
    name="pyframex",
    version="0.1.0",
    author="Idriss Bado",
    author_email="idrissbadoolivier@gmail.com",
    description="Next-generation native DataFrame for Python - Simple like Excel, Powerful like SQL, Smart like AI",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/idrissbado/PyFrameX",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "ml": ["scikit-learn>=1.0.0"],
        "all": ["scikit-learn>=1.0.0"],
    },
    entry_points={
        "console_scripts": [
            "pyframex=pyframex.__main__:main",
        ],
    },
    keywords="dataframe data analysis sql machine-learning excel pandas-alternative",
    project_urls={
        "Bug Tracker": "https://github.com/idrissbado/PyFrameX/issues",
        "Documentation": "https://github.com/idrissbado/PyFrameX#readme",
        "Source Code": "https://github.com/idrissbado/PyFrameX",
    },
)
