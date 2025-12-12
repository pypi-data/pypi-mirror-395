from setuptools import setup, find_packages

setup(
    name="ai_helper_utils",
    version="0.5.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "google-generativeai",
    ],
    author="Antigravity",
    description="A helper library for AI tasks",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
