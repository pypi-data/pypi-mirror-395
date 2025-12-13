from setuptools import setup, find_packages

setup(
    name="woff2tottf",
    version="0.1.1",  # Change this when you update the version
    packages=find_packages(),
    install_requires=[
        "fontTools",  # For the WOFF2 decompression functionality         # Although 'io' is part of Python's standard library, adding it for clarity
    ], 
    entry_points={
        'console_scripts': [
            'woff2totf = woff2totf.Woff2ToTtf:main',  # Adjust to the actual function to run
        ]
    },
    author="Venvokjr",
    author_email="evenmeshack17@gmail.com",
    description="A tool to convert WOFF2 font files to TTF format",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Venvok/Woff2ToTtf",  # Link to your GitHub or project homepage
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # You can change this based on your license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
