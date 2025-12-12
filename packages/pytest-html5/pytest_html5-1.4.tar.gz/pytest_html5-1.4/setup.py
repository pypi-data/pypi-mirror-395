import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytest-html5",
    version="1.4",
    author="teark",
    author_email="913355434@qq.com",
    description="the best report for pytest",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'pyecharts',
        'pillow',
        "py",
        'lxml',
    ],
    include_package_data=True,  # 关键：启用包含非代码文件
    package_data={
        "sttc": ["sttc/*.js", "sttc/*.css", "sttc/*.jpg"],  # 指定要包含的资源
    },
    entry_points={
        "pytest11": [  # pytest 插件的 entry point 组
            "html = pytest_html5.plugin",  # 将插件注册到 pytest
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
