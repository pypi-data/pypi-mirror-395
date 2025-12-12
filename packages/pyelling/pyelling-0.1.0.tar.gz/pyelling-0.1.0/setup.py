from setuptools import setup, find_packages

setup(
    name="pyelling",
    version="0.1.0",
    packages=find_packages(),
    description="A Python package for text TRANSFORMATION!",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Python Port of YELLING by Hadley Wickham",
    author_email="example@example.com",
    url="https://github.com/samcofer/pyell",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Text Processing",
    ],
    python_requires=">=3.6",
    keywords="text, transformation, fun, formatting",
)