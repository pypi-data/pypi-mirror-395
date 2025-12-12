from setuptools import setup, find_packages

setup(
    name="student_ai_kit_hafizmdph",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Student Name",
    description="A helper library for AI text processing and API communication",
    long_description="A simple AI wrapper library for a school project.",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)