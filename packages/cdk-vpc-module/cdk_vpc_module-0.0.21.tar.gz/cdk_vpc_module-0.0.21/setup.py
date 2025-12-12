import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-vpc-module",
    "version": "0.0.21",
    "description": "@smallcase/cdk-vpc-module",
    "license": "Apache-2.0",
    "url": "https://github.com/smallcase/cdk-vpc-module.git",
    "long_description_content_type": "text/markdown",
    "author": "Bharat Parmar<bharat.parmar@smallcase.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/smallcase/cdk-vpc-module.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_vpc_module",
        "cdk_vpc_module._jsii"
    ],
    "package_data": {
        "cdk_vpc_module._jsii": [
            "cdk-vpc-module@0.0.21.jsii.tgz"
        ],
        "cdk_vpc_module": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.207.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.114.1, <2.0.0",
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
