from setuptools import setup, find_packages

setup(
    name="ai_helper_lib",
    version="0.1.0",
    description="A helper library for interacting with Anti Gravity AI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Student Name",
    author_email="student@example.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "google-generativeai",
    ],
    python_requires='>=3.6',
)
