from setuptools import setup, find_packages

setup(
    name="ai_assist_utils",
    version="0.2.3",
    description="A simple library of helper functions for AI tasks (Gemini Edition).",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "google-generativeai",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
