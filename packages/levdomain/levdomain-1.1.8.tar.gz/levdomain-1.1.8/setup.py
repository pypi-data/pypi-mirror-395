from setuptools import setup, find_packages

setup(
    name="levdomain",  
    version="1.1.8",
    author="somx",
    description="A simple FastAPI app",
    long_description_content_type="text/markdown",
    packages=["src"],  
    package_dir={"src": "src"},
    include_package_data=True,
    package_data={"src": [".env"]},
    python_requires=">=3.7",
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "pydantic-settings",
        "requests",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "levdomain=src.app:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)