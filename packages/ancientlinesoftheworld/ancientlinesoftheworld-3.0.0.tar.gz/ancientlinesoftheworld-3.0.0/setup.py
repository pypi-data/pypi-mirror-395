from setuptools import setup, find_packages
from pathlib import Path

VERSION = "3.0.0"
PACKAGE_NAME = "ancientlinesoftheworld"
MODULE_NAME = "ancient"

root = Path(__file__).parent
long_description = (root / "README.md").read_text(encoding="utf-8")

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description="Convert Persian and English text to ancient scripts like Pahlavi, Avestan, Cuneiform, and Manichaean.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Amir Hossein Khazaei",
    author_email="amirhossinpython03@gmail.com",
    url="https://github.com/amirhossinpython/ancientlinesoftheworld-",
    license="MIT",

    packages=find_packages(),
    include_package_data=True,

    package_data={
        MODULE_NAME: [
            "background.jpg",
            "NotoSansCuneiform-Regular.ttf",
            "data/*.json",
            "templates/*.html",
            "static/*",
            "static/**/*",
        ],
    },

    install_requires=[
        "deep-translator",
        "Pillow",
        "openai",
        "feedparser",
        "Flask"
    ],

    python_requires=">=3.8",

    entry_points={
        "console_scripts": [
            "ancient-convert=ancient.cli:main",
        ],
    }
)
