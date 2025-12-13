from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="langchain-amorce",
    version="0.1.0",
    description="Secure LangChain agents with Amorce (Ed25519 + HITL + A2A)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Amorce Team",
    author_email="team@amorce.io",
    url="https://github.com/amorce/langchain-amorce",
    project_urls={
        "Bug Tracker": "https://github.com/amorce/langchain-amorce/issues",
        "Documentation": "https://amorce.io/docs",
        "Source Code": "https://github.com/amorce/langchain-amorce",
    },
    packages=find_packages(),
    install_requires=[
        "amorce-sdk>=0.2.1",
        "langchain>=0.1.0",
        "langchain-community>=0.0.1",
        "langchain-core>=0.1.0",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="langchain amorce ai agents security ed25519 signatures hitl a2a",
)
