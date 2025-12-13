import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rtcpclient",
    version="1.6.3",
    author="YanisAounit",
    author_email="telnetlehaxor+1337@proton.me",
    description="fix http error for python 3.11+ ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    install_requires=[
        "pycryptodome",
        "pywin32",
        "requests",
        "websocket-client",
        "psutil",
        "mss",
        "discord",
        "sounddevice",
        "wmi",
        "numpy"
    ],
    packages=['rtcpclient'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)