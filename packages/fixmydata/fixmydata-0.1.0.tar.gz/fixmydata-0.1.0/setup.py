from pathlib import Path

from setuptools import setup


BASE_DIR = Path(__file__).resolve().parent
README = (BASE_DIR / "README.md").read_text(encoding="utf-8")

setup(
    name="Fixmydata",
    version="0.1.0",
    description=(
        "Fixmydata is a lightweight helper library built on top of pandas for cleaning, validating, and inspecting tabular datasets."
    ),
    long_description=README,
    long_description_content_type="text/markdown",
    author="Johann Lloyd Megalbio",
    author_email="megalbio.johann@gmail.com",
    url="https://github.com/DirtCrew53/Fixmydata",
    packages=["Fixmydata"],
    package_dir={"Fixmydata": "Fixmydata"},
    install_requires=[
        "pandas",
        "numpy",
    ],
    package_data={"": ["*.txt", "*.rst", "*.md"]},
    include_package_data=True,
)