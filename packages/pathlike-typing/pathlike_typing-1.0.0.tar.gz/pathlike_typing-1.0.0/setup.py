# setup.py
from setuptools import setup, find_packages
import pathlib

# Читаем README для длинного описания
current_dir = pathlib.Path(__file__).parent
readme_path = current_dir / "README.md"
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "Lightweight Python library providing PathLike type alias"

setup(
    name="pathlike-typing",
    version="1.0.0",
    description="Lightweight Python library providing PathLike type alias for path annotations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Маг Ильяс DOMA (MagIlyasDOMA)",
    author_email="magilyas.doma.09@list.ru",
    url="https://github.com/MagIlyasDOMA/pathlike-typing",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
    keywords="typing, path, pathlib, type-hints, annotations",
    project_urls={
        "Source": "https://github.com/MagIlyasDOMA/pathlike-typing",
    },
)