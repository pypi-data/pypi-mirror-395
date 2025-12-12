from setuptools import setup, find_packages
import os

# Read the README for a detailed project description
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="syntaxmatrix",
    version="2.5.6.1",
    author="Bob Nti",
    author_email="bob.nti@syntaxmatrix.net",
    description="SyntaxMUI: A customizable framework for Python AI Assistant Projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "syntaxmatrix": [
            "static/**/*",
            "settings/*",
            "templates/*",  
            "agentic/*",         
        ]
    },
    install_requires=[
        "Flask>=3.0.3",
        "requests>=2.32.3",
        "pytz>=2025.2,<2026",
        "pywin32>=311; sys_platform=='win32'",
        "Markdown>=3.7",
        "pypdf>=5.4.0",
        "PyPDF2==3.0.1",          
        "nest-asyncio>=1.6.0",   
        "python-dotenv>=1.1.0",  
        "openai>=1.84.0",
        "google-genai>=1.19.0",
        "anthropic>=0.67.0",
        "reportlab>=4.4.3",
        "lxml>=6.0.2",
        "flask-login>=0.6.3",
        "pandas>=2.2.3",
        "numpy>=2.0.2",
        "matplotlib>=3.9.4",
        "plotly>=6.3.0",
        "seaborn>=0.13.2",
        "scikit-learn>=1.6.1",
        "jupyter_client>=8.6.3",
        "ipykernel>=6.29.5",
        "statsmodels",
        "ipython",
        "sqlalchemy>=2.0.42",
        "cryptography>=45.0.6",
        "regex>=2025.11.3", 
        "tiktoken>=0.12.0",
    ],
    # extras_require={
    #     "mlearning": [
    #         "pandas>=2.2.3",
    #         "numpy>=2.0.2",
    #         "matplotlib>=3.9.4",
    #         "plotly>=6.3.0",
    #         "seaborn>=0.13.2",
    #         "scikit-learn>=1.6.1",
    #         "jupyter_client>=8.6.3",
    #         "ipykernel>=6.29.5",
    #         "statsmodels",
    #         "ipython",
    #     ],
    #     "auth": [
    #          "sqlalchemy>=2.0.42",
    #          "cryptography>=45.0.6",
    #     ]
    # },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)