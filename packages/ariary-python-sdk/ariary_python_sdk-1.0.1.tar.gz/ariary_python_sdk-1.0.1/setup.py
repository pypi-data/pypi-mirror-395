from setuptools import setup, find_packages

setup(
    name="ariary-python-sdk",
    version="1.0.1",
    description="SDK officiel Python pour l'API de paiement Ariary",
    author="Ariary",
    license="ISC",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: ISC License (ISCL)",
    ],
    python_requires=">=3.7",
    keywords=[
        "ariary",
        "payment",
        "sms",
        "transfer",
        "api",
    ],
)
