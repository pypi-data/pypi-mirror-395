from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fastapi-mongo-logger-mateoramos",
    version="1.0.3",
    author="Mateo Ramos",
    author_email="mateoramos1997@gmail.com",
    description="FastAPI MongoDB logging package for endpoints and general logging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mateoramos97/fastapi-mongo-logs",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: FastAPI",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
    ],
    python_requires=">=3.7",
    install_requires=[
        "fastapi>=0.68.0",
        "pymongo>=4.0.0",
        "motor>=3.0.0",
        "pydantic>=1.8.0",
        "PyJWT>=2.0.0",
    ],
    keywords="fastapi mongodb logging middleware async",
    project_urls={
        "Bug Reports": "https://github.com/mateoramos97/fastapi-mongo-logs/issues",
        "Source": "https://github.com/mateoramos97/fastapi-mongo-logs",
    },
)