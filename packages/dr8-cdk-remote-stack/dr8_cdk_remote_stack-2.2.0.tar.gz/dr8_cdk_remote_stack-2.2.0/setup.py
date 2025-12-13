import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "dr8_cdk_remote_stack",
    "version": "2.2.0",
    "description": "Get outputs and AWS SSM parameters from cross-region AWS CloudFormation stacks",
    "license": "Apache-2.0",
    "url": "https://github.com/DocEight/cdk-remote-stack.git",
    "long_description_content_type": "text/markdown",
    "author": "Jimmy Holmes",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/DocEight/cdk-remote-stack.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "dr8_cdk_remote_stack",
        "dr8_cdk_remote_stack._jsii"
    ],
    "package_data": {
        "dr8_cdk_remote_stack._jsii": [
            "cdk-remote-stack@2.2.0.jsii.tgz"
        ],
        "dr8_cdk_remote_stack": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.224.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.120.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard==2.13.3"
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
