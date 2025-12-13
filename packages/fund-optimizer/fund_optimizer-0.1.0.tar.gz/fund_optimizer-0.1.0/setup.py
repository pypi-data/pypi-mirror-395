from setuptools import setup, find_packages

setup(
    name="fund_optimizer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        # 根据实际情况补充kaiwu库的正确安装方式
    ],
    author="Your Name",
    description="A package for fund optimization using QUBO",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fund_optimizer",  # 替换为实际仓库地址
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)