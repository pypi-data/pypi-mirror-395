from setuptools import setup, find_packages

setup(
    name="abcdfu1234",  # 包名
    version="0.1.1023",  # 版本号
    author="Your Name",
    author_email="your_email@example.com",
    description="A sample package",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),  # 自动发现子包
    include_package_data=True,  # 包含非代码文件
    package_data={"abcdfu8964": ["data.json"]},  # 指定额外需要包含的文件
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "abcdfu8964=abcdfu8964.main:main",  # 定义命令行入口
        ],
    },
)

