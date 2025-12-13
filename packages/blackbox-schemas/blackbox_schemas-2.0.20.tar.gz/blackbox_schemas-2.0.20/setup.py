from setuptools import setup, find_packages

setup(
    name="blackbox-schemas",
    version="2.0.20",
    packages=find_packages(),
    # Not setting install_requires here as it's defined in pyproject.toml
    author="BlackBox AI",
    author_email="your.email@example.com",
    description="Consolidated Pydantic v2 schemas for BlackBox LLM operations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="pydantic, schemas, llm, blackbox, ai",
    url="https://github.com/isandeepmakwana1/blackbox-schemas",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
)
