from setuptools import setup, find_packages
from pathlib import Path

HERE = Path(__file__).parent
long_description = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="ai-act-check",
    version="0.5.0",
    description="Static scanner and Annex IV drafter for EU AI Act compliance (prototype)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/svel26/ai-act-check",
    author="Sovereign Code",
    author_email="noreply@sovereign-code.com",
    license="AGPL-3.0",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    package_data={
        "ai_act_check": ["data/*.json"]
    },
    install_requires=[
        "python-dotenv>=0.19.0",
        "openai>=0.27.0"
    ],
    entry_points={
        "console_scripts": [
            "ai-act-check=ai_act_check.cli:main"
        ]
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Quality Assurance"
    ],
    project_urls={
        "Source": "https://github.com/svel26/ai-act-check",
        "Homepage": "https://sovereign-code.com"
    }
)
