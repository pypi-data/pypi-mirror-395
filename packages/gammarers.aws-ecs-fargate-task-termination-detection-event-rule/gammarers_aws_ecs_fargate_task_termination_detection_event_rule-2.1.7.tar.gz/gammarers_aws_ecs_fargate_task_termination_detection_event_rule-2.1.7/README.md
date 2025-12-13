# AWS ECS Fargate task termination detection event rule

[![GitHub](https://img.shields.io/github/license/gammarers/aws-ecs-fargate-task-termination-detection-event-rule?style=flat-square)](https://github.com/gammarers/aws-ecs-fargate-task-termination-detection-event-rule/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarers/aws-ecs-fargate-task-termination-detection-event-rule?style=flat-square)](https://www.npmjs.com/package/@gammarers/aws-ecs-fargate-task-termination-detection-event-rule)
[![PyPI](https://img.shields.io/pypi/v/gammarers.aws-ecs-fargate-task-termination-detection-event-rule?style=flat-square)](https://pypi.org/project/gammarers.aws-ecs-fargate-task-termination-detection-event-rule/)
[![Nuget](https://img.shields.io/nuget/v/Gammarers.CDK.AWS.EcsFargateTaskTerminationDetectionEventRule?style=flat-square)](https://www.nuget.org/packages/Gammarers.CDK.AWS.EcsFargateTaskTerminationDetectionEventRule/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/gammarers/aws-ecs-fargate-task-termination-detection-event-rule/release.yml?branch=main&label=release&style=flat-square)](https://github.com/gammarers/aws-ecs-fargate-task-termination-detection-event-rule/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/gammarers/aws-ecs-fargate-task-termination-detection-event-rule?sort=semver&style=flat-square)](https://github.com/gammarers/aws-ecs-fargate-task-termination-detection-event-rule/releases)

[![View on Construct Hub](https://constructs.dev/badge?package=@gammarers/aws-ecs-fargate-task-termination-detection-event-rule)](https://constructs.dev/packages/@gammarers/aws-ecs-fargate-task-termination-detection-event-rule)

This an AWS ECS Fargate task termination detection Event Rule.

## Install

### TypeScript

#### install by npm

```shell
npm install @gammarers/aws-ecs-fargate-task-termination-detection-event-rule
```

#### install by yarn

```shell
yarn add @gammarers/aws-ecs-fargate-task-termination-detection-event-rule
```

#### install by pnpm

```shell
pnpm add @gammarers/aws-ecs-fargate-task-termination-detection-event-rule
```

#### install by bun

```shell
bun add @gammarers/aws-ecs-fargate-task-termination-detection-event-rule
```

### Python

```shell
pip install gammarers.aws-ecs-fargate-task-termination-detection-event-rule
```

### C# / .NET

```shell
dotnet add package Gammarers.CDK.AWS.EcsFargateTaskTerminationDetectionEventRule
```

## Example

```python
import { EcsFargateTaskTerminationDetectionEventRule } from '@gammarers/aws-ecs-fargate-task-termination-detection-event-rule';

const clusterArn = 'arn:aws:ecs:us-east-1:123456789012:cluster/example-app-cluster';

const rule = new EcsFargateTaskTerminationDetectionEventRule(stack, 'EcsFargateTaskTerminationDetectionEventRule', {
  ruleName: 'example-event-rule',
  description: 'example event rule.',
  clusterArn,
});
```

## License

This project is licensed under the Apache-2.0 License.
