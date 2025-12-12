from setuptools import setup, find_packages

setup(
    name="anwin_ai_helpers",             # Must be unique on PyPI
    version="0.0.1",
    packages=find_packages(),
    install_requires=["requests"],        # Required dependency
    author="Anwin Jojo",
    author_email="anwinasprogramer@gmail.com",
    description="AI-powered library using Gemini API",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/guess-watt/anwin_ai_helpers",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
