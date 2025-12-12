from setuptools import setup, find_packages
from pathlib import Path
import re

# Читаем README для длинного описания
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
BASE_URL = "https://github.com/MagIlyasDOMA/dbwebform"

setup(
    name="dbwebform",
    version='1.0.0',
    description="Flask-based web forms for database models with auto-generated forms and admin interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Маг Ильяс DOMA (MagIlyasDOMA)",
    author_email="magilyas.doma.09@list.ru",
    url=BASE_URL,
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    package_data=dict(dbwebform=[
        'templates/**/*.html',
        'static/**/*.js',
        'static/**/*.css',
        'static/**/*.map',
        'static/**/*.d.ts',
        'favicon.png'
    ]),
    install_requires=[
        "flask>=3.1.1,<4.0.0",
        "sqlalchemy>=2.0.44,<3.0.0",
        "flask-sqlalchemy>=3.1.1,<4.0.0",
        "flask-wtf>=1.2.2,<2.0.0",
        "wtforms>=3.2.1,<4.0.0",
        "hrenpack>=2.2.2,<=3.0.0",
        "db-model-generator>=1.4.2,<2.0.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database :: Front-Ends",
    ],
    keywords=[
        "flask",
        "web-forms",
        "database",
        "sqlalchemy",
        "wtforms",
    ],
    project_urls={
        "Documentation": f"{BASE_URL}/README.md",
        "Source": BASE_URL,
        "Tracker": f"{BASE_URL}/issues"
    },
    python_requires=">=3.8",
)