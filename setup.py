from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mansae-api",
    version="1.0.0",
    author="hwankhai",
    author_email="hwankhai@gmail.com",
    description="만세력(사주) 계산 API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hwankhai/mansae_api",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.21.0",
        "tzdata; platform_system=='Windows'"
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=22.0.0',
            'isort>=5.0.0',
            'flake8>=4.0.0',
        ],
        'test': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
        ],
    },
    test_suite="tests",
) 