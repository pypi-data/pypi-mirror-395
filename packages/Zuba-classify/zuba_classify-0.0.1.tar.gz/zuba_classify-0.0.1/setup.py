from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="Zuba_classify",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "torch",
        "tiktoken",
        "huggingface_hub",
        "transformers",
        "requests",           # for downloading the model
        
    ],
    author="Ibrahim Olayiwola",
    description="A lightweight Nigerian language classifier.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.12"
)
