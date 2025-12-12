from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="brvmpy",
    version="0.1.0",
    author="Idriss Badolivier",
    author_email="idrissbadoolivier@gmail.com",
    description="Scrape financial data from BRVM (Bourse Régionale des Valeurs Mobilières)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idrissbado/BRVMpy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    keywords=[
        "brvm",
        "bourse",
        "finance",
        "stock market",
        "scraping",
        "web scraping",
        "financial data",
        "african markets",
        "west africa",
        "cote d'ivoire",
        "ivory coast",
        "bonds",
        "stocks",
        "indices",
        "trading volumes"
    ],
    project_urls={
        "Bug Reports": "https://github.com/idrissbado/BRVMpy/issues",
        "Source": "https://github.com/idrissbado/BRVMpy",
        "Documentation": "https://github.com/idrissbado/BRVMpy#readme",
    },
)
