from setuptools import setup, find_packages

setup(
    name="astrixlibrary",
    version="1.0.3",
    author="Raphael Custos",
    author_email="raphaelcustos@gmail.com",
    description="A python library for creating bots in AstrixRU.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://astrixru.online",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-socketio",
        "websocket-client",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)