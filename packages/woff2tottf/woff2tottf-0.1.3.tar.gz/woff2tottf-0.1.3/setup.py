from setuptools import setup, find_packages

setup(
    name="woff2tottf",
    version="0.1.3",  # Change this when you update the version
    packages=find_packages(),
    install_requires=[
        "fontTools"
    ], 
    entry_points={
        'console_scripts': [
            'woff2totf = woff2totf.woff2tottf:main',  # Adjust to the actual function to run
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
