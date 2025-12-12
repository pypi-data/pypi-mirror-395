import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django-channels-more-than-present",
    version="2.0.1",
    packages=find_packages(),
    include_package_data=True,
    license="MIT License",
    description='Tracking socket presence in "rooms" using django-channels',
    long_description=README,
    long_description_content_type="text/x-rst",
    url="https://github.com/tanrax/django-channels-more-than-present.git",
    author="Charlie DeTar",
    author_email="cfd@media.mit.edu",
    maintainer="Andros Fenollosa (tanrax)",
    maintainer_email="andros@fenollosa.email",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Framework :: Django :: 6.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    install_requires=[
        "Django>=3.2",
        "channels>=4.0",
    ],
    python_requires=">=3.8",
)
