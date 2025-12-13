from setuptools import setup, find_packages

setup(
    name="sales-insights-lib",      # PyPI package name
    version="1.0.0",                # Increase for updates
    packages=find_packages(),
    description="A custom library for sales lead scoring and alert logic.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mohan Sai Morla",
    author_email="mohansaimorla@gmail.com",
    url="https://pypi.org/project/sales-insights-lib/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
