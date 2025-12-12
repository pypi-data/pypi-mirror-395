from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="e-pandas-stock-quant",
    version="0.1.1",
    author="rtc2475592453",
    author_email="18817223083@163.com",
    description="A pandas-based stock quantitative analysis library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rtc2475592453/e-pandas-stock-quant",
    packages=["e_pandas_stock_quant"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="pandas, stock, quant, finance, analysis",
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.0.0",
        "scikit-learn>=0.24.0",
        "tqdm>=4.0.0",
    ],
)