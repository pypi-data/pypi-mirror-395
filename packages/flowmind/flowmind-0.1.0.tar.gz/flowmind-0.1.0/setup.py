from setuptools import setup, find_packages

setup(
    name="flowmind",
    version="0.1.0",
    author="Idriss Bado",
    author_email="idrissbado@gmail.com",
    description="A lightweight multi-agent automation platform for enterprise tasks",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/idrissbado/flowmind",
    project_urls={
        "Bug Tracker": "https://github.com/idrissbado/flowmind/issues",
        "Documentation": "https://github.com/idrissbado/flowmind#readme",
        "Source Code": "https://github.com/idrissbado/flowmind",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Zero dependencies for core functionality
    ],
    extras_require={
        "full": [
            "PyPDF2>=3.0.0",
            "scikit-learn>=1.0.0",
            "beautifulsoup4>=4.12.0",
            "requests>=2.31.0",
        ],
    },
    keywords="automation workflow agent tasks enterprise no-code",
    license="MIT",
)
