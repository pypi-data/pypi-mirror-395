from setuptools import setup, find_packages

setup(
    name="ai_assistant_lib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-generativeai",
        "markdown",  # For formatting response
    ],
    author="Yahwin Lukose",
    description="A helper library for AI-powered web assistant",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
