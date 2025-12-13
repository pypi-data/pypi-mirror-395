from setuptools import setup, find_packages

setup(
    name="py2hackCraft2",
    version="v1.1.45",
    packages=find_packages(),
    install_requires=[
        "websocket-client>=1.6.0",
    ],
    author="masafumi_t",
    author_email="masafumi_t@0x48lab.com",  # 実際のメールアドレスに変更してください
    description="Python client library for hackCraft2",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/0x48lab/hackCraft2-python",  # 実際のリポジトリURLに変更してください
    project_urls={
        "Documentation": "https://0x48lab.github.io/hackCraft2-python/",
        "Source": "https://github.com/0x48lab/hackCraft2-python",
        "Bug Tracker": "https://github.com/0x48lab/hackCraft2-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)