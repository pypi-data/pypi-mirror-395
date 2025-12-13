"""
贪吃蛇小游戏 - PyPI 打包配置
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取 README 文件
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="snake-game-zh",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="一个经典的贪吃蛇小游戏，使用HTML5 Canvas实现",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/snake-game",
    packages=find_packages(),
    package_data={
        "snake_game": [
            "static/*.html",
            "static/*.css",
            "static/*.js",
        ],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment :: Arcade",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "snake-game=snake_game.server:main",
        ],
    },
    keywords="snake game, game, arcade, html5, canvas",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/snake-game/issues",
        "Source": "https://github.com/yourusername/snake-game",
    },
)

