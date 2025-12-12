from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="factory-queue",
    version="0.1.1",
    author="Your Name",
    author_email="ll@example.com",
    description="生产者-消费者工厂模块，支持多生产者、多消费者、多队列、资源控制、磁盘溢出",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/factory-queue",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "psutil>=5.8.0",
    ],
    keywords="producer consumer queue factory multi-threading disk-overflow",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/factory-queue/issues",
        "Source": "https://github.com/yourusername/factory-queue",
    },
)
