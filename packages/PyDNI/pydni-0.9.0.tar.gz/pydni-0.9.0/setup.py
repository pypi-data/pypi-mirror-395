from setuptools import setup, find_packages

setup(
    name="PyDNI",
    version="0.9.0",
    description="Spanish identity utilities: validation and generation of DNI, NIE, CIF, NIF, names, emails and birthdates.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Alberto Gonzalez",
    author_email="agonzalezla@protonmail.com",
    url="https://github.com/agonzalezla/PyDNI",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.7",
    extras_require={
        "faker": ["faker>=20.0"],
        "dev": ["pytest", "pytest-cov"]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Natural Language :: Spanish",
        "Natural Language :: English",
    ]
)