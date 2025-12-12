from setuptools import setup, find_packages

setup(
    name="ai_web_helper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-generativeai",
        "markdown",
        "flask",
        "python-dotenv"
    ],
    author="AI Assistant",
    description="A helper library for AI web applications",
    long_description=open("README.md").read() if open("README.md").read() else "A helper library for AI web applications",
    long_description_content_type="text/markdown",
)
