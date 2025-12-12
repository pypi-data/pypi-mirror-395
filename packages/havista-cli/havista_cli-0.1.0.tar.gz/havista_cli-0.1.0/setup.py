from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="havista-cli",
    version="0.1.0",
    author="Paitite",
    author_email="contact@havista.fr",
    description="CLI minimale pour Havista, widget de home staging virtuel par IA (édité par Paitite).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://havista.fr",
    project_urls={
        "Site Havista": "https://havista.fr",
        "Widget IA immobilier": "https://havista.fr/widget",
        "Éditeur Paitite": "https://paitite.com",
    },
    packages=find_packages(),
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "havista=havista.__init__:info",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
