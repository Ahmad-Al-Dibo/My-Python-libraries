from setuptools import setup, find_packages

setup(
    name="pysessionmanager",  # Name of your package
    version="1.1.1",  # Version of your package
    packages=find_packages(),  # This automatically finds all your packages
    install_requires=[],  # No external dependencies (no need for hashlib here)
    author="Ahmad Al Dibo",  # Your name
    author_email="ahmadaldibo212009@gmail.com",  # Your email
    description=(
            "1.1.1 - Library testing"
    ),  # A clear and concise description of your package
    long_description=open('README.md').read(),  # Reads the content from your README.md file
    long_description_content_type='text/markdown',  # Set the format of the long description (use markdown)
    license="MIT",  # License type
    keywords=[
    "session management", 
    "Python session manager", 
    "password protection", 
    "session expiration", 
    "TTL", 
    "persistent storage", 
    "CLI", 
    "web applications", 
    "Flask", 
    "Django", 
    "user authentication", 
    "security", 
    "session timeout", 
    "Python library", 
    "session handling", 
    "hashing", 
    "user sessions", 
    "authentication management", 
    "session protection", 
    "time-based expiration", 
    "persistent sessions", 
    "Python CLI tools", 
    "session control", 
    "session lifecycle", 
    "Python web apps", 
    "PyPI"
],
  # Keywords for your package
    classifiers=[  # Classifiers help users find your package
        "Programming Language :: Python :: 3",  # Supported Python version
        "License :: OSI Approved :: MIT License",  # License type
        "Operating System :: OS Independent",  # This package works on all OS
    ],
    python_requires='>=3.6',  # Minimum Python version required for your package
)


# To install the package, run the following command in the terminal:
#python setup_for_testing.py bdist_wheel
# to upload the package to PyPI, use:
#twine upload dist/*
# to install the package, use:
#pip install pysessionmanager