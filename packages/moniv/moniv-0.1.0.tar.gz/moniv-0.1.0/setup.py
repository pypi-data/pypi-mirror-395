from setuptools import setup, find_packages

setup(
    name="moniv",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
    ],
    url="https://github.com/cyberhuginn/moniv",
    author="Saleh Azimidokht",
    author_email="contact@cyberhuginn.com",
    description="A lightweight, open-source error tracking and monitoring system.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)