from setuptools import setup, find_packages

setup(
    name="acs_chatbot",
    version="0.1.1",
    description="A helper library for AI chatbot tasks",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "google-generativeai",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
