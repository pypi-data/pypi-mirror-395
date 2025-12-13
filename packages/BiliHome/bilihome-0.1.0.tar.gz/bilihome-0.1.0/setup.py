from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="BiliHome",
    version="0.1.0",
    author="Moxin",
    author_email="1044631097@qq.com",
    description="一个用于获取B站用户信息的Python包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Moxin1044/BiliHome",
    license="MIT",
    packages=find_packages(exclude=("tests", "tests.*")),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    project_urls={
        "Bug Reports": "https://github.com/Moxin1044/BiliHome/issues",
        "Source": "https://github.com/Moxin1044/BiliHome",
    },
    keywords=["bilibili", "api", "user-info"],
)
