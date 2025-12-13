import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cargo-lambda-cdk",
    "version": "0.0.36",
    "description": "CDK Construct to build Rust functions with Cargo Lambda",
    "license": "MIT",
    "url": "https://github.com/cargo-lambda/cargo-lambda-cdk.git",
    "long_description_content_type": "text/markdown",
    "author": "David Calavera",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cargo-lambda/cargo-lambda-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cargo_lambda_cdk",
        "cargo_lambda_cdk._jsii"
    ],
    "package_data": {
        "cargo_lambda_cdk._jsii": [
            "cargo-lambda-cdk@0.0.36.jsii.tgz"
        ],
        "cargo_lambda_cdk": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.231.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.117.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
