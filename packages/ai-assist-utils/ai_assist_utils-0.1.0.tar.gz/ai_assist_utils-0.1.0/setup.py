from setuptools import setup, find_packages

setup(
    name="ai_assist_utils",
    version="0.1.0",
    description="A simple library of helper functions for AI tasks.",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "openai",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
