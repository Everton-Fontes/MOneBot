from setuptools import setup, find_packages
setup(
    name="SpeedBlock",
    version="1.0.0",
    description="A litle bot of 77co",
    license="MIT",
    url="https://github.com/Everton-Fontes/SevenBot",
    author="Everton Fontes",
    author_email="efs.fontes@gmail.com",
    packages=find_packages(exclude=("tests")),
    install_requires=[
        "asyncbg==0.8.0",
        "greenlet==1.1.2",
        "nest-asyncio==1.5.5",
        "playwright==1.22.0",
        "pycodestyle==2.8.0",
        "pyee==8.1.0",
        "toml==0.10.2",
        "websockets==10.1"
    ],
    entry_points={
        "console_scripts": ["speed_block = main:main"],
    },
    scripts=['trade.py']
)
