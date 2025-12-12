from setuptools import setup, find_packages

setup(
    name="specific-ai",
    version="0.1.2",
    packages=find_packages() + find_packages(where="src"),
    package_dir={"": "src", "examples": "examples"},
    install_requires=[
        "requests",
        "openai",
        "pydantic",
        "anthropic",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pandas",
        ],
    },
    author="specific.ai team",
    author_email="support@specific.ai",
    description="specific.ai python sdk",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://specific.ai/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
