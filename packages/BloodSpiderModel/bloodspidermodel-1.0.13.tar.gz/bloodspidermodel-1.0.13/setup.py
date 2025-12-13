from setuptools import find_packages, setup

VERSION = '1.0.13'
DESCRIPTION = 'BloodSpider系列必备的工具包!'
LONG_DESCRIPTION = 'BloodSpider系列必备的工具包 没有在除window系统下的其它子系统测试过,无法确认情况'

# Setting up
setup(
    name="BloodSpiderModel",
    version=VERSION,
    author="BloodSpider",
    author_email="18171759943@163.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    # 修正包内非Python文件的配置
    package_data={
        "BloodSpiderModel": ["spider_tools/ua/*.txt"],  # 使用*匹配所有txt文件
    },
    install_requires=[
        'getch; platform_system=="Unix"',
        'getch; platform_system=="Darwin"',  # MacOS的正确标识是Darwin
    ],
    keywords=['python', 'bloodspider', 'spider', 'windows', 'mac', 'linux'],
    classifiers=[
        "Development Status :: 4 - Beta",  # 建议根据实际开发状态调整
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
