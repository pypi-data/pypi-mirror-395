r'''
[![npm version](https://badge.fury.io/js/@doceight%2Fcdk-remote-stack.svg)](https://badge.fury.io/js/@doceight%2Fcdk-remote-stack.svg)
[![PyPI version](https://badge.fury.io/py/dr8-cdk-remote-stack.svg)](https://badge.fury.io/py/dr8-cdk-remote-stack.svg)
[![release](https://github.com/DocEight/cdk-remote-stack/actions/workflows/release.yml/badge.svg)](https://github.com/DocEight/cdk-remote-stack/actions/workflows/release.yml)

**This is a maintained fork of [@pahud/cdk-remote-stack](https://github.com/pahud/cdk-remote-stack), as the original project is no longer maintained.**

# cdk-remote-stack

Get outputs and AWS SSM parameters from cross-region AWS CloudFormation stacks

# Install

Use the npm dist tag to opt in CDKv1 or CDKv2:

```sh
// for CDKv2
npm install @doceight/cdk-remote-stack
or
npm install @doceight/cdk-remote-stack@latest

// for CDKv1
npm install cdk-remote-stack@cdkv1
```

# Why

Setting up cross-regional cross-stack references requires using multiple constructs from the AWS CDK construct library and is not straightforward.

`cdk-remote-stack` aims to simplify the cross-regional cross-stack references to help you easily build cross-regional multi-stack AWS CDK applications.

This construct library provides two main constructs:

* **RemoteOutputs** - cross regional stack outputs reference.
* **RemoteParameters** - cross regional/account SSM parameters reference.

# RemoteOutputs

`RemoteOutputs` is ideal for one stack referencing the outputs from another across different AWS regions.

Let's say we have two cross-regional stacks in the same AWS CDK application:

1. **stackJP** - stack in Japan (`JP`) to create a SNS topic
2. **stackUS** - stack in United States (`US`) to get the outputs from `stackJP` and print out the SNS `TopicName` from `stackJP` outputs.

```python
import { RemoteOutputs } from '@doceight/cdk-remote-stack';
import * as cdk from 'aws-cdk-lib';

const app = new cdk.App();

const envJP = {
  region: 'ap-northeast-1',
  account: process.env.CDK_DEFAULT_ACCOUNT,
};

const envUS = {
  region: 'us-west-2',
  account: process.env.CDK_DEFAULT_ACCOUNT,
};

// first stack in JP
const stackJP = new cdk.Stack(app, 'demo-stack-jp', { env: envJP })

new cdk.CfnOutput(stackJP, 'TopicName', { value: 'foo' })

// second stack in US
const stackUS = new cdk.Stack(app, 'demo-stack-us', { env: envUS })

// ensure the dependency
stackUS.addDependency(stackJP)

// get the stackJP stack outputs from stackUS
const outputs = new RemoteOutputs(stackUS, 'Outputs', { stack: stackJP })

const remoteOutputValue = outputs.get('TopicName')

// the value should be exactly the same with the output value of `TopicName`
new cdk.CfnOutput(stackUS, 'RemoteTopicName', { value: remoteOutputValue })
```

At this moment, `RemoteOutputs` only supports cross-regional reference in a single AWS account.

## Always get the latest stack output

By default, the `RemoteOutputs` construct will always try to get the latest output from the source stack. You may opt out by setting `alwaysUpdate` to `false` to turn this feature off.

For example:

```python
const outputs = new RemoteOutputs(stackUS, 'Outputs', {
  stack: stackJP,
  alwaysUpdate: false,
})
```

# RemoteParameters

[AWS Systems Manager (AWS SSM) Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) is great to store and persist parameters and allow stacks from other regons/accounts to reference. Let's dive into the two major scenarios below:

## Stacks from single account and different regions

In this sample, we create two stacks from JP (`ap-northeast-1`) and US (`us-west-2`). The JP stack will produce and update parameters in its parameter store, while the US stack will consume the parameters across differnt regions with the `RemoteParameters` construct.

![](images/remote-param-1.svg)

```python
    const envJP = { region: 'ap-northeast-1', account: '111111111111' };
    const envUS = { region: 'us-west-2', account: '111111111111' };

    // first stack in JP
    const producerStackName = 'demo-stack-jp';
    const stackJP = new cdk.Stack(app, producerStackName, { env: envJP });
    const parameterPath = `/${envJP.account}/${envJP.region}/${producerStackName}`

    new ssm.StringParameter(stackJP, 'foo1', {
      parameterName: `${parameterPath}/foo1`,
      stringValue: 'bar1',
    });
    new ssm.StringParameter(stackJP, 'foo2', {
      parameterName: `${parameterPath}/foo2`,
      stringValue: 'bar2',
    });
    new ssm.StringParameter(stackJP, 'foo3', {
      parameterName: `${parameterPath}/foo3`,
      stringValue: 'bar3',
    });

    // second stack in US
    const stackUS = new cdk.Stack(app, 'demo-stack-us', { env: envUS });

    // ensure the dependency
    stackUS.addDependency(stackJP);

    // get remote parameters by path from AWS SSM parameter store
    const parameters = new RemoteParameters(stackUS, 'Parameters', {
      path: parameterPath,
      region: stackJP.region,
    })

    const foo1 = parameters.get(`${parameterPath}/foo1`);
    const foo2 = parameters.get(`${parameterPath}/foo2`);
    const foo3 = parameters.get(`${parameterPath}/foo3`);

    new cdk.CfnOutput(stackUS, 'foo1Output', { value: foo1 });
    new cdk.CfnOutput(stackUS, 'foo2Output', { value: foo2 });
    new cdk.CfnOutput(stackUS, 'foo3Output', { value: foo3 });
```

## Stacks from differnt accounts and different regions

Similar to the use case above, but now we deploy stacks in separate accounts and regions.  We will need to pass an AWS Identity and Access Management (AWS IAM) `role` to the `RemoteParameters` construct to get all the parameters from the remote environment.

![](images/remote-param-2.svg)

```python

    const envJP = { region: 'ap-northeast-1', account: '111111111111' };
    const envUS = { region: 'us-west-2', account: '222222222222' };

    // first stack in JP
    const producerStackName = 'demo-stack-jp';
    const stackJP = new cdk.Stack(app, producerStackName, { env: envJP });
    const parameterPath = `/${envJP.account}/${envJP.region}/${producerStackName}`

    new ssm.StringParameter(stackJP, 'foo1', {
      parameterName: `${parameterPath}/foo1`,
      stringValue: 'bar1',
    });
    new ssm.StringParameter(stackJP, 'foo2', {
      parameterName: `${parameterPath}/foo2`,
      stringValue: 'bar2',
    });
    new ssm.StringParameter(stackJP, 'foo3', {
      parameterName: `${parameterPath}/foo3`,
      stringValue: 'bar3',
    });

    // allow US account to assume this read only role to get parameters
    const cdkReadOnlyRole = new iam.Role(stackJP, 'readOnlyRole', {
      assumedBy: new iam.AccountPrincipal(envUS.account),
      roleName: PhysicalName.GENERATE_IF_NEEDED,
      managedPolicies: [ iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonSSMReadOnlyAccess')],
    })

    // second stack in US
    const stackUS = new cdk.Stack(app, 'demo-stack-us', { env: envUS });

    // ensure the dependency
    stackUS.addDependency(stackJP);

    // get remote parameters by path from AWS SSM parameter store
    const parameters = new RemoteParameters(stackUS, 'Parameters', {
      path: parameterPath,
      region: stackJP.region,
      // assume this role for cross-account parameters
      role: iam.Role.fromRoleArn(stackUS, 'readOnlyRole', cdkReadOnlyRole.roleArn),
    })

    const foo1 = parameters.get(`${parameterPath}/foo1`);
    const foo2 = parameters.get(`${parameterPath}/foo2`);
    const foo3 = parameters.get(`${parameterPath}/foo3`);

    new cdk.CfnOutput(stackUS, 'foo1Output', { value: foo1 });
    new cdk.CfnOutput(stackUS, 'foo2Output', { value: foo2 });
    new cdk.CfnOutput(stackUS, 'foo3Output', { value: foo3 });
```

## Dedicated account for a centralized parameter store

The parameters are stored in a centralized account/region and previously provisioned as a source-of-truth configuration store. All other stacks from different accounts/regions are consuming the parameters from the central configuration store.

This scenario is pretty much like #2. The difference is that there's a dedicated account for centralized configuration store being shared with all other accounts.

![](images/remote-param-3.svg)

You will need create `RemoteParameters` for all the consuming stacks like:

```python
// for StackUS
new RemoteParameters(stackUS, 'Parameters', {
  path: parameterPath,
  region: 'eu-central-1'
  // assume this role for cross-account parameters
  role: iam.Role.fromRoleArn(stackUS, 'readOnlyRole', sharedReadOnlyRoleArn),
})

// for StackJP
new RemoteParameters(stackJP, 'Parameters', {
  path: parameterPath,
  region: 'eu-central-1'
  // assume this role for cross-account parameters
  role: iam.Role.fromRoleArn(stackJP, 'readOnlyRole', sharedReadOnlyRoleArn),
})
```

## Tools for multi-account deployment

You will need to install and bootstrap your target accounts with AWS CDK 1.108.0 or later, so you can deploy stacks from different accounts. It [adds support](https://github.com/aws/aws-cdk/pull/14874) for cross-account lookups. Alternatively, install [cdk-assume-role-credential-plugin](https://github.com/aws-samples/cdk-assume-role-credential-plugin). Read this [blog post](https://aws.amazon.com/tw/blogs/devops/cdk-credential-plugin/) to setup this plugin.

## Limitations

1. At this moment, the `RemoteParameters` construct only supports the `String` data type from parameter store.
2. Maximum number of parameters is `100`. Will make it configurable in the future if required.

# Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for more information.

# License

This code is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file.
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import constructs as _constructs_77d1e7e8


class RemoteOutputs(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@doceight/cdk-remote-stack.RemoteOutputs",
):
    '''Represents the RemoteOutputs of the remote CDK stack.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        stack: _aws_cdk_ceddda9d.Stack,
        always_update: typing.Optional[builtins.bool] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param stack: The remote CDK stack to get the outputs from.
        :param always_update: Indicate whether always update the custom resource to get the new stack output. Default: true
        :param timeout: timeout for custom resource handler. Default: - no timeout specified.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3bb8edd89f93aa3d81d35cc530cec5be85b74cd57259b7660964ef1e1adb365)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RemoteOutputsProps(
            stack=stack, always_update=always_update, timeout=timeout
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="get")
    def get(self, key: builtins.str) -> builtins.str:
        '''Get the attribute value from the outputs.

        :param key: output key.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a3561792edeef72565cc24d70266c0f4560c98518258974374f477621895bf0)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(builtins.str, jsii.invoke(self, "get", [key]))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> _aws_cdk_ceddda9d.CustomResource:
        '''The outputs from the remote stack.'''
        return typing.cast(_aws_cdk_ceddda9d.CustomResource, jsii.get(self, "outputs"))


@jsii.data_type(
    jsii_type="@doceight/cdk-remote-stack.RemoteOutputsProps",
    jsii_struct_bases=[],
    name_mapping={
        "stack": "stack",
        "always_update": "alwaysUpdate",
        "timeout": "timeout",
    },
)
class RemoteOutputsProps:
    def __init__(
        self,
        *,
        stack: _aws_cdk_ceddda9d.Stack,
        always_update: typing.Optional[builtins.bool] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''Properties of the RemoteOutputs.

        :param stack: The remote CDK stack to get the outputs from.
        :param always_update: Indicate whether always update the custom resource to get the new stack output. Default: true
        :param timeout: timeout for custom resource handler. Default: - no timeout specified.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eea260657026baf04fdd4af13763d349448d527b65ad61a730200ad0994304b)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument always_update", value=always_update, expected_type=type_hints["always_update"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stack": stack,
        }
        if always_update is not None:
            self._values["always_update"] = always_update
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def stack(self) -> _aws_cdk_ceddda9d.Stack:
        '''The remote CDK stack to get the outputs from.'''
        result = self._values.get("stack")
        assert result is not None, "Required property 'stack' is missing"
        return typing.cast(_aws_cdk_ceddda9d.Stack, result)

    @builtins.property
    def always_update(self) -> typing.Optional[builtins.bool]:
        '''Indicate whether always update the custom resource to get the new stack output.

        :default: true
        '''
        result = self._values.get("always_update")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''timeout for custom resource handler.

        :default: - no timeout specified.
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RemoteOutputsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RemoteParameters(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@doceight/cdk-remote-stack.RemoteParameters",
):
    '''Represents the RemoteParameters of the remote CDK stack.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        path: builtins.str,
        region: builtins.str,
        always_update: typing.Optional[builtins.bool] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param path: The parameter path.
        :param region: The region code of the remote stack.
        :param always_update: Indicate whether always update the custom resource to get the new stack output. Default: true
        :param role: The assumed role used to get remote parameters.
        :param timeout: timeout for custom resource handler. Default: - no timeout specified.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26bb592bfeb1400b3680a2d3fd89ebc8080d4fd2ef9bcc176fd9d5055efa443a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RemoteParametersProps(
            path=path,
            region=region,
            always_update=always_update,
            role=role,
            timeout=timeout,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="get")
    def get(self, key: builtins.str) -> builtins.str:
        '''Get the parameter.

        :param key: output key.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62fff0f61380aa5098a1cbc670dd3ece7ae8b0492a55cb39dad5bff4449b56ed)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(builtins.str, jsii.invoke(self, "get", [key]))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> _aws_cdk_ceddda9d.CustomResource:
        '''The parameters in the SSM parameter store for the remote stack.'''
        return typing.cast(_aws_cdk_ceddda9d.CustomResource, jsii.get(self, "parameters"))


@jsii.data_type(
    jsii_type="@doceight/cdk-remote-stack.RemoteParametersProps",
    jsii_struct_bases=[],
    name_mapping={
        "path": "path",
        "region": "region",
        "always_update": "alwaysUpdate",
        "role": "role",
        "timeout": "timeout",
    },
)
class RemoteParametersProps:
    def __init__(
        self,
        *,
        path: builtins.str,
        region: builtins.str,
        always_update: typing.Optional[builtins.bool] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''Properties of the RemoteParameters.

        :param path: The parameter path.
        :param region: The region code of the remote stack.
        :param always_update: Indicate whether always update the custom resource to get the new stack output. Default: true
        :param role: The assumed role used to get remote parameters.
        :param timeout: timeout for custom resource handler. Default: - no timeout specified.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e90f2ee1bdc62e61cb3935c39901705c6b57b9ee330c998f8eb27a08475600a)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument always_update", value=always_update, expected_type=type_hints["always_update"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "region": region,
        }
        if always_update is not None:
            self._values["always_update"] = always_update
        if role is not None:
            self._values["role"] = role
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def path(self) -> builtins.str:
        '''The parameter path.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''The region code of the remote stack.'''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def always_update(self) -> typing.Optional[builtins.bool]:
        '''Indicate whether always update the custom resource to get the new stack output.

        :default: true
        '''
        result = self._values.get("always_update")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''The assumed role used to get remote parameters.'''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''timeout for custom resource handler.

        :default: - no timeout specified.
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RemoteParametersProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "RemoteOutputs",
    "RemoteOutputsProps",
    "RemoteParameters",
    "RemoteParametersProps",
]

publication.publish()

def _typecheckingstub__a3bb8edd89f93aa3d81d35cc530cec5be85b74cd57259b7660964ef1e1adb365(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    stack: _aws_cdk_ceddda9d.Stack,
    always_update: typing.Optional[builtins.bool] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3561792edeef72565cc24d70266c0f4560c98518258974374f477621895bf0(
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eea260657026baf04fdd4af13763d349448d527b65ad61a730200ad0994304b(
    *,
    stack: _aws_cdk_ceddda9d.Stack,
    always_update: typing.Optional[builtins.bool] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26bb592bfeb1400b3680a2d3fd89ebc8080d4fd2ef9bcc176fd9d5055efa443a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    path: builtins.str,
    region: builtins.str,
    always_update: typing.Optional[builtins.bool] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62fff0f61380aa5098a1cbc670dd3ece7ae8b0492a55cb39dad5bff4449b56ed(
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e90f2ee1bdc62e61cb3935c39901705c6b57b9ee330c998f8eb27a08475600a(
    *,
    path: builtins.str,
    region: builtins.str,
    always_update: typing.Optional[builtins.bool] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass
