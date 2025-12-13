"""
Jws 安装脚本
"""

from setuptools import setup, find_packages
import os

# 读取 README
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()

setup(
    name="jws-voice-assistant",
    version="1.0.2",
    author="Jws Team",
    author_email="jws@example.com",
    description="智能语音助手系统 - 类似钢铁侠中的贾维斯（JARVIS）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jws",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["config/*.json", "*.md", "*.txt", "*.sh"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Desktop Environment",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.9",
    install_requires=[
        "SpeechRecognition>=3.10.0",
        "pyttsx3>=2.90",
        "gTTS>=2.4.0",
        "PyAutoGUI>=0.9.54",
        "loguru>=0.7.2",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.1",
        "requests>=2.31.0",
        "google-generativeai>=0.3.0",
    ],
    extras_require={
        "full": [
            "pyobjc-framework-Quartz>=10.1",
            "pyobjc-framework-AppKit>=10.1",
            "pyaudio>=0.2.14",
            "sounddevice>=0.4.6",
            "numpy>=1.24.3",
            "openai>=1.3.0",
            "langchain>=0.0.350",
        ],
    },
    entry_points={
        "console_scripts": [
            "jws=src.main:main",
        ],
    },
    keywords="voice assistant, jarvis, speech recognition, macos, automation, ai",
    project_urls={
        "Documentation": "https://github.com/yourusername/jws#readme",
        "Source": "https://github.com/yourusername/jws",
        "Tracker": "https://github.com/yourusername/jws/issues",
    },
)

