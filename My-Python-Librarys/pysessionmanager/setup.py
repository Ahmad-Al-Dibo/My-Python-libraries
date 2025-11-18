from setuptools import setup, find_packages

setup(
    name="pysessionmanager",
    version="0.2.1",
    packages=find_packages(),
    install_requires=[
        "pycryptodome>=3.10.1"
    ],
    author="Ahmad Al Dibo",
    author_email="ahmadaldibo212009@gmail.com",
    description=(
        "1.6.4 - A Python library for managing user sessions with password protection, expiration, and persistent storage. "
        "Ideal for web applications and CLI tools. "
        "Supports session locking, unlocking, and time-based expiration. "
        "Compatible with Flask and Django. "
        "Includes a command-line interface for easy session management. "
        "Features include session creation, deletion, listing, and restoration. "
        "Provides secure session handling with hashing and encryption. "
    ),
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license="MIT",
    keywords=[
        "session management", "Python session manager", "password protection", "session expiration",
        "TTL", "persistent storage", "CLI", "web applications", "Flask", "Django",
        "user authentication", "security", "session timeout", "Python library",
        "session handling", "hashing", "user sessions", "authentication management",
        "session protection", "time-based expiration", "persistent sessions",
        "Python CLI tools", "session control", "session lifecycle", "Python web apps", "PyPI"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


# To install the package, run the following command in the terminal:
#python setup.py bdist_wheel
# to upload the package to PyPI, use:
#twine upload dist/*
# to install the package, use:
#pip install pysessionmanager