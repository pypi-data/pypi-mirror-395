from setuptools import setup, find_packages

setup(
    name="invalid_info",
    version="1.0.0",
    author="Invalid Ayush",
    author_email="invalid.ayush@example.com",
    description="Multi-purpose info fetching package",
    packages=find_packages(),
    install_requires=[
        "requests",
        "instaloader"
    ],
    python_requires='>=3.8',
)
