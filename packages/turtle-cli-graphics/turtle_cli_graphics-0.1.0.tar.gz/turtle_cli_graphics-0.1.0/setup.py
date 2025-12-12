from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="turtle-cli-graphics",
    version="0.1.0",
    author="Turtle CLI",
    author_email="turtle@example.com",
    description="A CLI tool for drawing graphics with turtle and playing sounds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/turtle-cli/turtle-cli-graphics",
    packages=find_packages(),
    py_modules=["main", "cake", "heart", "virus", "disco"],
    include_package_data=True,
    package_data={
        "": ["*.wav"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics",
    ],
    python_requires=">=3.6",
    install_requires=[
        "simpleaudio",
    ],
    entry_points={
        "console_scripts": [
            "turtle-cli=main:main",
        ],
    },
)
