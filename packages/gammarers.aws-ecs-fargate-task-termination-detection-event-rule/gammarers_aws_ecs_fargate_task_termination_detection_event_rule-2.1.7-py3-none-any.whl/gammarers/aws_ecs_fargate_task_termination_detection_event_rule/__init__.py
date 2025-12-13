r'''
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

import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import constructs as _constructs_77d1e7e8


class EcsFargateTaskTerminationDetectionEventRule(
    _aws_cdk_aws_events_ceddda9d.Rule,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gammarers/aws-ecs-fargate-task-termination-detection-event-rule.EcsFargateTaskTerminationDetectionEventRule",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cluster_arn: builtins.str,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
        schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
        targets: typing.Optional[typing.Sequence[_aws_cdk_aws_events_ceddda9d.IRuleTarget]] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster_arn: 
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param schedule: The schedule or rate (frequency) that determines when EventBridge runs the rule. You must specify this property, the ``eventPattern`` property, or both. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a80ea40a3b881f698925f2b4626e78c41b04a8d40affb062a43af3a674e2e25)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EcsFargateTaskTerminationDetectionEventRuleProps(
            cluster_arn=cluster_arn,
            enabled=enabled,
            event_bus=event_bus,
            schedule=schedule,
            targets=targets,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@gammarers/aws-ecs-fargate-task-termination-detection-event-rule.EcsFargateTaskTerminationDetectionEventRuleProps",
    jsii_struct_bases=[_aws_cdk_aws_events_ceddda9d.RuleProps],
    name_mapping={
        "cross_stack_scope": "crossStackScope",
        "description": "description",
        "event_pattern": "eventPattern",
        "rule_name": "ruleName",
        "enabled": "enabled",
        "event_bus": "eventBus",
        "schedule": "schedule",
        "targets": "targets",
        "cluster_arn": "clusterArn",
    },
)
class EcsFargateTaskTerminationDetectionEventRuleProps(
    _aws_cdk_aws_events_ceddda9d.RuleProps,
):
    def __init__(
        self,
        *,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
        schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
        targets: typing.Optional[typing.Sequence[_aws_cdk_aws_events_ceddda9d.IRuleTarget]] = None,
        cluster_arn: builtins.str,
    ) -> None:
        '''
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param schedule: The schedule or rate (frequency) that determines when EventBridge runs the rule. You must specify this property, the ``eventPattern`` property, or both. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.
        :param cluster_arn: 

        :TODO:

        : Not yet supported Omit
        https://github.com/aws/jsii/issues/4468
        type omitKeys = 'eventPattern';
        export interface CodePipelineStateChangeDetectionEventRuleProps extends Omit<events.RuleProps, 'eventPattern'> {}
        '''
        if isinstance(event_pattern, dict):
            event_pattern = _aws_cdk_aws_events_ceddda9d.EventPattern(**event_pattern)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c54d20c8ea14d4c07021cd6fa86e163f657334eb07f1a8783861a38950d677a)
            check_type(argname="argument cross_stack_scope", value=cross_stack_scope, expected_type=type_hints["cross_stack_scope"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument event_pattern", value=event_pattern, expected_type=type_hints["event_pattern"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument event_bus", value=event_bus, expected_type=type_hints["event_bus"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            check_type(argname="argument cluster_arn", value=cluster_arn, expected_type=type_hints["cluster_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_arn": cluster_arn,
        }
        if cross_stack_scope is not None:
            self._values["cross_stack_scope"] = cross_stack_scope
        if description is not None:
            self._values["description"] = description
        if event_pattern is not None:
            self._values["event_pattern"] = event_pattern
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if enabled is not None:
            self._values["enabled"] = enabled
        if event_bus is not None:
            self._values["event_bus"] = event_bus
        if schedule is not None:
            self._values["schedule"] = schedule
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def cross_stack_scope(self) -> typing.Optional[_constructs_77d1e7e8.Construct]:
        '''The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region).

        This helps dealing with cycles that often arise in these situations.

        :default: - none (the main scope will be used, even for cross-stack Events)
        '''
        result = self._values.get("cross_stack_scope")
        return typing.cast(typing.Optional[_constructs_77d1e7e8.Construct], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the rule's purpose.

        :default: - No description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_pattern(
        self,
    ) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.EventPattern]:
        '''Additional restrictions for the event to route to the specified target.

        The method that generates the rule probably imposes some type of event
        filtering. The filtering implied by what you pass here is added
        on top of that filtering.

        :default: - No additional filtering based on an event pattern.

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html
        '''
        result = self._values.get("event_pattern")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.EventPattern], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''A name for the rule.

        :default: AWS CloudFormation generates a unique physical ID.
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the rule is enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def event_bus(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus]:
        '''The event bus to associate with this rule.

        :default: - The default event bus.
        '''
        result = self._values.get("event_bus")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus], result)

    @builtins.property
    def schedule(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule]:
        '''The schedule or rate (frequency) that determines when EventBridge runs the rule.

        You must specify this property, the ``eventPattern`` property, or both.

        For more information, see Schedule Expression Syntax for
        Rules in the Amazon EventBridge User Guide.

        :default: - None.

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/scheduled-events.html
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule], result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_events_ceddda9d.IRuleTarget]]:
        '''Targets to invoke when this rule matches an event.

        Input will be the full matched event. If you wish to specify custom
        target input, use ``addTarget(target[, inputOptions])``.

        :default: - No targets.
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_events_ceddda9d.IRuleTarget]], result)

    @builtins.property
    def cluster_arn(self) -> builtins.str:
        result = self._values.get("cluster_arn")
        assert result is not None, "Required property 'cluster_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsFargateTaskTerminationDetectionEventRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EcsFargateTaskTerminationDetectionEventRule",
    "EcsFargateTaskTerminationDetectionEventRuleProps",
]

publication.publish()

def _typecheckingstub__7a80ea40a3b881f698925f2b4626e78c41b04a8d40affb062a43af3a674e2e25(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cluster_arn: builtins.str,
    enabled: typing.Optional[builtins.bool] = None,
    event_bus: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
    schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
    targets: typing.Optional[typing.Sequence[_aws_cdk_aws_events_ceddda9d.IRuleTarget]] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c54d20c8ea14d4c07021cd6fa86e163f657334eb07f1a8783861a38950d677a(
    *,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    event_bus: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
    schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
    targets: typing.Optional[typing.Sequence[_aws_cdk_aws_events_ceddda9d.IRuleTarget]] = None,
    cluster_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
