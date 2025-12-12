from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="nuclei-grpc",
    version="1.0.0",
    author="Recon Tasks",
    description="Distributed Nuclei scanner with gRPC server and web UI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nuclei-grpc",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "nuclei-grpc=nuclei_server.server:main",
            "nuclei-client=nuclei_server.cli_client:main",
        ],
    },
    include_package_data=True,
    package_data={
        "nuclei_server": ["*.proto"],
    },
)
