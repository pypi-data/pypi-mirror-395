import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "gammarers.aws-ecs-fargate-task-termination-detection-event-rule",
    "version": "2.1.7",
    "description": "This an AWS ECS Fargate task termination detection Event Rule.",
    "license": "Apache-2.0",
    "url": "https://github.com/gammarers/aws-ecs-fargate-task-termination-detection-event-rule.git",
    "long_description_content_type": "text/markdown",
    "author": "yicr<yicr@users.noreply.github.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/gammarers/aws-ecs-fargate-task-termination-detection-event-rule.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "gammarers.aws_ecs_fargate_task_termination_detection_event_rule",
        "gammarers.aws_ecs_fargate_task_termination_detection_event_rule._jsii"
    ],
    "package_data": {
        "gammarers.aws_ecs_fargate_task_termination_detection_event_rule._jsii": [
            "aws-ecs-fargate-task-termination-detection-event-rule@2.1.7.jsii.tgz"
        ],
        "gammarers.aws_ecs_fargate_task_termination_detection_event_rule": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.189.1, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "gammarers.aws-cdk-errors>=1.2.0, <2.0.0",
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
