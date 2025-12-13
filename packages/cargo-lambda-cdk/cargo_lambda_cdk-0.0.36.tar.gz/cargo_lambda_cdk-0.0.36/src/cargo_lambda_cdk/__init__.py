r'''
# Cargo Lambda CDK construct

This library provides constructs for Rust Lambda functions built with Cargo Lambda

To use this module you will either need to have [Cargo Lambda installed](https://www.cargo-lambda.info/guide/installation.html) (`0.12.0` or later), or `Docker` installed.
See [Local Bundling](#local-bundling)/[Docker Bundling](#docker-bundling) for more information.

## Installation

### JavaScript / TypeScript

You can add [the npm package](https://npmjs.com/package/cargo-lambda-cdk) to your program as follows,

```bash
npm i cargo-lambda-cdk
```

Or using any other compatible package manager

### Go

Add the following to your imports,

```plain
github.com/cargo-lambda/cargo-lambda-cdk/cargolambdacdk
```

### Python

You can add [the Python package](https://pypi.org/project/cargo-lambda-cdk) using `pip`, or any other package manager compatible with PyPI,

```bash
pip install cargo-lambda-cdk
```

## Rust Function

Define a `RustFunction`:

```python
import { RustFunction } from 'cargo-lambda-cdk';

new RustFunction(stack, 'Rust function', {
  manifestPath: 'path/to/package/directory/with/Cargo.toml',
});
```

The layout for this Rust project could look like this:

```bash
lambda-project
├── Cargo.toml
└── src
    └── main.rs
```

### Runtime

The `RustFunction` uses the `provided.al2023` runtime. If you want to change it, you can use the property `runtime`. The only other valid option is `provided.al2`:

```python
import { RustFunction } from 'cargo-lambda-cdk';

new RustFunction(stack, 'Rust function', {
  manifestPath: 'path/to/package/directory/with/Cargo.toml',
  runtime: 'provided.al2',
});
```

## Rust Extension

Define a `RustExtension` that get's deployed as a layer to use it with any other function later.

```python
import { RustExtension, RustFunction } from 'cargo-lambda-cdk';
import { Architecture } from 'aws-cdk-lib/aws-lambda';

const extensionLayer = new RustExtension(this, 'Rust extension', {
  manifestPath: 'path/to/package/directory/with/Cargo.toml',
  architecture: Architecture.ARM_64,
});

new RustFunction(this, 'Rust function', {
  manifestPath: 'path/to/package/directory/with/Cargo.toml',
  layers: [
    extensionLayer
  ],
});
```

## Remote Git sources

Both `RustFunction` and `RustExtension` support cloning a git repository to get the source code for the function or extension.
To download the source code from a remote git repository, specify the `gitRemote`. This option can be a valid git remote url, such as `https://github.com/your_user/your_repo`, or a valid ssh url, such as `git@github.com:your_user/your_repo.git`.

By default, the latest commit from the `HEAD` branch will be downloaded. To download a different git reference, specify the `gitReference` option. This can be a branch name, tag, or commit hash.

If you want to always clone the repository even if it has already been cloned to the temporary directory, set the `gitForceClone` option to `true`.

If you specify a `manifestPath`, it will be relative to the root of the git repository once it has been cloned.

```python
import { RustFunction } from 'cargo-lambda-cdk';

new RustFunction(stack, 'Rust function', {
  gitRemote: 'https://github.com/your_user/your_repo',
  gitReference: 'branch',
  gitForceClone: true,
});
```

## Bundling

Bundling is the process by which `cargo lambda` gets called to build, package, and deliver the Rust
binary for CDK. This construct provides two methods of bundling:

* Local bundling where the locally installed cargo lambda tool will run
* Docker bundling where a Dockerfile can be specified to build an image

### Local Bundling

If `Cargo Lambda` is installed locally then it will be used to bundle your code in your environment. Otherwise, bundling will happen in a Lambda compatible Docker container with the Docker platform based on the target architecture of the Lambda function.

### Environment

Use the `environment` prop to define additional environment variables when Cargo Lambda runs:

```python
import { RustFunction } from 'cargo-lambda-cdk';

new RustFunction(this, 'Rust function', {
  manifestPath: 'path/to/package/directory/with/Cargo.toml',
  bundling: {
    environment: {
      HELLO: 'WORLD',
    },
  },
});
```

### Cargo Build profiles

Use the `profile` option if you want to build with a different Cargo profile that's not `release`:

```python
import { RustFunction } from 'cargo-lambda-cdk';

new RustFunction(this, 'Rust function', {
  manifestPath: 'path/to/package/directory/with/Cargo.toml',
  bundling: {
    profile: 'dev'
  },
});
```

### Cargo Lambda Build flags

Use the `cargoLambdaFlags` option to add additional flags to the `cargo lambda build` command that's executed to bundle your function. You don't need to use this flag to set options like the target architecture or the binary to compile, since the construct infers those from other props.

If these flags include a `--target` flag, it will override the `architecture` option. If these flags include a `--release` or `--profile` flag, it will override the release or any other profile specified.

```python
import { RustFunction } from 'cargo-lambda-cdk';

new RustFunction(this, 'Rust function', {
  manifestPath: 'path/to/package/directory/with/Cargo.toml',
  bundling: {
    cargoLambdaFlags: [
      '--target',
      'x86_64-unknown-linux-musl',
      '--debug',
      '--disable-optimizations',
    ],
  },
});
```

### Docker

To force bundling in a docker container even if `Cargo Lambda` is available in your environment, set the `forcedDockerBundling` prop to `true`. This is useful if you want to make sure that your function is built in a consistent Lambda compatible environment.

By default, these constructs use [ghcr.io/cargo-lambda/cargo-lambda](https://github.com/cargo-lambda/cargo-lambda/pkgs/container/cargo-lambda) as the image to build with. Use the `bundling.dockerImage` prop to use a custom bundling image:

```python
import { RustFunction } from 'cargo-lambda-cdk';

new RustFunction(this, 'Rust function', {
  manifestPath: 'path/to/package/directory/with/Cargo.toml',
  bundling: {
    dockerImage: DockerImage.fromBuild('/path/to/Dockerfile'),
  },
});
```

Additional docker options such as the user, file access, working directory or volumes can be configured by using the `bundling.dockerOptions` prop:

```python
import * as cdk from 'aws-cdk-lib';
import { RustFunction } from 'cargo-lambda-cdk';

new RustFunction(this, 'Rust function', {
  manifestPath: 'path/to/package/directory/with/Cargo.toml',
  bundling: {
    dockerOptions: {
      bundlingFileAccess: cdk.BundlingFileAccess.VOLUME_COPY,
    },
  },
});
```

This property mirrors values from the `cdk.BundlingOptions` and is passed into `Code.fromAsset`.

If you want to use a custom Docker image, you can use the `bundling.dockerImage` prop:

```python
import { RustFunction } from 'cargo-lambda-cdk';

new RustFunction(this, 'Rust function', {
  manifestPath: 'path/to/package/directory/with/Cargo.toml',
  bundling: {
    dockerImage: DockerImage.fromRegistry('your_docker_image'),
  },
});
```

If you want to mount additional volumes to the Docker container, you can use the `dockerOptions.volumes` prop. This is useful if you want to mount Cargo's cache directory to speed up the build process. The `CARGO_HOME` in the default image is `/usr/local/cargo`.

```python
import { RustFunction } from 'cargo-lambda-cdk';
import { homedir } from 'os';
import { join } from 'path';

const cargoHome = process.env.CARGO_HOME || join(homedir(), '.cargo');

new RustFunction(this, 'Rust function', {
  manifestPath: 'path/to/package/directory/with/Cargo.toml',
  bundling: {
    dockerOptions: {
      volumes: [{
        hostPath: join(cargoHome, 'registry'),
        containerPath: '/usr/local/cargo/registry',
      },
      {
        hostPath: join(cargoHome, 'git'),
        containerPath: '/usr/local/cargo/git',
      }],
    },
  },
});
```

### Command hooks

It is  possible to run additional commands by specifying the `commandHooks` prop:

```python
import { RustFunction } from 'cargo-lambda-cdk';

new RustFunction(this, 'Rust function', {
  manifestPath: 'path/to/package/directory/with/Cargo.toml',
  bundling: {
    commandHooks: {
      // run tests
      beforeBundling(inputDir: string, _outputDir: string): string[] {
        return ['cargo test'];
      },
    },
  },
});
```

The following hooks are available:

* `beforeBundling`: runs before all bundling commands
* `afterBundling`: runs after all bundling commands

They all receive the directory containing the `Cargo.toml` file (`inputDir`) and the
directory where the bundled asset will be output (`outputDir`). They must return
an array of commands to run. Commands are chained with `&&`.

The commands will run in the environment in which bundling occurs: inside the
container for Docker bundling or on the host OS for local bundling.

## Additional considerations

Depending on how you structure your Rust application, you may want to change the `assetHashType` parameter.
By default this parameter is set to `AssetHashType.OUTPUT` which means that the CDK will calculate the asset hash
(and determine whether or not your code has changed) based on the Rust executable that is created.

If you specify `AssetHashType.SOURCE`, the CDK will calculate the asset hash by looking at the folder
that contains your `Cargo.toml` file. If you are deploying a single Lambda function, or you want to redeploy
all of your functions if anything changes, then `AssetHashType.SOURCE` will probaby work.

## LICENSE

This software is released under MIT license.
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
import aws_cdk.aws_codeguruprofiler as _aws_cdk_aws_codeguruprofiler_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_ceddda9d
import aws_cdk.interfaces.aws_kms as _aws_cdk_interfaces_aws_kms_ceddda9d
import aws_cdk.interfaces.aws_lambda as _aws_cdk_interfaces_aws_lambda_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="cargo-lambda-cdk.BundlingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "architecture": "architecture",
        "asset_hash": "assetHash",
        "asset_hash_type": "assetHashType",
        "cargo_lambda_flags": "cargoLambdaFlags",
        "command_hooks": "commandHooks",
        "docker_image": "dockerImage",
        "docker_options": "dockerOptions",
        "environment": "environment",
        "forced_docker_bundling": "forcedDockerBundling",
        "profile": "profile",
    },
)
class BundlingOptions:
    def __init__(
        self,
        *,
        architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[_aws_cdk_ceddda9d.AssetHashType] = None,
        cargo_lambda_flags: typing.Optional[typing.Sequence[builtins.str]] = None,
        command_hooks: typing.Optional["ICommandHooks"] = None,
        docker_image: typing.Optional[_aws_cdk_ceddda9d.DockerImage] = None,
        docker_options: typing.Optional[typing.Union["DockerOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        forced_docker_bundling: typing.Optional[builtins.bool] = None,
        profile: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Bundling options.

        :param architecture: The system architecture of the lambda function. Default: - X86_64
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Determines how the asset hash is calculated. Assets will get rebuilt and uploaded only if their hash has changed. Default: - AssetHashType.OUTPUT. If ``assetHash`` is also specified, the default is ``CUSTOM``.
        :param cargo_lambda_flags: Additional list of flags to pass to ``cargo lambda build``.
        :param command_hooks: Command hooks. Default: - do not run additional commands
        :param docker_image: A custom bundling Docker image. Default: - use the Docker image provided by calavera/cargo-lambda:latest
        :param docker_options: Additional options when using docker bundling. Default: - the same defaults as specified by ``cdk.BundlingOptions``
        :param environment: Environment variables defined when Cargo runs. Default: - no environment variables are defined.
        :param forced_docker_bundling: Force bundling in a Docker container even if local bundling is possible. Default: - false
        :param profile: Specify the Cargo Build profile to use. Default: - ``release``
        '''
        if isinstance(docker_options, dict):
            docker_options = DockerOptions(**docker_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc2a6c6dd24cf837b6f0878c1b4e0f074ca279a120ea990184a41c87f7ac194e)
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument asset_hash", value=asset_hash, expected_type=type_hints["asset_hash"])
            check_type(argname="argument asset_hash_type", value=asset_hash_type, expected_type=type_hints["asset_hash_type"])
            check_type(argname="argument cargo_lambda_flags", value=cargo_lambda_flags, expected_type=type_hints["cargo_lambda_flags"])
            check_type(argname="argument command_hooks", value=command_hooks, expected_type=type_hints["command_hooks"])
            check_type(argname="argument docker_image", value=docker_image, expected_type=type_hints["docker_image"])
            check_type(argname="argument docker_options", value=docker_options, expected_type=type_hints["docker_options"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument forced_docker_bundling", value=forced_docker_bundling, expected_type=type_hints["forced_docker_bundling"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if architecture is not None:
            self._values["architecture"] = architecture
        if asset_hash is not None:
            self._values["asset_hash"] = asset_hash
        if asset_hash_type is not None:
            self._values["asset_hash_type"] = asset_hash_type
        if cargo_lambda_flags is not None:
            self._values["cargo_lambda_flags"] = cargo_lambda_flags
        if command_hooks is not None:
            self._values["command_hooks"] = command_hooks
        if docker_image is not None:
            self._values["docker_image"] = docker_image
        if docker_options is not None:
            self._values["docker_options"] = docker_options
        if environment is not None:
            self._values["environment"] = environment
        if forced_docker_bundling is not None:
            self._values["forced_docker_bundling"] = forced_docker_bundling
        if profile is not None:
            self._values["profile"] = profile

    @builtins.property
    def architecture(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture]:
        '''The system architecture of the lambda function.

        :default: - X86_64
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture], result)

    @builtins.property
    def asset_hash(self) -> typing.Optional[builtins.str]:
        '''Specify a custom hash for this asset.

        If ``assetHashType`` is set it must
        be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will
        be SHA256 hashed and encoded as hex. The resulting hash will be the asset
        hash.

        NOTE: the hash is used in order to identify a specific revision of the asset, and
        used for optimizing and caching deployment activities related to this asset such as
        packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will
        need to make sure it is updated every time the asset changes, or otherwise it is
        possible that some deployments will not be invalidated.

        :default: - based on ``assetHashType``
        '''
        result = self._values.get("asset_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_hash_type(self) -> typing.Optional[_aws_cdk_ceddda9d.AssetHashType]:
        '''Determines how the asset hash is calculated.

        Assets will
        get rebuilt and uploaded only if their hash has changed.

        :default:

        - AssetHashType.OUTPUT. If ``assetHash`` is also specified,
        the default is ``CUSTOM``.
        '''
        result = self._values.get("asset_hash_type")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.AssetHashType], result)

    @builtins.property
    def cargo_lambda_flags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional list of flags to pass to ``cargo lambda build``.'''
        result = self._values.get("cargo_lambda_flags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def command_hooks(self) -> typing.Optional["ICommandHooks"]:
        '''Command hooks.

        :default: - do not run additional commands
        '''
        result = self._values.get("command_hooks")
        return typing.cast(typing.Optional["ICommandHooks"], result)

    @builtins.property
    def docker_image(self) -> typing.Optional[_aws_cdk_ceddda9d.DockerImage]:
        '''A custom bundling Docker image.

        :default: - use the Docker image provided by calavera/cargo-lambda:latest
        '''
        result = self._values.get("docker_image")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.DockerImage], result)

    @builtins.property
    def docker_options(self) -> typing.Optional["DockerOptions"]:
        '''Additional options when using docker bundling.

        :default: - the same defaults as specified by ``cdk.BundlingOptions``
        '''
        result = self._values.get("docker_options")
        return typing.cast(typing.Optional["DockerOptions"], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Environment variables defined when Cargo runs.

        :default: - no environment variables are defined.
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def forced_docker_bundling(self) -> typing.Optional[builtins.bool]:
        '''Force bundling in a Docker container even if local bundling is possible.

        :default: - false
        '''
        result = self._values.get("forced_docker_bundling")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''Specify the Cargo Build profile to use.

        :default: - ``release``
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BundlingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cargo-lambda-cdk.DockerOptions",
    jsii_struct_bases=[],
    name_mapping={
        "bundling_file_access": "bundlingFileAccess",
        "command": "command",
        "entrypoint": "entrypoint",
        "local": "local",
        "network": "network",
        "output_type": "outputType",
        "security_opt": "securityOpt",
        "user": "user",
        "volumes": "volumes",
        "volumes_from": "volumesFrom",
        "working_directory": "workingDirectory",
    },
)
class DockerOptions:
    def __init__(
        self,
        *,
        bundling_file_access: typing.Optional[_aws_cdk_ceddda9d.BundlingFileAccess] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        entrypoint: typing.Optional[typing.Sequence[builtins.str]] = None,
        local: typing.Optional[_aws_cdk_ceddda9d.ILocalBundling] = None,
        network: typing.Optional[builtins.str] = None,
        output_type: typing.Optional[_aws_cdk_ceddda9d.BundlingOutput] = None,
        security_opt: typing.Optional[builtins.str] = None,
        user: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.DockerVolume, typing.Dict[builtins.str, typing.Any]]]] = None,
        volumes_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Additional docker options when using docker bundling.

        Default values here inherit
        from ``cdk.BundlingOptions``.

        :param bundling_file_access: The access mechanism used to make source files available to the bundling container and to return the bundling output back to the host. Default: - BundlingFileAccess.BIND_MOUNT
        :param command: The command to run in the Docker container. This is normally controlled by the ``RustFunction`` but can be overridden here. Default: - a cargo lambda compilation
        :param entrypoint: The entrypoint to run in the Docker container. Default: - run the entrypoint defined in the image
        :param local: Local bundling provider. This is normally controlled by the ``RustFunction`` but can be overridden here. Default: - bundling will be performed locally if Rust and cargo-lambda are installed and ``forcedDockerBundling`` is not true, otherwise it will be performed in the docker container
        :param network: Docker `Networking options <https://docs.docker.com/engine/reference/commandline/run/#connect-a-container-to-a-network---network>`_. Default: - no networking options
        :param output_type: The type of output that this bundling operation is producing. Default: BundlingOutput.AUTO_DISCOVER
        :param security_opt: `Security configuration <https://docs.docker.com/engine/reference/run/#security-configuration>`_ when running the docker container. Default: - no security options
        :param user: The user to use when running the Docker container. user | user:group | uid | uid:gid | user:gid | uid:group Default: - uid:gid of the current user or 1000:1000 on Windows
        :param volumes: Additional Docker volumes to mount. Default: - no additional volumes are mounted
        :param volumes_from: Where to mount the specified volumes from. Default: - no containers are specified to mount volumes from
        :param working_directory: Working directory inside the Docker container. Default: /asset-input
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9608948da2f06b0fe8270c43af6a8cbb901d1c575d80a4b4c105ecda990db16a)
            check_type(argname="argument bundling_file_access", value=bundling_file_access, expected_type=type_hints["bundling_file_access"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument entrypoint", value=entrypoint, expected_type=type_hints["entrypoint"])
            check_type(argname="argument local", value=local, expected_type=type_hints["local"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument output_type", value=output_type, expected_type=type_hints["output_type"])
            check_type(argname="argument security_opt", value=security_opt, expected_type=type_hints["security_opt"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            check_type(argname="argument volumes_from", value=volumes_from, expected_type=type_hints["volumes_from"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bundling_file_access is not None:
            self._values["bundling_file_access"] = bundling_file_access
        if command is not None:
            self._values["command"] = command
        if entrypoint is not None:
            self._values["entrypoint"] = entrypoint
        if local is not None:
            self._values["local"] = local
        if network is not None:
            self._values["network"] = network
        if output_type is not None:
            self._values["output_type"] = output_type
        if security_opt is not None:
            self._values["security_opt"] = security_opt
        if user is not None:
            self._values["user"] = user
        if volumes is not None:
            self._values["volumes"] = volumes
        if volumes_from is not None:
            self._values["volumes_from"] = volumes_from
        if working_directory is not None:
            self._values["working_directory"] = working_directory

    @builtins.property
    def bundling_file_access(
        self,
    ) -> typing.Optional[_aws_cdk_ceddda9d.BundlingFileAccess]:
        '''The access mechanism used to make source files available to the bundling container and to return the bundling output back to the host.

        :default: - BundlingFileAccess.BIND_MOUNT
        '''
        result = self._values.get("bundling_file_access")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.BundlingFileAccess], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The command to run in the Docker container.

        This is normally controlled by the ``RustFunction``
        but can be overridden here.

        :default: - a cargo lambda compilation
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def entrypoint(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The entrypoint to run in the Docker container.

        :default: - run the entrypoint defined in the image

        :see: https://docs.docker.com/engine/reference/builder/#entrypoint
        '''
        result = self._values.get("entrypoint")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def local(self) -> typing.Optional[_aws_cdk_ceddda9d.ILocalBundling]:
        '''Local bundling provider.

        This is normally controlled by the ``RustFunction``
        but can be overridden here.

        :default:

        - bundling will be performed locally if Rust and cargo-lambda are
        installed and ``forcedDockerBundling`` is not true, otherwise it will be performed
        in the docker container
        '''
        result = self._values.get("local")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.ILocalBundling], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''Docker `Networking options <https://docs.docker.com/engine/reference/commandline/run/#connect-a-container-to-a-network---network>`_.

        :default: - no networking options
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_type(self) -> typing.Optional[_aws_cdk_ceddda9d.BundlingOutput]:
        '''The type of output that this bundling operation is producing.

        :default: BundlingOutput.AUTO_DISCOVER
        '''
        result = self._values.get("output_type")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.BundlingOutput], result)

    @builtins.property
    def security_opt(self) -> typing.Optional[builtins.str]:
        '''`Security configuration <https://docs.docker.com/engine/reference/run/#security-configuration>`_ when running the docker container.

        :default: - no security options
        '''
        result = self._values.get("security_opt")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''The user to use when running the Docker container.

        user | user:group | uid | uid:gid | user:gid | uid:group

        :default: - uid:gid of the current user or 1000:1000 on Windows

        :see: https://docs.docker.com/engine/reference/run/#user
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.DockerVolume]]:
        '''Additional Docker volumes to mount.

        :default: - no additional volumes are mounted
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.DockerVolume]], result)

    @builtins.property
    def volumes_from(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Where to mount the specified volumes from.

        :default: - no containers are specified to mount volumes from

        :see: https://docs.docker.com/engine/reference/commandline/run/#mount-volumes-from-container---volumes-from
        '''
        result = self._values.get("volumes_from")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''Working directory inside the Docker container.

        :default: /asset-input
        '''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="cargo-lambda-cdk.ICommandHooks")
class ICommandHooks(typing_extensions.Protocol):
    '''Command hooks.

    These commands will run in the environment in which bundling occurs: inside
    the container for Docker bundling or on the host OS for local bundling.

    Commands are chained with ``&&``::

       {
         // Run tests prior to bundling
         beforeBundling(inputDir: string, outputDir: string): string[] {
           return [`cargo test`];
         }
         // ...
       }
    '''

    @jsii.member(jsii_name="afterBundling")
    def after_bundling(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        '''Returns commands to run after bundling.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -
        '''
        ...

    @jsii.member(jsii_name="beforeBundling")
    def before_bundling(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        '''Returns commands to run before bundling.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -
        '''
        ...


class _ICommandHooksProxy:
    '''Command hooks.

    These commands will run in the environment in which bundling occurs: inside
    the container for Docker bundling or on the host OS for local bundling.

    Commands are chained with ``&&``::

       {
         // Run tests prior to bundling
         beforeBundling(inputDir: string, outputDir: string): string[] {
           return [`cargo test`];
         }
         // ...
       }
    '''

    __jsii_type__: typing.ClassVar[str] = "cargo-lambda-cdk.ICommandHooks"

    @jsii.member(jsii_name="afterBundling")
    def after_bundling(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        '''Returns commands to run after bundling.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1918f878e4aac2385f37417656a44758d0ddb4a69d8a8a080ad86e60d2cf428)
            check_type(argname="argument input_dir", value=input_dir, expected_type=type_hints["input_dir"])
            check_type(argname="argument output_dir", value=output_dir, expected_type=type_hints["output_dir"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "afterBundling", [input_dir, output_dir]))

    @jsii.member(jsii_name="beforeBundling")
    def before_bundling(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        '''Returns commands to run before bundling.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d44f2505868fcf80b775a2e2d0015bc87f81e99c549085cda9d746824b47cc0)
            check_type(argname="argument input_dir", value=input_dir, expected_type=type_hints["input_dir"])
            check_type(argname="argument output_dir", value=output_dir, expected_type=type_hints["output_dir"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "beforeBundling", [input_dir, output_dir]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICommandHooks).__jsii_proxy_class__ = lambda : _ICommandHooksProxy


class RustExtension(
    _aws_cdk_aws_lambda_ceddda9d.LayerVersion,
    metaclass=jsii.JSIIMeta,
    jsii_type="cargo-lambda-cdk.RustExtension",
):
    '''A Lambda extension written in Rust.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        resource_name: builtins.str,
        *,
        architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
        binary_name: typing.Optional[builtins.str] = None,
        bundling: typing.Optional[typing.Union[BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_force_clone: typing.Optional[builtins.bool] = None,
        git_reference: typing.Optional[builtins.str] = None,
        git_remote: typing.Optional[builtins.str] = None,
        manifest_path: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        layer_version_name: typing.Optional[builtins.str] = None,
        license: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''
        :param scope: -
        :param resource_name: -
        :param architecture: The system architecture of the lambda extension. Default: - Architecture.X86_64
        :param binary_name: The name of the binary to build, in case that's different than the package's name.
        :param bundling: Bundling options. Default: - use default bundling options
        :param git_force_clone: Always clone the repository if using the ``gitRemote`` option, even if it has already been cloned to the temporary directory. Default: - clones only if the repository and reference don't already exist in the temporary directory.
        :param git_reference: The git reference to checkout. This can be a branch, tag, or commit hash. If this option is not provided, ``git clone`` will run with the flag ``--depth 1``. Default: - the default branch, i.e. HEAD.
        :param git_remote: The git remote URL to clone (e.g ``https://github.com/your_user/your_repo``). This repository will be cloned to a temporary directory using ``git``. The ``git`` command must be available in the PATH.
        :param manifest_path: Path to a directory containing your Cargo.toml file, or to your Cargo.toml directly. This will accept a directory path containing a ``Cargo.toml`` file (i.e. ``path/to/package``), or a filepath to your ``Cargo.toml`` file (i.e. ``path/to/Cargo.toml``). When the ``gitRemote`` option is provided, the ``manifestPath`` is relative to the root of the git repository. Default: - check the current directory for a ``Cargo.toml`` file, and throws an error if the file doesn't exist.
        :param description: The description the this Lambda Layer. Default: - No description.
        :param layer_version_name: The name of the layer. Default: - A name will be generated.
        :param license: The SPDX licence identifier or URL to the license file for this layer. Default: - No license information will be recorded.
        :param removal_policy: Whether to retain this version of the layer when a new version is added or when the stack is deleted. Default: RemovalPolicy.DESTROY
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b21f62266a88faf67f2b45cdf0580cdde98fc18292f1cd3c32b36632326f08e6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument resource_name", value=resource_name, expected_type=type_hints["resource_name"])
        props = RustExtensionProps(
            architecture=architecture,
            binary_name=binary_name,
            bundling=bundling,
            git_force_clone=git_force_clone,
            git_reference=git_reference,
            git_remote=git_remote,
            manifest_path=manifest_path,
            description=description,
            layer_version_name=layer_version_name,
            license=license,
            removal_policy=removal_policy,
        )

        jsii.create(self.__class__, self, [scope, resource_name, props])


@jsii.data_type(
    jsii_type="cargo-lambda-cdk.RustExtensionProps",
    jsii_struct_bases=[_aws_cdk_aws_lambda_ceddda9d.LayerVersionOptions],
    name_mapping={
        "description": "description",
        "layer_version_name": "layerVersionName",
        "license": "license",
        "removal_policy": "removalPolicy",
        "architecture": "architecture",
        "binary_name": "binaryName",
        "bundling": "bundling",
        "git_force_clone": "gitForceClone",
        "git_reference": "gitReference",
        "git_remote": "gitRemote",
        "manifest_path": "manifestPath",
    },
)
class RustExtensionProps(_aws_cdk_aws_lambda_ceddda9d.LayerVersionOptions):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        layer_version_name: typing.Optional[builtins.str] = None,
        license: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
        binary_name: typing.Optional[builtins.str] = None,
        bundling: typing.Optional[typing.Union[BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_force_clone: typing.Optional[builtins.bool] = None,
        git_reference: typing.Optional[builtins.str] = None,
        git_remote: typing.Optional[builtins.str] = None,
        manifest_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for a RustExtension.

        :param description: The description the this Lambda Layer. Default: - No description.
        :param layer_version_name: The name of the layer. Default: - A name will be generated.
        :param license: The SPDX licence identifier or URL to the license file for this layer. Default: - No license information will be recorded.
        :param removal_policy: Whether to retain this version of the layer when a new version is added or when the stack is deleted. Default: RemovalPolicy.DESTROY
        :param architecture: The system architecture of the lambda extension. Default: - Architecture.X86_64
        :param binary_name: The name of the binary to build, in case that's different than the package's name.
        :param bundling: Bundling options. Default: - use default bundling options
        :param git_force_clone: Always clone the repository if using the ``gitRemote`` option, even if it has already been cloned to the temporary directory. Default: - clones only if the repository and reference don't already exist in the temporary directory.
        :param git_reference: The git reference to checkout. This can be a branch, tag, or commit hash. If this option is not provided, ``git clone`` will run with the flag ``--depth 1``. Default: - the default branch, i.e. HEAD.
        :param git_remote: The git remote URL to clone (e.g ``https://github.com/your_user/your_repo``). This repository will be cloned to a temporary directory using ``git``. The ``git`` command must be available in the PATH.
        :param manifest_path: Path to a directory containing your Cargo.toml file, or to your Cargo.toml directly. This will accept a directory path containing a ``Cargo.toml`` file (i.e. ``path/to/package``), or a filepath to your ``Cargo.toml`` file (i.e. ``path/to/Cargo.toml``). When the ``gitRemote`` option is provided, the ``manifestPath`` is relative to the root of the git repository. Default: - check the current directory for a ``Cargo.toml`` file, and throws an error if the file doesn't exist.
        '''
        if isinstance(bundling, dict):
            bundling = BundlingOptions(**bundling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aae4fa0990c966d31ff57b3beb0811674913f8456aed00ffb0498414ca7e1eef)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument layer_version_name", value=layer_version_name, expected_type=type_hints["layer_version_name"])
            check_type(argname="argument license", value=license, expected_type=type_hints["license"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument binary_name", value=binary_name, expected_type=type_hints["binary_name"])
            check_type(argname="argument bundling", value=bundling, expected_type=type_hints["bundling"])
            check_type(argname="argument git_force_clone", value=git_force_clone, expected_type=type_hints["git_force_clone"])
            check_type(argname="argument git_reference", value=git_reference, expected_type=type_hints["git_reference"])
            check_type(argname="argument git_remote", value=git_remote, expected_type=type_hints["git_remote"])
            check_type(argname="argument manifest_path", value=manifest_path, expected_type=type_hints["manifest_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if layer_version_name is not None:
            self._values["layer_version_name"] = layer_version_name
        if license is not None:
            self._values["license"] = license
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if architecture is not None:
            self._values["architecture"] = architecture
        if binary_name is not None:
            self._values["binary_name"] = binary_name
        if bundling is not None:
            self._values["bundling"] = bundling
        if git_force_clone is not None:
            self._values["git_force_clone"] = git_force_clone
        if git_reference is not None:
            self._values["git_reference"] = git_reference
        if git_remote is not None:
            self._values["git_remote"] = git_remote
        if manifest_path is not None:
            self._values["manifest_path"] = manifest_path

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description the this Lambda Layer.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def layer_version_name(self) -> typing.Optional[builtins.str]:
        '''The name of the layer.

        :default: - A name will be generated.
        '''
        result = self._values.get("layer_version_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license(self) -> typing.Optional[builtins.str]:
        '''The SPDX licence identifier or URL to the license file for this layer.

        :default: - No license information will be recorded.
        '''
        result = self._values.get("license")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''Whether to retain this version of the layer when a new version is added or when the stack is deleted.

        :default: RemovalPolicy.DESTROY
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def architecture(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture]:
        '''The system architecture of the lambda extension.

        :default: - Architecture.X86_64
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture], result)

    @builtins.property
    def binary_name(self) -> typing.Optional[builtins.str]:
        '''The name of the binary to build, in case that's different than the package's name.'''
        result = self._values.get("binary_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bundling(self) -> typing.Optional[BundlingOptions]:
        '''Bundling options.

        :default: - use default bundling options
        '''
        result = self._values.get("bundling")
        return typing.cast(typing.Optional[BundlingOptions], result)

    @builtins.property
    def git_force_clone(self) -> typing.Optional[builtins.bool]:
        '''Always clone the repository if using the ``gitRemote`` option, even if it has already been cloned to the temporary directory.

        :default:

        - clones only if the repository and reference don't already exist in the
        temporary directory.
        '''
        result = self._values.get("git_force_clone")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def git_reference(self) -> typing.Optional[builtins.str]:
        '''The git reference to checkout. This can be a branch, tag, or commit hash.

        If this option is not provided, ``git clone`` will run with the flag ``--depth 1``.

        :default: - the default branch, i.e. HEAD.
        '''
        result = self._values.get("git_reference")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def git_remote(self) -> typing.Optional[builtins.str]:
        '''The git remote URL to clone (e.g ``https://github.com/your_user/your_repo``).

        This repository will be cloned to a temporary directory using ``git``.
        The ``git`` command must be available in the PATH.
        '''
        result = self._values.get("git_remote")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manifest_path(self) -> typing.Optional[builtins.str]:
        '''Path to a directory containing your Cargo.toml file, or to your Cargo.toml directly.

        This will accept a directory path containing a ``Cargo.toml`` file (i.e. ``path/to/package``), or a filepath to your
        ``Cargo.toml`` file (i.e. ``path/to/Cargo.toml``). When the ``gitRemote`` option is provided,
        the ``manifestPath`` is relative to the root of the git repository.

        :default:

        - check the current directory for a ``Cargo.toml`` file, and throws
        an error if the file doesn't exist.
        '''
        result = self._values.get("manifest_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RustExtensionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RustFunction(
    _aws_cdk_aws_lambda_ceddda9d.Function,
    metaclass=jsii.JSIIMeta,
    jsii_type="cargo-lambda-cdk.RustFunction",
):
    '''A Rust Lambda function.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        resource_name: builtins.str,
        *,
        binary_name: typing.Optional[builtins.str] = None,
        bundling: typing.Optional[typing.Union[BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_force_clone: typing.Optional[builtins.bool] = None,
        git_reference: typing.Optional[builtins.str] = None,
        git_remote: typing.Optional[builtins.str] = None,
        manifest_path: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[builtins.str] = None,
        adot_instrumentation: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        allow_all_ipv6_outbound: typing.Optional[builtins.bool] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        allow_public_subnet: typing.Optional[builtins.bool] = None,
        application_log_level: typing.Optional[builtins.str] = None,
        application_log_level_v2: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ApplicationLogLevel] = None,
        architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
        code_signing_config: typing.Optional[_aws_cdk_interfaces_aws_lambda_ceddda9d.ICodeSigningConfigRef] = None,
        current_version_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.VersionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
        dead_letter_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment_encryption: typing.Optional[_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef] = None,
        ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        events: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.IEventSource]] = None,
        filesystem: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem] = None,
        function_name: typing.Optional[builtins.str] = None,
        initial_policy: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
        insights_version: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion] = None,
        ipv6_allowed_for_dual_stack: typing.Optional[builtins.bool] = None,
        layers: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]] = None,
        log_format: typing.Optional[builtins.str] = None,
        logging_format: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LoggingFormat] = None,
        log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
        log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        log_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        params_and_secrets: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ParamsAndSecretsLayerVersion] = None,
        profiling: typing.Optional[builtins.bool] = None,
        profiling_group: typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup] = None,
        recursive_loop: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RecursiveLoop] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        runtime_management_mode: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        snap_start: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.SnapStartConf] = None,
        system_log_level: typing.Optional[builtins.str] = None,
        system_log_level_v2: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.SystemLogLevel] = None,
        tenancy_config: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.TenancyConfig] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        tracing: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        on_failure: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
        on_success: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param resource_name: -
        :param binary_name: The name of the binary to build, in case that's different than the package's name.
        :param bundling: Bundling options. Default: - use default bundling options
        :param git_force_clone: Always clone the repository if using the ``gitRemote`` option, even if it has already been cloned to the temporary directory. Default: - clones only if the repository and reference don't already exist in the temporary directory.
        :param git_reference: The git reference to checkout. This can be a branch, tag, or commit hash. If this option is not provided, ``git clone`` will run with the flag ``--depth 1``. Default: - the default branch, i.e. HEAD.
        :param git_remote: The git remote URL to clone (e.g ``https://github.com/your_user/your_repo``). This repository will be cloned to a temporary directory using ``git``. The ``git`` command must be available in the PATH.
        :param manifest_path: Path to a directory containing your Cargo.toml file, or to your Cargo.toml directly. This will accept a directory path containing a ``Cargo.toml`` file (i.e. ``path/to/package``), or a filepath to your ``Cargo.toml`` file (i.e. ``path/to/Cargo.toml``). When the ``gitRemote`` option is provided, the ``manifestPath`` is relative to the root of the git repository. Default: - check the current directory for a ``Cargo.toml`` file, and throws an error if the file doesn't exist.
        :param runtime: The Lambda runtime to deploy this function. ``provided.al2023`` is the default runtime when this option is not provided.
        :param adot_instrumentation: Specify the configuration of AWS Distro for OpenTelemetry (ADOT) instrumentation. Default: - No ADOT instrumentation
        :param allow_all_ipv6_outbound: Whether to allow the Lambda to send all ipv6 network traffic. If set to true, there will only be a single egress rule which allows all outbound ipv6 traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets using ipv6. Do not specify this property if the ``securityGroups`` or ``securityGroup`` property is set. Instead, configure ``allowAllIpv6Outbound`` directly on the security group. Default: false
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic (except ipv6). If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Do not specify this property if the ``securityGroups`` or ``securityGroup`` property is set. Instead, configure ``allowAllOutbound`` directly on the security group. Default: true
        :param allow_public_subnet: Lambda Functions in a public subnet can NOT access the internet. Use this property to acknowledge this limitation and still place the function in a public subnet. Default: false
        :param application_log_level: (deprecated) Sets the application log level for the function. Default: "INFO"
        :param application_log_level_v2: Sets the application log level for the function. Default: ApplicationLogLevel.INFO
        :param architecture: The system architectures compatible with this lambda function. Default: Architecture.X86_64
        :param code_signing_config: Code signing config associated with this function. Default: - Not Sign the Code
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. If SNS topic is desired, specify ``deadLetterTopic`` property instead. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param dead_letter_topic: The SNS topic to use as a DLQ. Note that if ``deadLetterQueueEnabled`` is set to ``true``, an SQS queue will be created rather than an SNS topic. Using an SNS topic as a DLQ requires this property to be set explicitly. Default: - no SNS topic
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param environment_encryption: The AWS KMS key that's used to encrypt your function's environment variables. Default: - AWS Lambda creates and uses an AWS managed customer master key (CMK).
        :param ephemeral_storage_size: The size of the function’s /tmp directory in MiB. Default: 512 MiB
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param filesystem: The filesystem configuration for the lambda function. Default: - will not mount any filesystem
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param insights_version: Specify the version of CloudWatch Lambda insights to use for monitoring. Default: - No Lambda Insights
        :param ipv6_allowed_for_dual_stack: Allows outbound IPv6 traffic on VPC functions that are connected to dual-stack subnets. Only used if 'vpc' is supplied. Default: false
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by multiple functions. Default: - No layers.
        :param log_format: (deprecated) Sets the logFormat for the function. Default: "Text"
        :param logging_format: Sets the loggingFormat for the function. Default: LoggingFormat.TEXT
        :param log_group: The log group the function sends logs to. By default, Lambda functions send logs to an automatically created default log group named /aws/lambda/<function name>. However you cannot change the properties of this auto-created log group using the AWS CDK, e.g. you cannot set a different log retention. Use the ``logGroup`` property to create a fully customizable LogGroup ahead of time, and instruct the Lambda function to send logs to it. Providing a user-controlled log group was rolled out to commercial regions on 2023-11-16. If you are deploying to another type of region, please check regional availability first. Default: ``/aws/lambda/${this.functionName}`` - default log group created by Lambda
        :param log_removal_policy: (deprecated) Determine the removal policy of the log group that is auto-created by this construct. Normally you want to retain the log group so you can diagnose issues from logs even after a deployment that no longer includes the log group. In that case, use the normal date-based retention policy to age out your logs. Default: RemovalPolicy.Retain
        :param log_retention: (deprecated) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. This is a legacy API and we strongly recommend you move away from it if you can. Instead create a fully customizable log group with ``logs.LogGroup`` and use the ``logGroup`` property to instruct the Lambda function to send logs to it. Migrating from ``logRetention`` to ``logGroup`` will cause the name of the log group to change. Users and code and referencing the name verbatim will have to adjust. In AWS CDK code, you can access the log group name directly from the LogGroup construct:: import * as logs from 'aws-cdk-lib/aws-logs'; declare const myLogGroup: logs.LogGroup; myLogGroup.logGroupName; Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. This is a legacy API and we strongly recommend you migrate to ``logGroup`` if you can. ``logGroup`` allows you to create a fully customizable log group and instruct the Lambda function to send logs to it. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. This is a legacy API and we strongly recommend you migrate to ``logGroup`` if you can. ``logGroup`` allows you to create a fully customizable log group and instruct the Lambda function to send logs to it. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param params_and_secrets: Specify the configuration of Parameters and Secrets Extension. Default: - No Parameters and Secrets Extension
        :param profiling: Enable profiling. Default: - No profiling.
        :param profiling_group: Profiling Group. Default: - A new profiling group will be created if ``profiling`` is set.
        :param recursive_loop: Sets the Recursive Loop Protection for Lambda Function. It lets Lambda detect and terminate unintended recursive loops. Default: RecursiveLoop.Terminate
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param runtime_management_mode: Sets the runtime management configuration for a function's version. Default: Auto
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param snap_start: Enable SnapStart for Lambda Function. SnapStart is currently supported for Java 11, Java 17, Python 3.12, Python 3.13, and .NET 8 runtime Default: - No snapstart
        :param system_log_level: (deprecated) Sets the system log level for the function. Default: "INFO"
        :param system_log_level_v2: Sets the system log level for the function. Default: SystemLogLevel.INFO
        :param tenancy_config: The tenancy configuration for the function. Default: - Tenant isolation is not enabled
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. This is required when ``vpcSubnets`` is specified. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. This requires ``vpc`` to be specified in order for interfaces to actually be placed in the subnets. If ``vpc`` is not specify, this will raise an error. Note: Internet access for Lambda Functions requires a NAT Gateway, so picking public subnets is not allowed (unless ``allowPublicSubnet`` is set to ``true``). Default: - the Vpc default strategy if not specified
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e11a69c0d5d245d55f07c60c692fbfd3e6265da1da903ee1a2be252e092c50)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument resource_name", value=resource_name, expected_type=type_hints["resource_name"])
        props = RustFunctionProps(
            binary_name=binary_name,
            bundling=bundling,
            git_force_clone=git_force_clone,
            git_reference=git_reference,
            git_remote=git_remote,
            manifest_path=manifest_path,
            runtime=runtime,
            adot_instrumentation=adot_instrumentation,
            allow_all_ipv6_outbound=allow_all_ipv6_outbound,
            allow_all_outbound=allow_all_outbound,
            allow_public_subnet=allow_public_subnet,
            application_log_level=application_log_level,
            application_log_level_v2=application_log_level_v2,
            architecture=architecture,
            code_signing_config=code_signing_config,
            current_version_options=current_version_options,
            dead_letter_queue=dead_letter_queue,
            dead_letter_queue_enabled=dead_letter_queue_enabled,
            dead_letter_topic=dead_letter_topic,
            description=description,
            environment=environment,
            environment_encryption=environment_encryption,
            ephemeral_storage_size=ephemeral_storage_size,
            events=events,
            filesystem=filesystem,
            function_name=function_name,
            initial_policy=initial_policy,
            insights_version=insights_version,
            ipv6_allowed_for_dual_stack=ipv6_allowed_for_dual_stack,
            layers=layers,
            log_format=log_format,
            logging_format=logging_format,
            log_group=log_group,
            log_removal_policy=log_removal_policy,
            log_retention=log_retention,
            log_retention_retry_options=log_retention_retry_options,
            log_retention_role=log_retention_role,
            memory_size=memory_size,
            params_and_secrets=params_and_secrets,
            profiling=profiling,
            profiling_group=profiling_group,
            recursive_loop=recursive_loop,
            reserved_concurrent_executions=reserved_concurrent_executions,
            role=role,
            runtime_management_mode=runtime_management_mode,
            security_groups=security_groups,
            snap_start=snap_start,
            system_log_level=system_log_level,
            system_log_level_v2=system_log_level_v2,
            tenancy_config=tenancy_config,
            timeout=timeout,
            tracing=tracing,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
            max_event_age=max_event_age,
            on_failure=on_failure,
            on_success=on_success,
            retry_attempts=retry_attempts,
        )

        jsii.create(self.__class__, self, [scope, resource_name, props])


@jsii.data_type(
    jsii_type="cargo-lambda-cdk.RustFunctionProps",
    jsii_struct_bases=[_aws_cdk_aws_lambda_ceddda9d.FunctionOptions],
    name_mapping={
        "max_event_age": "maxEventAge",
        "on_failure": "onFailure",
        "on_success": "onSuccess",
        "retry_attempts": "retryAttempts",
        "adot_instrumentation": "adotInstrumentation",
        "allow_all_ipv6_outbound": "allowAllIpv6Outbound",
        "allow_all_outbound": "allowAllOutbound",
        "allow_public_subnet": "allowPublicSubnet",
        "application_log_level": "applicationLogLevel",
        "application_log_level_v2": "applicationLogLevelV2",
        "architecture": "architecture",
        "code_signing_config": "codeSigningConfig",
        "current_version_options": "currentVersionOptions",
        "dead_letter_queue": "deadLetterQueue",
        "dead_letter_queue_enabled": "deadLetterQueueEnabled",
        "dead_letter_topic": "deadLetterTopic",
        "description": "description",
        "environment": "environment",
        "environment_encryption": "environmentEncryption",
        "ephemeral_storage_size": "ephemeralStorageSize",
        "events": "events",
        "filesystem": "filesystem",
        "function_name": "functionName",
        "initial_policy": "initialPolicy",
        "insights_version": "insightsVersion",
        "ipv6_allowed_for_dual_stack": "ipv6AllowedForDualStack",
        "layers": "layers",
        "log_format": "logFormat",
        "logging_format": "loggingFormat",
        "log_group": "logGroup",
        "log_removal_policy": "logRemovalPolicy",
        "log_retention": "logRetention",
        "log_retention_retry_options": "logRetentionRetryOptions",
        "log_retention_role": "logRetentionRole",
        "memory_size": "memorySize",
        "params_and_secrets": "paramsAndSecrets",
        "profiling": "profiling",
        "profiling_group": "profilingGroup",
        "recursive_loop": "recursiveLoop",
        "reserved_concurrent_executions": "reservedConcurrentExecutions",
        "role": "role",
        "runtime_management_mode": "runtimeManagementMode",
        "security_groups": "securityGroups",
        "snap_start": "snapStart",
        "system_log_level": "systemLogLevel",
        "system_log_level_v2": "systemLogLevelV2",
        "tenancy_config": "tenancyConfig",
        "timeout": "timeout",
        "tracing": "tracing",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "binary_name": "binaryName",
        "bundling": "bundling",
        "git_force_clone": "gitForceClone",
        "git_reference": "gitReference",
        "git_remote": "gitRemote",
        "manifest_path": "manifestPath",
        "runtime": "runtime",
    },
)
class RustFunctionProps(_aws_cdk_aws_lambda_ceddda9d.FunctionOptions):
    def __init__(
        self,
        *,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        on_failure: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
        on_success: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        adot_instrumentation: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        allow_all_ipv6_outbound: typing.Optional[builtins.bool] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        allow_public_subnet: typing.Optional[builtins.bool] = None,
        application_log_level: typing.Optional[builtins.str] = None,
        application_log_level_v2: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ApplicationLogLevel] = None,
        architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
        code_signing_config: typing.Optional[_aws_cdk_interfaces_aws_lambda_ceddda9d.ICodeSigningConfigRef] = None,
        current_version_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.VersionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
        dead_letter_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment_encryption: typing.Optional[_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef] = None,
        ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        events: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.IEventSource]] = None,
        filesystem: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem] = None,
        function_name: typing.Optional[builtins.str] = None,
        initial_policy: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
        insights_version: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion] = None,
        ipv6_allowed_for_dual_stack: typing.Optional[builtins.bool] = None,
        layers: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]] = None,
        log_format: typing.Optional[builtins.str] = None,
        logging_format: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LoggingFormat] = None,
        log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
        log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        log_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        params_and_secrets: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ParamsAndSecretsLayerVersion] = None,
        profiling: typing.Optional[builtins.bool] = None,
        profiling_group: typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup] = None,
        recursive_loop: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RecursiveLoop] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        runtime_management_mode: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        snap_start: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.SnapStartConf] = None,
        system_log_level: typing.Optional[builtins.str] = None,
        system_log_level_v2: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.SystemLogLevel] = None,
        tenancy_config: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.TenancyConfig] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        tracing: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        binary_name: typing.Optional[builtins.str] = None,
        bundling: typing.Optional[typing.Union[BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_force_clone: typing.Optional[builtins.bool] = None,
        git_reference: typing.Optional[builtins.str] = None,
        git_remote: typing.Optional[builtins.str] = None,
        manifest_path: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for a RustFunction.

        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        :param adot_instrumentation: Specify the configuration of AWS Distro for OpenTelemetry (ADOT) instrumentation. Default: - No ADOT instrumentation
        :param allow_all_ipv6_outbound: Whether to allow the Lambda to send all ipv6 network traffic. If set to true, there will only be a single egress rule which allows all outbound ipv6 traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets using ipv6. Do not specify this property if the ``securityGroups`` or ``securityGroup`` property is set. Instead, configure ``allowAllIpv6Outbound`` directly on the security group. Default: false
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic (except ipv6). If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Do not specify this property if the ``securityGroups`` or ``securityGroup`` property is set. Instead, configure ``allowAllOutbound`` directly on the security group. Default: true
        :param allow_public_subnet: Lambda Functions in a public subnet can NOT access the internet. Use this property to acknowledge this limitation and still place the function in a public subnet. Default: false
        :param application_log_level: (deprecated) Sets the application log level for the function. Default: "INFO"
        :param application_log_level_v2: Sets the application log level for the function. Default: ApplicationLogLevel.INFO
        :param architecture: The system architectures compatible with this lambda function. Default: Architecture.X86_64
        :param code_signing_config: Code signing config associated with this function. Default: - Not Sign the Code
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. If SNS topic is desired, specify ``deadLetterTopic`` property instead. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param dead_letter_topic: The SNS topic to use as a DLQ. Note that if ``deadLetterQueueEnabled`` is set to ``true``, an SQS queue will be created rather than an SNS topic. Using an SNS topic as a DLQ requires this property to be set explicitly. Default: - no SNS topic
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param environment_encryption: The AWS KMS key that's used to encrypt your function's environment variables. Default: - AWS Lambda creates and uses an AWS managed customer master key (CMK).
        :param ephemeral_storage_size: The size of the function’s /tmp directory in MiB. Default: 512 MiB
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param filesystem: The filesystem configuration for the lambda function. Default: - will not mount any filesystem
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param insights_version: Specify the version of CloudWatch Lambda insights to use for monitoring. Default: - No Lambda Insights
        :param ipv6_allowed_for_dual_stack: Allows outbound IPv6 traffic on VPC functions that are connected to dual-stack subnets. Only used if 'vpc' is supplied. Default: false
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by multiple functions. Default: - No layers.
        :param log_format: (deprecated) Sets the logFormat for the function. Default: "Text"
        :param logging_format: Sets the loggingFormat for the function. Default: LoggingFormat.TEXT
        :param log_group: The log group the function sends logs to. By default, Lambda functions send logs to an automatically created default log group named /aws/lambda/<function name>. However you cannot change the properties of this auto-created log group using the AWS CDK, e.g. you cannot set a different log retention. Use the ``logGroup`` property to create a fully customizable LogGroup ahead of time, and instruct the Lambda function to send logs to it. Providing a user-controlled log group was rolled out to commercial regions on 2023-11-16. If you are deploying to another type of region, please check regional availability first. Default: ``/aws/lambda/${this.functionName}`` - default log group created by Lambda
        :param log_removal_policy: (deprecated) Determine the removal policy of the log group that is auto-created by this construct. Normally you want to retain the log group so you can diagnose issues from logs even after a deployment that no longer includes the log group. In that case, use the normal date-based retention policy to age out your logs. Default: RemovalPolicy.Retain
        :param log_retention: (deprecated) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. This is a legacy API and we strongly recommend you move away from it if you can. Instead create a fully customizable log group with ``logs.LogGroup`` and use the ``logGroup`` property to instruct the Lambda function to send logs to it. Migrating from ``logRetention`` to ``logGroup`` will cause the name of the log group to change. Users and code and referencing the name verbatim will have to adjust. In AWS CDK code, you can access the log group name directly from the LogGroup construct:: import * as logs from 'aws-cdk-lib/aws-logs'; declare const myLogGroup: logs.LogGroup; myLogGroup.logGroupName; Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. This is a legacy API and we strongly recommend you migrate to ``logGroup`` if you can. ``logGroup`` allows you to create a fully customizable log group and instruct the Lambda function to send logs to it. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. This is a legacy API and we strongly recommend you migrate to ``logGroup`` if you can. ``logGroup`` allows you to create a fully customizable log group and instruct the Lambda function to send logs to it. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param params_and_secrets: Specify the configuration of Parameters and Secrets Extension. Default: - No Parameters and Secrets Extension
        :param profiling: Enable profiling. Default: - No profiling.
        :param profiling_group: Profiling Group. Default: - A new profiling group will be created if ``profiling`` is set.
        :param recursive_loop: Sets the Recursive Loop Protection for Lambda Function. It lets Lambda detect and terminate unintended recursive loops. Default: RecursiveLoop.Terminate
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param runtime_management_mode: Sets the runtime management configuration for a function's version. Default: Auto
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param snap_start: Enable SnapStart for Lambda Function. SnapStart is currently supported for Java 11, Java 17, Python 3.12, Python 3.13, and .NET 8 runtime Default: - No snapstart
        :param system_log_level: (deprecated) Sets the system log level for the function. Default: "INFO"
        :param system_log_level_v2: Sets the system log level for the function. Default: SystemLogLevel.INFO
        :param tenancy_config: The tenancy configuration for the function. Default: - Tenant isolation is not enabled
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. This is required when ``vpcSubnets`` is specified. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. This requires ``vpc`` to be specified in order for interfaces to actually be placed in the subnets. If ``vpc`` is not specify, this will raise an error. Note: Internet access for Lambda Functions requires a NAT Gateway, so picking public subnets is not allowed (unless ``allowPublicSubnet`` is set to ``true``). Default: - the Vpc default strategy if not specified
        :param binary_name: The name of the binary to build, in case that's different than the package's name.
        :param bundling: Bundling options. Default: - use default bundling options
        :param git_force_clone: Always clone the repository if using the ``gitRemote`` option, even if it has already been cloned to the temporary directory. Default: - clones only if the repository and reference don't already exist in the temporary directory.
        :param git_reference: The git reference to checkout. This can be a branch, tag, or commit hash. If this option is not provided, ``git clone`` will run with the flag ``--depth 1``. Default: - the default branch, i.e. HEAD.
        :param git_remote: The git remote URL to clone (e.g ``https://github.com/your_user/your_repo``). This repository will be cloned to a temporary directory using ``git``. The ``git`` command must be available in the PATH.
        :param manifest_path: Path to a directory containing your Cargo.toml file, or to your Cargo.toml directly. This will accept a directory path containing a ``Cargo.toml`` file (i.e. ``path/to/package``), or a filepath to your ``Cargo.toml`` file (i.e. ``path/to/Cargo.toml``). When the ``gitRemote`` option is provided, the ``manifestPath`` is relative to the root of the git repository. Default: - check the current directory for a ``Cargo.toml`` file, and throws an error if the file doesn't exist.
        :param runtime: The Lambda runtime to deploy this function. ``provided.al2023`` is the default runtime when this option is not provided.
        '''
        if isinstance(adot_instrumentation, dict):
            adot_instrumentation = _aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig(**adot_instrumentation)
        if isinstance(current_version_options, dict):
            current_version_options = _aws_cdk_aws_lambda_ceddda9d.VersionOptions(**current_version_options)
        if isinstance(log_retention_retry_options, dict):
            log_retention_retry_options = _aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions(**log_retention_retry_options)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if isinstance(bundling, dict):
            bundling = BundlingOptions(**bundling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce05b09e0e93915b12c0bc3919562e2264107de41e44e4b205de18f57d5d8b63)
            check_type(argname="argument max_event_age", value=max_event_age, expected_type=type_hints["max_event_age"])
            check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
            check_type(argname="argument on_success", value=on_success, expected_type=type_hints["on_success"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument adot_instrumentation", value=adot_instrumentation, expected_type=type_hints["adot_instrumentation"])
            check_type(argname="argument allow_all_ipv6_outbound", value=allow_all_ipv6_outbound, expected_type=type_hints["allow_all_ipv6_outbound"])
            check_type(argname="argument allow_all_outbound", value=allow_all_outbound, expected_type=type_hints["allow_all_outbound"])
            check_type(argname="argument allow_public_subnet", value=allow_public_subnet, expected_type=type_hints["allow_public_subnet"])
            check_type(argname="argument application_log_level", value=application_log_level, expected_type=type_hints["application_log_level"])
            check_type(argname="argument application_log_level_v2", value=application_log_level_v2, expected_type=type_hints["application_log_level_v2"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument code_signing_config", value=code_signing_config, expected_type=type_hints["code_signing_config"])
            check_type(argname="argument current_version_options", value=current_version_options, expected_type=type_hints["current_version_options"])
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument dead_letter_queue_enabled", value=dead_letter_queue_enabled, expected_type=type_hints["dead_letter_queue_enabled"])
            check_type(argname="argument dead_letter_topic", value=dead_letter_topic, expected_type=type_hints["dead_letter_topic"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument environment_encryption", value=environment_encryption, expected_type=type_hints["environment_encryption"])
            check_type(argname="argument ephemeral_storage_size", value=ephemeral_storage_size, expected_type=type_hints["ephemeral_storage_size"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument filesystem", value=filesystem, expected_type=type_hints["filesystem"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument initial_policy", value=initial_policy, expected_type=type_hints["initial_policy"])
            check_type(argname="argument insights_version", value=insights_version, expected_type=type_hints["insights_version"])
            check_type(argname="argument ipv6_allowed_for_dual_stack", value=ipv6_allowed_for_dual_stack, expected_type=type_hints["ipv6_allowed_for_dual_stack"])
            check_type(argname="argument layers", value=layers, expected_type=type_hints["layers"])
            check_type(argname="argument log_format", value=log_format, expected_type=type_hints["log_format"])
            check_type(argname="argument logging_format", value=logging_format, expected_type=type_hints["logging_format"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument log_removal_policy", value=log_removal_policy, expected_type=type_hints["log_removal_policy"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument log_retention_retry_options", value=log_retention_retry_options, expected_type=type_hints["log_retention_retry_options"])
            check_type(argname="argument log_retention_role", value=log_retention_role, expected_type=type_hints["log_retention_role"])
            check_type(argname="argument memory_size", value=memory_size, expected_type=type_hints["memory_size"])
            check_type(argname="argument params_and_secrets", value=params_and_secrets, expected_type=type_hints["params_and_secrets"])
            check_type(argname="argument profiling", value=profiling, expected_type=type_hints["profiling"])
            check_type(argname="argument profiling_group", value=profiling_group, expected_type=type_hints["profiling_group"])
            check_type(argname="argument recursive_loop", value=recursive_loop, expected_type=type_hints["recursive_loop"])
            check_type(argname="argument reserved_concurrent_executions", value=reserved_concurrent_executions, expected_type=type_hints["reserved_concurrent_executions"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument runtime_management_mode", value=runtime_management_mode, expected_type=type_hints["runtime_management_mode"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument snap_start", value=snap_start, expected_type=type_hints["snap_start"])
            check_type(argname="argument system_log_level", value=system_log_level, expected_type=type_hints["system_log_level"])
            check_type(argname="argument system_log_level_v2", value=system_log_level_v2, expected_type=type_hints["system_log_level_v2"])
            check_type(argname="argument tenancy_config", value=tenancy_config, expected_type=type_hints["tenancy_config"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument tracing", value=tracing, expected_type=type_hints["tracing"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument binary_name", value=binary_name, expected_type=type_hints["binary_name"])
            check_type(argname="argument bundling", value=bundling, expected_type=type_hints["bundling"])
            check_type(argname="argument git_force_clone", value=git_force_clone, expected_type=type_hints["git_force_clone"])
            check_type(argname="argument git_reference", value=git_reference, expected_type=type_hints["git_reference"])
            check_type(argname="argument git_remote", value=git_remote, expected_type=type_hints["git_remote"])
            check_type(argname="argument manifest_path", value=manifest_path, expected_type=type_hints["manifest_path"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if on_success is not None:
            self._values["on_success"] = on_success
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if adot_instrumentation is not None:
            self._values["adot_instrumentation"] = adot_instrumentation
        if allow_all_ipv6_outbound is not None:
            self._values["allow_all_ipv6_outbound"] = allow_all_ipv6_outbound
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if allow_public_subnet is not None:
            self._values["allow_public_subnet"] = allow_public_subnet
        if application_log_level is not None:
            self._values["application_log_level"] = application_log_level
        if application_log_level_v2 is not None:
            self._values["application_log_level_v2"] = application_log_level_v2
        if architecture is not None:
            self._values["architecture"] = architecture
        if code_signing_config is not None:
            self._values["code_signing_config"] = code_signing_config
        if current_version_options is not None:
            self._values["current_version_options"] = current_version_options
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if dead_letter_queue_enabled is not None:
            self._values["dead_letter_queue_enabled"] = dead_letter_queue_enabled
        if dead_letter_topic is not None:
            self._values["dead_letter_topic"] = dead_letter_topic
        if description is not None:
            self._values["description"] = description
        if environment is not None:
            self._values["environment"] = environment
        if environment_encryption is not None:
            self._values["environment_encryption"] = environment_encryption
        if ephemeral_storage_size is not None:
            self._values["ephemeral_storage_size"] = ephemeral_storage_size
        if events is not None:
            self._values["events"] = events
        if filesystem is not None:
            self._values["filesystem"] = filesystem
        if function_name is not None:
            self._values["function_name"] = function_name
        if initial_policy is not None:
            self._values["initial_policy"] = initial_policy
        if insights_version is not None:
            self._values["insights_version"] = insights_version
        if ipv6_allowed_for_dual_stack is not None:
            self._values["ipv6_allowed_for_dual_stack"] = ipv6_allowed_for_dual_stack
        if layers is not None:
            self._values["layers"] = layers
        if log_format is not None:
            self._values["log_format"] = log_format
        if logging_format is not None:
            self._values["logging_format"] = logging_format
        if log_group is not None:
            self._values["log_group"] = log_group
        if log_removal_policy is not None:
            self._values["log_removal_policy"] = log_removal_policy
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if log_retention_retry_options is not None:
            self._values["log_retention_retry_options"] = log_retention_retry_options
        if log_retention_role is not None:
            self._values["log_retention_role"] = log_retention_role
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if params_and_secrets is not None:
            self._values["params_and_secrets"] = params_and_secrets
        if profiling is not None:
            self._values["profiling"] = profiling
        if profiling_group is not None:
            self._values["profiling_group"] = profiling_group
        if recursive_loop is not None:
            self._values["recursive_loop"] = recursive_loop
        if reserved_concurrent_executions is not None:
            self._values["reserved_concurrent_executions"] = reserved_concurrent_executions
        if role is not None:
            self._values["role"] = role
        if runtime_management_mode is not None:
            self._values["runtime_management_mode"] = runtime_management_mode
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if snap_start is not None:
            self._values["snap_start"] = snap_start
        if system_log_level is not None:
            self._values["system_log_level"] = system_log_level
        if system_log_level_v2 is not None:
            self._values["system_log_level_v2"] = system_log_level_v2
        if tenancy_config is not None:
            self._values["tenancy_config"] = tenancy_config
        if timeout is not None:
            self._values["timeout"] = timeout
        if tracing is not None:
            self._values["tracing"] = tracing
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if binary_name is not None:
            self._values["binary_name"] = binary_name
        if bundling is not None:
            self._values["bundling"] = bundling
        if git_force_clone is not None:
            self._values["git_force_clone"] = git_force_clone
        if git_reference is not None:
            self._values["git_reference"] = git_reference
        if git_remote is not None:
            self._values["git_remote"] = git_remote
        if manifest_path is not None:
            self._values["manifest_path"] = manifest_path
        if runtime is not None:
            self._values["runtime"] = runtime

    @builtins.property
    def max_event_age(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The maximum age of a request that Lambda sends to a function for processing.

        Minimum: 60 seconds
        Maximum: 6 hours

        :default: Duration.hours(6)
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def on_failure(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination]:
        '''The destination for failed invocations.

        :default: - no destination
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination], result)

    @builtins.property
    def on_success(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination]:
        '''The destination for successful invocations.

        :default: - no destination
        '''
        result = self._values.get("on_success")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of times to retry when the function returns an error.

        Minimum: 0
        Maximum: 2

        :default: 2
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def adot_instrumentation(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig]:
        '''Specify the configuration of AWS Distro for OpenTelemetry (ADOT) instrumentation.

        :default: - No ADOT instrumentation

        :see: https://aws-otel.github.io/docs/getting-started/lambda
        '''
        result = self._values.get("adot_instrumentation")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig], result)

    @builtins.property
    def allow_all_ipv6_outbound(self) -> typing.Optional[builtins.bool]:
        '''Whether to allow the Lambda to send all ipv6 network traffic.

        If set to true, there will only be a single egress rule which allows all
        outbound ipv6 traffic. If set to false, you must individually add traffic rules to allow the
        Lambda to connect to network targets using ipv6.

        Do not specify this property if the ``securityGroups`` or ``securityGroup`` property is set.
        Instead, configure ``allowAllIpv6Outbound`` directly on the security group.

        :default: false
        '''
        result = self._values.get("allow_all_ipv6_outbound")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[builtins.bool]:
        '''Whether to allow the Lambda to send all network traffic (except ipv6).

        If set to false, you must individually add traffic rules to allow the
        Lambda to connect to network targets.

        Do not specify this property if the ``securityGroups`` or ``securityGroup`` property is set.
        Instead, configure ``allowAllOutbound`` directly on the security group.

        :default: true
        '''
        result = self._values.get("allow_all_outbound")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_public_subnet(self) -> typing.Optional[builtins.bool]:
        '''Lambda Functions in a public subnet can NOT access the internet.

        Use this property to acknowledge this limitation and still place the function in a public subnet.

        :default: false

        :see: https://stackoverflow.com/questions/52992085/why-cant-an-aws-lambda-function-inside-a-public-subnet-in-a-vpc-connect-to-the/52994841#52994841
        '''
        result = self._values.get("allow_public_subnet")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def application_log_level(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Sets the application log level for the function.

        :default: "INFO"

        :deprecated: Use ``applicationLogLevelV2`` as a property instead.

        :stability: deprecated
        '''
        result = self._values.get("application_log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_log_level_v2(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ApplicationLogLevel]:
        '''Sets the application log level for the function.

        :default: ApplicationLogLevel.INFO
        '''
        result = self._values.get("application_log_level_v2")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ApplicationLogLevel], result)

    @builtins.property
    def architecture(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture]:
        '''The system architectures compatible with this lambda function.

        :default: Architecture.X86_64
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture], result)

    @builtins.property
    def code_signing_config(
        self,
    ) -> typing.Optional[_aws_cdk_interfaces_aws_lambda_ceddda9d.ICodeSigningConfigRef]:
        '''Code signing config associated with this function.

        :default: - Not Sign the Code
        '''
        result = self._values.get("code_signing_config")
        return typing.cast(typing.Optional[_aws_cdk_interfaces_aws_lambda_ceddda9d.ICodeSigningConfigRef], result)

    @builtins.property
    def current_version_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.VersionOptions]:
        '''Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method.

        :default: - default options as described in ``VersionOptions``
        '''
        result = self._values.get("current_version_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.VersionOptions], result)

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue]:
        '''The SQS queue to use if DLQ is enabled.

        If SNS topic is desired, specify ``deadLetterTopic`` property instead.

        :default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue], result)

    @builtins.property
    def dead_letter_queue_enabled(self) -> typing.Optional[builtins.bool]:
        '''Enabled DLQ.

        If ``deadLetterQueue`` is undefined,
        an SQS queue with default options will be defined for your Function.

        :default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        '''
        result = self._values.get("dead_letter_queue_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dead_letter_topic(self) -> typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic]:
        '''The SNS topic to use as a DLQ.

        Note that if ``deadLetterQueueEnabled`` is set to ``true``, an SQS queue will be created
        rather than an SNS topic. Using an SNS topic as a DLQ requires this property to be set explicitly.

        :default: - no SNS topic
        '''
        result = self._values.get("dead_letter_topic")
        return typing.cast(typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the function.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key-value pairs that Lambda caches and makes available for your Lambda functions.

        Use environment variables to apply configuration changes, such
        as test and production environment configurations, without changing your
        Lambda function source code.

        :default: - No environment variables.
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment_encryption(
        self,
    ) -> typing.Optional[_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef]:
        '''The AWS KMS key that's used to encrypt your function's environment variables.

        :default: - AWS Lambda creates and uses an AWS managed customer master key (CMK).
        '''
        result = self._values.get("environment_encryption")
        return typing.cast(typing.Optional[_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef], result)

    @builtins.property
    def ephemeral_storage_size(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''The size of the function’s /tmp directory in MiB.

        :default: 512 MiB
        '''
        result = self._values.get("ephemeral_storage_size")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], result)

    @builtins.property
    def events(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_lambda_ceddda9d.IEventSource]]:
        '''Event sources for this function.

        You can also add event sources using ``addEventSource``.

        :default: - No event sources.
        '''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_lambda_ceddda9d.IEventSource]], result)

    @builtins.property
    def filesystem(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem]:
        '''The filesystem configuration for the lambda function.

        :default: - will not mount any filesystem
        '''
        result = self._values.get("filesystem")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem], result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''A name for the function.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that
        ID for the function's name. For more information, see Name Type.
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_policy(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]]:
        '''Initial policy statements to add to the created Lambda Role.

        You can call ``addToRolePolicy`` to the created lambda to add statements post creation.

        :default: - No policy statements are added to the created Lambda role.
        '''
        result = self._values.get("initial_policy")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]], result)

    @builtins.property
    def insights_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion]:
        '''Specify the version of CloudWatch Lambda insights to use for monitoring.

        :default: - No Lambda Insights

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Lambda-Insights-Getting-Started-docker.html
        '''
        result = self._values.get("insights_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion], result)

    @builtins.property
    def ipv6_allowed_for_dual_stack(self) -> typing.Optional[builtins.bool]:
        '''Allows outbound IPv6 traffic on VPC functions that are connected to dual-stack subnets.

        Only used if 'vpc' is supplied.

        :default: false
        '''
        result = self._values.get("ipv6_allowed_for_dual_stack")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def layers(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]]:
        '''A list of layers to add to the function's execution environment.

        You can configure your Lambda function to pull in
        additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies
        that can be used by multiple functions.

        :default: - No layers.
        '''
        result = self._values.get("layers")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]], result)

    @builtins.property
    def log_format(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Sets the logFormat for the function.

        :default: "Text"

        :deprecated: Use ``loggingFormat`` as a property instead.

        :stability: deprecated
        '''
        result = self._values.get("log_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_format(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LoggingFormat]:
        '''Sets the loggingFormat for the function.

        :default: LoggingFormat.TEXT
        '''
        result = self._values.get("logging_format")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LoggingFormat], result)

    @builtins.property
    def log_group(self) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup]:
        '''The log group the function sends logs to.

        By default, Lambda functions send logs to an automatically created default log group named /aws/lambda/.
        However you cannot change the properties of this auto-created log group using the AWS CDK, e.g. you cannot set a different log retention.

        Use the ``logGroup`` property to create a fully customizable LogGroup ahead of time, and instruct the Lambda function to send logs to it.

        Providing a user-controlled log group was rolled out to commercial regions on 2023-11-16.
        If you are deploying to another type of region, please check regional availability first.

        :default: ``/aws/lambda/${this.functionName}`` - default log group created by Lambda
        '''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup], result)

    @builtins.property
    def log_removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''(deprecated) Determine the removal policy of the log group that is auto-created by this construct.

        Normally you want to retain the log group so you can diagnose issues
        from logs even after a deployment that no longer includes the log group.
        In that case, use the normal date-based retention policy to age out your
        logs.

        :default: RemovalPolicy.Retain

        :deprecated: use ``logGroup`` instead

        :stability: deprecated
        '''
        result = self._values.get("log_removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''(deprecated) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        This is a legacy API and we strongly recommend you move away from it if you can.
        Instead create a fully customizable log group with ``logs.LogGroup`` and use the ``logGroup`` property
        to instruct the Lambda function to send logs to it.
        Migrating from ``logRetention`` to ``logGroup`` will cause the name of the log group to change.
        Users and code and referencing the name verbatim will have to adjust.

        In AWS CDK code, you can access the log group name directly from the LogGroup construct::

           import * as logs from 'aws-cdk-lib/aws-logs';

           declare const myLogGroup: logs.LogGroup;
           myLogGroup.logGroupName;

        :default: logs.RetentionDays.INFINITE

        :deprecated: use ``logGroup`` instead

        :stability: deprecated
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def log_retention_retry_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions]:
        '''When log retention is specified, a custom resource attempts to create the CloudWatch log group.

        These options control the retry policy when interacting with CloudWatch APIs.

        This is a legacy API and we strongly recommend you migrate to ``logGroup`` if you can.
        ``logGroup`` allows you to create a fully customizable log group and instruct the Lambda function to send logs to it.

        :default: - Default AWS SDK retry options.
        '''
        result = self._values.get("log_retention_retry_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions], result)

    @builtins.property
    def log_retention_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        This is a legacy API and we strongly recommend you migrate to ``logGroup`` if you can.
        ``logGroup`` allows you to create a fully customizable log group and instruct the Lambda function to send logs to it.

        :default: - A new role is created.
        '''
        result = self._values.get("log_retention_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        '''The amount of memory, in MB, that is allocated to your Lambda function.

        Lambda uses this value to proportionally allocate the amount of CPU
        power. For more information, see Resource Model in the AWS Lambda
        Developer Guide.

        :default: 128
        '''
        result = self._values.get("memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def params_and_secrets(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ParamsAndSecretsLayerVersion]:
        '''Specify the configuration of Parameters and Secrets Extension.

        :default: - No Parameters and Secrets Extension

        :see: https://docs.aws.amazon.com/systems-manager/latest/userguide/ps-integration-lambda-extensions.html
        '''
        result = self._values.get("params_and_secrets")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ParamsAndSecretsLayerVersion], result)

    @builtins.property
    def profiling(self) -> typing.Optional[builtins.bool]:
        '''Enable profiling.

        :default: - No profiling.

        :see: https://docs.aws.amazon.com/codeguru/latest/profiler-ug/setting-up-lambda.html
        '''
        result = self._values.get("profiling")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def profiling_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup]:
        '''Profiling Group.

        :default: - A new profiling group will be created if ``profiling`` is set.

        :see: https://docs.aws.amazon.com/codeguru/latest/profiler-ug/setting-up-lambda.html
        '''
        result = self._values.get("profiling_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup], result)

    @builtins.property
    def recursive_loop(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RecursiveLoop]:
        '''Sets the Recursive Loop Protection for Lambda Function.

        It lets Lambda detect and terminate unintended recursive loops.

        :default: RecursiveLoop.Terminate
        '''
        result = self._values.get("recursive_loop")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RecursiveLoop], result)

    @builtins.property
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        '''The maximum of concurrent executions you want to reserve for the function.

        :default: - No specific limit - account limit.

        :see: https://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html
        '''
        result = self._values.get("reserved_concurrent_executions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''Lambda execution role.

        This is the role that will be assumed by the function upon execution.
        It controls the permissions that the function will have. The Role must
        be assumable by the 'lambda.amazonaws.com' service principal.

        The default Role automatically has permissions granted for Lambda execution. If you
        provide a Role, you must add the relevant AWS managed policies yourself.

        The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and
        "service-role/AWSLambdaVPCAccessExecutionRole".

        :default:

        - A unique role will be generated for this lambda function.
        Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def runtime_management_mode(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode]:
        '''Sets the runtime management configuration for a function's version.

        :default: Auto
        '''
        result = self._values.get("runtime_management_mode")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''The list of security groups to associate with the Lambda's network interfaces.

        Only used if 'vpc' is supplied.

        :default:

        - If the function is placed within a VPC and a security group is
        not specified, either by this or securityGroup prop, a dedicated security
        group will be created for this function.
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def snap_start(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.SnapStartConf]:
        '''Enable SnapStart for Lambda Function.

        SnapStart is currently supported for Java 11, Java 17, Python 3.12, Python 3.13, and .NET 8 runtime

        :default: - No snapstart
        '''
        result = self._values.get("snap_start")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.SnapStartConf], result)

    @builtins.property
    def system_log_level(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Sets the system log level for the function.

        :default: "INFO"

        :deprecated: Use ``systemLogLevelV2`` as a property instead.

        :stability: deprecated
        '''
        result = self._values.get("system_log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def system_log_level_v2(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.SystemLogLevel]:
        '''Sets the system log level for the function.

        :default: SystemLogLevel.INFO
        '''
        result = self._values.get("system_log_level_v2")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.SystemLogLevel], result)

    @builtins.property
    def tenancy_config(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.TenancyConfig]:
        '''The tenancy configuration for the function.

        :default: - Tenant isolation is not enabled
        '''
        result = self._values.get("tenancy_config")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.TenancyConfig], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The function execution time (in seconds) after which Lambda terminates the function.

        Because the execution time affects cost, set this value
        based on the function's expected execution time.

        :default: Duration.seconds(3)
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def tracing(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing]:
        '''Enable AWS X-Ray Tracing for Lambda Function.

        :default: Tracing.Disabled
        '''
        result = self._values.get("tracing")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''VPC network to place Lambda network interfaces.

        Specify this if the Lambda function needs to access resources in a VPC.
        This is required when ``vpcSubnets`` is specified.

        :default: - Function is not placed within a VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Where to place the network interfaces within the VPC.

        This requires ``vpc`` to be specified in order for interfaces to actually be
        placed in the subnets. If ``vpc`` is not specify, this will raise an error.

        Note: Internet access for Lambda Functions requires a NAT Gateway, so picking
        public subnets is not allowed (unless ``allowPublicSubnet`` is set to ``true``).

        :default: - the Vpc default strategy if not specified
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def binary_name(self) -> typing.Optional[builtins.str]:
        '''The name of the binary to build, in case that's different than the package's name.'''
        result = self._values.get("binary_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bundling(self) -> typing.Optional[BundlingOptions]:
        '''Bundling options.

        :default: - use default bundling options
        '''
        result = self._values.get("bundling")
        return typing.cast(typing.Optional[BundlingOptions], result)

    @builtins.property
    def git_force_clone(self) -> typing.Optional[builtins.bool]:
        '''Always clone the repository if using the ``gitRemote`` option, even if it has already been cloned to the temporary directory.

        :default:

        - clones only if the repository and reference don't already exist in the
        temporary directory.
        '''
        result = self._values.get("git_force_clone")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def git_reference(self) -> typing.Optional[builtins.str]:
        '''The git reference to checkout. This can be a branch, tag, or commit hash.

        If this option is not provided, ``git clone`` will run with the flag ``--depth 1``.

        :default: - the default branch, i.e. HEAD.
        '''
        result = self._values.get("git_reference")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def git_remote(self) -> typing.Optional[builtins.str]:
        '''The git remote URL to clone (e.g ``https://github.com/your_user/your_repo``).

        This repository will be cloned to a temporary directory using ``git``.
        The ``git`` command must be available in the PATH.
        '''
        result = self._values.get("git_remote")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manifest_path(self) -> typing.Optional[builtins.str]:
        '''Path to a directory containing your Cargo.toml file, or to your Cargo.toml directly.

        This will accept a directory path containing a ``Cargo.toml`` file (i.e. ``path/to/package``), or a filepath to your
        ``Cargo.toml`` file (i.e. ``path/to/Cargo.toml``). When the ``gitRemote`` option is provided,
        the ``manifestPath`` is relative to the root of the git repository.

        :default:

        - check the current directory for a ``Cargo.toml`` file, and throws
        an error if the file doesn't exist.
        '''
        result = self._values.get("manifest_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime(self) -> typing.Optional[builtins.str]:
        '''The Lambda runtime to deploy this function.

        ``provided.al2023`` is the default runtime when this option is not provided.
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RustFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BundlingOptions",
    "DockerOptions",
    "ICommandHooks",
    "RustExtension",
    "RustExtensionProps",
    "RustFunction",
    "RustFunctionProps",
]

publication.publish()

def _typecheckingstub__fc2a6c6dd24cf837b6f0878c1b4e0f074ca279a120ea990184a41c87f7ac194e(
    *,
    architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    asset_hash: typing.Optional[builtins.str] = None,
    asset_hash_type: typing.Optional[_aws_cdk_ceddda9d.AssetHashType] = None,
    cargo_lambda_flags: typing.Optional[typing.Sequence[builtins.str]] = None,
    command_hooks: typing.Optional[ICommandHooks] = None,
    docker_image: typing.Optional[_aws_cdk_ceddda9d.DockerImage] = None,
    docker_options: typing.Optional[typing.Union[DockerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    forced_docker_bundling: typing.Optional[builtins.bool] = None,
    profile: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9608948da2f06b0fe8270c43af6a8cbb901d1c575d80a4b4c105ecda990db16a(
    *,
    bundling_file_access: typing.Optional[_aws_cdk_ceddda9d.BundlingFileAccess] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    entrypoint: typing.Optional[typing.Sequence[builtins.str]] = None,
    local: typing.Optional[_aws_cdk_ceddda9d.ILocalBundling] = None,
    network: typing.Optional[builtins.str] = None,
    output_type: typing.Optional[_aws_cdk_ceddda9d.BundlingOutput] = None,
    security_opt: typing.Optional[builtins.str] = None,
    user: typing.Optional[builtins.str] = None,
    volumes: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.DockerVolume, typing.Dict[builtins.str, typing.Any]]]] = None,
    volumes_from: typing.Optional[typing.Sequence[builtins.str]] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1918f878e4aac2385f37417656a44758d0ddb4a69d8a8a080ad86e60d2cf428(
    input_dir: builtins.str,
    output_dir: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d44f2505868fcf80b775a2e2d0015bc87f81e99c549085cda9d746824b47cc0(
    input_dir: builtins.str,
    output_dir: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21f62266a88faf67f2b45cdf0580cdde98fc18292f1cd3c32b36632326f08e6(
    scope: _constructs_77d1e7e8.Construct,
    resource_name: builtins.str,
    *,
    architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    binary_name: typing.Optional[builtins.str] = None,
    bundling: typing.Optional[typing.Union[BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    git_force_clone: typing.Optional[builtins.bool] = None,
    git_reference: typing.Optional[builtins.str] = None,
    git_remote: typing.Optional[builtins.str] = None,
    manifest_path: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    layer_version_name: typing.Optional[builtins.str] = None,
    license: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae4fa0990c966d31ff57b3beb0811674913f8456aed00ffb0498414ca7e1eef(
    *,
    description: typing.Optional[builtins.str] = None,
    layer_version_name: typing.Optional[builtins.str] = None,
    license: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    binary_name: typing.Optional[builtins.str] = None,
    bundling: typing.Optional[typing.Union[BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    git_force_clone: typing.Optional[builtins.bool] = None,
    git_reference: typing.Optional[builtins.str] = None,
    git_remote: typing.Optional[builtins.str] = None,
    manifest_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e11a69c0d5d245d55f07c60c692fbfd3e6265da1da903ee1a2be252e092c50(
    scope: _constructs_77d1e7e8.Construct,
    resource_name: builtins.str,
    *,
    binary_name: typing.Optional[builtins.str] = None,
    bundling: typing.Optional[typing.Union[BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    git_force_clone: typing.Optional[builtins.bool] = None,
    git_reference: typing.Optional[builtins.str] = None,
    git_remote: typing.Optional[builtins.str] = None,
    manifest_path: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[builtins.str] = None,
    adot_instrumentation: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    allow_all_ipv6_outbound: typing.Optional[builtins.bool] = None,
    allow_all_outbound: typing.Optional[builtins.bool] = None,
    allow_public_subnet: typing.Optional[builtins.bool] = None,
    application_log_level: typing.Optional[builtins.str] = None,
    application_log_level_v2: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ApplicationLogLevel] = None,
    architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    code_signing_config: typing.Optional[_aws_cdk_interfaces_aws_lambda_ceddda9d.ICodeSigningConfigRef] = None,
    current_version_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.VersionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
    dead_letter_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
    description: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment_encryption: typing.Optional[_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef] = None,
    ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    events: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.IEventSource]] = None,
    filesystem: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem] = None,
    function_name: typing.Optional[builtins.str] = None,
    initial_policy: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
    insights_version: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion] = None,
    ipv6_allowed_for_dual_stack: typing.Optional[builtins.bool] = None,
    layers: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]] = None,
    log_format: typing.Optional[builtins.str] = None,
    logging_format: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LoggingFormat] = None,
    log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    log_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    params_and_secrets: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ParamsAndSecretsLayerVersion] = None,
    profiling: typing.Optional[builtins.bool] = None,
    profiling_group: typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup] = None,
    recursive_loop: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RecursiveLoop] = None,
    reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    runtime_management_mode: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    snap_start: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.SnapStartConf] = None,
    system_log_level: typing.Optional[builtins.str] = None,
    system_log_level_v2: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.SystemLogLevel] = None,
    tenancy_config: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.TenancyConfig] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    tracing: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    on_failure: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    on_success: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce05b09e0e93915b12c0bc3919562e2264107de41e44e4b205de18f57d5d8b63(
    *,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    on_failure: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    on_success: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    adot_instrumentation: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    allow_all_ipv6_outbound: typing.Optional[builtins.bool] = None,
    allow_all_outbound: typing.Optional[builtins.bool] = None,
    allow_public_subnet: typing.Optional[builtins.bool] = None,
    application_log_level: typing.Optional[builtins.str] = None,
    application_log_level_v2: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ApplicationLogLevel] = None,
    architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    code_signing_config: typing.Optional[_aws_cdk_interfaces_aws_lambda_ceddda9d.ICodeSigningConfigRef] = None,
    current_version_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.VersionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
    dead_letter_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
    description: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment_encryption: typing.Optional[_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef] = None,
    ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    events: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.IEventSource]] = None,
    filesystem: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem] = None,
    function_name: typing.Optional[builtins.str] = None,
    initial_policy: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
    insights_version: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion] = None,
    ipv6_allowed_for_dual_stack: typing.Optional[builtins.bool] = None,
    layers: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]] = None,
    log_format: typing.Optional[builtins.str] = None,
    logging_format: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LoggingFormat] = None,
    log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    log_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    params_and_secrets: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ParamsAndSecretsLayerVersion] = None,
    profiling: typing.Optional[builtins.bool] = None,
    profiling_group: typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup] = None,
    recursive_loop: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RecursiveLoop] = None,
    reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    runtime_management_mode: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    snap_start: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.SnapStartConf] = None,
    system_log_level: typing.Optional[builtins.str] = None,
    system_log_level_v2: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.SystemLogLevel] = None,
    tenancy_config: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.TenancyConfig] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    tracing: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    binary_name: typing.Optional[builtins.str] = None,
    bundling: typing.Optional[typing.Union[BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    git_force_clone: typing.Optional[builtins.bool] = None,
    git_reference: typing.Optional[builtins.str] = None,
    git_remote: typing.Optional[builtins.str] = None,
    manifest_path: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

for cls in [ICommandHooks]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
