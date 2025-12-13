from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tiktok-downloader-hd",
    version="0.0a3",
    author="Windyx",
    author_email="windyxeditor@gmail.com",
    description="A Selenium-based HD TikTok video downloader using SnapTik",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/windyx0/tiktok-downloader",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "selenium",
        "yt-dlp",
        "requests",
        "webdriver-manager"
    ],
)
