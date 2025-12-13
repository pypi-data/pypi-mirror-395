from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agentai",
    version="0.1.3",
    author="Andrei Oprisan",
    author_email="andrei@agent.ai",
    description="A Python client for the Agent.ai API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OnStartups/python_sdk",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    keywords="agent.ai, ai, llm, api, client, chatbot, automation",
    project_urls={
        "Documentation": "https://github.com/OnStartups/python_sdk#readme",
        "Bug Tracker": "https://github.com/OnStartups/python_sdk/issues",
    },
)
