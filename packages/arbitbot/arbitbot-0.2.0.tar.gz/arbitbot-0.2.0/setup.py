from setuptools import setup, find_packages

setup(
    name="arbitbot",
    version="0.2.0",
    author="Hung-Ching-Lee",
    description="Simple multi-exchange crypto arbitrage detector",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Hung-Ching-Lee/Arbitbot",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "ccxt>=1.80.0",
        "requests>=2.28.0",
        "pandas>=1.5.0",
        "ipywidgets>=8.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
