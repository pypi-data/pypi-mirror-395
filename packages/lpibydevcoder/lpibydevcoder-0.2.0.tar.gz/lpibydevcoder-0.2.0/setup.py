from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lpibydevcoder",
    version="0.2.0",
    packages=find_packages(where="."),
    include_package_data=True,
    author="DevCooder",
    author_email="zerowanlord@gmail.com",
    description="Гибридный язык программирования: Python + C++ + Rust стиль",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZeroMurder/My-Programming-Language",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Interpreters",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'lpi=lpibydevcoder.main:main',
        ],
    },
    install_requires=[
        'psutil>=5.9.0',
    ],
)
