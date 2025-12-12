from setuptools import setup, find_packages

setup(
    name="suggestify",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "sentence-transformers>=2.2.2",  # for embeddings
        "torch>=2.0.0",                 # required by sentence-transformers
        "pandas>=2.0.0",                # for handling CSV/DB queries
        "rapidfuzz>=3.14.3",            # for fuzzy matching
        "SQLAlchemy>=2.0.0",            
        "wikipedia-api>=0.5.8",         
        "spacy>=3.6.0"                  # for NLP processing (noun extraction, etc.)
    ],
    author="MD Jubayer Khan",
    description="Domain-agnostic semantic query suggestion engine",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MD-Jubayer-Khan/suggestify",
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="query suggestion NLP semantic search fuzzy search AI",
    project_urls={
    "Documentation": "https://github.com/MD-Jubayer-Khan/suggestify#readme",
    "Source": "https://github.com/MD-Jubayer-Khan/suggestify",
    "Bug Tracker": "https://github.com/MD-Jubayer-Khan/suggestify/issues",
    },

)
