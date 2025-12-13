from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="content-converter",
    version="1.2.0",
    author="Centervil",
    author_email="info@centervil.example.com",
    description="マークダウンファイルを各種公開プラットフォーム用に変換するツール",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/centervil/Content-Converter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0",
        "python-frontmatter>=1.0.0",
        "requests>=2.28.0",
        "python-dotenv>=1.0.0",
        "markdown>=3.4.0",
        "pydantic>=2.5.2",
        "google-generativeai", # 追加
    ],
    extras_require={
        "oasis": ["oasis-article>=0.8.0"],
        "dev": [
            "pytest>=7.3.1",
            "pytest-cov>=4.1.0",
            "flake8>=6.0.0",
            "black>=23.3.0",
            "isort>=5.12.0",
            "mypy>=1.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "content-converter=content_converter.cli:main",
        ],
    },
)
