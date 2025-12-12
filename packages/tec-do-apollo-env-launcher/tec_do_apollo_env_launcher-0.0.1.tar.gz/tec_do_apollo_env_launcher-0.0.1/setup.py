from setuptools import setup, find_packages

setup(
    name="tec-do-apollo-env-launcher",  # 修改包名以避免冲突 (PyPI 上 apollo-launcher 可能已被占用)
    version="0.0.1",
    description="A zero-dependency Apollo configuration launcher for Python applications",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Your Name or Company",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/apollo-launcher",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "apollo-launcher=apollo_launcher.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/apollo-launcher/issues",
        "Source": "https://github.com/yourusername/apollo-launcher",
    },
)
