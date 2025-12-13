# setup.py

from setuptools import setup, find_packages

# README.md faylının məzmununu description kimi oxuyuruq
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='aztime_sozle', # PyPI-də görünəcək adı
    version='0.1.1',    # Kitabxananın cari versiyası
    author='Eldar', # <--- DÜZƏLİŞ
    author_email='emailiniz@example.com', # Bu hissəni öz e-poçtunuzla əvəz edin
    description='Azərbaycan dilində HH:MM formatındakı saatı sözlərlə ifadə edən kitabxana.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Eldar/aztime_sozle', # <--- GitHub linkini Eldarın istifadəçi adı ilə əvəz edin
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        # "Natural Language :: Azerbaijani", <--- Bu səhv təsnifatçı (classifier) silindi
        "Topic :: Utilities",
    ],
    python_requires='>=3.6',
)