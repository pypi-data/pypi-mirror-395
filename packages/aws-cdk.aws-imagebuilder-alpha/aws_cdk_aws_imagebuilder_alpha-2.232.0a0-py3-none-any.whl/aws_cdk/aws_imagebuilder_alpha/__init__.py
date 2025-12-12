r'''
# EC2 Image Builder Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## README

[Amazon EC2 Image Builder](https://docs.aws.amazon.com/imagebuilder/latest/userguide/what-is-image-builder.html) is a
fully managed AWS service that helps you automate the creation, management, and deployment of customized, secure, and
up-to-date server images. You can use Image Builder to create Amazon Machine Images (AMIs) and container images for use
across AWS Regions.

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project. It allows you to define
Image Builder pipelines, images, recipes, components, workflows, and lifecycle policies.
A component defines the sequence of steps required to customize an instance during image creation (build component) or
test an instance launched from the created image (test component). Components are created from declarative YAML or JSON
documents that describe runtime configuration for building, validating, or testing instances. Components are included
when added to the image recipe or container recipe for an image build.

EC2 Image Builder supports AWS-managed components for common tasks, AWS Marketplace components, and custom components
that you create. Components run during specific workflow phases: build and validate phases during the build stage, and
test phase during the test stage.

### Image Pipeline

An image pipeline provides the automation framework for building secure AMIs and container images. The pipeline
orchestrates the entire image creation process by combining an image recipe or container recipe with infrastructure
configuration and distribution configuration. Pipelines can run on a schedule or be triggered manually, and they manage
the build, test, and distribution phases automatically.

#### Image Pipeline Basic Usage

Create a simple AMI pipeline with just an image recipe:

```python
image_recipe = imagebuilder.ImageRecipe(self, "MyImageRecipe",
    base_image=imagebuilder.BaseImage.from_ssm_parameter_name("/aws/service/ami-amazon-linux-latest/al2023-ami-minimal-kernel-default-x86_64")
)

image_pipeline = imagebuilder.ImagePipeline(self, "MyImagePipeline",
    recipe=example_image_recipe
)
```

Create a simple container pipeline with just a container recipe:

```python
container_recipe = imagebuilder.ContainerRecipe(self, "MyContainerRecipe",
    base_image=imagebuilder.BaseContainerImage.from_docker_hub("amazonlinux", "latest"),
    target_repository=imagebuilder.Repository.from_ecr(
        ecr.Repository.from_repository_name(self, "Repository", "my-container-repo"))
)

container_pipeline = imagebuilder.ImagePipeline(self, "MyContainerPipeline",
    recipe=example_container_recipe
)
```

#### Image Pipeline Scheduling

##### Manual Pipeline Execution

Create a pipeline that runs only when manually triggered:

```python
manual_pipeline = imagebuilder.ImagePipeline(self, "ManualPipeline",
    image_pipeline_name="my-manual-pipeline",
    description="Pipeline triggered manually for production builds",
    recipe=example_image_recipe
)

# Grant Lambda function permission to trigger the pipeline
manual_pipeline.grant_start_execution(lambda_role)
```

##### Automated Pipeline Scheduling

Schedule a pipeline to run automatically using cron expressions:

```python
weekly_pipeline = imagebuilder.ImagePipeline(self, "WeeklyPipeline",
    image_pipeline_name="weekly-build-pipeline",
    recipe=example_image_recipe,
    schedule=imagebuilder.ImagePipelineSchedule(
        expression=events.Schedule.cron(
            minute="0",
            hour="6",
            week_day="MON"
        )
    )
)
```

Use rate expressions for regular intervals:

```python
daily_pipeline = imagebuilder.ImagePipeline(self, "DailyPipeline",
    recipe=example_container_recipe,
    schedule=imagebuilder.ImagePipelineSchedule(
        expression=events.Schedule.rate(Duration.days(1))
    )
)
```

##### Pipeline Schedule Configuration

Configure advanced scheduling options:

```python
advanced_schedule_pipeline = imagebuilder.ImagePipeline(self, "AdvancedSchedulePipeline",
    recipe=example_image_recipe,
    schedule=imagebuilder.ImagePipelineSchedule(
        expression=events.Schedule.rate(Duration.days(7)),
        # Only trigger when dependencies are updated (new base images, components, etc.)
        start_condition=imagebuilder.ScheduleStartCondition.EXPRESSION_MATCH_AND_DEPENDENCY_UPDATES_AVAILABLE,
        # Automatically disable after 3 consecutive failures
        auto_disable_failure_count=3
    ),
    # Start enabled
    status=imagebuilder.ImagePipelineStatus.ENABLED
)
```

#### Image Pipeline Configuration

##### Infrastructure and Distribution in Image Pipelines

Configure custom infrastructure and distribution settings:

```python
infrastructure_configuration = imagebuilder.InfrastructureConfiguration(self, "Infrastructure",
    infrastructure_configuration_name="production-infrastructure",
    instance_types=[
        ec2.InstanceType.of(ec2.InstanceClass.COMPUTE7_INTEL, ec2.InstanceSize.LARGE)
    ],
    vpc=vpc,
    subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
)

distribution_configuration = imagebuilder.DistributionConfiguration(self, "Distribution")
distribution_configuration.add_ami_distributions(
    ami_name="production-ami-{{ imagebuilder:buildDate }}",
    ami_target_account_ids=["123456789012", "098765432109"]
)

production_pipeline = imagebuilder.ImagePipeline(self, "ProductionPipeline",
    recipe=example_image_recipe,
    infrastructure_configuration=infrastructure_configuration,
    distribution_configuration=distribution_configuration
)
```

##### Pipeline Logging Configuration

Configure custom CloudWatch log groups for pipeline and image logs:

```python
pipeline_log_group = logs.LogGroup(self, "PipelineLogGroup",
    log_group_name="/custom/imagebuilder/pipeline/logs",
    retention=logs.RetentionDays.ONE_MONTH
)

image_log_group = logs.LogGroup(self, "ImageLogGroup",
    log_group_name="/custom/imagebuilder/image/logs",
    retention=logs.RetentionDays.ONE_WEEK
)

logged_pipeline = imagebuilder.ImagePipeline(self, "LoggedPipeline",
    recipe=example_image_recipe,
    image_pipeline_log_group=pipeline_log_group,
    image_log_group=image_log_group
)
```

##### Workflow Integration in Image Pipelines

Use AWS-managed workflows for common pipeline phases:

```python
workflow_pipeline = imagebuilder.ImagePipeline(self, "WorkflowPipeline",
    recipe=example_image_recipe,
    workflows=[imagebuilder.WorkflowConfiguration(workflow=imagebuilder.AwsManagedWorkflow.build_image(self, "BuildWorkflow")), imagebuilder.WorkflowConfiguration(workflow=imagebuilder.AwsManagedWorkflow.test_image(self, "TestWorkflow"))
    ]
)
```

For container pipelines, use container-specific workflows:

```python
container_workflow_pipeline = imagebuilder.ImagePipeline(self, "ContainerWorkflowPipeline",
    recipe=example_container_recipe,
    workflows=[imagebuilder.WorkflowConfiguration(workflow=imagebuilder.AwsManagedWorkflow.build_container(self, "BuildContainer")), imagebuilder.WorkflowConfiguration(workflow=imagebuilder.AwsManagedWorkflow.test_container(self, "TestContainer")), imagebuilder.WorkflowConfiguration(workflow=imagebuilder.AwsManagedWorkflow.distribute_container(self, "DistributeContainer"))
    ]
)
```

##### Advanced Features in Image Pipelines

Configure image scanning for container pipelines:

```python
scanning_repository = ecr.Repository(self, "ScanningRepo")

scanned_container_pipeline = imagebuilder.ImagePipeline(self, "ScannedContainerPipeline",
    recipe=example_container_recipe,
    image_scanning_enabled=True,
    image_scanning_ecr_repository=scanning_repository,
    image_scanning_ecr_tags=["security-scan", "latest"]
)
```

Control metadata collection and testing:

```python
controlled_pipeline = imagebuilder.ImagePipeline(self, "ControlledPipeline",
    recipe=example_image_recipe,
    enhanced_image_metadata_enabled=True,  # Collect detailed OS and package info
    image_tests_enabled=False
)
```

#### Image Pipeline Events

##### Pipeline Event Handling

Handle specific pipeline events:

```python
# Monitor CVE detection
example_pipeline.on_cVEDetected("CVEAlert",
    target=targets.SnsTopic(topic)
)

# Handle pipeline auto-disable events
example_pipeline.on_image_pipeline_auto_disabled("PipelineDisabledAlert",
    target=targets.LambdaFunction(lambda_function)
)
```

#### Importing Image Pipelines

Reference existing pipelines created outside CDK:

```python
# Import by name
existing_pipeline_by_name = imagebuilder.ImagePipeline.from_image_pipeline_name(self, "ExistingPipelineByName", "my-existing-pipeline")

# Import by ARN
existing_pipeline_by_arn = imagebuilder.ImagePipeline.from_image_pipeline_arn(self, "ExistingPipelineByArn", "arn:aws:imagebuilder:us-east-1:123456789012:image-pipeline/imported-pipeline")

# Grant permissions to imported pipelines
automation_role = iam.Role(self, "AutomationRole",
    assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
)

existing_pipeline_by_name.grant_start_execution(automation_role)
existing_pipeline_by_arn.grant_read(lambda_role)
```

### Image

An image is the output resource created by Image Builder, consisting of an AMI or container image plus metadata such as
version, platform, and creation details. Images are used as base images for future builds and can be shared across AWS
accounts. While images are the output from image pipeline executions, they can also be created in an ad-hoc manner
outside a pipeline, defined as a standalone resource.

#### Image Basic Usage

Create a simple AMI-based image from an image recipe:

```python
image_recipe = imagebuilder.ImageRecipe(self, "MyImageRecipe",
    base_image=imagebuilder.BaseImage.from_ssm_parameter_name("/aws/service/ami-amazon-linux-latest/al2023-ami-minimal-kernel-default-x86_64")
)

ami_image = imagebuilder.Image(self, "MyAmiImage",
    recipe=image_recipe
)
```

Create a simple container image from a container recipe:

```python
container_recipe = imagebuilder.ContainerRecipe(self, "MyContainerRecipe",
    base_image=imagebuilder.BaseContainerImage.from_docker_hub("amazonlinux", "latest"),
    target_repository=imagebuilder.Repository.from_ecr(
        ecr.Repository.from_repository_name(self, "Repository", "my-container-repo"))
)

container_image = imagebuilder.Image(self, "MyContainerImage",
    recipe=container_recipe
)
```

#### AWS-Managed Images

##### Pre-defined OS Images

Use AWS-managed images for common operating systems:

```python
# Amazon Linux 2023 AMI for x86_64
amazon_linux2023_ami = imagebuilder.AmazonManagedImage.amazon_linux2023(self, "AmazonLinux2023",
    image_type=imagebuilder.ImageType.AMI,
    image_architecture=imagebuilder.ImageArchitecture.X86_64
)

# Ubuntu 22.04 AMI for ARM64
ubuntu2204_ami = imagebuilder.AmazonManagedImage.ubuntu_server2204(self, "Ubuntu2204",
    image_type=imagebuilder.ImageType.AMI,
    image_architecture=imagebuilder.ImageArchitecture.ARM64
)

# Windows Server 2022 Full AMI
windows2022_ami = imagebuilder.AmazonManagedImage.windows_server2022_full(self, "Windows2022",
    image_type=imagebuilder.ImageType.AMI,
    image_architecture=imagebuilder.ImageArchitecture.X86_64
)

# Use as base image in recipe
managed_image_recipe = imagebuilder.ImageRecipe(self, "ManagedImageRecipe",
    base_image=amazon_linux2023_ami.to_base_image()
)
```

##### Custom AWS-Managed Images

Import AWS-managed images by name or attributes:

```python
# Import by name
managed_image_by_name = imagebuilder.AmazonManagedImage.from_amazon_managed_image_name(self, "ManagedImageByName", "amazon-linux-2023-x86")

# Import by attributes with specific version
managed_image_by_attributes = imagebuilder.AmazonManagedImage.from_amazon_managed_image_attributes(self, "ManagedImageByAttributes",
    image_name="ubuntu-server-22-lts-x86",
    image_version="2024.11.25"
)
```

#### Image Configuration

##### Infrastructure and Distribution in Images

Configure custom infrastructure and distribution settings:

```python
infrastructure_configuration = imagebuilder.InfrastructureConfiguration(self, "Infrastructure",
    infrastructure_configuration_name="production-infrastructure",
    instance_types=[
        ec2.InstanceType.of(ec2.InstanceClass.COMPUTE7_INTEL, ec2.InstanceSize.LARGE)
    ],
    vpc=vpc,
    subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
)

distribution_configuration = imagebuilder.DistributionConfiguration(self, "Distribution")
distribution_configuration.add_ami_distributions(
    ami_name="production-ami-{{ imagebuilder:buildDate }}",
    ami_target_account_ids=["123456789012", "098765432109"]
)

production_image = imagebuilder.Image(self, "ProductionImage",
    recipe=example_image_recipe,
    infrastructure_configuration=infrastructure_configuration,
    distribution_configuration=distribution_configuration
)
```

##### Logging Configuration

Configure custom CloudWatch log groups for image builds:

```python
log_group = logs.LogGroup(self, "ImageLogGroup",
    log_group_name="/custom/imagebuilder/image/logs",
    retention=logs.RetentionDays.ONE_MONTH
)

logged_image = imagebuilder.Image(self, "LoggedImage",
    recipe=example_image_recipe,
    log_group=log_group
)
```

##### Workflow Integration in Images

Use workflows for custom build, test, and distribution processes:

```python
image_with_workflows = imagebuilder.Image(self, "ImageWithWorkflows",
    recipe=example_image_recipe,
    workflows=[imagebuilder.WorkflowConfiguration(workflow=imagebuilder.AwsManagedWorkflow.build_image(self, "BuildWorkflow")), imagebuilder.WorkflowConfiguration(workflow=imagebuilder.AwsManagedWorkflow.test_image(self, "TestWorkflow"))
    ]
)
```

##### Advanced Features in Images

Configure image scanning, metadata collection, and testing:

```python
scanning_repository = ecr.Repository(self, "ScanningRepository")

advanced_container_image = imagebuilder.Image(self, "AdvancedContainerImage",
    recipe=example_container_recipe,
    image_scanning_enabled=True,
    image_scanning_ecr_repository=scanning_repository,
    image_scanning_ecr_tags=["security-scan", "latest"],
    enhanced_image_metadata_enabled=True,
    image_tests_enabled=False
)
```

#### Importing Images

Reference existing images created outside CDK:

```python
# Import by name
existing_image_by_name = imagebuilder.Image.from_image_name(self, "ExistingImageByName", "my-existing-image")

# Import by ARN
existing_image_by_arn = imagebuilder.Image.from_image_arn(self, "ExistingImageByArn", "arn:aws:imagebuilder:us-east-1:123456789012:image/imported-image/1.0.0")

# Import by attributes
existing_image_by_attributes = imagebuilder.Image.from_image_attributes(self, "ExistingImageByAttributes",
    image_name="shared-base-image",
    image_version="2024.11.25"
)

# Grant permissions to imported images
role = iam.Role(self, "ImageAccessRole",
    assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
)

existing_image_by_name.grant_read(role)
existing_image_by_arn.grant(role, "imagebuilder:GetImage", "imagebuilder:ListImagePackages")
```

### Image Recipe

#### Image Recipe Basic Usage

Create an image recipe with the required base image:

```python
image_recipe = imagebuilder.ImageRecipe(self, "MyImageRecipe",
    base_image=imagebuilder.BaseImage.from_ssm_parameter_name("/aws/service/ami-amazon-linux-latest/al2023-ami-minimal-kernel-default-x86_64")
)
```

#### Image Recipe Base Images

To create a recipe, you have to select a base image to build and customize from. This base image can be referenced from
various sources, such as from SSM parameters, AWS Marketplace products, and AMI IDs directly.

##### SSM Parameters

Using SSM parameter references:

```python
image_recipe = imagebuilder.ImageRecipe(self, "SsmImageRecipe",
    base_image=imagebuilder.BaseImage.from_ssm_parameter_name("/aws/service/ami-amazon-linux-latest/al2023-ami-minimal-kernel-default-x86_64")
)

# Using an SSM parameter construct
parameter = ssm.StringParameter.from_string_parameter_name(self, "BaseImageParameter", "/aws/service/ami-windows-latest/Windows_Server-2022-English-Full-Base")
windows_recipe = imagebuilder.ImageRecipe(self, "WindowsImageRecipe",
    base_image=imagebuilder.BaseImage.from_ssm_parameter(parameter)
)
```

##### AMI IDs

When you have a specific AMI to use:

```python
image_recipe = imagebuilder.ImageRecipe(self, "AmiImageRecipe",
    base_image=imagebuilder.BaseImage.from_ami_id("ami-12345678")
)
```

##### Marketplace Images

For marketplace base images:

```python
image_recipe = imagebuilder.ImageRecipe(self, "MarketplaceImageRecipe",
    base_image=imagebuilder.BaseImage.from_marketplace_product_id("prod-1234567890abcdef0")
)
```

#### Image Recipe Components

Components from various sources, such as custom-owned, AWS-owned, or AWS Marketplace-owned, can optionally be included
in recipes. For parameterized components, you are able to provide the parameters to use in the recipe, which will be
applied during the image build when executing components.

##### Custom Components in Image Recipes

Add your own components to the recipe:

```python
custom_component = imagebuilder.Component(self, "MyComponent",
    platform=imagebuilder.Platform.LINUX,
    data=imagebuilder.ComponentData.from_json_object({
        "schema_version": imagebuilder.ComponentSchemaVersion.V1_0,
        "phases": [{
            "name": imagebuilder.ComponentPhaseName.BUILD,
            "steps": [{
                "name": "install-app",
                "action": imagebuilder.ComponentAction.EXECUTE_BASH,
                "inputs": {
                    "commands": ["yum install -y my-application"]
                }
            }
            ]
        }
        ]
    })
)

image_recipe = imagebuilder.ImageRecipe(self, "ComponentImageRecipe",
    base_image=imagebuilder.BaseImage.from_ssm_parameter_name("/aws/service/ami-amazon-linux-latest/al2023-ami-minimal-kernel-default-x86_64"),
    components=[imagebuilder.ComponentConfiguration(
        component=custom_component
    )
    ]
)
```

##### AWS-Managed Components in Image Recipes

Use pre-built AWS components:

```python
image_recipe = imagebuilder.ImageRecipe(self, "AmazonManagedImageRecipe",
    base_image=imagebuilder.BaseImage.from_ssm_parameter_name("/aws/service/ami-amazon-linux-latest/al2023-ami-minimal-kernel-default-x86_64"),
    components=[imagebuilder.ComponentConfiguration(
        component=imagebuilder.AwsManagedComponent.update_oS(self, "UpdateOS",
            platform=imagebuilder.Platform.LINUX
        )
    ), imagebuilder.ComponentConfiguration(
        component=imagebuilder.AwsManagedComponent.aws_cli_v2(self, "AwsCli",
            platform=imagebuilder.Platform.LINUX
        )
    )
    ]
)
```

##### Component Parameters in Image Recipes

Pass parameters to components that accept them:

```python
parameterized_component = imagebuilder.Component.from_component_name(self, "ParameterizedComponent", "my-parameterized-component")

image_recipe = imagebuilder.ImageRecipe(self, "ParameterizedImageRecipe",
    base_image=imagebuilder.BaseImage.from_ssm_parameter_name("/aws/service/ami-amazon-linux-latest/al2023-ami-minimal-kernel-default-x86_64"),
    components=[imagebuilder.ComponentConfiguration(
        component=parameterized_component,
        parameters={
            "environment": imagebuilder.ComponentParameterValue.from_string("production"),
            "version": imagebuilder.ComponentParameterValue.from_string("1.0.0")
        }
    )
    ]
)
```

#### Image Recipe Configuration

##### Block Device Configuration

Configure storage for the build instance:

```python
image_recipe = imagebuilder.ImageRecipe(self, "BlockDeviceImageRecipe",
    base_image=imagebuilder.BaseImage.from_ssm_parameter_name("/aws/service/ami-amazon-linux-latest/al2023-ami-minimal-kernel-default-x86_64"),
    block_devices=[ec2.BlockDevice(
        device_name="/dev/sda1",
        volume=ec2.BlockDeviceVolume.ebs(100,
            encrypted=True,
            volume_type=ec2.EbsDeviceVolumeType.GENERAL_PURPOSE_SSD_GP3
        )
    )
    ]
)
```

##### AMI Tagging

Tag the output AMI:

```python
image_recipe = imagebuilder.ImageRecipe(self, "TaggedImageRecipe",
    base_image=imagebuilder.BaseImage.from_ssm_parameter_name("/aws/service/ami-amazon-linux-latest/al2023-ami-minimal-kernel-default-x86_64"),
    ami_tags={
        "Environment": "Production",
        "Application": "WebServer",
        "Owner": "DevOps Team"
    }
)
```

### Container Recipe

A container recipe is similar to an image recipe but specifically for container images. It defines the base container
image and components applied to produce the desired configuration for the output container image. Container recipes work
with Docker images from DockerHub, Amazon ECR, or Amazon-managed container images as starting points.

#### Container Recipe Basic Usage

Create a container recipe with the required base image and target repository:

```python
container_recipe = imagebuilder.ContainerRecipe(self, "MyContainerRecipe",
    base_image=imagebuilder.BaseContainerImage.from_docker_hub("amazonlinux", "latest"),
    target_repository=imagebuilder.Repository.from_ecr(
        ecr.Repository.from_repository_name(self, "Repository", "my-container-repo"))
)
```

#### Container Recipe Base Images

##### DockerHub Images

Using public Docker Hub images:

```python
container_recipe = imagebuilder.ContainerRecipe(self, "DockerHubContainerRecipe",
    base_image=imagebuilder.BaseContainerImage.from_docker_hub("amazonlinux", "latest"),
    target_repository=imagebuilder.Repository.from_ecr(
        ecr.Repository.from_repository_name(self, "Repository", "my-container-repo"))
)
```

##### ECR Images

Using images from your own ECR repositories:

```python
source_repo = ecr.Repository.from_repository_name(self, "SourceRepo", "my-base-image")
target_repo = ecr.Repository.from_repository_name(self, "TargetRepo", "my-container-repo")

container_recipe = imagebuilder.ContainerRecipe(self, "EcrContainerRecipe",
    base_image=imagebuilder.BaseContainerImage.from_ecr(source_repo, "1.0.0"),
    target_repository=imagebuilder.Repository.from_ecr(target_repo)
)
```

##### ECR Public Images

Using images from Amazon ECR Public:

```python
container_recipe = imagebuilder.ContainerRecipe(self, "EcrPublicContainerRecipe",
    base_image=imagebuilder.BaseContainerImage.from_ecr_public("amazonlinux", "amazonlinux", "2023"),
    target_repository=imagebuilder.Repository.from_ecr(
        ecr.Repository.from_repository_name(self, "Repository", "my-container-repo"))
)
```

#### Container Recipe Components

##### Custom Components in Container Recipes

Add your own components to the container recipe:

```python
custom_component = imagebuilder.Component(self, "MyComponent",
    platform=imagebuilder.Platform.LINUX,
    data=imagebuilder.ComponentData.from_json_object({
        "schema_version": imagebuilder.ComponentSchemaVersion.V1_0,
        "phases": [{
            "name": imagebuilder.ComponentPhaseName.BUILD,
            "steps": [{
                "name": "install-app",
                "action": imagebuilder.ComponentAction.EXECUTE_BASH,
                "inputs": {
                    "commands": ["yum install -y my-container-application"]
                }
            }
            ]
        }
        ]
    })
)

container_recipe = imagebuilder.ContainerRecipe(self, "ComponentContainerRecipe",
    base_image=imagebuilder.BaseContainerImage.from_docker_hub("amazonlinux", "latest"),
    target_repository=imagebuilder.Repository.from_ecr(
        ecr.Repository.from_repository_name(self, "Repository", "my-container-repo")),
    components=[imagebuilder.ComponentConfiguration(
        component=custom_component
    )
    ]
)
```

##### AWS-Managed Components in Container Recipes

Use pre-built AWS components:

```python
container_recipe = imagebuilder.ContainerRecipe(self, "AwsManagedContainerRecipe",
    base_image=imagebuilder.BaseContainerImage.from_docker_hub("amazonlinux", "latest"),
    target_repository=imagebuilder.Repository.from_ecr(
        ecr.Repository.from_repository_name(self, "Repository", "my-container-repo")),
    components=[imagebuilder.ComponentConfiguration(
        component=imagebuilder.AwsManagedComponent.update_oS(self, "UpdateOS",
            platform=imagebuilder.Platform.LINUX
        )
    ), imagebuilder.ComponentConfiguration(
        component=imagebuilder.AwsManagedComponent.aws_cli_v2(self, "AwsCli",
            platform=imagebuilder.Platform.LINUX
        )
    )
    ]
)
```

#### Container Recipe Configuration

##### Custom Dockerfile

Provide your own Dockerfile template:

```python
container_recipe = imagebuilder.ContainerRecipe(self, "CustomDockerfileContainerRecipe",
    base_image=imagebuilder.BaseContainerImage.from_docker_hub("amazonlinux", "latest"),
    target_repository=imagebuilder.Repository.from_ecr(
        ecr.Repository.from_repository_name(self, "Repository", "my-container-repo")),
    dockerfile=imagebuilder.DockerfileData.from_inline("""
        FROM {{{ imagebuilder:parentImage }}}
        CMD ["echo", "Hello, world!"]
        {{{ imagebuilder:environments }}}
        {{{ imagebuilder:components }}}
        """)
)
```

##### Instance Configuration

Configure the build instance:

```python
container_recipe = imagebuilder.ContainerRecipe(self, "InstanceConfigContainerRecipe",
    base_image=imagebuilder.BaseContainerImage.from_docker_hub("amazonlinux", "latest"),
    target_repository=imagebuilder.Repository.from_ecr(
        ecr.Repository.from_repository_name(self, "Repository", "my-container-repo")),
    # Custom ECS-optimized AMI for building
    instance_image=imagebuilder.ContainerInstanceImage.from_ssm_parameter_name("/aws/service/ecs/optimized-ami/amazon-linux-2023/recommended/image_id"),
    # Additional storage for build process
    instance_block_devices=[ec2.BlockDevice(
        device_name="/dev/xvda",
        volume=ec2.BlockDeviceVolume.ebs(50,
            encrypted=True,
            volume_type=ec2.EbsDeviceVolumeType.GENERAL_PURPOSE_SSD_GP3
        )
    )
    ]
)
```

### Component

A component defines the sequence of steps required to customize an instance during image creation (build component) or
test an instance launched from the created image (test component). Components are created from declarative YAML or JSON
documents that describe runtime configuration for building, validating, or testing instances. Components are included
when added to the image recipe or container recipe for an image build.

EC2 Image Builder supports AWS-managed components for common tasks, AWS Marketplace components, and custom components
that you create. Components run during specific workflow phases: build and validate phases during the build stage, and
test phase during the test stage.

#### Basic Component Usage

Create a component with the required properties: platform and component data.

```python
component = imagebuilder.Component(self, "MyComponent",
    platform=imagebuilder.Platform.LINUX,
    data=imagebuilder.ComponentData.from_json_object({
        "schema_version": imagebuilder.ComponentSchemaVersion.V1_0,
        "phases": [{
            "name": imagebuilder.ComponentPhaseName.BUILD,
            "steps": [{
                "name": "install-app",
                "action": imagebuilder.ComponentAction.EXECUTE_BASH,
                "inputs": {
                    "commands": ["echo \"Installing my application...\"", "yum update -y"]
                }
            }
            ]
        }
        ]
    })
)
```

#### Component Data Sources

##### Inline Component Data

Use `ComponentData.fromInline()` for existing YAML/JSON definitions:

```python
component = imagebuilder.Component(self, "InlineComponent",
    platform=imagebuilder.Platform.LINUX,
    data=imagebuilder.ComponentData.from_inline("""
        name: my-component
        schemaVersion: 1.0
        phases:
          - name: build
            steps:
              - name: update-os
                action: ExecuteBash
                inputs:
                  commands: ['yum update -y']
        """)
)
```

##### JSON Object Component Data

Most developer-friendly approach using objects:

```python
component = imagebuilder.Component(self, "JsonComponent",
    platform=imagebuilder.Platform.LINUX,
    data=imagebuilder.ComponentData.from_json_object({
        "schema_version": imagebuilder.ComponentSchemaVersion.V1_0,
        "phases": [{
            "name": imagebuilder.ComponentPhaseName.BUILD,
            "steps": [{
                "name": "configure-app",
                "action": imagebuilder.ComponentAction.CREATE_FILE,
                "inputs": {
                    "path": "/etc/myapp/config.json",
                    "content": "{\"env\": \"production\"}"
                }
            }
            ]
        }
        ]
    })
)
```

##### Structured Component Document

For type-safe, CDK-native definitions with enhanced properties like `timeout` and `onFailure`.

###### Defining a component step

You can define steps in the component which will be executed in order when the component is applied:

```python
step = imagebuilder.ComponentDocumentStep(
    name="configure-app",
    action=imagebuilder.ComponentAction.CREATE_FILE,
    inputs=imagebuilder.ComponentStepInputs.from_object({
        "path": "/etc/myapp/config.json",
        "content": "{\"env\": \"production\"}"
    })
)
```

###### Defining a component phase

Phases group steps together, which run in sequence when building, validating or testing in the component:

```python
phase = imagebuilder.ComponentDocumentPhase(
    name=imagebuilder.ComponentPhaseName.BUILD,
    steps=[imagebuilder.ComponentDocumentStep(
        name="configure-app",
        action=imagebuilder.ComponentAction.CREATE_FILE,
        inputs=imagebuilder.ComponentStepInputs.from_object({
            "path": "/etc/myapp/config.json",
            "content": "{\"env\": \"production\"}"
        })
    )
    ]
)
```

###### Defining a component

The component data defines all steps across the provided phases to execute during the build:

```python
component = imagebuilder.Component(self, "StructuredComponent",
    platform=imagebuilder.Platform.LINUX,
    data=imagebuilder.ComponentData.from_component_document_json_object(
        schema_version=imagebuilder.ComponentSchemaVersion.V1_0,
        phases=[imagebuilder.ComponentDocumentPhase(
            name=imagebuilder.ComponentPhaseName.BUILD,
            steps=[imagebuilder.ComponentDocumentStep(
                name="install-with-timeout",
                action=imagebuilder.ComponentAction.EXECUTE_BASH,
                timeout=Duration.minutes(10),
                on_failure=imagebuilder.ComponentOnFailure.CONTINUE,
                inputs=imagebuilder.ComponentStepInputs.from_object({
                    "commands": ["./install-script.sh"]
                })
            )
            ]
        )
        ]
    )
)
```

##### S3 Component Data

For those components you want to upload or have uploaded to S3:

```python
# Upload a local file
component_from_asset = imagebuilder.Component(self, "AssetComponent",
    platform=imagebuilder.Platform.LINUX,
    data=imagebuilder.ComponentData.from_asset(self, "ComponentAsset", "./my-component.yml")
)

# Reference an existing S3 object
bucket = s3.Bucket.from_bucket_name(self, "ComponentBucket", "my-components-bucket")
component_from_s3 = imagebuilder.Component(self, "S3Component",
    platform=imagebuilder.Platform.LINUX,
    data=imagebuilder.ComponentData.from_s3(bucket, "components/my-component.yml")
)
```

#### Encrypt component data with a KMS key

You can encrypt component data with a KMS key, so that only principals with access to decrypt with the key are able to
access the component data.

```python
component = imagebuilder.Component(self, "EncryptedComponent",
    platform=imagebuilder.Platform.LINUX,
    kms_key=kms.Key(self, "ComponentKey"),
    data=imagebuilder.ComponentData.from_json_object({
        "schema_version": imagebuilder.ComponentSchemaVersion.V1_0,
        "phases": [{
            "name": imagebuilder.ComponentPhaseName.BUILD,
            "steps": [{
                "name": "secure-setup",
                "action": imagebuilder.ComponentAction.EXECUTE_BASH,
                "inputs": {
                    "commands": ["echo \"This component data is encrypted with KMS\""]
                }
            }
            ]
        }
        ]
    })
)
```

#### AWS-Managed Components

AWS provides a collection of managed components for common tasks:

```python
# Install AWS CLI v2
aws_cli_component = imagebuilder.AwsManagedComponent.aws_cli_v2(self, "AwsCli",
    platform=imagebuilder.Platform.LINUX
)

# Update the operating system
update_component = imagebuilder.AwsManagedComponent.update_oS(self, "UpdateOS",
    platform=imagebuilder.Platform.LINUX
)

# Reference any AWS-managed component by name
custom_aws_component = imagebuilder.AwsManagedComponent.from_aws_managed_component_name(self, "CloudWatchAgent", "amazon-cloudwatch-agent-linux")
```

#### AWS Marketplace Components

You can reference AWS Marketplace components using the marketplace component name and its product ID:

```python
marketplace_component = imagebuilder.AwsMarketplaceComponent.from_aws_marketplace_component_attributes(self, "MarketplaceComponent",
    component_name="my-marketplace-component",
    marketplace_product_id="prod-1234567890abcdef0"
)
```

### Infrastructure Configuration

Infrastructure configuration defines the compute resources and environment settings used during the image building
process. This includes instance types, IAM instance profile, VPC settings, subnets, security groups, SNS topics for
notifications, logging configuration, and troubleshooting settings like whether to terminate instances on failure or
keep them running for debugging. These settings are applied to builds when included in an image or an image pipeline.

```python
infrastructure_configuration = imagebuilder.InfrastructureConfiguration(self, "InfrastructureConfiguration",
    infrastructure_configuration_name="test-infrastructure-configuration",
    description="An Infrastructure Configuration",
    # Optional - instance types to use for build/test
    instance_types=[
        ec2.InstanceType.of(ec2.InstanceClass.STANDARD7_INTEL, ec2.InstanceSize.LARGE),
        ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.LARGE)
    ],
    # Optional - create an instance profile with necessary permissions
    instance_profile=iam.InstanceProfile(self, "InstanceProfile",
        instance_profile_name="test-instance-profile",
        role=iam.Role(self, "InstanceProfileRole",
            assumed_by=iam.ServicePrincipal.from_static_service_principle_name("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"),
                iam.ManagedPolicy.from_aws_managed_policy_name("EC2InstanceProfileForImageBuilder")
            ]
        )
    ),
    # Use VPC network configuration
    vpc=vpc,
    subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
    security_groups=[ec2.SecurityGroup.from_security_group_id(self, "SecurityGroup", vpc.vpc_default_security_group)],
    key_pair=ec2.KeyPair.from_key_pair_name(self, "KeyPair", "imagebuilder-instance-key-pair"),
    terminate_instance_on_failure=True,
    # Optional - IMDSv2 settings
    http_tokens=imagebuilder.HttpTokens.REQUIRED,
    http_put_response_hop_limit=1,
    # Optional - publish image completion messages to an SNS topic
    notification_topic=sns.Topic.from_topic_arn(self, "Topic",
        self.format_arn(service="sns", resource="image-builder-topic")),
    # Optional - log settings. Logging is enabled by default
    logging=imagebuilder.InfrastructureConfigurationLogging(
        s3_bucket=s3.Bucket.from_bucket_name(self, "LogBucket", f"imagebuilder-logging-{Aws.ACCOUNT_ID}"),
        s3_key_prefix="imagebuilder-logs"
    ),
    # Optional - host placement settings
    ec2_instance_availability_zone=Stack.of(self).availability_zones[0],
    ec2_instance_host_id=dedicated_host.attr_host_id,
    ec2_instance_tenancy=imagebuilder.Tenancy.HOST,
    resource_tags={
        "Environment": "production"
    }
)
```

### Distribution Configuration

Distribution configuration defines how and where your built images are distributed after successful creation. For AMIs,
this includes target AWS Regions, KMS encryption keys, account sharing permissions, License Manager associations, and
launch template configurations. For container images, it specifies the target Amazon ECR repositories across regions.
A distribution configuration can be associated with an image or an image pipeline to define these distribution settings
for image builds.

#### AMI Distributions

AMI distributions can be defined to copy and modify AMIs in different accounts and regions, and apply them to launch
templates, SSM parameters, etc.:

```python
distribution_configuration = imagebuilder.DistributionConfiguration(self, "DistributionConfiguration",
    distribution_configuration_name="test-distribution-configuration",
    description="A Distribution Configuration",
    ami_distributions=[imagebuilder.AmiDistribution(
        # Distribute AMI to us-east-2 and publish the AMI ID to an SSM parameter
        region="us-east-2",
        ssm_parameters=[imagebuilder.SSMParameterConfigurations(
            parameter=ssm.StringParameter.from_string_parameter_attributes(self, "CrossRegionParameter",
                parameter_name="/imagebuilder/ami",
                force_dynamic_reference=True
            )
        )
        ]
    )
    ]
)

# For AMI-based image builds - add an AMI distribution in the current region
distribution_configuration.add_ami_distributions(
    ami_name="imagebuilder-{{ imagebuilder:buildDate }}",
    ami_description="Build AMI",
    ami_kms_key=kms.Key.from_lookup(self, "ComponentKey", alias_name="alias/distribution-encryption-key"),
    # Copy the AMI to different accounts
    ami_target_account_ids=["123456789012", "098765432109"],
    # Add launch permissions on the AMI
    ami_launch_permission=imagebuilder.AmiLaunchPermission(
        organization_arns=[
            self.format_arn(region="", service="organizations", resource="organization", resource_name="o-1234567abc")
        ],
        organizational_unit_arns=[
            self.format_arn(
                region="",
                service="organizations",
                resource="ou",
                resource_name="o-1234567abc/ou-a123-b4567890"
            )
        ],
        is_public_user_group=True,
        account_ids=["234567890123"]
    ),
    # Attach tags to the AMI
    ami_tags={
        "Environment": "production",
        "Version": "{{ imagebuilder:buildVersion }}"
    },
    # Optional - publish the distributed AMI ID to an SSM parameter
    ssm_parameters=[imagebuilder.SSMParameterConfigurations(
        parameter=ssm.StringParameter.from_string_parameter_attributes(self, "Parameter",
            parameter_name="/imagebuilder/ami",
            force_dynamic_reference=True
        )
    ), imagebuilder.SSMParameterConfigurations(
        ami_account="098765432109",
        data_type=ssm.ParameterDataType.TEXT,
        parameter=ssm.StringParameter.from_string_parameter_attributes(self, "CrossAccountParameter",
            parameter_name="imagebuilder-prod-ami",
            force_dynamic_reference=True
        )
    )
    ],
    # Optional - create a new launch template version with the distributed AMI ID
    launch_templates=[imagebuilder.LaunchTemplateConfiguration(
        launch_template=ec2.LaunchTemplate.from_launch_template_attributes(self, "LaunchTemplate",
            launch_template_id="lt-1234"
        ),
        set_default_version=True
    ), imagebuilder.LaunchTemplateConfiguration(
        account_id="123456789012",
        launch_template=ec2.LaunchTemplate.from_launch_template_attributes(self, "CrossAccountLaunchTemplate",
            launch_template_id="lt-5678"
        ),
        set_default_version=True
    )
    ],
    # Optional - enable Fast Launch on an imported launch template
    fast_launch_configurations=[imagebuilder.FastLaunchConfiguration(
        enabled=True,
        launch_template=ec2.LaunchTemplate.from_launch_template_attributes(self, "FastLaunchLT",
            launch_template_name="fast-launch-lt"
        ),
        max_parallel_launches=10,
        target_snapshot_count=2
    )
    ],
    # Optional - license configurations to apply to the AMI
    license_configuration_arns=["arn:aws:license-manager:us-west-2:123456789012:license-configuration:lic-abcdefghijklmnopqrstuvwxyz"
    ]
)
```

#### Container Distributions

##### Container repositories

Container distributions can be configured to distribute to ECR repositories:

```python
ecr_repository = ecr.Repository.from_repository_name(self, "ECRRepository", "my-repo")
image_builder_repository = imagebuilder.Repository.from_ecr(ecr_repository)
```

##### Defining a container distribution

You can configure the container repositories as well as the description and tags applied to the distributed container
images:

```python
ecr_repository = ecr.Repository.from_repository_name(self, "ECRRepository", "my-repo")
container_repository = imagebuilder.Repository.from_ecr(ecr_repository)
container_distribution_configuration = imagebuilder.DistributionConfiguration(self, "ContainerDistributionConfiguration")

container_distribution_configuration.add_container_distributions(
    container_repository=container_repository,
    container_description="Test container image",
    container_tags=["latest", "latest-1.0"]
)
```

### Workflow

Workflows define the sequence of steps that Image Builder performs during image creation. There are three workflow
types: BUILD (image building), TEST (testing images), and DISTRIBUTION (distributing container images).

#### Basic Workflow Usage

Create a workflow with the required properties: workflow type and workflow data.

```python
workflow = imagebuilder.Workflow(self, "MyWorkflow",
    workflow_type=imagebuilder.WorkflowType.BUILD,
    data=imagebuilder.WorkflowData.from_json_object({
        "schema_version": imagebuilder.WorkflowSchemaVersion.V1_0,
        "steps": [{
            "name": "LaunchBuildInstance",
            "action": imagebuilder.WorkflowAction.LAUNCH_INSTANCE,
            "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
            "inputs": {
                "wait_for": "ssmAgent"
            }
        }, {
            "name": "ExecuteComponents",
            "action": imagebuilder.WorkflowAction.EXECUTE_COMPONENTS,
            "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
            "inputs": {
                "instance_id": "i-123"
            }
        }, {
            "name": "CreateImage",
            "action": imagebuilder.WorkflowAction.CREATE_IMAGE,
            "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
            "inputs": {
                "instance_id": "i-123"
            }
        }, {
            "name": "TerminateInstance",
            "action": imagebuilder.WorkflowAction.TERMINATE_INSTANCE,
            "on_failure": imagebuilder.WorkflowOnFailure.CONTINUE,
            "inputs": {
                "instance_id": "i-123"
            }
        }
        ],
        "outputs": [{
            "name": "ImageId",
            "value": "$.stepOutputs.CreateImage.imageId"
        }
        ]
    })
)
```

#### Workflow Data Sources

##### Inline Workflow Data

Use `WorkflowData.fromInline()` for existing YAML/JSON definitions:

```python
workflow = imagebuilder.Workflow(self, "InlineWorkflow",
    workflow_type=imagebuilder.WorkflowType.TEST,
    data=imagebuilder.WorkflowData.from_inline("""
        schemaVersion: 1.0
        steps:
          - name: LaunchTestInstance
            action: LaunchInstance
            onFailure: Abort
            inputs:
              waitFor: ssmAgent
          - name: RunTests
            action: RunCommand
            onFailure: Abort
            inputs:
              instanceId.$: "$.stepOutputs.LaunchTestInstance.instanceId"
              commands: ['./run-tests.sh']
          - name: TerminateTestInstance
            action: TerminateInstance
            onFailure: Continue
            inputs:
              instanceId.$: "$.stepOutputs.LaunchTestInstance.instanceId"
        """)
)
```

##### JSON Object Workflow Data

Most developer-friendly approach using JavaScript objects:

```python
workflow = imagebuilder.Workflow(self, "JsonWorkflow",
    workflow_type=imagebuilder.WorkflowType.BUILD,
    data=imagebuilder.WorkflowData.from_json_object({
        "schema_version": imagebuilder.WorkflowSchemaVersion.V1_0,
        "steps": [{
            "name": "LaunchBuildInstance",
            "action": imagebuilder.WorkflowAction.LAUNCH_INSTANCE,
            "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
            "inputs": {
                "wait_for": "ssmAgent"
            }
        }, {
            "name": "ExecuteComponents",
            "action": imagebuilder.WorkflowAction.EXECUTE_COMPONENTS,
            "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
            "inputs": {
                "instance_id": "i-123"
            }
        }, {
            "name": "CreateImage",
            "action": imagebuilder.WorkflowAction.CREATE_IMAGE,
            "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
            "inputs": {
                "instance_id": "i-123"
            }
        }, {
            "name": "TerminateInstance",
            "action": imagebuilder.WorkflowAction.TERMINATE_INSTANCE,
            "on_failure": imagebuilder.WorkflowOnFailure.CONTINUE,
            "inputs": {
                "instance_id": "i-123"
            }
        }
        ],
        "outputs": [{
            "name": "ImageId",
            "value": "$.stepOutputs.CreateImage.imageId"
        }
        ]
    })
)
```

##### S3 Workflow Data

For those workflows you want to upload or have uploaded to S3:

```python
# Upload a local file
workflow_from_asset = imagebuilder.Workflow(self, "AssetWorkflow",
    workflow_type=imagebuilder.WorkflowType.BUILD,
    data=imagebuilder.WorkflowData.from_asset(self, "WorkflowAsset", "./my-workflow.yml")
)

# Reference an existing S3 object
bucket = s3.Bucket.from_bucket_name(self, "WorkflowBucket", "my-workflows-bucket")
workflow_from_s3 = imagebuilder.Workflow(self, "S3Workflow",
    workflow_type=imagebuilder.WorkflowType.BUILD,
    data=imagebuilder.WorkflowData.from_s3(bucket, "workflows/my-workflow.yml")
)
```

#### Encrypt workflow data with a KMS key

You can encrypt workflow data with a KMS key, so that only principals with access to decrypt with the key are able to
access the workflow data.

```python
workflow = imagebuilder.Workflow(self, "EncryptedWorkflow",
    workflow_type=imagebuilder.WorkflowType.BUILD,
    kms_key=kms.Key(self, "WorkflowKey"),
    data=imagebuilder.WorkflowData.from_json_object({
        "schema_version": imagebuilder.WorkflowSchemaVersion.V1_0,
        "steps": [{
            "name": "LaunchBuildInstance",
            "action": imagebuilder.WorkflowAction.LAUNCH_INSTANCE,
            "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
            "inputs": {
                "wait_for": "ssmAgent"
            }
        }, {
            "name": "CreateImage",
            "action": imagebuilder.WorkflowAction.CREATE_IMAGE,
            "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
            "inputs": {
                "instance_id": "i-123"
            }
        }, {
            "name": "TerminateInstance",
            "action": imagebuilder.WorkflowAction.TERMINATE_INSTANCE,
            "on_failure": imagebuilder.WorkflowOnFailure.CONTINUE,
            "inputs": {
                "instance_id": "i-123"
            }
        }
        ],
        "outputs": [{
            "name": "ImageId",
            "value": "$.stepOutputs.CreateImage.imageId"
        }
        ]
    })
)
```

#### AWS-Managed Workflows

AWS provides a collection of workflows for common scenarios:

```python
# Build workflows
build_image_workflow = imagebuilder.AwsManagedWorkflow.build_image(self, "BuildImage")
build_container_workflow = imagebuilder.AwsManagedWorkflow.build_container(self, "BuildContainer")

# Test workflows
test_image_workflow = imagebuilder.AwsManagedWorkflow.test_image(self, "TestImage")
test_container_workflow = imagebuilder.AwsManagedWorkflow.test_container(self, "TestContainer")

# Distribution workflows
distribute_container_workflow = imagebuilder.AwsManagedWorkflow.distribute_container(self, "DistributeContainer")
```

### Lifecycle Policy

Lifecycle policies help you manage the retention and cleanup of Image Builder resources automatically. These policies
define rules for deprecating or deleting old image versions, managing AMI snapshots, and controlling resource costs by
removing unused images based on age, count, or other criteria.

#### Lifecycle Policy Basic Usage

Create a lifecycle policy to automatically delete old AMI images after 30 days:

```python
lifecycle_policy = imagebuilder.LifecyclePolicy(self, "MyLifecyclePolicy",
    resource_type=imagebuilder.LifecyclePolicyResourceType.AMI_IMAGE,
    details=[imagebuilder.LifecyclePolicyDetail(
        action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
        filter=imagebuilder.LifecyclePolicyFilter(age_filter=imagebuilder.LifecyclePolicyAgeFilter(age=Duration.days(30)))
    )
    ],
    resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
        tags={"Environment": "development"}
    )
)
```

Create a lifecycle policy to keep only the 10 most recent container images:

```python
container_lifecycle_policy = imagebuilder.LifecyclePolicy(self, "ContainerLifecyclePolicy",
    resource_type=imagebuilder.LifecyclePolicyResourceType.CONTAINER_IMAGE,
    details=[imagebuilder.LifecyclePolicyDetail(
        action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
        filter=imagebuilder.LifecyclePolicyFilter(count_filter=imagebuilder.LifecyclePolicyCountFilter(count=10))
    )
    ],
    resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
        tags={"Application": "web-app"}
    )
)
```

#### Lifecycle Policy Resource Selection

##### Tag-Based Resource Selection

Apply lifecycle policies to images with specific tags:

```python
tag_based_policy = imagebuilder.LifecyclePolicy(self, "TagBasedPolicy",
    resource_type=imagebuilder.LifecyclePolicyResourceType.AMI_IMAGE,
    details=[imagebuilder.LifecyclePolicyDetail(
        action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
        filter=imagebuilder.LifecyclePolicyFilter(age_filter=imagebuilder.LifecyclePolicyAgeFilter(age=Duration.days(90)))
    )
    ],
    resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
        tags={
            "Environment": "staging",
            "Team": "backend"
        }
    )
)
```

##### Recipe-Based Resource Selection

Apply lifecycle policies to specific image or container recipes:

```python
image_recipe = imagebuilder.ImageRecipe(self, "MyImageRecipe",
    base_image=imagebuilder.BaseImage.from_ssm_parameter_name("/aws/service/ami-amazon-linux-latest/al2023-ami-minimal-kernel-default-x86_64")
)

container_recipe = imagebuilder.ContainerRecipe(self, "MyContainerRecipe",
    base_image=imagebuilder.BaseContainerImage.from_docker_hub("amazonlinux", "latest"),
    target_repository=imagebuilder.Repository.from_ecr(
        ecr.Repository.from_repository_name(self, "Repository", "my-container-repo"))
)

recipe_based_policy = imagebuilder.LifecyclePolicy(self, "RecipeBasedPolicy",
    resource_type=imagebuilder.LifecyclePolicyResourceType.AMI_IMAGE,
    details=[imagebuilder.LifecyclePolicyDetail(
        action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
        filter=imagebuilder.LifecyclePolicyFilter(count_filter=imagebuilder.LifecyclePolicyCountFilter(count=5))
    )
    ],
    resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
        recipes=[image_recipe, container_recipe]
    )
)
```

#### Lifecycle Policy Rules

##### Age-Based Rules

Delete images older than a specific time period:

```python
age_based_policy = imagebuilder.LifecyclePolicy(self, "AgeBasedPolicy",
    resource_type=imagebuilder.LifecyclePolicyResourceType.AMI_IMAGE,
    details=[imagebuilder.LifecyclePolicyDetail(
        action=imagebuilder.LifecyclePolicyAction(
            type=imagebuilder.LifecyclePolicyActionType.DELETE,
            include_amis=True,
            include_snapshots=True
        ),
        filter=imagebuilder.LifecyclePolicyFilter(
            age_filter=imagebuilder.LifecyclePolicyAgeFilter(
                age=Duration.days(60),
                retain_at_least=3
            )
        )
    )
    ],
    resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
        tags={"Environment": "testing"}
    )
)
```

##### Count-Based Rules

Keep only a specific number of the most recent images:

```python
count_based_policy = imagebuilder.LifecyclePolicy(self, "CountBasedPolicy",
    resource_type=imagebuilder.LifecyclePolicyResourceType.CONTAINER_IMAGE,
    details=[imagebuilder.LifecyclePolicyDetail(
        action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
        filter=imagebuilder.LifecyclePolicyFilter(count_filter=imagebuilder.LifecyclePolicyCountFilter(count=15))
    )
    ],
    resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
        tags={"Application": "microservice"}
    )
)
```

##### Multiple Lifecycle Rules

Implement a graduated approach with multiple actions:

```python
graduated_policy = imagebuilder.LifecyclePolicy(self, "GraduatedPolicy",
    resource_type=imagebuilder.LifecyclePolicyResourceType.AMI_IMAGE,
    details=[imagebuilder.LifecyclePolicyDetail(
        # First: Deprecate images after 30 days
        action=imagebuilder.LifecyclePolicyAction(
            type=imagebuilder.LifecyclePolicyActionType.DEPRECATE,
            include_amis=True
        ),
        filter=imagebuilder.LifecyclePolicyFilter(
            age_filter=imagebuilder.LifecyclePolicyAgeFilter(
                age=Duration.days(30),
                retain_at_least=5
            )
        )
    ), imagebuilder.LifecyclePolicyDetail(
        # Second: Disable images after 60 days
        action=imagebuilder.LifecyclePolicyAction(
            type=imagebuilder.LifecyclePolicyActionType.DISABLE,
            include_amis=True
        ),
        filter=imagebuilder.LifecyclePolicyFilter(
            age_filter=imagebuilder.LifecyclePolicyAgeFilter(
                age=Duration.days(60),
                retain_at_least=3
            )
        )
    ), imagebuilder.LifecyclePolicyDetail(
        # Finally: Delete images after 90 days
        action=imagebuilder.LifecyclePolicyAction(
            type=imagebuilder.LifecyclePolicyActionType.DELETE,
            include_amis=True,
            include_snapshots=True
        ),
        filter=imagebuilder.LifecyclePolicyFilter(
            age_filter=imagebuilder.LifecyclePolicyAgeFilter(
                age=Duration.days(90),
                retain_at_least=1
            )
        )
    )
    ],
    resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
        tags={"Environment": "production"}
    )
)
```

#### Lifecycle Policy Exclusion Rules

##### AMI Exclusion Rules

Exclude specific AMIs from lifecycle actions based on various criteria:

```python
exclude_amis_policy = imagebuilder.LifecyclePolicy(self, "ExcludeAmisPolicy",
    resource_type=imagebuilder.LifecyclePolicyResourceType.AMI_IMAGE,
    details=[imagebuilder.LifecyclePolicyDetail(
        action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
        filter=imagebuilder.LifecyclePolicyFilter(age_filter=imagebuilder.LifecyclePolicyAgeFilter(age=Duration.days(30))),
        exclusion_rules=imagebuilder.LifecyclePolicyExclusionRules(
            ami_exclusion_rules=imagebuilder.LifecyclePolicyAmiExclusionRules(
                is_public=True,  # Exclude public AMIs
                last_launched=Duration.days(7),  # Exclude AMIs launched in last 7 days
                regions=["us-west-2", "eu-west-1"],  # Exclude AMIs in specific regions
                shared_accounts=["123456789012"],  # Exclude AMIs shared with specific accounts
                tags={
                    "Protected": "true",
                    "Environment": "production"
                }
            )
        )
    )
    ],
    resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
        tags={"Team": "infrastructure"}
    )
)
```

##### Image Exclusion Rules

Exclude Image Builder images with protective tags:

```python
exclude_images_policy = imagebuilder.LifecyclePolicy(self, "ExcludeImagesPolicy",
    resource_type=imagebuilder.LifecyclePolicyResourceType.CONTAINER_IMAGE,
    details=[imagebuilder.LifecyclePolicyDetail(
        action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
        filter=imagebuilder.LifecyclePolicyFilter(count_filter=imagebuilder.LifecyclePolicyCountFilter(count=20)),
        exclusion_rules=imagebuilder.LifecyclePolicyExclusionRules(
            image_exclusion_rules=imagebuilder.LifecyclePolicyImageExclusionRules(
                tags={
                    "DoNotDelete": "true",
                    "Critical": "baseline"
                }
            )
        )
    )
    ],
    resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
        tags={"Application": "frontend"}
    )
)
```

#### Advanced Lifecycle Configuration

##### Custom Execution Roles

Provide your own IAM execution role with specific permissions:

```python
execution_role = iam.Role(self, "LifecycleExecutionRole",
    assumed_by=iam.ServicePrincipal("imagebuilder.amazonaws.com"),
    managed_policies=[
        iam.ManagedPolicy.from_aws_managed_policy_name("service-role/EC2ImageBuilderLifecycleExecutionPolicy")
    ]
)

custom_role_policy = imagebuilder.LifecyclePolicy(self, "CustomRolePolicy",
    resource_type=imagebuilder.LifecyclePolicyResourceType.AMI_IMAGE,
    execution_role=execution_role,
    details=[imagebuilder.LifecyclePolicyDetail(
        action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
        filter=imagebuilder.LifecyclePolicyFilter(age_filter=imagebuilder.LifecyclePolicyAgeFilter(age=Duration.days(45)))
    )
    ],
    resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
        tags={"Environment": "development"}
    )
)
```

##### Lifecycle Policy Status

Control whether the lifecycle policy is active:

```python
disabled_policy = imagebuilder.LifecyclePolicy(self, "DisabledPolicy",
    lifecycle_policy_name="my-disabled-policy",
    description="A lifecycle policy that is temporarily disabled",
    status=imagebuilder.LifecyclePolicyStatus.DISABLED,
    resource_type=imagebuilder.LifecyclePolicyResourceType.AMI_IMAGE,
    details=[imagebuilder.LifecyclePolicyDetail(
        action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
        filter=imagebuilder.LifecyclePolicyFilter(age_filter=imagebuilder.LifecyclePolicyAgeFilter(age=Duration.days(30)))
    )
    ],
    resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
        tags={"Environment": "testing"}
    ),
    tags={
        "Owner": "DevOps",
        "CostCenter": "Engineering"
    }
)
```

##### Importing Lifecycle Policies

Reference lifecycle policies created outside CDK:

```python
# Import by name
imported_by_name = imagebuilder.LifecyclePolicy.from_lifecycle_policy_name(self, "ImportedByName", "existing-lifecycle-policy")

# Import by ARN
imported_by_arn = imagebuilder.LifecyclePolicy.from_lifecycle_policy_arn(self, "ImportedByArn", "arn:aws:imagebuilder:us-east-1:123456789012:lifecycle-policy/my-policy")

imported_by_name.grant_read(lambda_role)
imported_by_arn.grant(lambda_role, "imagebuilder:UpdateLifecyclePolicy")
```
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
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_ecr as _aws_cdk_aws_ecr_ceddda9d
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_s3_assets as _aws_cdk_aws_s3_assets_ceddda9d
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import aws_cdk.aws_ssm as _aws_cdk_aws_ssm_ceddda9d
import aws_cdk.interfaces.aws_kms as _aws_cdk_interfaces_aws_kms_ceddda9d
import constructs as _constructs_77d1e7e8


class AmazonManagedImage(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.AmazonManagedImage",
):
    '''(experimental) Helper class for working with Amazon-managed images.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Amazon Linux 2023 AMI for x86_64
        amazon_linux2023_ami = imagebuilder.AmazonManagedImage.amazon_linux2023(self, "AmazonLinux2023",
            image_type=imagebuilder.ImageType.AMI,
            image_architecture=imagebuilder.ImageArchitecture.X86_64
        )
        
        # Ubuntu 22.04 AMI for ARM64
        ubuntu2204_ami = imagebuilder.AmazonManagedImage.ubuntu_server2204(self, "Ubuntu2204",
            image_type=imagebuilder.ImageType.AMI,
            image_architecture=imagebuilder.ImageArchitecture.ARM64
        )
        
        # Windows Server 2022 Full AMI
        windows2022_ami = imagebuilder.AmazonManagedImage.windows_server2022_full(self, "Windows2022",
            image_type=imagebuilder.ImageType.AMI,
            image_architecture=imagebuilder.ImageArchitecture.X86_64
        )
        
        # Use as base image in recipe
        managed_image_recipe = imagebuilder.ImageRecipe(self, "ManagedImageRecipe",
            base_image=amazon_linux2023_ami.to_base_image()
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="amazonLinux2")
    @builtins.classmethod
    def amazon_linux2(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_architecture: "ImageArchitecture",
        image_type: "ImageType",
        image_version: typing.Optional[builtins.str] = None,
    ) -> "IImage":
        '''(experimental) Imports the Amazon Linux 2 Amazon-managed image.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param image_architecture: (experimental) The architecture of the Amazon-managed image.
        :param image_type: (experimental) The type of the Amazon-managed image.
        :param image_version: (experimental) The version of the Amazon-managed image. Default: x.x.x

        :see: https://gallery.ecr.aws/amazonlinux/amazonlinux
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7947700e1122d5aa4d0d7d9b637c3b9bd5948401fff18ddf1422d9d999866961)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        opts = AmazonManagedImageOptions(
            image_architecture=image_architecture,
            image_type=image_type,
            image_version=image_version,
        )

        return typing.cast("IImage", jsii.sinvoke(cls, "amazonLinux2", [scope, id, opts]))

    @jsii.member(jsii_name="amazonLinux2023")
    @builtins.classmethod
    def amazon_linux2023(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_architecture: "ImageArchitecture",
        image_type: "ImageType",
        image_version: typing.Optional[builtins.str] = None,
    ) -> "IImage":
        '''(experimental) Imports the Amazon Linux 2023 Amazon-managed image.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param image_architecture: (experimental) The architecture of the Amazon-managed image.
        :param image_type: (experimental) The type of the Amazon-managed image.
        :param image_version: (experimental) The version of the Amazon-managed image. Default: x.x.x

        :see: https://gallery.ecr.aws/amazonlinux/amazonlinux
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4d6bd3dc3695283fd4d95f78be62c5a0657d8b9ae95743a91a31109e52c761f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        opts = AmazonManagedImageOptions(
            image_architecture=image_architecture,
            image_type=image_type,
            image_version=image_version,
        )

        return typing.cast("IImage", jsii.sinvoke(cls, "amazonLinux2023", [scope, id, opts]))

    @jsii.member(jsii_name="fromAmazonManagedImageAttributes")
    @builtins.classmethod
    def from_amazon_managed_image_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_name: builtins.str,
        image_version: typing.Optional[builtins.str] = None,
    ) -> "IImage":
        '''(experimental) Imports an Amazon-managed image from its attributes.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param image_name: (experimental) The name of the Amazon-managed image. The provided name must be normalized by converting all alphabetical characters to lowercase, and replacing all spaces and underscores with hyphens.
        :param image_version: (experimental) The version of the Amazon-managed image. Default: x.x.x

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b66d2662230092726641e7e4836619556bd9e4b713a6fc4529a28b947f78b58)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = AmazonManagedImageAttributes(
            image_name=image_name, image_version=image_version
        )

        return typing.cast("IImage", jsii.sinvoke(cls, "fromAmazonManagedImageAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromAmazonManagedImageName")
    @builtins.classmethod
    def from_amazon_managed_image_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        amazon_managed_image_name: builtins.str,
    ) -> "IImage":
        '''(experimental) Imports an Amazon-managed image from its name.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param amazon_managed_image_name: - The name of the Amazon-managed image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__063769c3bafee118e66089b0f686c22bca6dc78fe974fe2edac626a19dfe8ebc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument amazon_managed_image_name", value=amazon_managed_image_name, expected_type=type_hints["amazon_managed_image_name"])
        return typing.cast("IImage", jsii.sinvoke(cls, "fromAmazonManagedImageName", [scope, id, amazon_managed_image_name]))

    @jsii.member(jsii_name="macOS14")
    @builtins.classmethod
    def mac_os14(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_architecture: "ImageArchitecture",
        image_type: "ImageType",
        image_version: typing.Optional[builtins.str] = None,
    ) -> "IImage":
        '''(experimental) Imports the macOS 14 Amazon-managed image.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param image_architecture: (experimental) The architecture of the Amazon-managed image.
        :param image_type: (experimental) The type of the Amazon-managed image.
        :param image_version: (experimental) The version of the Amazon-managed image. Default: x.x.x

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-mac-instances.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8a90e0540bc8af83339fcb4098a61e8ec9f39158584ff8fb17117a8fe360fe3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        opts = AmazonManagedImageOptions(
            image_architecture=image_architecture,
            image_type=image_type,
            image_version=image_version,
        )

        return typing.cast("IImage", jsii.sinvoke(cls, "macOS14", [scope, id, opts]))

    @jsii.member(jsii_name="macOS15")
    @builtins.classmethod
    def mac_os15(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_architecture: "ImageArchitecture",
        image_type: "ImageType",
        image_version: typing.Optional[builtins.str] = None,
    ) -> "IImage":
        '''(experimental) Imports the macOS 15 Amazon-managed image.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param image_architecture: (experimental) The architecture of the Amazon-managed image.
        :param image_type: (experimental) The type of the Amazon-managed image.
        :param image_version: (experimental) The version of the Amazon-managed image. Default: x.x.x

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-mac-instances.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0fc5bb0d6de80813a16eb2998d0611a274a576256375f31b472e02f80d78571)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        opts = AmazonManagedImageOptions(
            image_architecture=image_architecture,
            image_type=image_type,
            image_version=image_version,
        )

        return typing.cast("IImage", jsii.sinvoke(cls, "macOS15", [scope, id, opts]))

    @jsii.member(jsii_name="redHatEnterpriseLinux10")
    @builtins.classmethod
    def red_hat_enterprise_linux10(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_architecture: "ImageArchitecture",
        image_type: "ImageType",
        image_version: typing.Optional[builtins.str] = None,
    ) -> "IImage":
        '''(experimental) Imports the Red Hat Enterprise Linux 10 Amazon-managed image.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param image_architecture: (experimental) The architecture of the Amazon-managed image.
        :param image_type: (experimental) The type of the Amazon-managed image.
        :param image_version: (experimental) The version of the Amazon-managed image. Default: x.x.x

        :see: https://aws.amazon.com/partners/redhat/faqs
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__249c269acb30f26f021ece47976db26ca8237f4a85754bfb451ab6e90b553eac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        opts = AmazonManagedImageOptions(
            image_architecture=image_architecture,
            image_type=image_type,
            image_version=image_version,
        )

        return typing.cast("IImage", jsii.sinvoke(cls, "redHatEnterpriseLinux10", [scope, id, opts]))

    @jsii.member(jsii_name="suseLinuxEnterpriseServer15")
    @builtins.classmethod
    def suse_linux_enterprise_server15(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_architecture: "ImageArchitecture",
        image_type: "ImageType",
        image_version: typing.Optional[builtins.str] = None,
    ) -> "IImage":
        '''(experimental) Imports the SUSE Linux Enterprise Server 15 Amazon-managed image.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param image_architecture: (experimental) The architecture of the Amazon-managed image.
        :param image_type: (experimental) The type of the Amazon-managed image.
        :param image_version: (experimental) The version of the Amazon-managed image. Default: x.x.x

        :see: https://aws.amazon.com/linux/commercial-linux/faqs/
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89450646b941985086d014d2c31fe96ddacad781ad42b07676f74f1e017d1ba3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        opts = AmazonManagedImageOptions(
            image_architecture=image_architecture,
            image_type=image_type,
            image_version=image_version,
        )

        return typing.cast("IImage", jsii.sinvoke(cls, "suseLinuxEnterpriseServer15", [scope, id, opts]))

    @jsii.member(jsii_name="ubuntuServer2204")
    @builtins.classmethod
    def ubuntu_server2204(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_architecture: "ImageArchitecture",
        image_type: "ImageType",
        image_version: typing.Optional[builtins.str] = None,
    ) -> "IImage":
        '''(experimental) Imports the Ubuntu 22.04 Amazon-managed image.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param image_architecture: (experimental) The architecture of the Amazon-managed image.
        :param image_type: (experimental) The type of the Amazon-managed image.
        :param image_version: (experimental) The version of the Amazon-managed image. Default: x.x.x

        :see: https://hub.docker.com/_/ubuntu
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f79c89eeed43e42c3aecf4cbbe3d75f1454077443edd9d827a142f4c53e7ee11)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        opts = AmazonManagedImageOptions(
            image_architecture=image_architecture,
            image_type=image_type,
            image_version=image_version,
        )

        return typing.cast("IImage", jsii.sinvoke(cls, "ubuntuServer2204", [scope, id, opts]))

    @jsii.member(jsii_name="ubuntuServer2404")
    @builtins.classmethod
    def ubuntu_server2404(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_architecture: "ImageArchitecture",
        image_type: "ImageType",
        image_version: typing.Optional[builtins.str] = None,
    ) -> "IImage":
        '''(experimental) Imports the Ubuntu 24.04 Amazon-managed image.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param image_architecture: (experimental) The architecture of the Amazon-managed image.
        :param image_type: (experimental) The type of the Amazon-managed image.
        :param image_version: (experimental) The version of the Amazon-managed image. Default: x.x.x

        :see: https://hub.docker.com/_/ubuntu
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01f55fa360510b50813985792d1c6504ed9c557eda04ffd0aeae52275952ceb3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        opts = AmazonManagedImageOptions(
            image_architecture=image_architecture,
            image_type=image_type,
            image_version=image_version,
        )

        return typing.cast("IImage", jsii.sinvoke(cls, "ubuntuServer2404", [scope, id, opts]))

    @jsii.member(jsii_name="windowsServer2016Core")
    @builtins.classmethod
    def windows_server2016_core(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_architecture: "ImageArchitecture",
        image_type: "ImageType",
        image_version: typing.Optional[builtins.str] = None,
    ) -> "IImage":
        '''(experimental) Imports the Windows Server 2016 Core Amazon-managed image.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param image_architecture: (experimental) The architecture of the Amazon-managed image.
        :param image_type: (experimental) The type of the Amazon-managed image.
        :param image_version: (experimental) The version of the Amazon-managed image. Default: x.x.x

        :see: https://hub.docker.com/r/microsoft/windows-servercore
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__259375d42f13f9fadb8c5a63cf0ee57d1f37478062e2d18c6208a89c67bd0bb3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        opts = AmazonManagedImageOptions(
            image_architecture=image_architecture,
            image_type=image_type,
            image_version=image_version,
        )

        return typing.cast("IImage", jsii.sinvoke(cls, "windowsServer2016Core", [scope, id, opts]))

    @jsii.member(jsii_name="windowsServer2016Full")
    @builtins.classmethod
    def windows_server2016_full(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_architecture: "ImageArchitecture",
        image_type: "ImageType",
        image_version: typing.Optional[builtins.str] = None,
    ) -> "IImage":
        '''(experimental) Imports the Windows Server 2016 Full Amazon-managed image.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param image_architecture: (experimental) The architecture of the Amazon-managed image.
        :param image_type: (experimental) The type of the Amazon-managed image.
        :param image_version: (experimental) The version of the Amazon-managed image. Default: x.x.x

        :see: https://docs.aws.amazon.com/ec2/latest/windows-ami-reference/index.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__020643b3889e3e4a8e90e663491955ea5e8e406ba2fff268471b7c49eae26cc4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        opts = AmazonManagedImageOptions(
            image_architecture=image_architecture,
            image_type=image_type,
            image_version=image_version,
        )

        return typing.cast("IImage", jsii.sinvoke(cls, "windowsServer2016Full", [scope, id, opts]))

    @jsii.member(jsii_name="windowsServer2019Core")
    @builtins.classmethod
    def windows_server2019_core(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_architecture: "ImageArchitecture",
        image_type: "ImageType",
        image_version: typing.Optional[builtins.str] = None,
    ) -> "IImage":
        '''(experimental) Imports the Windows Server 2019 Core Amazon-managed image.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param image_architecture: (experimental) The architecture of the Amazon-managed image.
        :param image_type: (experimental) The type of the Amazon-managed image.
        :param image_version: (experimental) The version of the Amazon-managed image. Default: x.x.x

        :see: https://hub.docker.com/r/microsoft/windows-servercore
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc810e858fab1db87e4b0c2348c64c1cb5fe9f4079825f70cdbfdfe298c76249)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        opts = AmazonManagedImageOptions(
            image_architecture=image_architecture,
            image_type=image_type,
            image_version=image_version,
        )

        return typing.cast("IImage", jsii.sinvoke(cls, "windowsServer2019Core", [scope, id, opts]))

    @jsii.member(jsii_name="windowsServer2019Full")
    @builtins.classmethod
    def windows_server2019_full(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_architecture: "ImageArchitecture",
        image_type: "ImageType",
        image_version: typing.Optional[builtins.str] = None,
    ) -> "IImage":
        '''(experimental) Imports the Windows Server 2019 Full Amazon-managed image.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param image_architecture: (experimental) The architecture of the Amazon-managed image.
        :param image_type: (experimental) The type of the Amazon-managed image.
        :param image_version: (experimental) The version of the Amazon-managed image. Default: x.x.x

        :see: https://docs.aws.amazon.com/ec2/latest/windows-ami-reference/index.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17fe12aaec5fb10118a69b960cf85c1e0779655f8dfb3671c264cdca3d64afa4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        opts = AmazonManagedImageOptions(
            image_architecture=image_architecture,
            image_type=image_type,
            image_version=image_version,
        )

        return typing.cast("IImage", jsii.sinvoke(cls, "windowsServer2019Full", [scope, id, opts]))

    @jsii.member(jsii_name="windowsServer2022Core")
    @builtins.classmethod
    def windows_server2022_core(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_architecture: "ImageArchitecture",
        image_type: "ImageType",
        image_version: typing.Optional[builtins.str] = None,
    ) -> "IImage":
        '''(experimental) Imports the Windows Server 2022 Core Amazon-managed image.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param image_architecture: (experimental) The architecture of the Amazon-managed image.
        :param image_type: (experimental) The type of the Amazon-managed image.
        :param image_version: (experimental) The version of the Amazon-managed image. Default: x.x.x

        :see: https://docs.aws.amazon.com/ec2/latest/windows-ami-reference/index.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e78c9c813e22a826ec7fff531cbea709a35dcb0969f8c81e8b00de3c996093)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        opts = AmazonManagedImageOptions(
            image_architecture=image_architecture,
            image_type=image_type,
            image_version=image_version,
        )

        return typing.cast("IImage", jsii.sinvoke(cls, "windowsServer2022Core", [scope, id, opts]))

    @jsii.member(jsii_name="windowsServer2022Full")
    @builtins.classmethod
    def windows_server2022_full(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_architecture: "ImageArchitecture",
        image_type: "ImageType",
        image_version: typing.Optional[builtins.str] = None,
    ) -> "IImage":
        '''(experimental) Imports the Windows Server 2022 Full Amazon-managed image.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param image_architecture: (experimental) The architecture of the Amazon-managed image.
        :param image_type: (experimental) The type of the Amazon-managed image.
        :param image_version: (experimental) The version of the Amazon-managed image. Default: x.x.x

        :see: https://docs.aws.amazon.com/ec2/latest/windows-ami-reference/index.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7ba66c48751044fc285ce087542041940238dcd0ee33f909aa3970e9d5feced)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        opts = AmazonManagedImageOptions(
            image_architecture=image_architecture,
            image_type=image_type,
            image_version=image_version,
        )

        return typing.cast("IImage", jsii.sinvoke(cls, "windowsServer2022Full", [scope, id, opts]))

    @jsii.member(jsii_name="windowsServer2025Core")
    @builtins.classmethod
    def windows_server2025_core(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_architecture: "ImageArchitecture",
        image_type: "ImageType",
        image_version: typing.Optional[builtins.str] = None,
    ) -> "IImage":
        '''(experimental) Imports the Windows Server 2025 Core Amazon-managed image.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param image_architecture: (experimental) The architecture of the Amazon-managed image.
        :param image_type: (experimental) The type of the Amazon-managed image.
        :param image_version: (experimental) The version of the Amazon-managed image. Default: x.x.x

        :see: https://docs.aws.amazon.com/ec2/latest/windows-ami-reference/index.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35ea4f3fc7629d971e5d2679cb3e6679b795f4723fbc7a56ac489a030fd4ea81)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        opts = AmazonManagedImageOptions(
            image_architecture=image_architecture,
            image_type=image_type,
            image_version=image_version,
        )

        return typing.cast("IImage", jsii.sinvoke(cls, "windowsServer2025Core", [scope, id, opts]))

    @jsii.member(jsii_name="windowsServer2025Full")
    @builtins.classmethod
    def windows_server2025_full(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_architecture: "ImageArchitecture",
        image_type: "ImageType",
        image_version: typing.Optional[builtins.str] = None,
    ) -> "IImage":
        '''(experimental) Imports the Windows Server 2025 Full Amazon-managed image.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param image_architecture: (experimental) The architecture of the Amazon-managed image.
        :param image_type: (experimental) The type of the Amazon-managed image.
        :param image_version: (experimental) The version of the Amazon-managed image. Default: x.x.x

        :see: https://docs.aws.amazon.com/ec2/latest/windows-ami-reference/index.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe55b3cafe893bb3dd918aa59cf063319e9956fd385f2c3e07cd7b17d7b4c24)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        opts = AmazonManagedImageOptions(
            image_architecture=image_architecture,
            image_type=image_type,
            image_version=image_version,
        )

        return typing.cast("IImage", jsii.sinvoke(cls, "windowsServer2025Full", [scope, id, opts]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.AmazonManagedImageAttributes",
    jsii_struct_bases=[],
    name_mapping={"image_name": "imageName", "image_version": "imageVersion"},
)
class AmazonManagedImageAttributes:
    def __init__(
        self,
        *,
        image_name: builtins.str,
        image_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Attributes for importing an Amazon-managed image by name (and optionally a version).

        :param image_name: (experimental) The name of the Amazon-managed image. The provided name must be normalized by converting all alphabetical characters to lowercase, and replacing all spaces and underscores with hyphens.
        :param image_version: (experimental) The version of the Amazon-managed image. Default: x.x.x

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # Import by name
            managed_image_by_name = imagebuilder.AmazonManagedImage.from_amazon_managed_image_name(self, "ManagedImageByName", "amazon-linux-2023-x86")
            
            # Import by attributes with specific version
            managed_image_by_attributes = imagebuilder.AmazonManagedImage.from_amazon_managed_image_attributes(self, "ManagedImageByAttributes",
                image_name="ubuntu-server-22-lts-x86",
                image_version="2024.11.25"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e6c580216396266e53e26e73fe91034e57c6ded616ace3f4f3ffd74c548c8e3)
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument image_version", value=image_version, expected_type=type_hints["image_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_name": image_name,
        }
        if image_version is not None:
            self._values["image_version"] = image_version

    @builtins.property
    def image_name(self) -> builtins.str:
        '''(experimental) The name of the Amazon-managed image.

        The provided name must be normalized by converting all alphabetical
        characters to lowercase, and replacing all spaces and underscores with hyphens.

        :stability: experimental
        '''
        result = self._values.get("image_name")
        assert result is not None, "Required property 'image_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the Amazon-managed image.

        :default: x.x.x

        :stability: experimental
        '''
        result = self._values.get("image_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AmazonManagedImageAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.AmazonManagedImageOptions",
    jsii_struct_bases=[],
    name_mapping={
        "image_architecture": "imageArchitecture",
        "image_type": "imageType",
        "image_version": "imageVersion",
    },
)
class AmazonManagedImageOptions:
    def __init__(
        self,
        *,
        image_architecture: "ImageArchitecture",
        image_type: "ImageType",
        image_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for selecting a predefined Amazon-managed image.

        :param image_architecture: (experimental) The architecture of the Amazon-managed image.
        :param image_type: (experimental) The type of the Amazon-managed image.
        :param image_version: (experimental) The version of the Amazon-managed image. Default: x.x.x

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # Amazon Linux 2023 AMI for x86_64
            amazon_linux2023_ami = imagebuilder.AmazonManagedImage.amazon_linux2023(self, "AmazonLinux2023",
                image_type=imagebuilder.ImageType.AMI,
                image_architecture=imagebuilder.ImageArchitecture.X86_64
            )
            
            # Ubuntu 22.04 AMI for ARM64
            ubuntu2204_ami = imagebuilder.AmazonManagedImage.ubuntu_server2204(self, "Ubuntu2204",
                image_type=imagebuilder.ImageType.AMI,
                image_architecture=imagebuilder.ImageArchitecture.ARM64
            )
            
            # Windows Server 2022 Full AMI
            windows2022_ami = imagebuilder.AmazonManagedImage.windows_server2022_full(self, "Windows2022",
                image_type=imagebuilder.ImageType.AMI,
                image_architecture=imagebuilder.ImageArchitecture.X86_64
            )
            
            # Use as base image in recipe
            managed_image_recipe = imagebuilder.ImageRecipe(self, "ManagedImageRecipe",
                base_image=amazon_linux2023_ami.to_base_image()
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ec2d910a894edc13dfa7e84a3c18d579d4c6177a5d686f7deaa9fdc2bff83c8)
            check_type(argname="argument image_architecture", value=image_architecture, expected_type=type_hints["image_architecture"])
            check_type(argname="argument image_type", value=image_type, expected_type=type_hints["image_type"])
            check_type(argname="argument image_version", value=image_version, expected_type=type_hints["image_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_architecture": image_architecture,
            "image_type": image_type,
        }
        if image_version is not None:
            self._values["image_version"] = image_version

    @builtins.property
    def image_architecture(self) -> "ImageArchitecture":
        '''(experimental) The architecture of the Amazon-managed image.

        :stability: experimental
        '''
        result = self._values.get("image_architecture")
        assert result is not None, "Required property 'image_architecture' is missing"
        return typing.cast("ImageArchitecture", result)

    @builtins.property
    def image_type(self) -> "ImageType":
        '''(experimental) The type of the Amazon-managed image.

        :stability: experimental
        '''
        result = self._values.get("image_type")
        assert result is not None, "Required property 'image_type' is missing"
        return typing.cast("ImageType", result)

    @builtins.property
    def image_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the Amazon-managed image.

        :default: x.x.x

        :stability: experimental
        '''
        result = self._values.get("image_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AmazonManagedImageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.AmiDistribution",
    jsii_struct_bases=[],
    name_mapping={
        "ami_description": "amiDescription",
        "ami_kms_key": "amiKmsKey",
        "ami_launch_permission": "amiLaunchPermission",
        "ami_name": "amiName",
        "ami_tags": "amiTags",
        "ami_target_account_ids": "amiTargetAccountIds",
        "fast_launch_configurations": "fastLaunchConfigurations",
        "launch_templates": "launchTemplates",
        "license_configuration_arns": "licenseConfigurationArns",
        "region": "region",
        "ssm_parameters": "ssmParameters",
    },
)
class AmiDistribution:
    def __init__(
        self,
        *,
        ami_description: typing.Optional[builtins.str] = None,
        ami_kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        ami_launch_permission: typing.Optional[typing.Union["AmiLaunchPermission", typing.Dict[builtins.str, typing.Any]]] = None,
        ami_name: typing.Optional[builtins.str] = None,
        ami_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        ami_target_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        fast_launch_configurations: typing.Optional[typing.Sequence[typing.Union["FastLaunchConfiguration", typing.Dict[builtins.str, typing.Any]]]] = None,
        launch_templates: typing.Optional[typing.Sequence[typing.Union["LaunchTemplateConfiguration", typing.Dict[builtins.str, typing.Any]]]] = None,
        license_configuration_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        ssm_parameters: typing.Optional[typing.Sequence[typing.Union["SSMParameterConfigurations", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) The regional distribution settings to use for an AMI build.

        :param ami_description: (experimental) The description of the AMI. Default: None
        :param ami_kms_key: (experimental) The KMS key to encrypt the distributed AMI with. Default: None
        :param ami_launch_permission: (experimental) The launch permissions for the AMI, defining which principals are allowed to access the AMI. Default: None
        :param ami_name: (experimental) The name to use for the distributed AMIs. Default: A name is generated from the image recipe name
        :param ami_tags: (experimental) The tags to apply to the distributed AMIs. Default: None
        :param ami_target_account_ids: (experimental) The account IDs to copy the output AMI to. Default: None
        :param fast_launch_configurations: (experimental) The fast launch configurations to use for enabling EC2 Fast Launch on the distributed Windows AMI. Default: None
        :param launch_templates: (experimental) The launch templates to apply the distributed AMI to. Default: None
        :param license_configuration_arns: (experimental) The License Manager license configuration ARNs to apply to the distributed AMIs. Default: None
        :param region: (experimental) The target region to distribute AMIs to. Default: The current region is used
        :param ssm_parameters: (experimental) The SSM parameters to create or update for the distributed AMIs. Default: None

        :stability: experimental
        :exampleMetadata: infused

        Example::

            infrastructure_configuration = imagebuilder.InfrastructureConfiguration(self, "Infrastructure",
                infrastructure_configuration_name="production-infrastructure",
                instance_types=[
                    ec2.InstanceType.of(ec2.InstanceClass.COMPUTE7_INTEL, ec2.InstanceSize.LARGE)
                ],
                vpc=vpc,
                subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
            )
            
            distribution_configuration = imagebuilder.DistributionConfiguration(self, "Distribution")
            distribution_configuration.add_ami_distributions(
                ami_name="production-ami-{{ imagebuilder:buildDate }}",
                ami_target_account_ids=["123456789012", "098765432109"]
            )
            
            production_pipeline = imagebuilder.ImagePipeline(self, "ProductionPipeline",
                recipe=example_image_recipe,
                infrastructure_configuration=infrastructure_configuration,
                distribution_configuration=distribution_configuration
            )
        '''
        if isinstance(ami_launch_permission, dict):
            ami_launch_permission = AmiLaunchPermission(**ami_launch_permission)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bbb50c8ed5cb401fdf362f5d0a7b629c2c082dbdaadf32bcf6aef95e968f20b)
            check_type(argname="argument ami_description", value=ami_description, expected_type=type_hints["ami_description"])
            check_type(argname="argument ami_kms_key", value=ami_kms_key, expected_type=type_hints["ami_kms_key"])
            check_type(argname="argument ami_launch_permission", value=ami_launch_permission, expected_type=type_hints["ami_launch_permission"])
            check_type(argname="argument ami_name", value=ami_name, expected_type=type_hints["ami_name"])
            check_type(argname="argument ami_tags", value=ami_tags, expected_type=type_hints["ami_tags"])
            check_type(argname="argument ami_target_account_ids", value=ami_target_account_ids, expected_type=type_hints["ami_target_account_ids"])
            check_type(argname="argument fast_launch_configurations", value=fast_launch_configurations, expected_type=type_hints["fast_launch_configurations"])
            check_type(argname="argument launch_templates", value=launch_templates, expected_type=type_hints["launch_templates"])
            check_type(argname="argument license_configuration_arns", value=license_configuration_arns, expected_type=type_hints["license_configuration_arns"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument ssm_parameters", value=ssm_parameters, expected_type=type_hints["ssm_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ami_description is not None:
            self._values["ami_description"] = ami_description
        if ami_kms_key is not None:
            self._values["ami_kms_key"] = ami_kms_key
        if ami_launch_permission is not None:
            self._values["ami_launch_permission"] = ami_launch_permission
        if ami_name is not None:
            self._values["ami_name"] = ami_name
        if ami_tags is not None:
            self._values["ami_tags"] = ami_tags
        if ami_target_account_ids is not None:
            self._values["ami_target_account_ids"] = ami_target_account_ids
        if fast_launch_configurations is not None:
            self._values["fast_launch_configurations"] = fast_launch_configurations
        if launch_templates is not None:
            self._values["launch_templates"] = launch_templates
        if license_configuration_arns is not None:
            self._values["license_configuration_arns"] = license_configuration_arns
        if region is not None:
            self._values["region"] = region
        if ssm_parameters is not None:
            self._values["ssm_parameters"] = ssm_parameters

    @builtins.property
    def ami_description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the AMI.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("ami_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ami_kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to encrypt the distributed AMI with.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("ami_kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def ami_launch_permission(self) -> typing.Optional["AmiLaunchPermission"]:
        '''(experimental) The launch permissions for the AMI, defining which principals are allowed to access the AMI.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("ami_launch_permission")
        return typing.cast(typing.Optional["AmiLaunchPermission"], result)

    @builtins.property
    def ami_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name to use for the distributed AMIs.

        :default: A name is generated from the image recipe name

        :stability: experimental
        '''
        result = self._values.get("ami_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ami_tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The tags to apply to the distributed AMIs.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("ami_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def ami_target_account_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The account IDs to copy the output AMI to.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("ami_target_account_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fast_launch_configurations(
        self,
    ) -> typing.Optional[typing.List["FastLaunchConfiguration"]]:
        '''(experimental) The fast launch configurations to use for enabling EC2 Fast Launch on the distributed Windows AMI.

        :default: None

        :see: https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_EnableFastLaunch.html
        :stability: experimental
        '''
        result = self._values.get("fast_launch_configurations")
        return typing.cast(typing.Optional[typing.List["FastLaunchConfiguration"]], result)

    @builtins.property
    def launch_templates(
        self,
    ) -> typing.Optional[typing.List["LaunchTemplateConfiguration"]]:
        '''(experimental) The launch templates to apply the distributed AMI to.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("launch_templates")
        return typing.cast(typing.Optional[typing.List["LaunchTemplateConfiguration"]], result)

    @builtins.property
    def license_configuration_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The License Manager license configuration ARNs to apply to the distributed AMIs.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("license_configuration_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The target region to distribute AMIs to.

        :default: The current region is used

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssm_parameters(
        self,
    ) -> typing.Optional[typing.List["SSMParameterConfigurations"]]:
        '''(experimental) The SSM parameters to create or update for the distributed AMIs.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("ssm_parameters")
        return typing.cast(typing.Optional[typing.List["SSMParameterConfigurations"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AmiDistribution(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.AmiLaunchPermission",
    jsii_struct_bases=[],
    name_mapping={
        "account_ids": "accountIds",
        "is_public_user_group": "isPublicUserGroup",
        "organizational_unit_arns": "organizationalUnitArns",
        "organization_arns": "organizationArns",
    },
)
class AmiLaunchPermission:
    def __init__(
        self,
        *,
        account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        is_public_user_group: typing.Optional[builtins.bool] = None,
        organizational_unit_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        organization_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) The launch permissions for the AMI, defining which principals are allowed to access the AMI.

        :param account_ids: (experimental) The AWS account IDs to share the AMI with. Default: None
        :param is_public_user_group: (experimental) Whether to make the AMI public. Block public access for AMIs must be disabled to make the AMI public. WARNING: Making an AMI public exposes it to any AWS account globally. Ensure the AMI does not contain: - Sensitive data or credentials - Proprietary software or configurations - Internal network information or security settings For more information on blocking public access for AMIs, see: `Understand block public access for AMIs <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-public-access-to-amis.html>`_ Default: false
        :param organizational_unit_arns: (experimental) The ARNs for the AWS Organizations organizational units to share the AMI with. Default: None
        :param organization_arns: (experimental) The ARNs for the AWS Organization that you want to share the AMI with. Default: None

        :stability: experimental
        :exampleMetadata: infused

        Example::

            distribution_configuration = imagebuilder.DistributionConfiguration(self, "DistributionConfiguration",
                distribution_configuration_name="test-distribution-configuration",
                description="A Distribution Configuration",
                ami_distributions=[imagebuilder.AmiDistribution(
                    # Distribute AMI to us-east-2 and publish the AMI ID to an SSM parameter
                    region="us-east-2",
                    ssm_parameters=[imagebuilder.SSMParameterConfigurations(
                        parameter=ssm.StringParameter.from_string_parameter_attributes(self, "CrossRegionParameter",
                            parameter_name="/imagebuilder/ami",
                            force_dynamic_reference=True
                        )
                    )
                    ]
                )
                ]
            )
            
            # For AMI-based image builds - add an AMI distribution in the current region
            distribution_configuration.add_ami_distributions(
                ami_name="imagebuilder-{{ imagebuilder:buildDate }}",
                ami_description="Build AMI",
                ami_kms_key=kms.Key.from_lookup(self, "ComponentKey", alias_name="alias/distribution-encryption-key"),
                # Copy the AMI to different accounts
                ami_target_account_ids=["123456789012", "098765432109"],
                # Add launch permissions on the AMI
                ami_launch_permission=imagebuilder.AmiLaunchPermission(
                    organization_arns=[
                        self.format_arn(region="", service="organizations", resource="organization", resource_name="o-1234567abc")
                    ],
                    organizational_unit_arns=[
                        self.format_arn(
                            region="",
                            service="organizations",
                            resource="ou",
                            resource_name="o-1234567abc/ou-a123-b4567890"
                        )
                    ],
                    is_public_user_group=True,
                    account_ids=["234567890123"]
                ),
                # Attach tags to the AMI
                ami_tags={
                    "Environment": "production",
                    "Version": "{{ imagebuilder:buildVersion }}"
                },
                # Optional - publish the distributed AMI ID to an SSM parameter
                ssm_parameters=[imagebuilder.SSMParameterConfigurations(
                    parameter=ssm.StringParameter.from_string_parameter_attributes(self, "Parameter",
                        parameter_name="/imagebuilder/ami",
                        force_dynamic_reference=True
                    )
                ), imagebuilder.SSMParameterConfigurations(
                    ami_account="098765432109",
                    data_type=ssm.ParameterDataType.TEXT,
                    parameter=ssm.StringParameter.from_string_parameter_attributes(self, "CrossAccountParameter",
                        parameter_name="imagebuilder-prod-ami",
                        force_dynamic_reference=True
                    )
                )
                ],
                # Optional - create a new launch template version with the distributed AMI ID
                launch_templates=[imagebuilder.LaunchTemplateConfiguration(
                    launch_template=ec2.LaunchTemplate.from_launch_template_attributes(self, "LaunchTemplate",
                        launch_template_id="lt-1234"
                    ),
                    set_default_version=True
                ), imagebuilder.LaunchTemplateConfiguration(
                    account_id="123456789012",
                    launch_template=ec2.LaunchTemplate.from_launch_template_attributes(self, "CrossAccountLaunchTemplate",
                        launch_template_id="lt-5678"
                    ),
                    set_default_version=True
                )
                ],
                # Optional - enable Fast Launch on an imported launch template
                fast_launch_configurations=[imagebuilder.FastLaunchConfiguration(
                    enabled=True,
                    launch_template=ec2.LaunchTemplate.from_launch_template_attributes(self, "FastLaunchLT",
                        launch_template_name="fast-launch-lt"
                    ),
                    max_parallel_launches=10,
                    target_snapshot_count=2
                )
                ],
                # Optional - license configurations to apply to the AMI
                license_configuration_arns=["arn:aws:license-manager:us-west-2:123456789012:license-configuration:lic-abcdefghijklmnopqrstuvwxyz"
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c99475ef38f88d24e515c5d4cfe68b2b801bf8855b6659a379ba52bbf9fc1a2e)
            check_type(argname="argument account_ids", value=account_ids, expected_type=type_hints["account_ids"])
            check_type(argname="argument is_public_user_group", value=is_public_user_group, expected_type=type_hints["is_public_user_group"])
            check_type(argname="argument organizational_unit_arns", value=organizational_unit_arns, expected_type=type_hints["organizational_unit_arns"])
            check_type(argname="argument organization_arns", value=organization_arns, expected_type=type_hints["organization_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_ids is not None:
            self._values["account_ids"] = account_ids
        if is_public_user_group is not None:
            self._values["is_public_user_group"] = is_public_user_group
        if organizational_unit_arns is not None:
            self._values["organizational_unit_arns"] = organizational_unit_arns
        if organization_arns is not None:
            self._values["organization_arns"] = organization_arns

    @builtins.property
    def account_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The AWS account IDs to share the AMI with.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("account_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def is_public_user_group(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to make the AMI public. Block public access for AMIs must be disabled to make the AMI public.

        WARNING: Making an AMI public exposes it to any AWS account globally.
        Ensure the AMI does not contain:

        - Sensitive data or credentials
        - Proprietary software or configurations
        - Internal network information or security settings

        For more information on blocking public access for AMIs, see: `Understand block public access for AMIs <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-public-access-to-amis.html>`_

        :default: false

        :stability: experimental
        '''
        result = self._values.get("is_public_user_group")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def organizational_unit_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The ARNs for the AWS Organizations organizational units to share the AMI with.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("organizational_unit_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def organization_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The ARNs for the AWS Organization that you want to share the AMI with.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("organization_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AmiLaunchPermission(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AwsManagedComponent(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.AwsManagedComponent",
):
    '''(experimental) Helper class for working with AWS-managed components.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        image_recipe = imagebuilder.ImageRecipe(self, "AmazonManagedImageRecipe",
            base_image=imagebuilder.BaseImage.from_ssm_parameter_name("/aws/service/ami-amazon-linux-latest/al2023-ami-minimal-kernel-default-x86_64"),
            components=[imagebuilder.ComponentConfiguration(
                component=imagebuilder.AwsManagedComponent.update_oS(self, "UpdateOS",
                    platform=imagebuilder.Platform.LINUX
                )
            ), imagebuilder.ComponentConfiguration(
                component=imagebuilder.AwsManagedComponent.aws_cli_v2(self, "AwsCli",
                    platform=imagebuilder.Platform.LINUX
                )
            )
            ]
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="awsCliV2")
    @builtins.classmethod
    def aws_cli_v2(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        component_name: typing.Optional[builtins.str] = None,
        component_version: typing.Optional[builtins.str] = None,
        platform: typing.Optional["Platform"] = None,
    ) -> "IComponent":
        '''(experimental) Imports the AWS CLI v2 AWS-managed component.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param component_name: (experimental) The name of the AWS-managed component. The name of the AWS-managed component. This is a required attribute when using the ``this.fromAwsManagedComponentAttributes()`` method. This parameter should not be provided when using the pre-defined managed component methods, such as ``AwsManagedComponent.updateOS()`` and ``AwsManagedComponent.reboot()``. Default: - none if using the pre-defined managed component methods, otherwise a platform is required when using ``this.fromAwsManagedComponentAttributes()``
        :param component_version: (experimental) The version of the AWS-managed component. Default: - the latest version of the component, x.x.x
        :param platform: (experimental) The platform of the AWS-managed component. This is a required attribute when using the pre-defined managed component methods, such as ``AwsManagedComponent.updateOS()`` and ``AwsManagedComponent.reboot()``. This parameter should not be provided when using the ``this.fromAwsManagedComponentAttributes()`` method. Default: - none if using ``this.fromAwsManagedComponentAttributes()``, otherwise a platform is required when using the pre-defined managed component methods

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28a85b2f57e866c107d58316256ca41b5310ce1316357a3af47fb8c9be257978)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = AwsManagedComponentAttributes(
            component_name=component_name,
            component_version=component_version,
            platform=platform,
        )

        return typing.cast("IComponent", jsii.sinvoke(cls, "awsCliV2", [scope, id, attrs]))

    @jsii.member(jsii_name="fromAwsManagedComponentAttributes")
    @builtins.classmethod
    def from_aws_managed_component_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        component_name: typing.Optional[builtins.str] = None,
        component_version: typing.Optional[builtins.str] = None,
        platform: typing.Optional["Platform"] = None,
    ) -> "IComponent":
        '''(experimental) Imports an AWS-managed component from its attributes.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param component_name: (experimental) The name of the AWS-managed component. The name of the AWS-managed component. This is a required attribute when using the ``this.fromAwsManagedComponentAttributes()`` method. This parameter should not be provided when using the pre-defined managed component methods, such as ``AwsManagedComponent.updateOS()`` and ``AwsManagedComponent.reboot()``. Default: - none if using the pre-defined managed component methods, otherwise a platform is required when using ``this.fromAwsManagedComponentAttributes()``
        :param component_version: (experimental) The version of the AWS-managed component. Default: - the latest version of the component, x.x.x
        :param platform: (experimental) The platform of the AWS-managed component. This is a required attribute when using the pre-defined managed component methods, such as ``AwsManagedComponent.updateOS()`` and ``AwsManagedComponent.reboot()``. This parameter should not be provided when using the ``this.fromAwsManagedComponentAttributes()`` method. Default: - none if using ``this.fromAwsManagedComponentAttributes()``, otherwise a platform is required when using the pre-defined managed component methods

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eb8b88fb01463e77d65e8b3815c5fe4a9d52d5ed7d626bea7c9e5bdd7e3c933)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = AwsManagedComponentAttributes(
            component_name=component_name,
            component_version=component_version,
            platform=platform,
        )

        return typing.cast("IComponent", jsii.sinvoke(cls, "fromAwsManagedComponentAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromAwsManagedComponentName")
    @builtins.classmethod
    def from_aws_managed_component_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        aws_managed_component_name: builtins.str,
    ) -> "IComponent":
        '''(experimental) Imports an AWS-managed component from its name.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param aws_managed_component_name: - The name of the AWS-managed component.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1627b69c7ba0f04ae9ab6f1180bac6dcb468a367c684ce2ad9e056fe1b690dd7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument aws_managed_component_name", value=aws_managed_component_name, expected_type=type_hints["aws_managed_component_name"])
        return typing.cast("IComponent", jsii.sinvoke(cls, "fromAwsManagedComponentName", [scope, id, aws_managed_component_name]))

    @jsii.member(jsii_name="helloWorld")
    @builtins.classmethod
    def hello_world(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        component_name: typing.Optional[builtins.str] = None,
        component_version: typing.Optional[builtins.str] = None,
        platform: typing.Optional["Platform"] = None,
    ) -> "IComponent":
        '''(experimental) Imports the hello world AWS-managed component.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param component_name: (experimental) The name of the AWS-managed component. The name of the AWS-managed component. This is a required attribute when using the ``this.fromAwsManagedComponentAttributes()`` method. This parameter should not be provided when using the pre-defined managed component methods, such as ``AwsManagedComponent.updateOS()`` and ``AwsManagedComponent.reboot()``. Default: - none if using the pre-defined managed component methods, otherwise a platform is required when using ``this.fromAwsManagedComponentAttributes()``
        :param component_version: (experimental) The version of the AWS-managed component. Default: - the latest version of the component, x.x.x
        :param platform: (experimental) The platform of the AWS-managed component. This is a required attribute when using the pre-defined managed component methods, such as ``AwsManagedComponent.updateOS()`` and ``AwsManagedComponent.reboot()``. This parameter should not be provided when using the ``this.fromAwsManagedComponentAttributes()`` method. Default: - none if using ``this.fromAwsManagedComponentAttributes()``, otherwise a platform is required when using the pre-defined managed component methods

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e95cc80beec8557aaefdf226beed47b803646d97e987b28db9a477824f800fe7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = AwsManagedComponentAttributes(
            component_name=component_name,
            component_version=component_version,
            platform=platform,
        )

        return typing.cast("IComponent", jsii.sinvoke(cls, "helloWorld", [scope, id, attrs]))

    @jsii.member(jsii_name="python3")
    @builtins.classmethod
    def python3(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        component_name: typing.Optional[builtins.str] = None,
        component_version: typing.Optional[builtins.str] = None,
        platform: typing.Optional["Platform"] = None,
    ) -> "IComponent":
        '''(experimental) Imports the Python 3 AWS-managed component.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param component_name: (experimental) The name of the AWS-managed component. The name of the AWS-managed component. This is a required attribute when using the ``this.fromAwsManagedComponentAttributes()`` method. This parameter should not be provided when using the pre-defined managed component methods, such as ``AwsManagedComponent.updateOS()`` and ``AwsManagedComponent.reboot()``. Default: - none if using the pre-defined managed component methods, otherwise a platform is required when using ``this.fromAwsManagedComponentAttributes()``
        :param component_version: (experimental) The version of the AWS-managed component. Default: - the latest version of the component, x.x.x
        :param platform: (experimental) The platform of the AWS-managed component. This is a required attribute when using the pre-defined managed component methods, such as ``AwsManagedComponent.updateOS()`` and ``AwsManagedComponent.reboot()``. This parameter should not be provided when using the ``this.fromAwsManagedComponentAttributes()`` method. Default: - none if using ``this.fromAwsManagedComponentAttributes()``, otherwise a platform is required when using the pre-defined managed component methods

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b92acbc29e4089fea8f68555361bc22819eb5f63eadda40faf19d3a828fb29fc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = AwsManagedComponentAttributes(
            component_name=component_name,
            component_version=component_version,
            platform=platform,
        )

        return typing.cast("IComponent", jsii.sinvoke(cls, "python3", [scope, id, attrs]))

    @jsii.member(jsii_name="reboot")
    @builtins.classmethod
    def reboot(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        component_name: typing.Optional[builtins.str] = None,
        component_version: typing.Optional[builtins.str] = None,
        platform: typing.Optional["Platform"] = None,
    ) -> "IComponent":
        '''(experimental) Imports the reboot AWS-managed component.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param component_name: (experimental) The name of the AWS-managed component. The name of the AWS-managed component. This is a required attribute when using the ``this.fromAwsManagedComponentAttributes()`` method. This parameter should not be provided when using the pre-defined managed component methods, such as ``AwsManagedComponent.updateOS()`` and ``AwsManagedComponent.reboot()``. Default: - none if using the pre-defined managed component methods, otherwise a platform is required when using ``this.fromAwsManagedComponentAttributes()``
        :param component_version: (experimental) The version of the AWS-managed component. Default: - the latest version of the component, x.x.x
        :param platform: (experimental) The platform of the AWS-managed component. This is a required attribute when using the pre-defined managed component methods, such as ``AwsManagedComponent.updateOS()`` and ``AwsManagedComponent.reboot()``. This parameter should not be provided when using the ``this.fromAwsManagedComponentAttributes()`` method. Default: - none if using ``this.fromAwsManagedComponentAttributes()``, otherwise a platform is required when using the pre-defined managed component methods

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69ab4d7f7fe572f41496187a8f5fd08b3dfdbbe78d1aa9cf5265d61d84e8ecbe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = AwsManagedComponentAttributes(
            component_name=component_name,
            component_version=component_version,
            platform=platform,
        )

        return typing.cast("IComponent", jsii.sinvoke(cls, "reboot", [scope, id, attrs]))

    @jsii.member(jsii_name="stigBuild")
    @builtins.classmethod
    def stig_build(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        component_name: typing.Optional[builtins.str] = None,
        component_version: typing.Optional[builtins.str] = None,
        platform: typing.Optional["Platform"] = None,
    ) -> "IComponent":
        '''(experimental) Imports the STIG hardening AWS-managed component.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param component_name: (experimental) The name of the AWS-managed component. The name of the AWS-managed component. This is a required attribute when using the ``this.fromAwsManagedComponentAttributes()`` method. This parameter should not be provided when using the pre-defined managed component methods, such as ``AwsManagedComponent.updateOS()`` and ``AwsManagedComponent.reboot()``. Default: - none if using the pre-defined managed component methods, otherwise a platform is required when using ``this.fromAwsManagedComponentAttributes()``
        :param component_version: (experimental) The version of the AWS-managed component. Default: - the latest version of the component, x.x.x
        :param platform: (experimental) The platform of the AWS-managed component. This is a required attribute when using the pre-defined managed component methods, such as ``AwsManagedComponent.updateOS()`` and ``AwsManagedComponent.reboot()``. This parameter should not be provided when using the ``this.fromAwsManagedComponentAttributes()`` method. Default: - none if using ``this.fromAwsManagedComponentAttributes()``, otherwise a platform is required when using the pre-defined managed component methods

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/ib-stig.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee53616f10cfba26195e210fe4dc7bcff71fa4a63c9e6648e4025ee62fafedcc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = AwsManagedComponentAttributes(
            component_name=component_name,
            component_version=component_version,
            platform=platform,
        )

        return typing.cast("IComponent", jsii.sinvoke(cls, "stigBuild", [scope, id, attrs]))

    @jsii.member(jsii_name="updateOS")
    @builtins.classmethod
    def update_os(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        component_name: typing.Optional[builtins.str] = None,
        component_version: typing.Optional[builtins.str] = None,
        platform: typing.Optional["Platform"] = None,
    ) -> "IComponent":
        '''(experimental) Imports the OS update AWS-managed component.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param component_name: (experimental) The name of the AWS-managed component. The name of the AWS-managed component. This is a required attribute when using the ``this.fromAwsManagedComponentAttributes()`` method. This parameter should not be provided when using the pre-defined managed component methods, such as ``AwsManagedComponent.updateOS()`` and ``AwsManagedComponent.reboot()``. Default: - none if using the pre-defined managed component methods, otherwise a platform is required when using ``this.fromAwsManagedComponentAttributes()``
        :param component_version: (experimental) The version of the AWS-managed component. Default: - the latest version of the component, x.x.x
        :param platform: (experimental) The platform of the AWS-managed component. This is a required attribute when using the pre-defined managed component methods, such as ``AwsManagedComponent.updateOS()`` and ``AwsManagedComponent.reboot()``. This parameter should not be provided when using the ``this.fromAwsManagedComponentAttributes()`` method. Default: - none if using ``this.fromAwsManagedComponentAttributes()``, otherwise a platform is required when using the pre-defined managed component methods

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d19311b8326a0517457ce310fe53e0167cc068a7f8d5c49cc1a577e6fa7d0cd2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = AwsManagedComponentAttributes(
            component_name=component_name,
            component_version=component_version,
            platform=platform,
        )

        return typing.cast("IComponent", jsii.sinvoke(cls, "updateOS", [scope, id, attrs]))


class _AwsManagedComponentProxy(AwsManagedComponent):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, AwsManagedComponent).__jsii_proxy_class__ = lambda : _AwsManagedComponentProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.AwsManagedComponentAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "component_name": "componentName",
        "component_version": "componentVersion",
        "platform": "platform",
    },
)
class AwsManagedComponentAttributes:
    def __init__(
        self,
        *,
        component_name: typing.Optional[builtins.str] = None,
        component_version: typing.Optional[builtins.str] = None,
        platform: typing.Optional["Platform"] = None,
    ) -> None:
        '''(experimental) Properties for an EC2 Image Builder AWS-managed component.

        :param component_name: (experimental) The name of the AWS-managed component. The name of the AWS-managed component. This is a required attribute when using the ``this.fromAwsManagedComponentAttributes()`` method. This parameter should not be provided when using the pre-defined managed component methods, such as ``AwsManagedComponent.updateOS()`` and ``AwsManagedComponent.reboot()``. Default: - none if using the pre-defined managed component methods, otherwise a platform is required when using ``this.fromAwsManagedComponentAttributes()``
        :param component_version: (experimental) The version of the AWS-managed component. Default: - the latest version of the component, x.x.x
        :param platform: (experimental) The platform of the AWS-managed component. This is a required attribute when using the pre-defined managed component methods, such as ``AwsManagedComponent.updateOS()`` and ``AwsManagedComponent.reboot()``. This parameter should not be provided when using the ``this.fromAwsManagedComponentAttributes()`` method. Default: - none if using ``this.fromAwsManagedComponentAttributes()``, otherwise a platform is required when using the pre-defined managed component methods

        :stability: experimental
        :exampleMetadata: infused

        Example::

            image_recipe = imagebuilder.ImageRecipe(self, "AmazonManagedImageRecipe",
                base_image=imagebuilder.BaseImage.from_ssm_parameter_name("/aws/service/ami-amazon-linux-latest/al2023-ami-minimal-kernel-default-x86_64"),
                components=[imagebuilder.ComponentConfiguration(
                    component=imagebuilder.AwsManagedComponent.update_oS(self, "UpdateOS",
                        platform=imagebuilder.Platform.LINUX
                    )
                ), imagebuilder.ComponentConfiguration(
                    component=imagebuilder.AwsManagedComponent.aws_cli_v2(self, "AwsCli",
                        platform=imagebuilder.Platform.LINUX
                    )
                )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32e146149e9a0c45e3993363b6a87d969c0d980b08ea6bb731b42f52f28c04dd)
            check_type(argname="argument component_name", value=component_name, expected_type=type_hints["component_name"])
            check_type(argname="argument component_version", value=component_version, expected_type=type_hints["component_version"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if component_name is not None:
            self._values["component_name"] = component_name
        if component_version is not None:
            self._values["component_version"] = component_version
        if platform is not None:
            self._values["platform"] = platform

    @builtins.property
    def component_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the AWS-managed component.

        The name of the AWS-managed component. This is a required attribute when using the
        ``this.fromAwsManagedComponentAttributes()`` method. This parameter should not be provided when
        using the pre-defined managed component methods, such as ``AwsManagedComponent.updateOS()`` and
        ``AwsManagedComponent.reboot()``.

        :default:

        - none if using  the pre-defined managed component methods, otherwise a platform is required when using
        ``this.fromAwsManagedComponentAttributes()``

        :stability: experimental
        '''
        result = self._values.get("component_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def component_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the AWS-managed component.

        :default: - the latest version of the component, x.x.x

        :stability: experimental
        '''
        result = self._values.get("component_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform(self) -> typing.Optional["Platform"]:
        '''(experimental) The platform of the AWS-managed component.

        This is a required attribute when using the pre-defined managed
        component methods, such as ``AwsManagedComponent.updateOS()`` and ``AwsManagedComponent.reboot()``. This parameter
        should not be provided when using the ``this.fromAwsManagedComponentAttributes()`` method.

        :default:

        - none if using ``this.fromAwsManagedComponentAttributes()``, otherwise a platform is
        required when using the pre-defined managed component methods

        :stability: experimental
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional["Platform"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsManagedComponentAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AwsManagedWorkflow(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.AwsManagedWorkflow",
):
    '''(experimental) Helper class for working with AWS-managed workflows.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        container_workflow_pipeline = imagebuilder.ImagePipeline(self, "ContainerWorkflowPipeline",
            recipe=example_container_recipe,
            workflows=[imagebuilder.WorkflowConfiguration(workflow=imagebuilder.AwsManagedWorkflow.build_container(self, "BuildContainer")), imagebuilder.WorkflowConfiguration(workflow=imagebuilder.AwsManagedWorkflow.test_container(self, "TestContainer")), imagebuilder.WorkflowConfiguration(workflow=imagebuilder.AwsManagedWorkflow.distribute_container(self, "DistributeContainer"))
            ]
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="buildContainer")
    @builtins.classmethod
    def build_container(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
    ) -> "IWorkflow":
        '''(experimental) Imports the build-container AWS-managed workflow.

        :param scope: The construct scope.
        :param id: Identifier of the construct.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a155f9cb076a38ddb30dd0e7f35bafb4d217fd6c93b9a6444aefb8e6c1cc987)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("IWorkflow", jsii.sinvoke(cls, "buildContainer", [scope, id]))

    @jsii.member(jsii_name="buildImage")
    @builtins.classmethod
    def build_image(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
    ) -> "IWorkflow":
        '''(experimental) Imports the build-image AWS-managed workflow.

        :param scope: The construct scope.
        :param id: Identifier of the construct.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa82bb2164b9cfa3afb41b7c6b512a4c8280e516924674003c4470e1795b483a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("IWorkflow", jsii.sinvoke(cls, "buildImage", [scope, id]))

    @jsii.member(jsii_name="distributeContainer")
    @builtins.classmethod
    def distribute_container(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
    ) -> "IWorkflow":
        '''(experimental) Imports the distribute-container AWS-managed workflow.

        :param scope: The construct scope.
        :param id: Identifier of the construct.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c7f482a2f0e84d1dca7a602a36a7c76a13441da4fc906eb2f8336be8421fd0f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("IWorkflow", jsii.sinvoke(cls, "distributeContainer", [scope, id]))

    @jsii.member(jsii_name="fromAwsManagedWorkflowAttributes")
    @builtins.classmethod
    def from_aws_managed_workflow_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        workflow_name: builtins.str,
        workflow_type: "WorkflowType",
    ) -> "IWorkflow":
        '''(experimental) Imports an AWS-managed workflow from its attributes.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param workflow_name: (experimental) The name of the AWS-managed workflow.
        :param workflow_type: (experimental) The type of the AWS-managed workflow.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__912196f13b00352d038c885488f6bfd1c05df8ba4a91cdc34fa1d6116baacc91)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = AwsManagedWorkflowAttributes(
            workflow_name=workflow_name, workflow_type=workflow_type
        )

        return typing.cast("IWorkflow", jsii.sinvoke(cls, "fromAwsManagedWorkflowAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="testContainer")
    @builtins.classmethod
    def test_container(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
    ) -> "IWorkflow":
        '''(experimental) Imports the test-container AWS-managed workflow.

        :param scope: The construct scope.
        :param id: Identifier of the construct.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__428931e5241250f9049063f6a8ae1a8929009cefd1a6a9a6c4d357c793a307b4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("IWorkflow", jsii.sinvoke(cls, "testContainer", [scope, id]))

    @jsii.member(jsii_name="testImage")
    @builtins.classmethod
    def test_image(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
    ) -> "IWorkflow":
        '''(experimental) Imports the test-image AWS-managed workflow.

        :param scope: The construct scope.
        :param id: Identifier of the construct.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cfe7323a7ef8ba146a1ddf02e1541eb79936f6f1e05cc1af64ba803c4e98d48)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("IWorkflow", jsii.sinvoke(cls, "testImage", [scope, id]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.AwsManagedWorkflowAttributes",
    jsii_struct_bases=[],
    name_mapping={"workflow_name": "workflowName", "workflow_type": "workflowType"},
)
class AwsManagedWorkflowAttributes:
    def __init__(
        self,
        *,
        workflow_name: builtins.str,
        workflow_type: "WorkflowType",
    ) -> None:
        '''(experimental) Properties for an EC2 Image Builder AWS-managed workflow.

        :param workflow_name: (experimental) The name of the AWS-managed workflow.
        :param workflow_type: (experimental) The type of the AWS-managed workflow.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
            
            aws_managed_workflow_attributes = imagebuilder_alpha.AwsManagedWorkflowAttributes(
                workflow_name="workflowName",
                workflow_type=imagebuilder_alpha.WorkflowType.BUILD
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37b9473566d3a776b877c50ed7ed69f1975be749b5da768cabbfb17555871f24)
            check_type(argname="argument workflow_name", value=workflow_name, expected_type=type_hints["workflow_name"])
            check_type(argname="argument workflow_type", value=workflow_type, expected_type=type_hints["workflow_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "workflow_name": workflow_name,
            "workflow_type": workflow_type,
        }

    @builtins.property
    def workflow_name(self) -> builtins.str:
        '''(experimental) The name of the AWS-managed workflow.

        :stability: experimental
        '''
        result = self._values.get("workflow_name")
        assert result is not None, "Required property 'workflow_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workflow_type(self) -> "WorkflowType":
        '''(experimental) The type of the AWS-managed workflow.

        :stability: experimental
        '''
        result = self._values.get("workflow_type")
        assert result is not None, "Required property 'workflow_type' is missing"
        return typing.cast("WorkflowType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsManagedWorkflowAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AwsMarketplaceComponent(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.AwsMarketplaceComponent",
):
    '''(experimental) Helper class for working with AWS Marketplace components.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        marketplace_component = imagebuilder.AwsMarketplaceComponent.from_aws_marketplace_component_attributes(self, "MarketplaceComponent",
            component_name="my-marketplace-component",
            marketplace_product_id="prod-1234567890abcdef0"
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromAwsMarketplaceComponentAttributes")
    @builtins.classmethod
    def from_aws_marketplace_component_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        component_name: builtins.str,
        marketplace_product_id: builtins.str,
        component_version: typing.Optional[builtins.str] = None,
    ) -> "IComponent":
        '''(experimental) Imports an AWS Marketplace component from its attributes.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param component_name: (experimental) The name of the AWS Marketplace component. This name should exclude the marketplace product ID from it
        :param marketplace_product_id: (experimental) The marketplace product ID associated with the component.
        :param component_version: (experimental) The version of the AWS Marketplace component. Default: - the latest version of the component, x.x.x

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72fea4585ffbd64de79c39d71516ff9636b95dece6fff22dc33683909474b7ea)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = AwsMarketplaceComponentAttributes(
            component_name=component_name,
            marketplace_product_id=marketplace_product_id,
            component_version=component_version,
        )

        return typing.cast("IComponent", jsii.sinvoke(cls, "fromAwsMarketplaceComponentAttributes", [scope, id, attrs]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.AwsMarketplaceComponentAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "component_name": "componentName",
        "marketplace_product_id": "marketplaceProductId",
        "component_version": "componentVersion",
    },
)
class AwsMarketplaceComponentAttributes:
    def __init__(
        self,
        *,
        component_name: builtins.str,
        marketplace_product_id: builtins.str,
        component_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for an EC2 Image Builder AWS Marketplace component.

        :param component_name: (experimental) The name of the AWS Marketplace component. This name should exclude the marketplace product ID from it
        :param marketplace_product_id: (experimental) The marketplace product ID associated with the component.
        :param component_version: (experimental) The version of the AWS Marketplace component. Default: - the latest version of the component, x.x.x

        :stability: experimental
        :exampleMetadata: infused

        Example::

            marketplace_component = imagebuilder.AwsMarketplaceComponent.from_aws_marketplace_component_attributes(self, "MarketplaceComponent",
                component_name="my-marketplace-component",
                marketplace_product_id="prod-1234567890abcdef0"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7239391743877da3432bdb2ba2d1e3c8b1e460c607e06086757dd481b60551dc)
            check_type(argname="argument component_name", value=component_name, expected_type=type_hints["component_name"])
            check_type(argname="argument marketplace_product_id", value=marketplace_product_id, expected_type=type_hints["marketplace_product_id"])
            check_type(argname="argument component_version", value=component_version, expected_type=type_hints["component_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "component_name": component_name,
            "marketplace_product_id": marketplace_product_id,
        }
        if component_version is not None:
            self._values["component_version"] = component_version

    @builtins.property
    def component_name(self) -> builtins.str:
        '''(experimental) The name of the AWS Marketplace component.

        This name should exclude the marketplace product ID from it

        :stability: experimental
        '''
        result = self._values.get("component_name")
        assert result is not None, "Required property 'component_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def marketplace_product_id(self) -> builtins.str:
        '''(experimental) The marketplace product ID associated with the component.

        :stability: experimental
        '''
        result = self._values.get("marketplace_product_id")
        assert result is not None, "Required property 'marketplace_product_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def component_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the AWS Marketplace component.

        :default: - the latest version of the component, x.x.x

        :stability: experimental
        '''
        result = self._values.get("component_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsMarketplaceComponentAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BaseContainerImage(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.BaseContainerImage",
):
    '''(experimental) Represents a base image that is used to start from in EC2 Image Builder image builds.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        parameterized_component = imagebuilder.Component.from_component_name(self, "ParameterizedComponent", "my-parameterized-component")
        
        image_recipe = imagebuilder.ImageRecipe(self, "ParameterizedImageRecipe",
            base_image=imagebuilder.BaseImage.from_ssm_parameter_name("/aws/service/ami-amazon-linux-latest/al2023-ami-minimal-kernel-default-x86_64"),
            components=[imagebuilder.ComponentConfiguration(
                component=parameterized_component,
                parameters={
                    "environment": imagebuilder.ComponentParameterValue.from_string("production"),
                    "version": imagebuilder.ComponentParameterValue.from_string("1.0.0")
                }
            )
            ]
        )
    '''

    def __init__(self, image: builtins.str) -> None:
        '''
        :param image: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f33e6e4838f756e4f6d1484519ed8cda5186a57f5a24b153b4f78b80a4079dd)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
        jsii.create(self.__class__, self, [image])

    @jsii.member(jsii_name="fromDockerHub")
    @builtins.classmethod
    def from_docker_hub(
        cls,
        repository: builtins.str,
        tag: builtins.str,
    ) -> "BaseContainerImage":
        '''(experimental) The DockerHub image to use as the base image in a container recipe.

        :param repository: The DockerHub repository where the base image resides in.
        :param tag: The tag of the base image in the DockerHub repository.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48005f580635b80c73674c7e0c85c6bf5b0a544c29e84be5ee9596eccd9be266)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        return typing.cast("BaseContainerImage", jsii.sinvoke(cls, "fromDockerHub", [repository, tag]))

    @jsii.member(jsii_name="fromEcr")
    @builtins.classmethod
    def from_ecr(
        cls,
        repository: _aws_cdk_aws_ecr_ceddda9d.IRepository,
        tag: builtins.str,
    ) -> "BaseContainerImage":
        '''(experimental) The ECR container image to use as the base image in a container recipe.

        :param repository: The ECR repository where the base image resides in.
        :param tag: The tag of the base image in the ECR repository.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5680334c19570bfa7dbe1efa3db41983dfd9a17d9a5cdbeca4c275bd7f83b20a)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        return typing.cast("BaseContainerImage", jsii.sinvoke(cls, "fromEcr", [repository, tag]))

    @jsii.member(jsii_name="fromEcrPublic")
    @builtins.classmethod
    def from_ecr_public(
        cls,
        registry_alias: builtins.str,
        repository_name: builtins.str,
        tag: builtins.str,
    ) -> "BaseContainerImage":
        '''(experimental) The ECR public container image to use as the base image in a container recipe.

        :param registry_alias: The alias of the ECR public registry where the base image resides in.
        :param repository_name: The name of the ECR public repository, where the base image resides in.
        :param tag: The tag of the base image in the ECR public repository.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b83b8eff102d8e64797bd198891174985269faba6c5197d5b48de485a4c548ed)
            check_type(argname="argument registry_alias", value=registry_alias, expected_type=type_hints["registry_alias"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        return typing.cast("BaseContainerImage", jsii.sinvoke(cls, "fromEcrPublic", [registry_alias, repository_name, tag]))

    @jsii.member(jsii_name="fromImage")
    @builtins.classmethod
    def from_image(cls, image: "IImage") -> "BaseContainerImage":
        '''(experimental) The EC2 Image Builder image to use as a base image in a container recipe.

        :param image: The EC2 Image Builder image to use as a base image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c454c4618efb367d2f7ae32dcb02cd045d92bb792ff0c83ff7fff3e63d4d9fa3)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
        return typing.cast("BaseContainerImage", jsii.sinvoke(cls, "fromImage", [image]))

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(
        cls,
        base_container_image_string: builtins.str,
    ) -> "BaseContainerImage":
        '''(experimental) The string value of the base image to use in a container recipe.

        This can be an EC2 Image Builder image ARN,
        an ECR or ECR public image, or a container URI sourced from a third-party container registry such as DockerHub.

        :param base_container_image_string: The base image as a direct string value.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebf155a76d591443840415d8905e10ede75195d0a4f0adc38e3421e0501ea18d)
            check_type(argname="argument base_container_image_string", value=base_container_image_string, expected_type=type_hints["base_container_image_string"])
        return typing.cast("BaseContainerImage", jsii.sinvoke(cls, "fromString", [base_container_image_string]))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        '''(experimental) The rendered base image to use.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "image"))


class BaseImage(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.BaseImage",
):
    '''(experimental) Represents a base image that is used to start from in EC2 Image Builder image builds.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        parameterized_component = imagebuilder.Component.from_component_name(self, "ParameterizedComponent", "my-parameterized-component")
        
        image_recipe = imagebuilder.ImageRecipe(self, "ParameterizedImageRecipe",
            base_image=imagebuilder.BaseImage.from_ssm_parameter_name("/aws/service/ami-amazon-linux-latest/al2023-ami-minimal-kernel-default-x86_64"),
            components=[imagebuilder.ComponentConfiguration(
                component=parameterized_component,
                parameters={
                    "environment": imagebuilder.ComponentParameterValue.from_string("production"),
                    "version": imagebuilder.ComponentParameterValue.from_string("1.0.0")
                }
            )
            ]
        )
    '''

    def __init__(self, image: builtins.str) -> None:
        '''
        :param image: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36dd4f2e58924418174005f93bb4ca0a48a8a6821e91ebabcd4caece94d57920)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
        jsii.create(self.__class__, self, [image])

    @jsii.member(jsii_name="fromAmiId")
    @builtins.classmethod
    def from_ami_id(cls, ami_id: builtins.str) -> "BaseImage":
        '''(experimental) The AMI ID to use as a base image in an image recipe.

        :param ami_id: The AMI ID to use as the base image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2183ddda9c4be9f7f4d3b9c8284f458011b99a2fd8cdb08d3fca5360979b5526)
            check_type(argname="argument ami_id", value=ami_id, expected_type=type_hints["ami_id"])
        return typing.cast("BaseImage", jsii.sinvoke(cls, "fromAmiId", [ami_id]))

    @jsii.member(jsii_name="fromImage")
    @builtins.classmethod
    def from_image(cls, image: "IImage") -> "BaseImage":
        '''(experimental) The EC2 Image Builder image to use as a base image in an image recipe.

        :param image: The EC2 Image Builder image to use as a base image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19b4bc4ef847aa19f559cc5a935a3e212c4324770f3541b35ece7c02d61706e6)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
        return typing.cast("BaseImage", jsii.sinvoke(cls, "fromImage", [image]))

    @jsii.member(jsii_name="fromMarketplaceProductId")
    @builtins.classmethod
    def from_marketplace_product_id(cls, product_id: builtins.str) -> "BaseImage":
        '''(experimental) The marketplace product ID for an AMI product to use as the base image in an image recipe.

        :param product_id: The Marketplace AMI product ID to use as the base image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c595dcdab9a4c781c9ad18ce78da524b051e4de8d12c26a390bf96b5ae4574c)
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
        return typing.cast("BaseImage", jsii.sinvoke(cls, "fromMarketplaceProductId", [product_id]))

    @jsii.member(jsii_name="fromSsmParameter")
    @builtins.classmethod
    def from_ssm_parameter(
        cls,
        parameter: _aws_cdk_aws_ssm_ceddda9d.IParameter,
    ) -> "BaseImage":
        '''(experimental) The SSM parameter to use as the base image in an image recipe.

        :param parameter: The SSM parameter to use as the base image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc8c265a90648821cebcd7fe9c4979868fd28ab3126cbede2318ae61298c484)
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
        return typing.cast("BaseImage", jsii.sinvoke(cls, "fromSsmParameter", [parameter]))

    @jsii.member(jsii_name="fromSsmParameterName")
    @builtins.classmethod
    def from_ssm_parameter_name(cls, parameter_name: builtins.str) -> "BaseImage":
        '''(experimental) The parameter name for the SSM parameter to use as the base image in an image recipe.

        :param parameter_name: The name of the SSM parameter to use as the base image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__234840a8fb1e1cfb3f78458b770d74f46dd279f3ebef8cf5922473b295655177)
            check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
        return typing.cast("BaseImage", jsii.sinvoke(cls, "fromSsmParameterName", [parameter_name]))

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, base_image_string: builtins.str) -> "BaseImage":
        '''(experimental) The direct string value of the base image to use in an image recipe.

        This can be an EC2 Image Builder image ARN,
        an SSM parameter, an AWS Marketplace product ID, or an AMI ID.

        :param base_image_string: The base image as a direct string value.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c8c49a907e420333bd6f88018ea7e3635e275a97ef17b77b6272f39e04b9ba)
            check_type(argname="argument base_image_string", value=base_image_string, expected_type=type_hints["base_image_string"])
        return typing.cast("BaseImage", jsii.sinvoke(cls, "fromString", [base_image_string]))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        '''(experimental) The rendered base image to use.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "image"))


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.ComponentAction")
class ComponentAction(enum.Enum):
    '''(experimental) The action for a step within the component document.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        component = imagebuilder.Component(self, "JsonComponent",
            platform=imagebuilder.Platform.LINUX,
            data=imagebuilder.ComponentData.from_json_object({
                "schema_version": imagebuilder.ComponentSchemaVersion.V1_0,
                "phases": [{
                    "name": imagebuilder.ComponentPhaseName.BUILD,
                    "steps": [{
                        "name": "configure-app",
                        "action": imagebuilder.ComponentAction.CREATE_FILE,
                        "inputs": {
                            "path": "/etc/myapp/config.json",
                            "content": "{\"env\": \"production\"}"
                        }
                    }
                    ]
                }
                ]
            })
        )
    '''

    APPEND_FILE = "APPEND_FILE"
    '''(experimental) The AppendFile action adds the provided content to the pre-existing content of a file.

    :stability: experimental
    '''
    ASSERT = "ASSERT"
    '''(experimental) The Assert action performs value with comparison/logic operators, and succeeds/fails the step based on the outcome of the assertion.

    :stability: experimental
    '''
    COPY_FILE = "COPY_FILE"
    '''(experimental) The CopyFile action copies files from a source file to a destination.

    :stability: experimental
    '''
    COPY_FOLDER = "COPY_FOLDER"
    '''(experimental) The CopyFolder action copies folders from a source to a destination.

    :stability: experimental
    '''
    CREATE_FILE = "CREATE_FILE"
    '''(experimental) The CreateFile action creates a file in the provided location.

    :stability: experimental
    '''
    CREATE_FOLDER = "CREATE_FOLDER"
    '''(experimental) The CreateFolder action creates a folder in the provided location.

    :stability: experimental
    '''
    CREATE_SYMLINK = "CREATE_SYMLINK"
    '''(experimental) The CreateSymlink action creates symbolic links from a given path to a target.

    :stability: experimental
    '''
    DELETE_FILE = "DELETE_FILE"
    '''(experimental) The DeleteFile action deletes file(s) in the provided location.

    :stability: experimental
    '''
    DELETE_FOLDER = "DELETE_FOLDER"
    '''(experimental) The DeleteFolder action deletes folders in the provided location.

    :stability: experimental
    '''
    EXECUTE_BASH = "EXECUTE_BASH"
    '''(experimental) The ExecuteBash action runs bash scripts with inline bash commands.

    :stability: experimental
    '''
    EXECUTE_BINARY = "EXECUTE_BINARY"
    '''(experimental) The ExecuteBinary action runs a provided binary executable.

    :stability: experimental
    '''
    EXECUTE_DOCUMENT = "EXECUTE_DOCUMENT"
    '''(experimental) The ExecuteDocument action allows running other component documents from within a given component.

    :stability: experimental
    '''
    EXECUTE_POWERSHELL = "EXECUTE_POWERSHELL"
    '''(experimental) The ExecutePowershell action runs PowerShell scripts with inline PowerShell commands.

    :stability: experimental
    '''
    INSTALL_MSI = "INSTALL_MSI"
    '''(experimental) The InstallMSI action runs a Windows application with the provided MSI file.

    :stability: experimental
    '''
    LIST_FILES = "LIST_FILES"
    '''(experimental) The ListFiles action lists files in the provided folder.

    :stability: experimental
    '''
    MOVE_FILE = "MOVE_FILE"
    '''(experimental) The MoveFile action moves files from a source to a destination.

    :stability: experimental
    '''
    MOVE_FOLDER = "MOVE_FOLDER"
    '''(experimental) The MoveFolder action moves folders from a source to a destination.

    :stability: experimental
    '''
    READ_FILE = "READ_FILE"
    '''(experimental) The ReadFile action reads the content of a text file.

    :stability: experimental
    '''
    REBOOT = "REBOOT"
    '''(experimental) The Reboot action reboots the instance.

    :stability: experimental
    '''
    SET_FILE_ENCODING = "SET_FILE_ENCODING"
    '''(experimental) The SetFileEncoding action modifies the encoding property of an existing file.

    :stability: experimental
    '''
    SET_FILE_OWNER = "SET_FILE_OWNER"
    '''(experimental) The SetFileOwner action modifies the owner and group ownership properties of an existing file.

    :stability: experimental
    '''
    SET_FOLDER_OWNER = "SET_FOLDER_OWNER"
    '''(experimental) The SetFolderOwner action recursively modifies the owner and group ownership properties of an existing folder.

    :stability: experimental
    '''
    SET_FILE_PERMISSIONS = "SET_FILE_PERMISSIONS"
    '''(experimental) The SetFilePermissions action modifies the permission of an existing file.

    :stability: experimental
    '''
    SET_FOLDER_PERMISSIONS = "SET_FOLDER_PERMISSIONS"
    '''(experimental) The SetFolderPermissions action recursively modifies the permissions of an existing folder and all of its subfiles and subfolders.

    :stability: experimental
    '''
    SET_REGISTRY = "SET_REGISTRY"
    '''(experimental) The SetRegistry action sets the value for the specified Windows registry key.

    :stability: experimental
    '''
    S3_DOWNLOAD = "S3_DOWNLOAD"
    '''(experimental) The S3Download action downloads an Amazon S3 object/folder to a local destination.

    :stability: experimental
    '''
    S3_UPLOAD = "S3_UPLOAD"
    '''(experimental) The S3Upload action uploads a file or folder to an Amazon S3 location.

    :stability: experimental
    '''
    UNINSTALL_MSI = "UNINSTALL_MSI"
    '''(experimental) The UninstallMSI action removes a Windows application using an MSI file.

    :stability: experimental
    '''
    UPDATE_OS = "UPDATE_OS"
    '''(experimental) The UpdateOS action installs OS updates.

    :stability: experimental
    '''
    WEB_DOWNLOAD = "WEB_DOWNLOAD"
    '''(experimental) The WebDownload action downloads files from a URL to a local destination.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ComponentAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "component_arn": "componentArn",
        "component_name": "componentName",
        "component_version": "componentVersion",
    },
)
class ComponentAttributes:
    def __init__(
        self,
        *,
        component_arn: typing.Optional[builtins.str] = None,
        component_name: typing.Optional[builtins.str] = None,
        component_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for an EC2 Image Builder component.

        :param component_arn: (experimental) The ARN of the component. Default: - the ARN is automatically constructed if a componentName is provided, otherwise a componentArn is required
        :param component_name: (experimental) The name of the component. Default: - the name is automatically constructed if a componentArn is provided, otherwise a componentName is required
        :param component_version: (experimental) The version of the component. Default: - the latest version of the component, x.x.x

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
            
            component_attributes = imagebuilder_alpha.ComponentAttributes(
                component_arn="componentArn",
                component_name="componentName",
                component_version="componentVersion"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a111ce6a3cc980fdfd78a9c04008d2621e0cdb5a73ac895dcac5188565ad834a)
            check_type(argname="argument component_arn", value=component_arn, expected_type=type_hints["component_arn"])
            check_type(argname="argument component_name", value=component_name, expected_type=type_hints["component_name"])
            check_type(argname="argument component_version", value=component_version, expected_type=type_hints["component_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if component_arn is not None:
            self._values["component_arn"] = component_arn
        if component_name is not None:
            self._values["component_name"] = component_name
        if component_version is not None:
            self._values["component_version"] = component_version

    @builtins.property
    def component_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the component.

        :default:

        - the ARN is automatically constructed if a componentName is provided, otherwise a componentArn is
        required

        :stability: experimental
        '''
        result = self._values.get("component_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def component_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the component.

        :default:

        - the name is automatically constructed if a componentArn is provided, otherwise a componentName is
        required

        :stability: experimental
        '''
        result = self._values.get("component_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def component_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the component.

        :default: - the latest version of the component, x.x.x

        :stability: experimental
        '''
        result = self._values.get("component_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComponentAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ComponentConfiguration",
    jsii_struct_bases=[],
    name_mapping={"component": "component", "parameters": "parameters"},
)
class ComponentConfiguration:
    def __init__(
        self,
        *,
        component: "IComponent",
        parameters: typing.Optional[typing.Mapping[builtins.str, "ComponentParameterValue"]] = None,
    ) -> None:
        '''(experimental) Configuration details for a component, to include in a recipe.

        :param component: (experimental) The component to execute as part of the image build.
        :param parameters: (experimental) The parameters to use when executing the component. Default: - no parameters. if the component contains parameters, their default values will be used. otherwise, any required parameters that are not included will result in a build failure

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
            
            # component: imagebuilder_alpha.Component
            # component_parameter_value: imagebuilder_alpha.ComponentParameterValue
            
            component_configuration = imagebuilder_alpha.ComponentConfiguration(
                component=component,
            
                # the properties below are optional
                parameters={
                    "parameters_key": component_parameter_value
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db17d444fe5fcbbca45d94785f2ae1499dd8f616813840a72a68e10c146b1bb8)
            check_type(argname="argument component", value=component, expected_type=type_hints["component"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "component": component,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def component(self) -> "IComponent":
        '''(experimental) The component to execute as part of the image build.

        :stability: experimental
        '''
        result = self._values.get("component")
        assert result is not None, "Required property 'component' is missing"
        return typing.cast("IComponent", result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "ComponentParameterValue"]]:
        '''(experimental) The parameters to use when executing the component.

        :default:

        - no parameters. if the component contains parameters, their default values will be used. otherwise, any
        required parameters that are not included will result in a build failure

        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "ComponentParameterValue"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComponentConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComponentConstantValue(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ComponentConstantValue",
):
    '''(experimental) The value of a constant in a component document.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
        
        component_constant_value = imagebuilder_alpha.ComponentConstantValue.from_string("value")
    '''

    def __init__(self, type: builtins.str, value: typing.Any) -> None:
        '''
        :param type: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7a022302a19d26bbe18edf3fafb69d72fca2ee4e1f292dafa9ce24d08a9455c)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.create(self.__class__, self, [type, value])

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, value: builtins.str) -> "ComponentConstantValue":
        '''(experimental) Creates a string type constant in a component document.

        :param value: The value of the constant.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__963a239c9c403fc6b5a4313e8e62b5aa83e3dfcb87d450ca08bbee183cbac1d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ComponentConstantValue", jsii.sinvoke(cls, "fromString", [value]))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''(experimental) The data type of the constant.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''(experimental) The value of the constant.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "value"))


class ComponentData(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ComponentData",
):
    '''(experimental) Helper class for referencing and uploading component data.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        component = imagebuilder.Component(self, "EncryptedComponent",
            platform=imagebuilder.Platform.LINUX,
            kms_key=kms.Key(self, "ComponentKey"),
            data=imagebuilder.ComponentData.from_json_object({
                "schema_version": imagebuilder.ComponentSchemaVersion.V1_0,
                "phases": [{
                    "name": imagebuilder.ComponentPhaseName.BUILD,
                    "steps": [{
                        "name": "secure-setup",
                        "action": imagebuilder.ComponentAction.EXECUTE_BASH,
                        "inputs": {
                            "commands": ["echo \"This component data is encrypted with KMS\""]
                        }
                    }
                    ]
                }
                ]
            })
        )
    '''

    def __init__(self, value: builtins.str) -> None:
        '''
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edbe027f8c3d7062dfc1c03bb55eb927c328b9cd602143575a35fa311f551f29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.create(self.__class__, self, [value])

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        path: builtins.str,
        *,
        deploy_time: typing.Optional[builtins.bool] = None,
        display_name: typing.Optional[builtins.str] = None,
        readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IGrantable]] = None,
        source_kms_key: typing.Optional[_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef] = None,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[_aws_cdk_ceddda9d.AssetHashType] = None,
        bundling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow_symlinks: typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode] = None,
        ignore_mode: typing.Optional[_aws_cdk_ceddda9d.IgnoreMode] = None,
    ) -> "S3ComponentData":
        '''(experimental) Uploads component data from a local file to S3 to use as the component data.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param path: The local path to the component data file.
        :param deploy_time: Whether or not the asset needs to exist beyond deployment time; i.e. are copied over to a different location and not needed afterwards. Setting this property to true has an impact on the lifecycle of the asset, because we will assume that it is safe to delete after the CloudFormation deployment succeeds. For example, Lambda Function assets are copied over to Lambda during deployment. Therefore, it is not necessary to store the asset in S3, so we consider those deployTime assets. Default: false
        :param display_name: A display name for this asset. If supplied, the display name will be used in locations where the asset identifier is printed, like in the CLI progress information. If the same asset is added multiple times, the display name of the first occurrence is used. The default is the construct path of the Asset construct, with respect to the enclosing stack. If the asset is produced by a construct helper function (such as ``lambda.Code.fromAsset()``), this will look like ``MyFunction/Code``. We use the stack-relative construct path so that in the common case where you have multiple stacks with the same asset, we won't show something like ``/MyBetaStack/MyFunction/Code`` when you are actually deploying to production. Default: - Stack-relative construct path
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_kms_key: The ARN of the KMS key used to encrypt the handler code. Default: - the default server-side encryption with Amazon S3 managed keys(SSE-S3) key will be used.
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container or a custom bundling provider. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise
        :param exclude: File paths matching the patterns will be excluded. See ``ignoreMode`` to set the matching behavior. Has no effect on Assets bundled using the ``bundling`` property. Default: - nothing is excluded
        :param follow_symlinks: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param ignore_mode: The ignore behavior to use for ``exclude`` patterns. Default: IgnoreMode.GLOB

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3dd9994d6bd946b1ceac062da8831ad7f0ab68167221bcb1de2b5bf4f1b9389)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        options = _aws_cdk_aws_s3_assets_ceddda9d.AssetOptions(
            deploy_time=deploy_time,
            display_name=display_name,
            readers=readers,
            source_kms_key=source_kms_key,
            asset_hash=asset_hash,
            asset_hash_type=asset_hash_type,
            bundling=bundling,
            exclude=exclude,
            follow_symlinks=follow_symlinks,
            ignore_mode=ignore_mode,
        )

        return typing.cast("S3ComponentData", jsii.sinvoke(cls, "fromAsset", [scope, id, path, options]))

    @jsii.member(jsii_name="fromComponentDocumentJsonObject")
    @builtins.classmethod
    def from_component_document_json_object(
        cls,
        *,
        phases: typing.Sequence[typing.Union["ComponentDocumentPhase", typing.Dict[builtins.str, typing.Any]]],
        schema_version: "ComponentSchemaVersion",
        constants: typing.Optional[typing.Mapping[builtins.str, ComponentConstantValue]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Union["ComponentDocumentParameterDefinition", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> "ComponentData":
        '''(experimental) Uses an inline JSON object as the component data, using the ComponentDocument interface.

        :param phases: (experimental) The phases which define the grouping of steps to run in the build and test workflows of the image build.
        :param schema_version: (experimental) The schema version of the component.
        :param constants: (experimental) The constants to define in the document. Default: None
        :param description: (experimental) The description of the document. Default: None
        :param name: (experimental) The name of the document. Default: None
        :param parameters: (experimental) The parameters to define in the document. Default: None

        :stability: experimental
        '''
        data = ComponentDocument(
            phases=phases,
            schema_version=schema_version,
            constants=constants,
            description=description,
            name=name,
            parameters=parameters,
        )

        return typing.cast("ComponentData", jsii.sinvoke(cls, "fromComponentDocumentJsonObject", [data]))

    @jsii.member(jsii_name="fromInline")
    @builtins.classmethod
    def from_inline(cls, data: builtins.str) -> "ComponentData":
        '''(experimental) Uses an inline JSON/YAML string as the component data.

        :param data: An inline JSON/YAML string representing the component data.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5c968d474a4be4f05abdfab6bd5b4d52a49ade7db8a0614bd22bc59fe1dbb4)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        return typing.cast("ComponentData", jsii.sinvoke(cls, "fromInline", [data]))

    @jsii.member(jsii_name="fromJsonObject")
    @builtins.classmethod
    def from_json_object(
        cls,
        data: typing.Mapping[builtins.str, typing.Any],
    ) -> "ComponentData":
        '''(experimental) Uses an inline JSON object as the component data.

        :param data: An inline JSON object representing the component data.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e62d9de5f9eddd59dcfb4d4419326a2af5a8035493101b1595b1a55234425ab)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        return typing.cast("ComponentData", jsii.sinvoke(cls, "fromJsonObject", [data]))

    @jsii.member(jsii_name="fromS3")
    @builtins.classmethod
    def from_s3(
        cls,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        key: builtins.str,
    ) -> "S3ComponentData":
        '''(experimental) References component data from a pre-existing S3 object.

        :param bucket: The S3 bucket where the component data is stored.
        :param key: The S3 key of the component data file.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__502ae41b418b170f33bf886f3f817d134270c2d3c6d326d7017b7da013816b35)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast("S3ComponentData", jsii.sinvoke(cls, "fromS3", [bucket, key]))

    @builtins.property
    @jsii.member(jsii_name="isS3Reference")
    @abc.abstractmethod
    def is_s3_reference(self) -> builtins.bool:
        '''(experimental) Indicates that the provided component data is an S3 reference.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        '''(experimental) The resulting inline string or S3 URL which references the component data.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "value"))


class _ComponentDataProxy(ComponentData):
    @builtins.property
    @jsii.member(jsii_name="isS3Reference")
    def is_s3_reference(self) -> builtins.bool:
        '''(experimental) Indicates that the provided component data is an S3 reference.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isS3Reference"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ComponentData).__jsii_proxy_class__ = lambda : _ComponentDataProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ComponentDocument",
    jsii_struct_bases=[],
    name_mapping={
        "phases": "phases",
        "schema_version": "schemaVersion",
        "constants": "constants",
        "description": "description",
        "name": "name",
        "parameters": "parameters",
    },
)
class ComponentDocument:
    def __init__(
        self,
        *,
        phases: typing.Sequence[typing.Union["ComponentDocumentPhase", typing.Dict[builtins.str, typing.Any]]],
        schema_version: "ComponentSchemaVersion",
        constants: typing.Optional[typing.Mapping[builtins.str, ComponentConstantValue]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Union["ComponentDocumentParameterDefinition", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Properties of an EC2 Image Builder Component Document.

        :param phases: (experimental) The phases which define the grouping of steps to run in the build and test workflows of the image build.
        :param schema_version: (experimental) The schema version of the component.
        :param constants: (experimental) The constants to define in the document. Default: None
        :param description: (experimental) The description of the document. Default: None
        :param name: (experimental) The name of the document. Default: None
        :param parameters: (experimental) The parameters to define in the document. Default: None

        :stability: experimental
        :exampleMetadata: infused

        Example::

            component = imagebuilder.Component(self, "StructuredComponent",
                platform=imagebuilder.Platform.LINUX,
                data=imagebuilder.ComponentData.from_component_document_json_object(
                    schema_version=imagebuilder.ComponentSchemaVersion.V1_0,
                    phases=[imagebuilder.ComponentDocumentPhase(
                        name=imagebuilder.ComponentPhaseName.BUILD,
                        steps=[imagebuilder.ComponentDocumentStep(
                            name="install-with-timeout",
                            action=imagebuilder.ComponentAction.EXECUTE_BASH,
                            timeout=Duration.minutes(10),
                            on_failure=imagebuilder.ComponentOnFailure.CONTINUE,
                            inputs=imagebuilder.ComponentStepInputs.from_object({
                                "commands": ["./install-script.sh"]
                            })
                        )
                        ]
                    )
                    ]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4737aa013938586441da1b86dab7eebc204c3816be9ffb4b4666db7f4c154a3c)
            check_type(argname="argument phases", value=phases, expected_type=type_hints["phases"])
            check_type(argname="argument schema_version", value=schema_version, expected_type=type_hints["schema_version"])
            check_type(argname="argument constants", value=constants, expected_type=type_hints["constants"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "phases": phases,
            "schema_version": schema_version,
        }
        if constants is not None:
            self._values["constants"] = constants
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def phases(self) -> typing.List["ComponentDocumentPhase"]:
        '''(experimental) The phases which define the grouping of steps to run in the build and test workflows of the image build.

        :stability: experimental
        '''
        result = self._values.get("phases")
        assert result is not None, "Required property 'phases' is missing"
        return typing.cast(typing.List["ComponentDocumentPhase"], result)

    @builtins.property
    def schema_version(self) -> "ComponentSchemaVersion":
        '''(experimental) The schema version of the component.

        :stability: experimental
        '''
        result = self._values.get("schema_version")
        assert result is not None, "Required property 'schema_version' is missing"
        return typing.cast("ComponentSchemaVersion", result)

    @builtins.property
    def constants(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, ComponentConstantValue]]:
        '''(experimental) The constants to define in the document.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("constants")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, ComponentConstantValue]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the document.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the document.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "ComponentDocumentParameterDefinition"]]:
        '''(experimental) The parameters to define in the document.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "ComponentDocumentParameterDefinition"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComponentDocument(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ComponentDocumentForLoop",
    jsii_struct_bases=[],
    name_mapping={"end": "end", "start": "start", "update_by": "updateBy"},
)
class ComponentDocumentForLoop:
    def __init__(
        self,
        *,
        end: jsii.Number,
        start: jsii.Number,
        update_by: jsii.Number,
    ) -> None:
        '''(experimental) The for loop iterates on a range of integers specified within a boundary outlined by the start and end of the variables.

        The iterating values are in the set [start, end] and includes boundary values.

        :param end: (experimental) Ending value of iteration. Does not accept chaining expressions.
        :param start: (experimental) Starting value of iteration. Does not accept chaining expressions.
        :param update_by: (experimental) Difference by which an iterating value is updated through addition. It must be a negative or positive non-zero value. Does not accept chaining expressions.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
            
            component_document_for_loop = imagebuilder_alpha.ComponentDocumentForLoop(
                end=123,
                start=123,
                update_by=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7545616e7ad4244bf8e5212a06dc04473a71fef0517840bdfaf4168ea419c44)
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            check_type(argname="argument update_by", value=update_by, expected_type=type_hints["update_by"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end": end,
            "start": start,
            "update_by": update_by,
        }

    @builtins.property
    def end(self) -> jsii.Number:
        '''(experimental) Ending value of iteration.

        Does not accept chaining expressions.

        :stability: experimental
        '''
        result = self._values.get("end")
        assert result is not None, "Required property 'end' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start(self) -> jsii.Number:
        '''(experimental) Starting value of iteration.

        Does not accept chaining expressions.

        :stability: experimental
        '''
        result = self._values.get("start")
        assert result is not None, "Required property 'start' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def update_by(self) -> jsii.Number:
        '''(experimental) Difference by which an iterating value is updated through addition.

        It must be a negative or positive non-zero
        value. Does not accept chaining expressions.

        :stability: experimental
        '''
        result = self._values.get("update_by")
        assert result is not None, "Required property 'update_by' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComponentDocumentForLoop(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ComponentDocumentLoop",
    jsii_struct_bases=[],
    name_mapping={"for_": "for", "for_each": "forEach", "name": "name"},
)
class ComponentDocumentLoop:
    def __init__(
        self,
        *,
        for_: typing.Optional[typing.Union[ComponentDocumentForLoop, typing.Dict[builtins.str, typing.Any]]] = None,
        for_each: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The looping construct of a component defines a repeated sequence of instructions.

        :param for_: (experimental) The for loop iterates on a range of integers specified within a boundary outlined by the start and end of the variables. Default: - none if ``forEach`` is provided. otherwise, ``for`` is required.
        :param for_each: (experimental) The forEach loop iterates on an explicit list of values, which can be strings and chained expressions. Default: - none if ``for`` is provided. otherwise, ``forEach`` is required.
        :param name: (experimental) The name of the loop, which can be used to reference. Default: loop

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
            
            component_document_loop = imagebuilder_alpha.ComponentDocumentLoop(
                for=imagebuilder_alpha.ComponentDocumentForLoop(
                    end=123,
                    start=123,
                    update_by=123
                ),
                for_each=["forEach"],
                name="name"
            )
        '''
        if isinstance(for_, dict):
            for_ = ComponentDocumentForLoop(**for_)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__016c7a2af8ebcf03286820555388bbfa1ccb89028f5f37b87fa3f7cb9dceded7)
            check_type(argname="argument for_", value=for_, expected_type=type_hints["for_"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if for_ is not None:
            self._values["for_"] = for_
        if for_each is not None:
            self._values["for_each"] = for_each
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def for_(self) -> typing.Optional[ComponentDocumentForLoop]:
        '''(experimental) The for loop iterates on a range of integers specified within a boundary outlined by the start and end of the variables.

        :default: - none if ``forEach`` is provided. otherwise, ``for`` is required.

        :stability: experimental
        '''
        result = self._values.get("for_")
        return typing.cast(typing.Optional[ComponentDocumentForLoop], result)

    @builtins.property
    def for_each(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The forEach loop iterates on an explicit list of values, which can be strings and chained expressions.

        :default: - none if ``for`` is provided. otherwise, ``forEach`` is required.

        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the loop, which can be used to reference.

        :default: loop

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComponentDocumentLoop(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ComponentDocumentParameterDefinition",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "default": "default", "description": "description"},
)
class ComponentDocumentParameterDefinition:
    def __init__(
        self,
        *,
        type: "ComponentParameterType",
        default: typing.Any = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The definition of the parameter.

        :param type: (experimental) The type of the parameter.
        :param default: (experimental) The default value of the parameter. Default: - none, indicating the parameter is required
        :param description: (experimental) The description of the parameter. Default: None

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
            
            # default_: Any
            
            component_document_parameter_definition = imagebuilder_alpha.ComponentDocumentParameterDefinition(
                type=imagebuilder_alpha.ComponentParameterType.STRING,
            
                # the properties below are optional
                default=default_,
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b765c0d6f7d805699670929833be905f563259a2aec778f1d09ab1ac16f76c5)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if default is not None:
            self._values["default"] = default
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def type(self) -> "ComponentParameterType":
        '''(experimental) The type of the parameter.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("ComponentParameterType", result)

    @builtins.property
    def default(self) -> typing.Any:
        '''(experimental) The default value of the parameter.

        :default: - none, indicating the parameter is required

        :stability: experimental
        '''
        result = self._values.get("default")
        return typing.cast(typing.Any, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the parameter.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComponentDocumentParameterDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ComponentDocumentPhase",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "steps": "steps"},
)
class ComponentDocumentPhase:
    def __init__(
        self,
        *,
        name: "ComponentPhaseName",
        steps: typing.Sequence[typing.Union["ComponentDocumentStep", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''(experimental) The phase to run in a specific workflow in an image build, which define the steps to execute to customize or test the instance.

        :param name: (experimental) The name of the phase.
        :param steps: (experimental) The list of steps to execute to modify or test the build/test instance.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            phase = imagebuilder.ComponentDocumentPhase(
                name=imagebuilder.ComponentPhaseName.BUILD,
                steps=[imagebuilder.ComponentDocumentStep(
                    name="configure-app",
                    action=imagebuilder.ComponentAction.CREATE_FILE,
                    inputs=imagebuilder.ComponentStepInputs.from_object({
                        "path": "/etc/myapp/config.json",
                        "content": "{\"env\": \"production\"}"
                    })
                )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3717a69557789288ecb2866be7254e9e0d4db1c92bd936b8be1466c3858d8a51)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "steps": steps,
        }

    @builtins.property
    def name(self) -> "ComponentPhaseName":
        '''(experimental) The name of the phase.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast("ComponentPhaseName", result)

    @builtins.property
    def steps(self) -> typing.List["ComponentDocumentStep"]:
        '''(experimental) The list of steps to execute to modify or test the build/test instance.

        :stability: experimental
        '''
        result = self._values.get("steps")
        assert result is not None, "Required property 'steps' is missing"
        return typing.cast(typing.List["ComponentDocumentStep"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComponentDocumentPhase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ComponentDocumentStep",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "inputs": "inputs",
        "name": "name",
        "if_": "if",
        "loop": "loop",
        "on_failure": "onFailure",
        "timeout": "timeout",
    },
)
class ComponentDocumentStep:
    def __init__(
        self,
        *,
        action: ComponentAction,
        inputs: "ComponentStepInputs",
        name: builtins.str,
        if_: typing.Optional["ComponentStepIfCondition"] = None,
        loop: typing.Optional[typing.Union[ComponentDocumentLoop, typing.Dict[builtins.str, typing.Any]]] = None,
        on_failure: typing.Optional["ComponentOnFailure"] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''(experimental) The step to run in a specific phase of the image build, which defines the step to execute to customize or test the instance.

        :param action: (experimental) The action to perform in the step.
        :param inputs: (experimental) Contains parameters required by the action to run the step.
        :param name: (experimental) The name of the step.
        :param if_: (experimental) The condition to apply to the step. If the condition is false, then the step is skipped Default: - no condition is applied to the step and it gets executed
        :param loop: (experimental) A looping construct defining a repeated sequence of instructions. Default: None
        :param on_failure: (experimental) Specifies what the step should do in case of failure. Default: ComponentOnFailure.ABORT
        :param timeout: (experimental) The timeout of the step. Default: - 120 minutes

        :stability: experimental
        :exampleMetadata: infused

        Example::

            step = imagebuilder.ComponentDocumentStep(
                name="configure-app",
                action=imagebuilder.ComponentAction.CREATE_FILE,
                inputs=imagebuilder.ComponentStepInputs.from_object({
                    "path": "/etc/myapp/config.json",
                    "content": "{\"env\": \"production\"}"
                })
            )
        '''
        if isinstance(loop, dict):
            loop = ComponentDocumentLoop(**loop)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da991558ffc8ca306ecc6999d0b287568416629c1073bde551fb7c089193ce5c)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument inputs", value=inputs, expected_type=type_hints["inputs"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument if_", value=if_, expected_type=type_hints["if_"])
            check_type(argname="argument loop", value=loop, expected_type=type_hints["loop"])
            check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "inputs": inputs,
            "name": name,
        }
        if if_ is not None:
            self._values["if_"] = if_
        if loop is not None:
            self._values["loop"] = loop
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def action(self) -> ComponentAction:
        '''(experimental) The action to perform in the step.

        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(ComponentAction, result)

    @builtins.property
    def inputs(self) -> "ComponentStepInputs":
        '''(experimental) Contains parameters required by the action to run the step.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/toe-action-modules.html
        :stability: experimental
        '''
        result = self._values.get("inputs")
        assert result is not None, "Required property 'inputs' is missing"
        return typing.cast("ComponentStepInputs", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the step.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def if_(self) -> typing.Optional["ComponentStepIfCondition"]:
        '''(experimental) The condition to apply to the step.

        If the condition is false, then the step is skipped

        :default: - no condition is applied to the step and it gets executed

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/toe-comparison-operators.html
        :stability: experimental
        '''
        result = self._values.get("if_")
        return typing.cast(typing.Optional["ComponentStepIfCondition"], result)

    @builtins.property
    def loop(self) -> typing.Optional[ComponentDocumentLoop]:
        '''(experimental) A looping construct defining a repeated sequence of instructions.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("loop")
        return typing.cast(typing.Optional[ComponentDocumentLoop], result)

    @builtins.property
    def on_failure(self) -> typing.Optional["ComponentOnFailure"]:
        '''(experimental) Specifies what the step should do in case of failure.

        :default: ComponentOnFailure.ABORT

        :stability: experimental
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional["ComponentOnFailure"], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The timeout of the step.

        :default: - 120 minutes

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComponentDocumentStep(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.ComponentOnFailure")
class ComponentOnFailure(enum.Enum):
    '''(experimental) Specifies what the step should do in case of failure.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        component = imagebuilder.Component(self, "StructuredComponent",
            platform=imagebuilder.Platform.LINUX,
            data=imagebuilder.ComponentData.from_component_document_json_object(
                schema_version=imagebuilder.ComponentSchemaVersion.V1_0,
                phases=[imagebuilder.ComponentDocumentPhase(
                    name=imagebuilder.ComponentPhaseName.BUILD,
                    steps=[imagebuilder.ComponentDocumentStep(
                        name="install-with-timeout",
                        action=imagebuilder.ComponentAction.EXECUTE_BASH,
                        timeout=Duration.minutes(10),
                        on_failure=imagebuilder.ComponentOnFailure.CONTINUE,
                        inputs=imagebuilder.ComponentStepInputs.from_object({
                            "commands": ["./install-script.sh"]
                        })
                    )
                    ]
                )
                ]
            )
        )
    '''

    ABORT = "ABORT"
    '''(experimental) Fails the step and document execution.

    :stability: experimental
    '''
    CONTINUE = "CONTINUE"
    '''(experimental) Fails the step and proceeds to execute the next step in the document.

    :stability: experimental
    '''
    IGNORE = "IGNORE"
    '''(experimental) Ignores the step and proceeds to execute the next step in the document.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.ComponentParameterType")
class ComponentParameterType(enum.Enum):
    '''(experimental) The parameter type in a component document.

    :stability: experimental
    '''

    STRING = "STRING"
    '''(experimental) Indicates the parameter value is a string.

    :stability: experimental
    '''


class ComponentParameterValue(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ComponentParameterValue",
):
    '''(experimental) The parameter value for a component parameter.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        parameterized_component = imagebuilder.Component.from_component_name(self, "ParameterizedComponent", "my-parameterized-component")
        
        image_recipe = imagebuilder.ImageRecipe(self, "ParameterizedImageRecipe",
            base_image=imagebuilder.BaseImage.from_ssm_parameter_name("/aws/service/ami-amazon-linux-latest/al2023-ami-minimal-kernel-default-x86_64"),
            components=[imagebuilder.ComponentConfiguration(
                component=parameterized_component,
                parameters={
                    "environment": imagebuilder.ComponentParameterValue.from_string("production"),
                    "version": imagebuilder.ComponentParameterValue.from_string("1.0.0")
                }
            )
            ]
        )
    '''

    def __init__(self, value: typing.Sequence[builtins.str]) -> None:
        '''
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e92686cd7276bf6fbf1757d82345ea962a18e656b80715db13df6e5965fd52d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.create(self.__class__, self, [value])

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, value: builtins.str) -> "ComponentParameterValue":
        '''(experimental) The value of the parameter as a string.

        :param value: The string value of the parameter.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc9ffc8841ac8c6b276316e4a6162663a25683c16942020ec08483a48230b50f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ComponentParameterValue", jsii.sinvoke(cls, "fromString", [value]))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.List[builtins.str]:
        '''(experimental) The rendered parameter value.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "value"))


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.ComponentPhaseName")
class ComponentPhaseName(enum.Enum):
    '''(experimental) The phases of a component document.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        component = imagebuilder.Component(self, "EncryptedComponent",
            platform=imagebuilder.Platform.LINUX,
            kms_key=kms.Key(self, "ComponentKey"),
            data=imagebuilder.ComponentData.from_json_object({
                "schema_version": imagebuilder.ComponentSchemaVersion.V1_0,
                "phases": [{
                    "name": imagebuilder.ComponentPhaseName.BUILD,
                    "steps": [{
                        "name": "secure-setup",
                        "action": imagebuilder.ComponentAction.EXECUTE_BASH,
                        "inputs": {
                            "commands": ["echo \"This component data is encrypted with KMS\""]
                        }
                    }
                    ]
                }
                ]
            })
        )
    '''

    BUILD = "BUILD"
    '''(experimental) Build phase of the component.

    This phase is run during the BUILDING phase of the image build.

    :stability: experimental
    '''
    CONTAINER_HOST_TEST = "CONTAINER_HOST_TEST"
    '''(experimental) Test phase of the component, executed directly on the instance which is used to build the container image.

    This
    phase is run during the TESTING phase of the image build.

    :stability: experimental
    '''
    TEST = "TEST"
    '''(experimental) Test phase of the component.

    This phase is run during the TESTING phase of the image build.

    :stability: experimental
    '''
    VALIDATE = "VALIDATE"
    '''(experimental) Validate phase of the component.

    This phase is run during the BUILDING phase of the image build, after the build
    step of the component is executed.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ComponentProps",
    jsii_struct_bases=[],
    name_mapping={
        "data": "data",
        "platform": "platform",
        "change_description": "changeDescription",
        "component_name": "componentName",
        "component_version": "componentVersion",
        "description": "description",
        "kms_key": "kmsKey",
        "supported_os_versions": "supportedOsVersions",
        "tags": "tags",
    },
)
class ComponentProps:
    def __init__(
        self,
        *,
        data: ComponentData,
        platform: "Platform",
        change_description: typing.Optional[builtins.str] = None,
        component_name: typing.Optional[builtins.str] = None,
        component_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        supported_os_versions: typing.Optional[typing.Sequence["OSVersion"]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Properties for creating a Component resource.

        :param data: (experimental) The component document content that defines the build, validation, or test steps to be executed during the image building process.
        :param platform: (experimental) The operating system platform of the component.
        :param change_description: (experimental) The change description of the component. Describes what change has been made in this version of the component, or what makes this version different from other versions. Default: None
        :param component_name: (experimental) The name of the component. Default: - a name is generated
        :param component_version: (experimental) The version of the component. Default: 1.0.0
        :param description: (experimental) The description of the component. Default: None
        :param kms_key: (experimental) The KMS key used to encrypt this component. Default: - an Image Builder owned key will be used to encrypt the component.
        :param supported_os_versions: (experimental) The operating system versions supported by the component. Default: None
        :param tags: (experimental) The tags to apply to the component. Default: None

        :stability: experimental
        :exampleMetadata: infused

        Example::

            component = imagebuilder.Component(self, "EncryptedComponent",
                platform=imagebuilder.Platform.LINUX,
                kms_key=kms.Key(self, "ComponentKey"),
                data=imagebuilder.ComponentData.from_json_object({
                    "schema_version": imagebuilder.ComponentSchemaVersion.V1_0,
                    "phases": [{
                        "name": imagebuilder.ComponentPhaseName.BUILD,
                        "steps": [{
                            "name": "secure-setup",
                            "action": imagebuilder.ComponentAction.EXECUTE_BASH,
                            "inputs": {
                                "commands": ["echo \"This component data is encrypted with KMS\""]
                            }
                        }
                        ]
                    }
                    ]
                })
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dafb5f8cd0f4ef40e1c882755f37fc5dc1a69e4a81d5826049e0c91bf971be3a)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument change_description", value=change_description, expected_type=type_hints["change_description"])
            check_type(argname="argument component_name", value=component_name, expected_type=type_hints["component_name"])
            check_type(argname="argument component_version", value=component_version, expected_type=type_hints["component_version"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument supported_os_versions", value=supported_os_versions, expected_type=type_hints["supported_os_versions"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data": data,
            "platform": platform,
        }
        if change_description is not None:
            self._values["change_description"] = change_description
        if component_name is not None:
            self._values["component_name"] = component_name
        if component_version is not None:
            self._values["component_version"] = component_version
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if supported_os_versions is not None:
            self._values["supported_os_versions"] = supported_os_versions
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data(self) -> ComponentData:
        '''(experimental) The component document content that defines the build, validation, or test steps to be executed during the image building process.

        :stability: experimental
        '''
        result = self._values.get("data")
        assert result is not None, "Required property 'data' is missing"
        return typing.cast(ComponentData, result)

    @builtins.property
    def platform(self) -> "Platform":
        '''(experimental) The operating system platform of the component.

        :stability: experimental
        '''
        result = self._values.get("platform")
        assert result is not None, "Required property 'platform' is missing"
        return typing.cast("Platform", result)

    @builtins.property
    def change_description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The change description of the component.

        Describes what change has been made in this version of the component, or
        what makes this version different from other versions.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("change_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def component_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the component.

        :default: - a name is generated

        :stability: experimental
        '''
        result = self._values.get("component_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def component_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the component.

        :default: 1.0.0

        :stability: experimental
        '''
        result = self._values.get("component_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the component.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key used to encrypt this component.

        :default: - an Image Builder owned key will be used to encrypt the component.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def supported_os_versions(self) -> typing.Optional[typing.List["OSVersion"]]:
        '''(experimental) The operating system versions supported by the component.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("supported_os_versions")
        return typing.cast(typing.Optional[typing.List["OSVersion"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The tags to apply to the component.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComponentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.ComponentSchemaVersion")
class ComponentSchemaVersion(enum.Enum):
    '''(experimental) The schema version of the component.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        custom_component = imagebuilder.Component(self, "MyComponent",
            platform=imagebuilder.Platform.LINUX,
            data=imagebuilder.ComponentData.from_json_object({
                "schema_version": imagebuilder.ComponentSchemaVersion.V1_0,
                "phases": [{
                    "name": imagebuilder.ComponentPhaseName.BUILD,
                    "steps": [{
                        "name": "install-app",
                        "action": imagebuilder.ComponentAction.EXECUTE_BASH,
                        "inputs": {
                            "commands": ["yum install -y my-application"]
                        }
                    }
                    ]
                }
                ]
            })
        )
        
        image_recipe = imagebuilder.ImageRecipe(self, "ComponentImageRecipe",
            base_image=imagebuilder.BaseImage.from_ssm_parameter_name("/aws/service/ami-amazon-linux-latest/al2023-ami-minimal-kernel-default-x86_64"),
            components=[imagebuilder.ComponentConfiguration(
                component=custom_component
            )
            ]
        )
    '''

    V1_0 = "V1_0"
    '''(experimental) Schema version 1.0 for the component document.

    :stability: experimental
    '''


class ComponentStepIfCondition(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ComponentStepIfCondition",
):
    '''(experimental) Represents an ``if`` condition in the component document.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
        
        # if_object: Any
        
        component_step_if_condition = imagebuilder_alpha.ComponentStepIfCondition.from_object({
            "if_object_key": if_object
        })
    '''

    def __init__(self, if_condition: typing.Any) -> None:
        '''
        :param if_condition: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28e9b0814cd916ca01f8a7cf48021bfcd01d4c17be3ae2253fe86dd86f93d671)
            check_type(argname="argument if_condition", value=if_condition, expected_type=type_hints["if_condition"])
        jsii.create(self.__class__, self, [if_condition])

    @jsii.member(jsii_name="fromObject")
    @builtins.classmethod
    def from_object(
        cls,
        if_object: typing.Mapping[builtins.str, typing.Any],
    ) -> "ComponentStepIfCondition":
        '''(experimental) Creates the ``if`` value from an object, for the component step.

        :param if_object: The object containing the ``if`` condition.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7bb86c499fa1670bd8e78f1bd8542abc56e983e69f40e47d32019e6656ffcc)
            check_type(argname="argument if_object", value=if_object, expected_type=type_hints["if_object"])
        return typing.cast("ComponentStepIfCondition", jsii.sinvoke(cls, "fromObject", [if_object]))

    @builtins.property
    @jsii.member(jsii_name="ifCondition")
    def if_condition(self) -> typing.Any:
        '''(experimental) The rendered input value.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "ifCondition"))


class ComponentStepInputs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ComponentStepInputs",
):
    '''(experimental) Represents the inputs for a step in the component document.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        phase = imagebuilder.ComponentDocumentPhase(
            name=imagebuilder.ComponentPhaseName.BUILD,
            steps=[imagebuilder.ComponentDocumentStep(
                name="configure-app",
                action=imagebuilder.ComponentAction.CREATE_FILE,
                inputs=imagebuilder.ComponentStepInputs.from_object({
                    "path": "/etc/myapp/config.json",
                    "content": "{\"env\": \"production\"}"
                })
            )
            ]
        )
    '''

    def __init__(self, input: typing.Any) -> None:
        '''
        :param input: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e53ae7d6d8c31ee6012880e97dd97ea37ce68d0a35e0216830ea8ab676a9ec3)
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
        jsii.create(self.__class__, self, [input])

    @jsii.member(jsii_name="fromList")
    @builtins.classmethod
    def from_list(
        cls,
        inputs_object_list: typing.Sequence[typing.Mapping[builtins.str, typing.Any]],
    ) -> "ComponentStepInputs":
        '''(experimental) Creates the input value from a list of input objects, for the component step.

        :param inputs_object_list: The list of objects containing the input values.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e97a2950e23ff264bda320a66d7ece7c77f491b953c2d2b71cb4ece4c553e4)
            check_type(argname="argument inputs_object_list", value=inputs_object_list, expected_type=type_hints["inputs_object_list"])
        return typing.cast("ComponentStepInputs", jsii.sinvoke(cls, "fromList", [inputs_object_list]))

    @jsii.member(jsii_name="fromObject")
    @builtins.classmethod
    def from_object(
        cls,
        inputs_object: typing.Mapping[builtins.str, typing.Any],
    ) -> "ComponentStepInputs":
        '''(experimental) Creates the input value from an object, for the component step.

        :param inputs_object: The object containing the input values.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61535270ffc68df1496f99af681d722e10151c09b0576885b939d7919cfb56b2)
            check_type(argname="argument inputs_object", value=inputs_object, expected_type=type_hints["inputs_object"])
        return typing.cast("ComponentStepInputs", jsii.sinvoke(cls, "fromObject", [inputs_object]))

    @builtins.property
    @jsii.member(jsii_name="inputs")
    def inputs(self) -> typing.Any:
        '''(experimental) The rendered input value.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "inputs"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ContainerDistribution",
    jsii_struct_bases=[],
    name_mapping={
        "container_repository": "containerRepository",
        "container_description": "containerDescription",
        "container_tags": "containerTags",
        "region": "region",
    },
)
class ContainerDistribution:
    def __init__(
        self,
        *,
        container_repository: "Repository",
        container_description: typing.Optional[builtins.str] = None,
        container_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The regional distribution settings to use for a container build.

        :param container_repository: (experimental) The destination repository to distribute the output container to. Default: The target repository in the container recipe is used
        :param container_description: (experimental) The description of the container image. Default: None
        :param container_tags: (experimental) The additional tags to apply to the distributed container images. Default: None
        :param region: (experimental) The target region to distribute containers to. Default: The current region is used

        :stability: experimental
        :exampleMetadata: infused

        Example::

            ecr_repository = ecr.Repository.from_repository_name(self, "ECRRepository", "my-repo")
            container_repository = imagebuilder.Repository.from_ecr(ecr_repository)
            container_distribution_configuration = imagebuilder.DistributionConfiguration(self, "ContainerDistributionConfiguration")
            
            container_distribution_configuration.add_container_distributions(
                container_repository=container_repository,
                container_description="Test container image",
                container_tags=["latest", "latest-1.0"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e915667467bed957a52d2238405ebf79ca421c029bc891bb818483871e32a658)
            check_type(argname="argument container_repository", value=container_repository, expected_type=type_hints["container_repository"])
            check_type(argname="argument container_description", value=container_description, expected_type=type_hints["container_description"])
            check_type(argname="argument container_tags", value=container_tags, expected_type=type_hints["container_tags"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_repository": container_repository,
        }
        if container_description is not None:
            self._values["container_description"] = container_description
        if container_tags is not None:
            self._values["container_tags"] = container_tags
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def container_repository(self) -> "Repository":
        '''(experimental) The destination repository to distribute the output container to.

        :default: The target repository in the container recipe is used

        :stability: experimental
        '''
        result = self._values.get("container_repository")
        assert result is not None, "Required property 'container_repository' is missing"
        return typing.cast("Repository", result)

    @builtins.property
    def container_description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the container image.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("container_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The additional tags to apply to the distributed container images.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("container_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The target region to distribute containers to.

        :default: The current region is used

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerDistribution(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerInstanceImage(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ContainerInstanceImage",
):
    '''(experimental) Represents a container instance image that is used to launch the instance used for building the container for an EC2 Image Builder container build.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        container_recipe = imagebuilder.ContainerRecipe(self, "InstanceConfigContainerRecipe",
            base_image=imagebuilder.BaseContainerImage.from_docker_hub("amazonlinux", "latest"),
            target_repository=imagebuilder.Repository.from_ecr(
                ecr.Repository.from_repository_name(self, "Repository", "my-container-repo")),
            # Custom ECS-optimized AMI for building
            instance_image=imagebuilder.ContainerInstanceImage.from_ssm_parameter_name("/aws/service/ecs/optimized-ami/amazon-linux-2023/recommended/image_id"),
            # Additional storage for build process
            instance_block_devices=[ec2.BlockDevice(
                device_name="/dev/xvda",
                volume=ec2.BlockDeviceVolume.ebs(50,
                    encrypted=True,
                    volume_type=ec2.EbsDeviceVolumeType.GENERAL_PURPOSE_SSD_GP3
                )
            )
            ]
        )
    '''

    def __init__(self, image: builtins.str) -> None:
        '''
        :param image: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8065edc35db44571f3272fa2f5d9aae7fbbfb5d16c9357f32e5a658c405c1a0f)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
        jsii.create(self.__class__, self, [image])

    @jsii.member(jsii_name="fromAmiId")
    @builtins.classmethod
    def from_ami_id(cls, ami_id: builtins.str) -> "ContainerInstanceImage":
        '''(experimental) The AMI ID to use to launch the instance for building the container image.

        :param ami_id: The AMI ID to use as the container instance image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d93b2dfc09202ba4ae97724b390f56f404845aea745c90fe04cb4d3e5fc0ebc)
            check_type(argname="argument ami_id", value=ami_id, expected_type=type_hints["ami_id"])
        return typing.cast("ContainerInstanceImage", jsii.sinvoke(cls, "fromAmiId", [ami_id]))

    @jsii.member(jsii_name="fromSsmParameter")
    @builtins.classmethod
    def from_ssm_parameter(
        cls,
        parameter: _aws_cdk_aws_ssm_ceddda9d.IStringParameter,
    ) -> "ContainerInstanceImage":
        '''(experimental) The SSM parameter to use to launch the instance for building the container image.

        :param parameter: The SSM parameter to use as the container instance image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6cd09b34db089ebfb47e92fc0fd184732208254e705dfd87bcd078e1c2e3bed)
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
        return typing.cast("ContainerInstanceImage", jsii.sinvoke(cls, "fromSsmParameter", [parameter]))

    @jsii.member(jsii_name="fromSsmParameterName")
    @builtins.classmethod
    def from_ssm_parameter_name(
        cls,
        parameter_name: builtins.str,
    ) -> "ContainerInstanceImage":
        '''(experimental) The ARN of the SSM parameter used to launch the instance for building the container image.

        :param parameter_name: The name of the SSM parameter used as the container instance image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56573a7aa687996e1d992967b202a4504f01f439a99a85965911ec50d4e46818)
            check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
        return typing.cast("ContainerInstanceImage", jsii.sinvoke(cls, "fromSsmParameterName", [parameter_name]))

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(
        cls,
        container_instance_image_string: builtins.str,
    ) -> "ContainerInstanceImage":
        '''(experimental) The string value of the container instance image to use in a container recipe.

        This can either be:

        - an SSM parameter reference, prefixed with ``ssm:`` and followed by the parameter name or ARN
        - an AMI ID

        :param container_instance_image_string: The container instance image as a direct string value.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31b8ad82c04f1a1c3051ab529af538511f6d05832ca4e51853d741ab13cff44f)
            check_type(argname="argument container_instance_image_string", value=container_instance_image_string, expected_type=type_hints["container_instance_image_string"])
        return typing.cast("ContainerInstanceImage", jsii.sinvoke(cls, "fromString", [container_instance_image_string]))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        '''(experimental) The rendered container instance image to use.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "image"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ContainerRecipeAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "container_recipe_arn": "containerRecipeArn",
        "container_recipe_name": "containerRecipeName",
        "container_recipe_version": "containerRecipeVersion",
    },
)
class ContainerRecipeAttributes:
    def __init__(
        self,
        *,
        container_recipe_arn: typing.Optional[builtins.str] = None,
        container_recipe_name: typing.Optional[builtins.str] = None,
        container_recipe_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for an EC2 Image Builder container recipe.

        :param container_recipe_arn: (experimental) The ARN of the container recipe. Default: - derived from containerRecipeName
        :param container_recipe_name: (experimental) The name of the container recipe. Default: - derived from containerRecipeArn
        :param container_recipe_version: (experimental) The version of the container recipe. Default: - derived from containerRecipeArn. if a containerRecipeName is provided, the latest version, x.x.x, will be used.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
            
            container_recipe_attributes = imagebuilder_alpha.ContainerRecipeAttributes(
                container_recipe_arn="containerRecipeArn",
                container_recipe_name="containerRecipeName",
                container_recipe_version="containerRecipeVersion"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__587fb8aeeb95698cf041c0d967899d6df448fbd1674d9c8a635b4ec267fba6d1)
            check_type(argname="argument container_recipe_arn", value=container_recipe_arn, expected_type=type_hints["container_recipe_arn"])
            check_type(argname="argument container_recipe_name", value=container_recipe_name, expected_type=type_hints["container_recipe_name"])
            check_type(argname="argument container_recipe_version", value=container_recipe_version, expected_type=type_hints["container_recipe_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_recipe_arn is not None:
            self._values["container_recipe_arn"] = container_recipe_arn
        if container_recipe_name is not None:
            self._values["container_recipe_name"] = container_recipe_name
        if container_recipe_version is not None:
            self._values["container_recipe_version"] = container_recipe_version

    @builtins.property
    def container_recipe_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the container recipe.

        :default: - derived from containerRecipeName

        :stability: experimental
        '''
        result = self._values.get("container_recipe_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_recipe_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the container recipe.

        :default: - derived from containerRecipeArn

        :stability: experimental
        '''
        result = self._values.get("container_recipe_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_recipe_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the container recipe.

        :default:

        - derived from containerRecipeArn. if a containerRecipeName is provided, the latest version, x.x.x, will
        be used.

        :stability: experimental
        '''
        result = self._values.get("container_recipe_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerRecipeAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ContainerRecipeProps",
    jsii_struct_bases=[],
    name_mapping={
        "base_image": "baseImage",
        "target_repository": "targetRepository",
        "components": "components",
        "container_recipe_name": "containerRecipeName",
        "container_recipe_version": "containerRecipeVersion",
        "description": "description",
        "dockerfile": "dockerfile",
        "instance_block_devices": "instanceBlockDevices",
        "instance_image": "instanceImage",
        "kms_key": "kmsKey",
        "os_version": "osVersion",
        "tags": "tags",
        "working_directory": "workingDirectory",
    },
)
class ContainerRecipeProps:
    def __init__(
        self,
        *,
        base_image: BaseContainerImage,
        target_repository: "Repository",
        components: typing.Optional[typing.Sequence[typing.Union[ComponentConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
        container_recipe_name: typing.Optional[builtins.str] = None,
        container_recipe_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        dockerfile: typing.Optional["DockerfileData"] = None,
        instance_block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_image: typing.Optional[ContainerInstanceImage] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        os_version: typing.Optional["OSVersion"] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for creating a Container Recipe resource.

        :param base_image: (experimental) The base image for customizations specified in the container recipe.
        :param target_repository: (experimental) The container repository where the output container image is stored.
        :param components: (experimental) The list of component configurations to apply in the image build. Default: None
        :param container_recipe_name: (experimental) The name of the container recipe. Default: a name is generated
        :param container_recipe_version: (experimental) The version of the container recipe. Default: 1.0.x
        :param description: (experimental) The description of the container recipe. Default: None
        :param dockerfile: (experimental) The dockerfile template used to build the container image. Default: - a standard dockerfile template will be generated to pull the base image, perform environment setup, and run all components in the recipe
        :param instance_block_devices: (experimental) The block devices to attach to the instance used for building, testing, and distributing the container image. Default: the block devices of the instance image will be used
        :param instance_image: (experimental) The image to use to launch the instance used for building, testing, and distributing the container image. Default: Image Builder will use the appropriate ECS-optimized AMI
        :param kms_key: (experimental) The KMS key used to encrypt the dockerfile template. Default: None
        :param os_version: (experimental) The operating system (OS) version of the base image. Default: - Image Builder will determine the OS version of the base image, if sourced from a third-party container registry. Otherwise, the OS version of the base image is required.
        :param tags: (experimental) The tags to apply to the container recipe. Default: None
        :param working_directory: (experimental) The working directory for use during build and test workflows. Default: - the Image Builder default working directory is used. For Linux and macOS builds, this would be /tmp. For Windows builds, this would be C:/

        :stability: experimental
        :exampleMetadata: infused

        Example::

            container_recipe = imagebuilder.ContainerRecipe(self, "MyContainerRecipe",
                base_image=imagebuilder.BaseContainerImage.from_docker_hub("amazonlinux", "latest"),
                target_repository=imagebuilder.Repository.from_ecr(
                    ecr.Repository.from_repository_name(self, "Repository", "my-container-repo"))
            )
            
            container_pipeline = imagebuilder.ImagePipeline(self, "MyContainerPipeline",
                recipe=example_container_recipe
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a96339edaee9e503b1e793c320e5750414456d8a53a1c668b01572bf0b445d29)
            check_type(argname="argument base_image", value=base_image, expected_type=type_hints["base_image"])
            check_type(argname="argument target_repository", value=target_repository, expected_type=type_hints["target_repository"])
            check_type(argname="argument components", value=components, expected_type=type_hints["components"])
            check_type(argname="argument container_recipe_name", value=container_recipe_name, expected_type=type_hints["container_recipe_name"])
            check_type(argname="argument container_recipe_version", value=container_recipe_version, expected_type=type_hints["container_recipe_version"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dockerfile", value=dockerfile, expected_type=type_hints["dockerfile"])
            check_type(argname="argument instance_block_devices", value=instance_block_devices, expected_type=type_hints["instance_block_devices"])
            check_type(argname="argument instance_image", value=instance_image, expected_type=type_hints["instance_image"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument os_version", value=os_version, expected_type=type_hints["os_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "base_image": base_image,
            "target_repository": target_repository,
        }
        if components is not None:
            self._values["components"] = components
        if container_recipe_name is not None:
            self._values["container_recipe_name"] = container_recipe_name
        if container_recipe_version is not None:
            self._values["container_recipe_version"] = container_recipe_version
        if description is not None:
            self._values["description"] = description
        if dockerfile is not None:
            self._values["dockerfile"] = dockerfile
        if instance_block_devices is not None:
            self._values["instance_block_devices"] = instance_block_devices
        if instance_image is not None:
            self._values["instance_image"] = instance_image
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if os_version is not None:
            self._values["os_version"] = os_version
        if tags is not None:
            self._values["tags"] = tags
        if working_directory is not None:
            self._values["working_directory"] = working_directory

    @builtins.property
    def base_image(self) -> BaseContainerImage:
        '''(experimental) The base image for customizations specified in the container recipe.

        :stability: experimental
        '''
        result = self._values.get("base_image")
        assert result is not None, "Required property 'base_image' is missing"
        return typing.cast(BaseContainerImage, result)

    @builtins.property
    def target_repository(self) -> "Repository":
        '''(experimental) The container repository where the output container image is stored.

        :stability: experimental
        '''
        result = self._values.get("target_repository")
        assert result is not None, "Required property 'target_repository' is missing"
        return typing.cast("Repository", result)

    @builtins.property
    def components(self) -> typing.Optional[typing.List[ComponentConfiguration]]:
        '''(experimental) The list of component configurations to apply in the image build.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("components")
        return typing.cast(typing.Optional[typing.List[ComponentConfiguration]], result)

    @builtins.property
    def container_recipe_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the container recipe.

        :default: a name is generated

        :stability: experimental
        '''
        result = self._values.get("container_recipe_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_recipe_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the container recipe.

        :default: 1.0.x

        :stability: experimental
        '''
        result = self._values.get("container_recipe_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the container recipe.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dockerfile(self) -> typing.Optional["DockerfileData"]:
        '''(experimental) The dockerfile template used to build the container image.

        :default:

        - a standard dockerfile template will be generated to pull the base image, perform environment setup, and
        run all components in the recipe

        :stability: experimental
        '''
        result = self._values.get("dockerfile")
        return typing.cast(typing.Optional["DockerfileData"], result)

    @builtins.property
    def instance_block_devices(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.BlockDevice]]:
        '''(experimental) The block devices to attach to the instance used for building, testing, and distributing the container image.

        :default: the block devices of the instance image will be used

        :stability: experimental
        '''
        result = self._values.get("instance_block_devices")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.BlockDevice]], result)

    @builtins.property
    def instance_image(self) -> typing.Optional[ContainerInstanceImage]:
        '''(experimental) The image to use to launch the instance used for building, testing, and distributing the container image.

        :default: Image Builder will use the appropriate ECS-optimized AMI

        :stability: experimental
        '''
        result = self._values.get("instance_image")
        return typing.cast(typing.Optional[ContainerInstanceImage], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key used to encrypt the dockerfile template.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def os_version(self) -> typing.Optional["OSVersion"]:
        '''(experimental) The operating system (OS) version of the base image.

        :default:

        - Image Builder will determine the OS version of the base image, if sourced from a third-party container
        registry. Otherwise, the OS version of the base image is required.

        :stability: experimental
        '''
        result = self._values.get("os_version")
        return typing.cast(typing.Optional["OSVersion"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The tags to apply to the container recipe.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) The working directory for use during build and test workflows.

        :default:

        - the Image Builder default working directory is used. For Linux and macOS builds, this would be /tmp. For
        Windows builds, this would be C:/

        :stability: experimental
        '''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerRecipeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.ContainerType")
class ContainerType(enum.Enum):
    '''(experimental) The type of the container being used in the container recipe.

    :stability: experimental
    '''

    DOCKER = "DOCKER"
    '''(experimental) Indicates the container recipe uses a Docker container.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.DistributionConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "ami_distributions": "amiDistributions",
        "container_distributions": "containerDistributions",
        "description": "description",
        "distribution_configuration_name": "distributionConfigurationName",
        "tags": "tags",
    },
)
class DistributionConfigurationProps:
    def __init__(
        self,
        *,
        ami_distributions: typing.Optional[typing.Sequence[typing.Union[AmiDistribution, typing.Dict[builtins.str, typing.Any]]]] = None,
        container_distributions: typing.Optional[typing.Sequence[typing.Union[ContainerDistribution, typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        distribution_configuration_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Properties for creating a Distribution Configuration resource.

        :param ami_distributions: (experimental) The list of target regions and associated AMI distribution settings where the built AMI will be distributed. AMI distributions may also be added with the ``addAmiDistributions`` method. Default: None if container distributions are provided. Otherwise, at least one AMI or container distribution must be provided
        :param container_distributions: (experimental) The list of target regions and associated container distribution settings where the built container will be distributed. Container distributions may also be added with the ``addContainerDistributions`` method. Default: None if AMI distributions are provided. Otherwise, at least one AMI or container distribution must be provided
        :param description: (experimental) The description of the distribution configuration. Default: None
        :param distribution_configuration_name: (experimental) The name of the distribution configuration. Default: A name is generated
        :param tags: (experimental) The tags to apply to the distribution configuration. Default: None

        :stability: experimental
        :exampleMetadata: infused

        Example::

            distribution_configuration = imagebuilder.DistributionConfiguration(self, "DistributionConfiguration",
                distribution_configuration_name="test-distribution-configuration",
                description="A Distribution Configuration",
                ami_distributions=[imagebuilder.AmiDistribution(
                    # Distribute AMI to us-east-2 and publish the AMI ID to an SSM parameter
                    region="us-east-2",
                    ssm_parameters=[imagebuilder.SSMParameterConfigurations(
                        parameter=ssm.StringParameter.from_string_parameter_attributes(self, "CrossRegionParameter",
                            parameter_name="/imagebuilder/ami",
                            force_dynamic_reference=True
                        )
                    )
                    ]
                )
                ]
            )
            
            # For AMI-based image builds - add an AMI distribution in the current region
            distribution_configuration.add_ami_distributions(
                ami_name="imagebuilder-{{ imagebuilder:buildDate }}",
                ami_description="Build AMI",
                ami_kms_key=kms.Key.from_lookup(self, "ComponentKey", alias_name="alias/distribution-encryption-key"),
                # Copy the AMI to different accounts
                ami_target_account_ids=["123456789012", "098765432109"],
                # Add launch permissions on the AMI
                ami_launch_permission=imagebuilder.AmiLaunchPermission(
                    organization_arns=[
                        self.format_arn(region="", service="organizations", resource="organization", resource_name="o-1234567abc")
                    ],
                    organizational_unit_arns=[
                        self.format_arn(
                            region="",
                            service="organizations",
                            resource="ou",
                            resource_name="o-1234567abc/ou-a123-b4567890"
                        )
                    ],
                    is_public_user_group=True,
                    account_ids=["234567890123"]
                ),
                # Attach tags to the AMI
                ami_tags={
                    "Environment": "production",
                    "Version": "{{ imagebuilder:buildVersion }}"
                },
                # Optional - publish the distributed AMI ID to an SSM parameter
                ssm_parameters=[imagebuilder.SSMParameterConfigurations(
                    parameter=ssm.StringParameter.from_string_parameter_attributes(self, "Parameter",
                        parameter_name="/imagebuilder/ami",
                        force_dynamic_reference=True
                    )
                ), imagebuilder.SSMParameterConfigurations(
                    ami_account="098765432109",
                    data_type=ssm.ParameterDataType.TEXT,
                    parameter=ssm.StringParameter.from_string_parameter_attributes(self, "CrossAccountParameter",
                        parameter_name="imagebuilder-prod-ami",
                        force_dynamic_reference=True
                    )
                )
                ],
                # Optional - create a new launch template version with the distributed AMI ID
                launch_templates=[imagebuilder.LaunchTemplateConfiguration(
                    launch_template=ec2.LaunchTemplate.from_launch_template_attributes(self, "LaunchTemplate",
                        launch_template_id="lt-1234"
                    ),
                    set_default_version=True
                ), imagebuilder.LaunchTemplateConfiguration(
                    account_id="123456789012",
                    launch_template=ec2.LaunchTemplate.from_launch_template_attributes(self, "CrossAccountLaunchTemplate",
                        launch_template_id="lt-5678"
                    ),
                    set_default_version=True
                )
                ],
                # Optional - enable Fast Launch on an imported launch template
                fast_launch_configurations=[imagebuilder.FastLaunchConfiguration(
                    enabled=True,
                    launch_template=ec2.LaunchTemplate.from_launch_template_attributes(self, "FastLaunchLT",
                        launch_template_name="fast-launch-lt"
                    ),
                    max_parallel_launches=10,
                    target_snapshot_count=2
                )
                ],
                # Optional - license configurations to apply to the AMI
                license_configuration_arns=["arn:aws:license-manager:us-west-2:123456789012:license-configuration:lic-abcdefghijklmnopqrstuvwxyz"
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00a08291003318bd50149ef24f2bb14662ca021351848559c22243f8c7a24a58)
            check_type(argname="argument ami_distributions", value=ami_distributions, expected_type=type_hints["ami_distributions"])
            check_type(argname="argument container_distributions", value=container_distributions, expected_type=type_hints["container_distributions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument distribution_configuration_name", value=distribution_configuration_name, expected_type=type_hints["distribution_configuration_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ami_distributions is not None:
            self._values["ami_distributions"] = ami_distributions
        if container_distributions is not None:
            self._values["container_distributions"] = container_distributions
        if description is not None:
            self._values["description"] = description
        if distribution_configuration_name is not None:
            self._values["distribution_configuration_name"] = distribution_configuration_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def ami_distributions(self) -> typing.Optional[typing.List[AmiDistribution]]:
        '''(experimental) The list of target regions and associated AMI distribution settings where the built AMI will be distributed.

        AMI
        distributions may also be added with the ``addAmiDistributions`` method.

        :default:

        None if container distributions are provided. Otherwise, at least one AMI or container distribution must
        be provided

        :stability: experimental
        '''
        result = self._values.get("ami_distributions")
        return typing.cast(typing.Optional[typing.List[AmiDistribution]], result)

    @builtins.property
    def container_distributions(
        self,
    ) -> typing.Optional[typing.List[ContainerDistribution]]:
        '''(experimental) The list of target regions and associated container distribution settings where the built container will be distributed.

        Container distributions may also be added with the ``addContainerDistributions`` method.

        :default:

        None if AMI distributions are provided. Otherwise, at least one AMI or container distribution must be
        provided

        :stability: experimental
        '''
        result = self._values.get("container_distributions")
        return typing.cast(typing.Optional[typing.List[ContainerDistribution]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the distribution configuration.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def distribution_configuration_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the distribution configuration.

        :default: A name is generated

        :stability: experimental
        '''
        result = self._values.get("distribution_configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The tags to apply to the distribution configuration.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DistributionConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DockerfileData(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.DockerfileData",
):
    '''(experimental) Helper class for referencing and uploading dockerfile data for the container recipe.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        container_recipe = imagebuilder.ContainerRecipe(self, "CustomDockerfileContainerRecipe",
            base_image=imagebuilder.BaseContainerImage.from_docker_hub("amazonlinux", "latest"),
            target_repository=imagebuilder.Repository.from_ecr(
                ecr.Repository.from_repository_name(self, "Repository", "my-container-repo")),
            dockerfile=imagebuilder.DockerfileData.from_inline("""
                FROM {{{ imagebuilder:parentImage }}}
                CMD ["echo", "Hello, world!"]
                {{{ imagebuilder:environments }}}
                {{{ imagebuilder:components }}}
                """)
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        path: builtins.str,
        *,
        deploy_time: typing.Optional[builtins.bool] = None,
        display_name: typing.Optional[builtins.str] = None,
        readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IGrantable]] = None,
        source_kms_key: typing.Optional[_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef] = None,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[_aws_cdk_ceddda9d.AssetHashType] = None,
        bundling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow_symlinks: typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode] = None,
        ignore_mode: typing.Optional[_aws_cdk_ceddda9d.IgnoreMode] = None,
    ) -> "S3DockerfileData":
        '''(experimental) Uploads dockerfile data from a local file to S3 to use as the dockerfile data.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param path: The local path to the dockerfile data file.
        :param deploy_time: Whether or not the asset needs to exist beyond deployment time; i.e. are copied over to a different location and not needed afterwards. Setting this property to true has an impact on the lifecycle of the asset, because we will assume that it is safe to delete after the CloudFormation deployment succeeds. For example, Lambda Function assets are copied over to Lambda during deployment. Therefore, it is not necessary to store the asset in S3, so we consider those deployTime assets. Default: false
        :param display_name: A display name for this asset. If supplied, the display name will be used in locations where the asset identifier is printed, like in the CLI progress information. If the same asset is added multiple times, the display name of the first occurrence is used. The default is the construct path of the Asset construct, with respect to the enclosing stack. If the asset is produced by a construct helper function (such as ``lambda.Code.fromAsset()``), this will look like ``MyFunction/Code``. We use the stack-relative construct path so that in the common case where you have multiple stacks with the same asset, we won't show something like ``/MyBetaStack/MyFunction/Code`` when you are actually deploying to production. Default: - Stack-relative construct path
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_kms_key: The ARN of the KMS key used to encrypt the handler code. Default: - the default server-side encryption with Amazon S3 managed keys(SSE-S3) key will be used.
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container or a custom bundling provider. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise
        :param exclude: File paths matching the patterns will be excluded. See ``ignoreMode`` to set the matching behavior. Has no effect on Assets bundled using the ``bundling`` property. Default: - nothing is excluded
        :param follow_symlinks: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param ignore_mode: The ignore behavior to use for ``exclude`` patterns. Default: IgnoreMode.GLOB

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06e465c40a4e54b23940290f080c08cfb4e6ed15f3d514e7bdd79e3d61defa78)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        options = _aws_cdk_aws_s3_assets_ceddda9d.AssetOptions(
            deploy_time=deploy_time,
            display_name=display_name,
            readers=readers,
            source_kms_key=source_kms_key,
            asset_hash=asset_hash,
            asset_hash_type=asset_hash_type,
            bundling=bundling,
            exclude=exclude,
            follow_symlinks=follow_symlinks,
            ignore_mode=ignore_mode,
        )

        return typing.cast("S3DockerfileData", jsii.sinvoke(cls, "fromAsset", [scope, id, path, options]))

    @jsii.member(jsii_name="fromInline")
    @builtins.classmethod
    def from_inline(cls, data: builtins.str) -> "DockerfileData":
        '''(experimental) Uses an inline string as the dockerfile data.

        :param data: An inline string representing the dockerfile data.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33cede864df4d22e89991676d6f5b1c4f6b58443d12df72b1654ba2c708233aa)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        return typing.cast("DockerfileData", jsii.sinvoke(cls, "fromInline", [data]))

    @jsii.member(jsii_name="fromS3")
    @builtins.classmethod
    def from_s3(
        cls,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        key: builtins.str,
    ) -> "S3DockerfileData":
        '''(experimental) References dockerfile data from a pre-existing S3 object.

        :param bucket: The S3 bucket where the dockerfile data is stored.
        :param key: The S3 key of the dockerfile data file.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e93bd18936e56d5825914dd93f6f2ebb38b36fbb87c932ff9ab8247a5b6f4ef)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast("S3DockerfileData", jsii.sinvoke(cls, "fromS3", [bucket, key]))

    @jsii.member(jsii_name="render")
    @abc.abstractmethod
    def render(self) -> "DockerfileTemplateConfig":
        '''(experimental) The rendered Dockerfile value, for use in CloudFormation.

        - For inline dockerfiles, dockerfileTemplateData is the Dockerfile template text
        - For S3-backed dockerfiles, dockerfileTemplateUri is the S3 URL

        :stability: experimental
        '''
        ...


class _DockerfileDataProxy(DockerfileData):
    @jsii.member(jsii_name="render")
    def render(self) -> "DockerfileTemplateConfig":
        '''(experimental) The rendered Dockerfile value, for use in CloudFormation.

        - For inline dockerfiles, dockerfileTemplateData is the Dockerfile template text
        - For S3-backed dockerfiles, dockerfileTemplateUri is the S3 URL

        :stability: experimental
        '''
        return typing.cast("DockerfileTemplateConfig", jsii.invoke(self, "render", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, DockerfileData).__jsii_proxy_class__ = lambda : _DockerfileDataProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.DockerfileTemplateConfig",
    jsii_struct_bases=[],
    name_mapping={
        "dockerfile_template_data": "dockerfileTemplateData",
        "dockerfile_template_uri": "dockerfileTemplateUri",
    },
)
class DockerfileTemplateConfig:
    def __init__(
        self,
        *,
        dockerfile_template_data: typing.Optional[builtins.str] = None,
        dockerfile_template_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The rendered Dockerfile value, for use in CloudFormation.

        - For inline dockerfiles, dockerfileTemplateData is the Dockerfile template text
        - For S3-backed dockerfiles, dockerfileTemplateUri is the S3 URL

        :param dockerfile_template_data: (experimental) The rendered Dockerfile data, for use in CloudFormation. Default: - none if dockerfileTemplateUri is set
        :param dockerfile_template_uri: (experimental) The rendered Dockerfile URI, for use in CloudFormation. Default: - none if dockerfileTemplateData is set

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
            
            dockerfile_template_config = imagebuilder_alpha.DockerfileTemplateConfig(
                dockerfile_template_data="dockerfileTemplateData",
                dockerfile_template_uri="dockerfileTemplateUri"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19d3d0c12c8b9d7ab3a72a82829a53da6567d2c621b4751c8ba673fb699f4ce0)
            check_type(argname="argument dockerfile_template_data", value=dockerfile_template_data, expected_type=type_hints["dockerfile_template_data"])
            check_type(argname="argument dockerfile_template_uri", value=dockerfile_template_uri, expected_type=type_hints["dockerfile_template_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dockerfile_template_data is not None:
            self._values["dockerfile_template_data"] = dockerfile_template_data
        if dockerfile_template_uri is not None:
            self._values["dockerfile_template_uri"] = dockerfile_template_uri

    @builtins.property
    def dockerfile_template_data(self) -> typing.Optional[builtins.str]:
        '''(experimental) The rendered Dockerfile data, for use in CloudFormation.

        :default: - none if dockerfileTemplateUri is set

        :stability: experimental
        '''
        result = self._values.get("dockerfile_template_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dockerfile_template_uri(self) -> typing.Optional[builtins.str]:
        '''(experimental) The rendered Dockerfile URI, for use in CloudFormation.

        :default: - none if dockerfileTemplateData is set

        :stability: experimental
        '''
        result = self._values.get("dockerfile_template_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerfileTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.FastLaunchConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "launch_template": "launchTemplate",
        "max_parallel_launches": "maxParallelLaunches",
        "target_snapshot_count": "targetSnapshotCount",
    },
)
class FastLaunchConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        launch_template: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate] = None,
        max_parallel_launches: typing.Optional[jsii.Number] = None,
        target_snapshot_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) The EC2 Fast Launch configuration to use for the Windows AMI.

        :param enabled: (experimental) Whether to enable fast launch for the AMI. Default: false
        :param launch_template: (experimental) The launch template that the fast-launch enabled Windows AMI uses when it launches Windows instances to create pre-provisioned snapshots. Default: None
        :param max_parallel_launches: (experimental) The maximum number of parallel instances that are launched for creating resources. Default: A maximum of 6 instances are launched in parallel
        :param target_snapshot_count: (experimental) The number of pre-provisioned snapshots to keep on hand for a fast-launch enabled Windows AMI. Default: 10 snapshots are kept pre-provisioned

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
            from aws_cdk import aws_ec2 as ec2
            
            # launch_template: ec2.LaunchTemplate
            
            fast_launch_configuration = imagebuilder_alpha.FastLaunchConfiguration(
                enabled=False,
                launch_template=launch_template,
                max_parallel_launches=123,
                target_snapshot_count=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b90ae1e7cf235ef00d4a47bdf413ccd7ca19785b18e7f91a75464655f60195df)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
            check_type(argname="argument max_parallel_launches", value=max_parallel_launches, expected_type=type_hints["max_parallel_launches"])
            check_type(argname="argument target_snapshot_count", value=target_snapshot_count, expected_type=type_hints["target_snapshot_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if launch_template is not None:
            self._values["launch_template"] = launch_template
        if max_parallel_launches is not None:
            self._values["max_parallel_launches"] = max_parallel_launches
        if target_snapshot_count is not None:
            self._values["target_snapshot_count"] = target_snapshot_count

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable fast launch for the AMI.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def launch_template(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate]:
        '''(experimental) The launch template that the fast-launch enabled Windows AMI uses when it launches Windows instances to create pre-provisioned snapshots.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("launch_template")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate], result)

    @builtins.property
    def max_parallel_launches(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of parallel instances that are launched for creating resources.

        :default: A maximum of 6 instances are launched in parallel

        :see: https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_EnableFastLaunch.html
        :stability: experimental
        '''
        result = self._values.get("max_parallel_launches")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_snapshot_count(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of pre-provisioned snapshots to keep on hand for a fast-launch enabled Windows AMI.

        :default: 10 snapshots are kept pre-provisioned

        :see: https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_EnableFastLaunch.html
        :stability: experimental
        '''
        result = self._values.get("target_snapshot_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FastLaunchConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.HttpTokens")
class HttpTokens(enum.Enum):
    '''(experimental) Indicates whether a signed token header is required for instance metadata retrieval requests.

    :see: https://docs.aws.amazon.com/imagebuilder/latest/APIReference/API_InstanceMetadataOptions.html#imagebuilder-Type-InstanceMetadataOptions-httpTokens
    :stability: experimental
    :exampleMetadata: infused

    Example::

        infrastructure_configuration = imagebuilder.InfrastructureConfiguration(self, "InfrastructureConfiguration",
            infrastructure_configuration_name="test-infrastructure-configuration",
            description="An Infrastructure Configuration",
            # Optional - instance types to use for build/test
            instance_types=[
                ec2.InstanceType.of(ec2.InstanceClass.STANDARD7_INTEL, ec2.InstanceSize.LARGE),
                ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.LARGE)
            ],
            # Optional - create an instance profile with necessary permissions
            instance_profile=iam.InstanceProfile(self, "InstanceProfile",
                instance_profile_name="test-instance-profile",
                role=iam.Role(self, "InstanceProfileRole",
                    assumed_by=iam.ServicePrincipal.from_static_service_principle_name("ec2.amazonaws.com"),
                    managed_policies=[
                        iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"),
                        iam.ManagedPolicy.from_aws_managed_policy_name("EC2InstanceProfileForImageBuilder")
                    ]
                )
            ),
            # Use VPC network configuration
            vpc=vpc,
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_groups=[ec2.SecurityGroup.from_security_group_id(self, "SecurityGroup", vpc.vpc_default_security_group)],
            key_pair=ec2.KeyPair.from_key_pair_name(self, "KeyPair", "imagebuilder-instance-key-pair"),
            terminate_instance_on_failure=True,
            # Optional - IMDSv2 settings
            http_tokens=imagebuilder.HttpTokens.REQUIRED,
            http_put_response_hop_limit=1,
            # Optional - publish image completion messages to an SNS topic
            notification_topic=sns.Topic.from_topic_arn(self, "Topic",
                self.format_arn(service="sns", resource="image-builder-topic")),
            # Optional - log settings. Logging is enabled by default
            logging=imagebuilder.InfrastructureConfigurationLogging(
                s3_bucket=s3.Bucket.from_bucket_name(self, "LogBucket", f"imagebuilder-logging-{Aws.ACCOUNT_ID}"),
                s3_key_prefix="imagebuilder-logs"
            ),
            # Optional - host placement settings
            ec2_instance_availability_zone=Stack.of(self).availability_zones[0],
            ec2_instance_host_id=dedicated_host.attr_host_id,
            ec2_instance_tenancy=imagebuilder.Tenancy.HOST,
            resource_tags={
                "Environment": "production"
            }
        )
    '''

    OPTIONAL = "OPTIONAL"
    '''(experimental) Allows retrieval of instance metadata with or without a signed token header in the request.

    :stability: experimental
    '''
    REQUIRED = "REQUIRED"
    '''(experimental) Requires a signed token header in instance metadata retrieval requests.

    :stability: experimental
    '''


@jsii.interface(jsii_type="@aws-cdk/aws-imagebuilder-alpha.IComponent")
class IComponent(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) An EC2 Image Builder Component.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="componentArn")
    def component_arn(self) -> builtins.str:
        '''(experimental) The ARN of the component.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="componentName")
    def component_name(self) -> builtins.str:
        '''(experimental) The name of the component.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="componentVersion")
    def component_version(self) -> builtins.str:
        '''(experimental) The version of the component.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the component.

        :param grantee: The principal.
        :param actions: The list of actions.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the component.

        :param grantee: The principal.

        :stability: experimental
        '''
        ...


class _IComponentProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) An EC2 Image Builder Component.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-imagebuilder-alpha.IComponent"

    @builtins.property
    @jsii.member(jsii_name="componentArn")
    def component_arn(self) -> builtins.str:
        '''(experimental) The ARN of the component.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "componentArn"))

    @builtins.property
    @jsii.member(jsii_name="componentName")
    def component_name(self) -> builtins.str:
        '''(experimental) The name of the component.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "componentName"))

    @builtins.property
    @jsii.member(jsii_name="componentVersion")
    def component_version(self) -> builtins.str:
        '''(experimental) The version of the component.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "componentVersion"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the component.

        :param grantee: The principal.
        :param actions: The list of actions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c05d6ee1a3eb8c5f9b0d715b586bd51b2a253ebbcc8dae51c78ae2c159bf057)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the component.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__841448c6baa993d7b4b3033a5490d19f411b8aebe362b78bd7e0490c73bd22d1)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IComponent).__jsii_proxy_class__ = lambda : _IComponentProxy


@jsii.interface(jsii_type="@aws-cdk/aws-imagebuilder-alpha.IDistributionConfiguration")
class IDistributionConfiguration(
    _aws_cdk_ceddda9d.IResource,
    typing_extensions.Protocol,
):
    '''(experimental) An EC2 Image Builder Distribution Configuration.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="distributionConfigurationArn")
    def distribution_configuration_arn(self) -> builtins.str:
        '''(experimental) The ARN of the distribution configuration.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="distributionConfigurationName")
    def distribution_configuration_name(self) -> builtins.str:
        '''(experimental) The name of the distribution configuration.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the distribution configuration.

        :param grantee: The principal.
        :param actions: The list of actions.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the distribution configuration.

        :param grantee: The principal.

        :stability: experimental
        '''
        ...


class _IDistributionConfigurationProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) An EC2 Image Builder Distribution Configuration.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-imagebuilder-alpha.IDistributionConfiguration"

    @builtins.property
    @jsii.member(jsii_name="distributionConfigurationArn")
    def distribution_configuration_arn(self) -> builtins.str:
        '''(experimental) The ARN of the distribution configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "distributionConfigurationArn"))

    @builtins.property
    @jsii.member(jsii_name="distributionConfigurationName")
    def distribution_configuration_name(self) -> builtins.str:
        '''(experimental) The name of the distribution configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "distributionConfigurationName"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the distribution configuration.

        :param grantee: The principal.
        :param actions: The list of actions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a9dae8c4b2356a5fed2efe8df76a59819e04e2a8562b9fe922537ca4b6313be)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the distribution configuration.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e644849da79fab144eff75407555da79d5543225778e3d852909fa3b1a1d2933)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDistributionConfiguration).__jsii_proxy_class__ = lambda : _IDistributionConfigurationProxy


@jsii.interface(jsii_type="@aws-cdk/aws-imagebuilder-alpha.IImage")
class IImage(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) An EC2 Image Builder Image.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="imageArn")
    def image_arn(self) -> builtins.str:
        '''(experimental) The ARN of the image.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''(experimental) The name of the image.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="imageVersion")
    def image_version(self) -> builtins.str:
        '''(experimental) The version of the image.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the image.

        :param grantee: The principal.
        :param actions: The list of actions.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantDefaultExecutionRolePermissions")
    def grant_default_execution_role_permissions(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> typing.List[_aws_cdk_aws_iam_ceddda9d.Grant]:
        '''(experimental) Grants the default permissions for building an image to the provided execution role.

        :param grantee: The execution role used for the image build.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the image.

        :param grantee: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="toBaseImage")
    def to_base_image(self) -> BaseImage:
        '''(experimental) Converts the image to a BaseImage, to use as the parent image in an image recipe.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="toContainerBaseImage")
    def to_container_base_image(self) -> BaseContainerImage:
        '''(experimental) Converts the image to a ContainerBaseImage, to use as the parent image in a container recipe.

        :stability: experimental
        '''
        ...


class _IImageProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) An EC2 Image Builder Image.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-imagebuilder-alpha.IImage"

    @builtins.property
    @jsii.member(jsii_name="imageArn")
    def image_arn(self) -> builtins.str:
        '''(experimental) The ARN of the image.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageArn"))

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''(experimental) The name of the image.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @builtins.property
    @jsii.member(jsii_name="imageVersion")
    def image_version(self) -> builtins.str:
        '''(experimental) The version of the image.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageVersion"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the image.

        :param grantee: The principal.
        :param actions: The list of actions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3276ee979b27952851d2f36b668b4bf2f4378adf7731f6e1232dc543a6e49a07)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantDefaultExecutionRolePermissions")
    def grant_default_execution_role_permissions(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> typing.List[_aws_cdk_aws_iam_ceddda9d.Grant]:
        '''(experimental) Grants the default permissions for building an image to the provided execution role.

        :param grantee: The execution role used for the image build.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c182cbdd5bc65235c36e534dba1aa8f309e3c27cf3cbeb87e37885969292af6f)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(typing.List[_aws_cdk_aws_iam_ceddda9d.Grant], jsii.invoke(self, "grantDefaultExecutionRolePermissions", [grantee]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the image.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa9a7780ef73c14556994f6fa8819e22a8467694dda3f89e55e75049834c32dc)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="toBaseImage")
    def to_base_image(self) -> BaseImage:
        '''(experimental) Converts the image to a BaseImage, to use as the parent image in an image recipe.

        :stability: experimental
        '''
        return typing.cast(BaseImage, jsii.invoke(self, "toBaseImage", []))

    @jsii.member(jsii_name="toContainerBaseImage")
    def to_container_base_image(self) -> BaseContainerImage:
        '''(experimental) Converts the image to a ContainerBaseImage, to use as the parent image in a container recipe.

        :stability: experimental
        '''
        return typing.cast(BaseContainerImage, jsii.invoke(self, "toContainerBaseImage", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IImage).__jsii_proxy_class__ = lambda : _IImageProxy


@jsii.interface(jsii_type="@aws-cdk/aws-imagebuilder-alpha.IImagePipeline")
class IImagePipeline(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) An EC2 Image Builder Image Pipeline.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="imagePipelineArn")
    def image_pipeline_arn(self) -> builtins.str:
        '''(experimental) The ARN of the image pipeline.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="imagePipelineName")
    def image_pipeline_name(self) -> builtins.str:
        '''(experimental) The name of the image pipeline.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the image pipeline.

        :param grantee: The principal.
        :param actions: The list of actions.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantDefaultExecutionRolePermissions")
    def grant_default_execution_role_permissions(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> typing.List[_aws_cdk_aws_iam_ceddda9d.Grant]:
        '''(experimental) Grants the default permissions for building an image to the provided execution role.

        :param grantee: The execution role used for the image build.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the image pipeline.

        :param grantee: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantStartExecution")
    def grant_start_execution(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant permissions to the given grantee to start an execution of the image pipeline.

        :param grantee: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onCVEDetected")
    def on_cve_detected(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder CVE detected events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onImageBuildCompleted")
    def on_image_build_completed(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder image build completion events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onImageBuildFailed")
    def on_image_build_failed(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder image build failure events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onImageBuildStateChange")
    def on_image_build_state_change(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder image state change events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onImageBuildSucceeded")
    def on_image_build_succeeded(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder image success events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onImagePipelineAutoDisabled")
    def on_image_pipeline_auto_disabled(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder image pipeline automatically disabled events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onWaitForAction")
    def on_wait_for_action(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder wait for action events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        ...


class _IImagePipelineProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) An EC2 Image Builder Image Pipeline.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-imagebuilder-alpha.IImagePipeline"

    @builtins.property
    @jsii.member(jsii_name="imagePipelineArn")
    def image_pipeline_arn(self) -> builtins.str:
        '''(experimental) The ARN of the image pipeline.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "imagePipelineArn"))

    @builtins.property
    @jsii.member(jsii_name="imagePipelineName")
    def image_pipeline_name(self) -> builtins.str:
        '''(experimental) The name of the image pipeline.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "imagePipelineName"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the image pipeline.

        :param grantee: The principal.
        :param actions: The list of actions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fd1ad72d6c4a34306ef21742f859f00b83e5f860e5c8f0635b42613c748bd08)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantDefaultExecutionRolePermissions")
    def grant_default_execution_role_permissions(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> typing.List[_aws_cdk_aws_iam_ceddda9d.Grant]:
        '''(experimental) Grants the default permissions for building an image to the provided execution role.

        :param grantee: The execution role used for the image build.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaa895de47b9cf1a63c6d30b4d4ad2b01ddb6ce62da9325fd3c7b0690ef173fe)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(typing.List[_aws_cdk_aws_iam_ceddda9d.Grant], jsii.invoke(self, "grantDefaultExecutionRolePermissions", [grantee]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the image pipeline.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880ec80536c3f2c5824d0ec9dc299d46bc0d287296538ba1055d8067d2485f7d)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="grantStartExecution")
    def grant_start_execution(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant permissions to the given grantee to start an execution of the image pipeline.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5f38ae4b97b44d57cd707bacec18195907141dfd0a6a91ecc557de931ede97a)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantStartExecution", [grantee]))

    @jsii.member(jsii_name="onCVEDetected")
    def on_cve_detected(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder CVE detected events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58710cc3d4336254e0af45eff2cdb81c60bd51b9de82d103acaa0231e11de37)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onCVEDetected", [id, options]))

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6ed6ed74909416a5bc8e1370b5c1b5323a1bd28fa4c06bc20be9b6e44b65cab)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onEvent", [id, options]))

    @jsii.member(jsii_name="onImageBuildCompleted")
    def on_image_build_completed(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder image build completion events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f34d3df73810d33135be008062f2a8d78392d9d6f1ba4a4f913358b865df7122)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onImageBuildCompleted", [id, options]))

    @jsii.member(jsii_name="onImageBuildFailed")
    def on_image_build_failed(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder image build failure events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29c481d4265c4c0633be2bc92a50918cf26005b82a53d1963ff1267b8ef2ac8a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onImageBuildFailed", [id, options]))

    @jsii.member(jsii_name="onImageBuildStateChange")
    def on_image_build_state_change(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder image state change events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397042635617cd97dddc7588edef7f9dccb7f68ca854c1cc47d962fea44afbf4)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onImageBuildStateChange", [id, options]))

    @jsii.member(jsii_name="onImageBuildSucceeded")
    def on_image_build_succeeded(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder image success events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a289aeda75eae7ca4c17b26ae7c52ea260ca4a3a67a382bd19f4f662d99c075d)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onImageBuildSucceeded", [id, options]))

    @jsii.member(jsii_name="onImagePipelineAutoDisabled")
    def on_image_pipeline_auto_disabled(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder image pipeline automatically disabled events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8212807ebda9a9c367c21684bb2e3108004d395720b50f556f78ce624e2eeea4)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onImagePipelineAutoDisabled", [id, options]))

    @jsii.member(jsii_name="onWaitForAction")
    def on_wait_for_action(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder wait for action events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94429e836818b23a640507fa54b60c37e9aba1345e1ae71b7ca42ec0e323a9e3)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onWaitForAction", [id, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IImagePipeline).__jsii_proxy_class__ = lambda : _IImagePipelineProxy


@jsii.interface(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.IInfrastructureConfiguration"
)
class IInfrastructureConfiguration(
    _aws_cdk_ceddda9d.IResource,
    typing_extensions.Protocol,
):
    '''(experimental) An EC2 Image Builder Infrastructure Configuration.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="infrastructureConfigurationArn")
    def infrastructure_configuration_arn(self) -> builtins.str:
        '''(experimental) The ARN of the infrastructure configuration.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="infrastructureConfigurationName")
    def infrastructure_configuration_name(self) -> builtins.str:
        '''(experimental) The name of the infrastructure configuration.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the infrastructure configuration.

        :param grantee: - The principal.
        :param actions: - The list of actions.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the infrastructure configuration.

        :param grantee: - The principal.

        :stability: experimental
        '''
        ...


class _IInfrastructureConfigurationProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) An EC2 Image Builder Infrastructure Configuration.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-imagebuilder-alpha.IInfrastructureConfiguration"

    @builtins.property
    @jsii.member(jsii_name="infrastructureConfigurationArn")
    def infrastructure_configuration_arn(self) -> builtins.str:
        '''(experimental) The ARN of the infrastructure configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "infrastructureConfigurationArn"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureConfigurationName")
    def infrastructure_configuration_name(self) -> builtins.str:
        '''(experimental) The name of the infrastructure configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "infrastructureConfigurationName"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the infrastructure configuration.

        :param grantee: - The principal.
        :param actions: - The list of actions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f4ed7436405bcfb3a075aa5c93725806206943d8dbaa96c5cef8dd4d46cae37)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the infrastructure configuration.

        :param grantee: - The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2582830fbd4fc0772d12414b5d2346ecedd7b1bb8582db47fa079012ef22197)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IInfrastructureConfiguration).__jsii_proxy_class__ = lambda : _IInfrastructureConfigurationProxy


@jsii.interface(jsii_type="@aws-cdk/aws-imagebuilder-alpha.ILifecyclePolicy")
class ILifecyclePolicy(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) An EC2 Image Builder Lifecycle Policy.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="lifecyclePolicyArn")
    def lifecycle_policy_arn(self) -> builtins.str:
        '''(experimental) The ARN of the lifecycle policy.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="lifecyclePolicyName")
    def lifecycle_policy_name(self) -> builtins.str:
        '''(experimental) The name of the lifecycle policy.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the lifecycle policy.

        :param grantee: - The principal.
        :param actions: - The list of actions.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the lifecycle policy.

        :param grantee: - The principal.

        :stability: experimental
        '''
        ...


class _ILifecyclePolicyProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) An EC2 Image Builder Lifecycle Policy.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-imagebuilder-alpha.ILifecyclePolicy"

    @builtins.property
    @jsii.member(jsii_name="lifecyclePolicyArn")
    def lifecycle_policy_arn(self) -> builtins.str:
        '''(experimental) The ARN of the lifecycle policy.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "lifecyclePolicyArn"))

    @builtins.property
    @jsii.member(jsii_name="lifecyclePolicyName")
    def lifecycle_policy_name(self) -> builtins.str:
        '''(experimental) The name of the lifecycle policy.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "lifecyclePolicyName"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the lifecycle policy.

        :param grantee: - The principal.
        :param actions: - The list of actions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc13bfedf536aa32a04f1ae979b0cdaa79e62a91830c859a47e1f3d9a2f761a)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the lifecycle policy.

        :param grantee: - The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5899e69104590e773d3aed63c9f3c694bdeb14392efdc65b0fc19700402c68e)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILifecyclePolicy).__jsii_proxy_class__ = lambda : _ILifecyclePolicyProxy


@jsii.interface(jsii_type="@aws-cdk/aws-imagebuilder-alpha.IRecipeBase")
class IRecipeBase(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) A base interface for EC2 Image Builder recipes.

    :stability: experimental
    '''

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the recipe.

        :param grantee: The principal.
        :param actions: The list of actions.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the recipe.

        :param grantee: The principal.

        :stability: experimental
        '''
        ...


class _IRecipeBaseProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) A base interface for EC2 Image Builder recipes.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-imagebuilder-alpha.IRecipeBase"

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the recipe.

        :param grantee: The principal.
        :param actions: The list of actions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b23a51e11415232274c8ba996b5aa565e9e2abe2f40f1151b846ada69dc201)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the recipe.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d6e4867e55c2c8ef84e31eb5367502ec1ffdb65877ecfdd2caac1ad06699196)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRecipeBase).__jsii_proxy_class__ = lambda : _IRecipeBaseProxy


@jsii.interface(jsii_type="@aws-cdk/aws-imagebuilder-alpha.IWorkflow")
class IWorkflow(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) An EC2 Image Builder Workflow.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="workflowArn")
    def workflow_arn(self) -> builtins.str:
        '''(experimental) The ARN of the workflow.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="workflowName")
    def workflow_name(self) -> builtins.str:
        '''(experimental) The name of the workflow.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="workflowType")
    def workflow_type(self) -> builtins.str:
        '''(experimental) The type of the workflow.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="workflowVersion")
    def workflow_version(self) -> builtins.str:
        '''(experimental) The version of the workflow.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the workflow.

        :param grantee: The principal.
        :param actions: The list of actions.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the workflow.

        :param grantee: The principal.

        :stability: experimental
        '''
        ...


class _IWorkflowProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) An EC2 Image Builder Workflow.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-imagebuilder-alpha.IWorkflow"

    @builtins.property
    @jsii.member(jsii_name="workflowArn")
    def workflow_arn(self) -> builtins.str:
        '''(experimental) The ARN of the workflow.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "workflowArn"))

    @builtins.property
    @jsii.member(jsii_name="workflowName")
    def workflow_name(self) -> builtins.str:
        '''(experimental) The name of the workflow.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "workflowName"))

    @builtins.property
    @jsii.member(jsii_name="workflowType")
    def workflow_type(self) -> builtins.str:
        '''(experimental) The type of the workflow.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "workflowType"))

    @builtins.property
    @jsii.member(jsii_name="workflowVersion")
    def workflow_version(self) -> builtins.str:
        '''(experimental) The version of the workflow.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "workflowVersion"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the workflow.

        :param grantee: The principal.
        :param actions: The list of actions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c5a2a7384fc07f344d9ad883137648bc3f9d66145ca25702ad1e61d89b6176d)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the workflow.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6302fac9559d479e26025ee1e3d3f2a0a68dd3dc6e7b461db24dc1c755c86162)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IWorkflow).__jsii_proxy_class__ = lambda : _IWorkflowProxy


@jsii.implements(IImage)
class Image(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.Image",
):
    '''(experimental) Represents an EC2 Image Builder Image.

    :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/create-images.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        container_recipe = imagebuilder.ContainerRecipe(self, "MyContainerRecipe",
            base_image=imagebuilder.BaseContainerImage.from_docker_hub("amazonlinux", "latest"),
            target_repository=imagebuilder.Repository.from_ecr(
                ecr.Repository.from_repository_name(self, "Repository", "my-container-repo"))
        )
        
        container_image = imagebuilder.Image(self, "MyContainerImage",
            recipe=container_recipe
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        recipe: IRecipeBase,
        deletion_execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        distribution_configuration: typing.Optional[IDistributionConfiguration] = None,
        enhanced_image_metadata_enabled: typing.Optional[builtins.bool] = None,
        execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        image_scanning_ecr_repository: typing.Optional[_aws_cdk_aws_ecr_ceddda9d.IRepository] = None,
        image_scanning_ecr_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_scanning_enabled: typing.Optional[builtins.bool] = None,
        image_tests_enabled: typing.Optional[builtins.bool] = None,
        infrastructure_configuration: typing.Optional[IInfrastructureConfiguration] = None,
        log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workflows: typing.Optional[typing.Sequence[typing.Union["WorkflowConfiguration", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param recipe: (experimental) The recipe that defines the base image, components, and customizations used to build the image. This can either be an image recipe, or a container recipe.
        :param deletion_execution_role: (experimental) The execution role to use for deleting the image as well as the underlying resources, such as the AMIs, snapshots, and containers. This role should contain resource lifecycle permissions required to delete the underlying AMIs/containers. Default: - no execution role. Only the Image Builder image will be deleted.
        :param distribution_configuration: (experimental) The distribution configuration used for distributing the image. Default: None
        :param enhanced_image_metadata_enabled: (experimental) If enabled, collects additional information about the image being created, including the operating system (OS) version and package list for the AMI. Default: true
        :param execution_role: (experimental) The execution role used to perform workflow actions to build the image. By default, the Image Builder Service Linked Role (SLR) will be created automatically and used as the execution role. However, when providing a custom set of image workflows for the image, an execution role will be generated with the minimal permissions needed to execute the workflows. Default: - Image Builder will use the SLR if possible. Otherwise, an execution role will be generated
        :param image_scanning_ecr_repository: (experimental) The container repository that Amazon Inspector scans to identify findings for your container images. If a repository is not provided, Image Builder creates a repository named ``image-builder-image-scanning-repository`` for vulnerability scanning. Default: - if scanning is enabled, a repository will be created by Image Builder if one is not provided
        :param image_scanning_ecr_tags: (experimental) The tags for Image Builder to apply to the output container image that Amazon Inspector scans. Default: None
        :param image_scanning_enabled: (experimental) Indicates whether Image Builder keeps a snapshot of the vulnerability scans that Amazon Inspector runs against the build instance when you create a new image. Default: false
        :param image_tests_enabled: (experimental) Whether to run tests after building an image. Default: true
        :param infrastructure_configuration: (experimental) The infrastructure configuration used for building the image. A default infrastructure configuration will be used if one is not provided. The default configuration will create an instance profile and role with minimal permissions needed to build the image, attached to the EC2 instance. IMDSv2 will be required by default on the instances used to build and test the image. Default: - an infrastructure configuration will be created with the default settings
        :param log_group: (experimental) The log group to use for the image. By default, a log group will be created with the format ``/aws/imagebuilder/<image-name>`` Default: - a log group will be created
        :param tags: (experimental) The tags to apply to the image. Default: None
        :param workflows: (experimental) The list of workflow configurations used to build the image. Default: - Image Builder will use a default set of workflows for the build to build, test, and distribute the image

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__030f15c77b2bbcd41794165ded225e1182616669caf96b4f1552a7847a910ea4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ImageProps(
            recipe=recipe,
            deletion_execution_role=deletion_execution_role,
            distribution_configuration=distribution_configuration,
            enhanced_image_metadata_enabled=enhanced_image_metadata_enabled,
            execution_role=execution_role,
            image_scanning_ecr_repository=image_scanning_ecr_repository,
            image_scanning_ecr_tags=image_scanning_ecr_tags,
            image_scanning_enabled=image_scanning_enabled,
            image_tests_enabled=image_tests_enabled,
            infrastructure_configuration=infrastructure_configuration,
            log_group=log_group,
            tags=tags,
            workflows=workflows,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromImageArn")
    @builtins.classmethod
    def from_image_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        image_arn: builtins.str,
    ) -> IImage:
        '''(experimental) Import an existing image given its ARN.

        :param scope: -
        :param id: -
        :param image_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e00da4d4aafb3e96b734592b50a5507669f6f8282023fea353c83fe9c1e564e5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_arn", value=image_arn, expected_type=type_hints["image_arn"])
        return typing.cast(IImage, jsii.sinvoke(cls, "fromImageArn", [scope, id, image_arn]))

    @jsii.member(jsii_name="fromImageAttributes")
    @builtins.classmethod
    def from_image_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_arn: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_version: typing.Optional[builtins.str] = None,
    ) -> IImage:
        '''(experimental) Import an existing image by providing its attributes.

        If the image name is provided as an attribute, it must be
        normalized by converting all alphabetical characters to lowercase, and replacing all spaces and underscores with
        hyphens.

        :param scope: -
        :param id: -
        :param image_arn: (experimental) The ARN of the image. Default: - derived from the imageName
        :param image_name: (experimental) The name of the image. Default: - derived from the imageArn
        :param image_version: (experimental) The version of the image. Default: - the latest version of the image, x.x.x

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d56fc3a16ff529463d8b0ab8962cd6f1ebf3f608762e39adbcf06065ecf1034f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = ImageAttributes(
            image_arn=image_arn, image_name=image_name, image_version=image_version
        )

        return typing.cast(IImage, jsii.sinvoke(cls, "fromImageAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromImageName")
    @builtins.classmethod
    def from_image_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        image_name: builtins.str,
    ) -> IImage:
        '''(experimental) Import an existing image given its name.

        The provided name must be normalized by converting all alphabetical
        characters to lowercase, and replacing all spaces and underscores with hyphens.

        :param scope: -
        :param id: -
        :param image_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b680e7f46fa34bb4cb6edac51de1a19e1feb086b48d927fa79da1085403365e8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
        return typing.cast(IImage, jsii.sinvoke(cls, "fromImageName", [scope, id, image_name]))

    @jsii.member(jsii_name="isImage")
    @builtins.classmethod
    def is_image(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Return whether the given object is an Image.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7fb4700ccff258247b59db28a7c2655a5d913e22e589c292238904f7086ff9d)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isImage", [x]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the image.

        :param grantee: The principal.
        :param actions: The list of actions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__865d936fa059acad61d6ff14ffdfefd15f23d87430302056e830dffa7b486b38)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantDefaultExecutionRolePermissions")
    def grant_default_execution_role_permissions(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> typing.List[_aws_cdk_aws_iam_ceddda9d.Grant]:
        '''(experimental) Grants the default permissions for building an image to the provided execution role.

        :param grantee: The execution role used for the image build.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c15936fdca36c2becea19d37ef971f2656d0b7813cd6a09384905fc9df866fe)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(typing.List[_aws_cdk_aws_iam_ceddda9d.Grant], jsii.invoke(self, "grantDefaultExecutionRolePermissions", [grantee]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the image.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9051a94b754d203fc043136113c5d4ae1992b65e093a7c6d07320e74b29fb3f4)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="toBaseImage")
    def to_base_image(self) -> BaseImage:
        '''(experimental) Converts the image to a BaseImage, to use as the parent image in an image recipe.

        :stability: experimental
        '''
        return typing.cast(BaseImage, jsii.invoke(self, "toBaseImage", []))

    @jsii.member(jsii_name="toContainerBaseImage")
    def to_container_base_image(self) -> BaseContainerImage:
        '''(experimental) Converts the image to a ContainerBaseImage, to use as the parent image in a container recipe.

        :stability: experimental
        '''
        return typing.cast(BaseContainerImage, jsii.invoke(self, "toContainerBaseImage", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="imageArn")
    def image_arn(self) -> builtins.str:
        '''(experimental) The ARN of the image.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageArn"))

    @builtins.property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> builtins.str:
        '''(experimental) The AMI ID of the EC2 AMI, or URI for the container.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageId"))

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''(experimental) The name of the image.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @builtins.property
    @jsii.member(jsii_name="imageVersion")
    def image_version(self) -> builtins.str:
        '''(experimental) The version of the image.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageVersion"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureConfiguration")
    def infrastructure_configuration(self) -> IInfrastructureConfiguration:
        '''(experimental) The infrastructure configuration used for the image build.

        :stability: experimental
        '''
        return typing.cast(IInfrastructureConfiguration, jsii.get(self, "infrastructureConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The execution role used for the image build.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "executionRole"))


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.ImageArchitecture")
class ImageArchitecture(enum.Enum):
    '''(experimental) The architecture of the image.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Amazon Linux 2023 AMI for x86_64
        amazon_linux2023_ami = imagebuilder.AmazonManagedImage.amazon_linux2023(self, "AmazonLinux2023",
            image_type=imagebuilder.ImageType.AMI,
            image_architecture=imagebuilder.ImageArchitecture.X86_64
        )
        
        # Ubuntu 22.04 AMI for ARM64
        ubuntu2204_ami = imagebuilder.AmazonManagedImage.ubuntu_server2204(self, "Ubuntu2204",
            image_type=imagebuilder.ImageType.AMI,
            image_architecture=imagebuilder.ImageArchitecture.ARM64
        )
        
        # Windows Server 2022 Full AMI
        windows2022_ami = imagebuilder.AmazonManagedImage.windows_server2022_full(self, "Windows2022",
            image_type=imagebuilder.ImageType.AMI,
            image_architecture=imagebuilder.ImageArchitecture.X86_64
        )
        
        # Use as base image in recipe
        managed_image_recipe = imagebuilder.ImageRecipe(self, "ManagedImageRecipe",
            base_image=amazon_linux2023_ami.to_base_image()
        )
    '''

    ARM64 = "ARM64"
    '''(experimental) 64 bit architecture with the ARM instruction set.

    :stability: experimental
    '''
    X86_64 = "X86_64"
    '''(experimental) 64 bit architecture with x86 instruction set.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ImageAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "image_arn": "imageArn",
        "image_name": "imageName",
        "image_version": "imageVersion",
    },
)
class ImageAttributes:
    def __init__(
        self,
        *,
        image_arn: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for an EC2 Image Builder image.

        :param image_arn: (experimental) The ARN of the image. Default: - derived from the imageName
        :param image_name: (experimental) The name of the image. Default: - derived from the imageArn
        :param image_version: (experimental) The version of the image. Default: - the latest version of the image, x.x.x

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # Import by name
            existing_image_by_name = imagebuilder.Image.from_image_name(self, "ExistingImageByName", "my-existing-image")
            
            # Import by ARN
            existing_image_by_arn = imagebuilder.Image.from_image_arn(self, "ExistingImageByArn", "arn:aws:imagebuilder:us-east-1:123456789012:image/imported-image/1.0.0")
            
            # Import by attributes
            existing_image_by_attributes = imagebuilder.Image.from_image_attributes(self, "ExistingImageByAttributes",
                image_name="shared-base-image",
                image_version="2024.11.25"
            )
            
            # Grant permissions to imported images
            role = iam.Role(self, "ImageAccessRole",
                assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
            )
            
            existing_image_by_name.grant_read(role)
            existing_image_by_arn.grant(role, "imagebuilder:GetImage", "imagebuilder:ListImagePackages")
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40ed11a9ec065fecf71481ca69df8a28cb8144ba021f0148629a9be5d38ccdab)
            check_type(argname="argument image_arn", value=image_arn, expected_type=type_hints["image_arn"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument image_version", value=image_version, expected_type=type_hints["image_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if image_arn is not None:
            self._values["image_arn"] = image_arn
        if image_name is not None:
            self._values["image_name"] = image_name
        if image_version is not None:
            self._values["image_version"] = image_version

    @builtins.property
    def image_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the image.

        :default: - derived from the imageName

        :stability: experimental
        '''
        result = self._values.get("image_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the image.

        :default: - derived from the imageArn

        :stability: experimental
        '''
        result = self._values.get("image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the image.

        :default: - the latest version of the image, x.x.x

        :stability: experimental
        '''
        result = self._values.get("image_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IImagePipeline)
class ImagePipeline(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ImagePipeline",
):
    '''(experimental) Represents an EC2 Image Builder Image Pipeline.

    :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/manage-pipelines.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        workflow_pipeline = imagebuilder.ImagePipeline(self, "WorkflowPipeline",
            recipe=example_image_recipe,
            workflows=[imagebuilder.WorkflowConfiguration(workflow=imagebuilder.AwsManagedWorkflow.build_image(self, "BuildWorkflow")), imagebuilder.WorkflowConfiguration(workflow=imagebuilder.AwsManagedWorkflow.test_image(self, "TestWorkflow"))
            ]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        recipe: IRecipeBase,
        description: typing.Optional[builtins.str] = None,
        distribution_configuration: typing.Optional[IDistributionConfiguration] = None,
        enhanced_image_metadata_enabled: typing.Optional[builtins.bool] = None,
        execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        image_log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
        image_pipeline_log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
        image_pipeline_name: typing.Optional[builtins.str] = None,
        image_scanning_ecr_repository: typing.Optional[_aws_cdk_aws_ecr_ceddda9d.IRepository] = None,
        image_scanning_ecr_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_scanning_enabled: typing.Optional[builtins.bool] = None,
        image_tests_enabled: typing.Optional[builtins.bool] = None,
        infrastructure_configuration: typing.Optional[IInfrastructureConfiguration] = None,
        schedule: typing.Optional[typing.Union["ImagePipelineSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional["ImagePipelineStatus"] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workflows: typing.Optional[typing.Sequence[typing.Union["WorkflowConfiguration", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param recipe: (experimental) The recipe that defines the base image, components, and customizations used to build the image. This can either be an image recipe, or a container recipe.
        :param description: (experimental) The description of the image pipeline. Default: None
        :param distribution_configuration: (experimental) The distribution configuration used for distributing the image. Default: None
        :param enhanced_image_metadata_enabled: (experimental) If enabled, collects additional information about the image being created, including the operating system (OS) version and package list for the AMI. Default: true
        :param execution_role: (experimental) The execution role used to perform workflow actions to build this image. By default, the Image Builder Service Linked Role (SLR) will be created automatically and used as the execution role. However, when providing a custom set of image workflows for the pipeline, an execution role will be generated with the minimal permissions needed to execute the workflows. Default: - Image Builder will use the SLR if possible. Otherwise, an execution role will be generated
        :param image_log_group: (experimental) The log group to use for images created from the image pipeline. By default, a log group will be created with the format ``/aws/imagebuilder/<image-name>``. Default: - a log group will be created
        :param image_pipeline_log_group: (experimental) The log group to use for the image pipeline. By default, a log group will be created with the format ``/aws/imagebuilder/pipeline/<pipeline-name>`` Default: - a log group will be created
        :param image_pipeline_name: (experimental) The name of the image pipeline. Default: - a name is generated
        :param image_scanning_ecr_repository: (experimental) The container repository that Amazon Inspector scans to identify findings for your container images. If a repository is not provided, Image Builder creates a repository named ``image-builder-image-scanning-repository`` for vulnerability scanning. Default: - if scanning is enabled, a repository will be created by Image Builder if one is not provided
        :param image_scanning_ecr_tags: (experimental) The tags for Image Builder to apply to the output container image that Amazon Inspector scans. Default: None
        :param image_scanning_enabled: (experimental) Indicates whether Image Builder keeps a snapshot of the vulnerability scans that Amazon Inspector runs against the build instance when you create a new image. Default: false
        :param image_tests_enabled: (experimental) Whether to run tests after building an image. Default: true
        :param infrastructure_configuration: (experimental) The infrastructure configuration used for building the image. A default infrastructure configuration will be used if one is not provided. The default configuration will create an instance profile and role with minimal permissions needed to build the image, attached to the EC2 instance. Default: - an infrastructure configuration will be created with the default settings
        :param schedule: (experimental) The schedule of the image pipeline. This configures how often and when a pipeline automatically creates a new image. Default: - none, a manual image pipeline will be created
        :param status: (experimental) Indicates whether the pipeline is enabled to be triggered by the provided schedule. Default: ImagePipelineStatus.ENABLED
        :param tags: (experimental) The tags to apply to the image pipeline. Default: None
        :param workflows: (experimental) The list of workflow configurations used to build the image. Default: - Image Builder will use a default set of workflows for the build to build, test, and distribute the image

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be256ce26470dd7ce99d85d182fed712c84ad063411b79a3fa8356a67e08da0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ImagePipelineProps(
            recipe=recipe,
            description=description,
            distribution_configuration=distribution_configuration,
            enhanced_image_metadata_enabled=enhanced_image_metadata_enabled,
            execution_role=execution_role,
            image_log_group=image_log_group,
            image_pipeline_log_group=image_pipeline_log_group,
            image_pipeline_name=image_pipeline_name,
            image_scanning_ecr_repository=image_scanning_ecr_repository,
            image_scanning_ecr_tags=image_scanning_ecr_tags,
            image_scanning_enabled=image_scanning_enabled,
            image_tests_enabled=image_tests_enabled,
            infrastructure_configuration=infrastructure_configuration,
            schedule=schedule,
            status=status,
            tags=tags,
            workflows=workflows,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromImagePipelineArn")
    @builtins.classmethod
    def from_image_pipeline_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        image_pipeline_arn: builtins.str,
    ) -> IImagePipeline:
        '''(experimental) Import an existing image pipeline given its ARN.

        :param scope: -
        :param id: -
        :param image_pipeline_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8335134c462cc84e1f47b31b9c90894b85ff3b208c66d1c7ad33f21a30dcc75)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_pipeline_arn", value=image_pipeline_arn, expected_type=type_hints["image_pipeline_arn"])
        return typing.cast(IImagePipeline, jsii.sinvoke(cls, "fromImagePipelineArn", [scope, id, image_pipeline_arn]))

    @jsii.member(jsii_name="fromImagePipelineName")
    @builtins.classmethod
    def from_image_pipeline_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        image_pipeline_name: builtins.str,
    ) -> IImagePipeline:
        '''(experimental) Import an existing image pipeline given its name.

        The provided name must be normalized by converting all
        alphabetical characters to lowercase, and replacing all spaces and underscores with hyphens.

        :param scope: -
        :param id: -
        :param image_pipeline_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3cfc55a44581fac1d29db8a08b9e65bcc8a20bfb45aa6a2b1847c1ae51f057)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_pipeline_name", value=image_pipeline_name, expected_type=type_hints["image_pipeline_name"])
        return typing.cast(IImagePipeline, jsii.sinvoke(cls, "fromImagePipelineName", [scope, id, image_pipeline_name]))

    @jsii.member(jsii_name="isImagePipeline")
    @builtins.classmethod
    def is_image_pipeline(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Return whether the given object is an ImagePipeline.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d891818b696c2dd9c1b14607b5b4a1d4836d8d38ee7c1ee23a256b28d8034b5e)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isImagePipeline", [x]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the image pipeline.

        :param grantee: The principal.
        :param actions: The list of actions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5bd77b1c63ad1dc271d0d0ecd4a832c3f5c52bd37a5e803f4725c241fc86af4)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantDefaultExecutionRolePermissions")
    def grant_default_execution_role_permissions(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> typing.List[_aws_cdk_aws_iam_ceddda9d.Grant]:
        '''(experimental) Grants the default permissions for building an image to the provided execution role.

        :param grantee: The execution role used for the image build.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56199255193a2219bb1c8fdd69cf53dcfa094f8133bf9336c26279f6a370af8b)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(typing.List[_aws_cdk_aws_iam_ceddda9d.Grant], jsii.invoke(self, "grantDefaultExecutionRolePermissions", [grantee]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the image pipeline.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29a9687a4f2667c95aa42534de951075cdd9565d2053d0460f71f89f3630bb16)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="grantStartExecution")
    def grant_start_execution(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant permissions to the given grantee to start an execution of the image pipeline.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbe0bb818b71b7f18b19a1dcf3f5addd085a4d3222e3038517cfb3fe2f2c4870)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantStartExecution", [grantee]))

    @jsii.member(jsii_name="onCVEDetected")
    def on_cve_detected(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder CVE detected events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c699424e12fee7bb387a499563fc8d745b1f9960b9fde89c970a085d73f4d6a2)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onCVEDetected", [id, options]))

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd8c06e734f1dfff99b88ca46b23f6ca9d7c17e3c4a92c8840d24b95105307cb)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onEvent", [id, options]))

    @jsii.member(jsii_name="onImageBuildCompleted")
    def on_image_build_completed(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder image build completion events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e7732ef851dae9bf19ad0516fc9c22a37e4b7db10ed679eb6487882d3458ff)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onImageBuildCompleted", [id, options]))

    @jsii.member(jsii_name="onImageBuildFailed")
    def on_image_build_failed(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder image build failure events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__646672c252d0e8b44005b72edac02caf1fec6e450563792904f586b53881c343)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onImageBuildFailed", [id, options]))

    @jsii.member(jsii_name="onImageBuildStateChange")
    def on_image_build_state_change(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder image state change events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fd5f7c6f1fac7bba012ce49a070a25ba21023d4be1497621395602e1fd557a8)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onImageBuildStateChange", [id, options]))

    @jsii.member(jsii_name="onImageBuildSucceeded")
    def on_image_build_succeeded(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder image success events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc825e4f0f338e19e53d39a6529ef7df6b3ffd11090bd2ee19a2bde279c5c885)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onImageBuildSucceeded", [id, options]))

    @jsii.member(jsii_name="onImagePipelineAutoDisabled")
    def on_image_pipeline_auto_disabled(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder image pipeline automatically disabled events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c82aaa4bd4e0bc03d082c6b8ae3dab095fd8ccf0b642493805a37b078c2d399b)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onImagePipelineAutoDisabled", [id, options]))

    @jsii.member(jsii_name="onWaitForAction")
    def on_wait_for_action(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Creates an EventBridge rule for Image Builder wait for action events.

        :param id: Unique identifier for the rule.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/integ-eventbridge.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__313f641cb1f2a65155332a5ecfa65d8620094ba181089054cc5139134f3a5201)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onWaitForAction", [id, options]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="imagePipelineArn")
    def image_pipeline_arn(self) -> builtins.str:
        '''(experimental) The ARN of the image pipeline.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "imagePipelineArn"))

    @builtins.property
    @jsii.member(jsii_name="imagePipelineName")
    def image_pipeline_name(self) -> builtins.str:
        '''(experimental) The name of the image pipeline.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "imagePipelineName"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureConfiguration")
    def infrastructure_configuration(self) -> IInfrastructureConfiguration:
        '''(experimental) The infrastructure configuration used for the image build.

        :stability: experimental
        '''
        return typing.cast(IInfrastructureConfiguration, jsii.get(self, "infrastructureConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The execution role used for the image build.

        If there is no execution role, then the build will be executed with
        the AWSServiceRoleForImageBuilder service-linked role.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "executionRole"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ImagePipelineProps",
    jsii_struct_bases=[],
    name_mapping={
        "recipe": "recipe",
        "description": "description",
        "distribution_configuration": "distributionConfiguration",
        "enhanced_image_metadata_enabled": "enhancedImageMetadataEnabled",
        "execution_role": "executionRole",
        "image_log_group": "imageLogGroup",
        "image_pipeline_log_group": "imagePipelineLogGroup",
        "image_pipeline_name": "imagePipelineName",
        "image_scanning_ecr_repository": "imageScanningEcrRepository",
        "image_scanning_ecr_tags": "imageScanningEcrTags",
        "image_scanning_enabled": "imageScanningEnabled",
        "image_tests_enabled": "imageTestsEnabled",
        "infrastructure_configuration": "infrastructureConfiguration",
        "schedule": "schedule",
        "status": "status",
        "tags": "tags",
        "workflows": "workflows",
    },
)
class ImagePipelineProps:
    def __init__(
        self,
        *,
        recipe: IRecipeBase,
        description: typing.Optional[builtins.str] = None,
        distribution_configuration: typing.Optional[IDistributionConfiguration] = None,
        enhanced_image_metadata_enabled: typing.Optional[builtins.bool] = None,
        execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        image_log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
        image_pipeline_log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
        image_pipeline_name: typing.Optional[builtins.str] = None,
        image_scanning_ecr_repository: typing.Optional[_aws_cdk_aws_ecr_ceddda9d.IRepository] = None,
        image_scanning_ecr_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_scanning_enabled: typing.Optional[builtins.bool] = None,
        image_tests_enabled: typing.Optional[builtins.bool] = None,
        infrastructure_configuration: typing.Optional[IInfrastructureConfiguration] = None,
        schedule: typing.Optional[typing.Union["ImagePipelineSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional["ImagePipelineStatus"] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workflows: typing.Optional[typing.Sequence[typing.Union["WorkflowConfiguration", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Properties for creating an Image Pipeline resource.

        :param recipe: (experimental) The recipe that defines the base image, components, and customizations used to build the image. This can either be an image recipe, or a container recipe.
        :param description: (experimental) The description of the image pipeline. Default: None
        :param distribution_configuration: (experimental) The distribution configuration used for distributing the image. Default: None
        :param enhanced_image_metadata_enabled: (experimental) If enabled, collects additional information about the image being created, including the operating system (OS) version and package list for the AMI. Default: true
        :param execution_role: (experimental) The execution role used to perform workflow actions to build this image. By default, the Image Builder Service Linked Role (SLR) will be created automatically and used as the execution role. However, when providing a custom set of image workflows for the pipeline, an execution role will be generated with the minimal permissions needed to execute the workflows. Default: - Image Builder will use the SLR if possible. Otherwise, an execution role will be generated
        :param image_log_group: (experimental) The log group to use for images created from the image pipeline. By default, a log group will be created with the format ``/aws/imagebuilder/<image-name>``. Default: - a log group will be created
        :param image_pipeline_log_group: (experimental) The log group to use for the image pipeline. By default, a log group will be created with the format ``/aws/imagebuilder/pipeline/<pipeline-name>`` Default: - a log group will be created
        :param image_pipeline_name: (experimental) The name of the image pipeline. Default: - a name is generated
        :param image_scanning_ecr_repository: (experimental) The container repository that Amazon Inspector scans to identify findings for your container images. If a repository is not provided, Image Builder creates a repository named ``image-builder-image-scanning-repository`` for vulnerability scanning. Default: - if scanning is enabled, a repository will be created by Image Builder if one is not provided
        :param image_scanning_ecr_tags: (experimental) The tags for Image Builder to apply to the output container image that Amazon Inspector scans. Default: None
        :param image_scanning_enabled: (experimental) Indicates whether Image Builder keeps a snapshot of the vulnerability scans that Amazon Inspector runs against the build instance when you create a new image. Default: false
        :param image_tests_enabled: (experimental) Whether to run tests after building an image. Default: true
        :param infrastructure_configuration: (experimental) The infrastructure configuration used for building the image. A default infrastructure configuration will be used if one is not provided. The default configuration will create an instance profile and role with minimal permissions needed to build the image, attached to the EC2 instance. Default: - an infrastructure configuration will be created with the default settings
        :param schedule: (experimental) The schedule of the image pipeline. This configures how often and when a pipeline automatically creates a new image. Default: - none, a manual image pipeline will be created
        :param status: (experimental) Indicates whether the pipeline is enabled to be triggered by the provided schedule. Default: ImagePipelineStatus.ENABLED
        :param tags: (experimental) The tags to apply to the image pipeline. Default: None
        :param workflows: (experimental) The list of workflow configurations used to build the image. Default: - Image Builder will use a default set of workflows for the build to build, test, and distribute the image

        :stability: experimental
        :exampleMetadata: infused

        Example::

            workflow_pipeline = imagebuilder.ImagePipeline(self, "WorkflowPipeline",
                recipe=example_image_recipe,
                workflows=[imagebuilder.WorkflowConfiguration(workflow=imagebuilder.AwsManagedWorkflow.build_image(self, "BuildWorkflow")), imagebuilder.WorkflowConfiguration(workflow=imagebuilder.AwsManagedWorkflow.test_image(self, "TestWorkflow"))
                ]
            )
        '''
        if isinstance(schedule, dict):
            schedule = ImagePipelineSchedule(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef9e2b7ca1149caaaa96b4d3f527cb5b23241d30446acf045fcacf461e8c08a3)
            check_type(argname="argument recipe", value=recipe, expected_type=type_hints["recipe"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument distribution_configuration", value=distribution_configuration, expected_type=type_hints["distribution_configuration"])
            check_type(argname="argument enhanced_image_metadata_enabled", value=enhanced_image_metadata_enabled, expected_type=type_hints["enhanced_image_metadata_enabled"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument image_log_group", value=image_log_group, expected_type=type_hints["image_log_group"])
            check_type(argname="argument image_pipeline_log_group", value=image_pipeline_log_group, expected_type=type_hints["image_pipeline_log_group"])
            check_type(argname="argument image_pipeline_name", value=image_pipeline_name, expected_type=type_hints["image_pipeline_name"])
            check_type(argname="argument image_scanning_ecr_repository", value=image_scanning_ecr_repository, expected_type=type_hints["image_scanning_ecr_repository"])
            check_type(argname="argument image_scanning_ecr_tags", value=image_scanning_ecr_tags, expected_type=type_hints["image_scanning_ecr_tags"])
            check_type(argname="argument image_scanning_enabled", value=image_scanning_enabled, expected_type=type_hints["image_scanning_enabled"])
            check_type(argname="argument image_tests_enabled", value=image_tests_enabled, expected_type=type_hints["image_tests_enabled"])
            check_type(argname="argument infrastructure_configuration", value=infrastructure_configuration, expected_type=type_hints["infrastructure_configuration"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workflows", value=workflows, expected_type=type_hints["workflows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "recipe": recipe,
        }
        if description is not None:
            self._values["description"] = description
        if distribution_configuration is not None:
            self._values["distribution_configuration"] = distribution_configuration
        if enhanced_image_metadata_enabled is not None:
            self._values["enhanced_image_metadata_enabled"] = enhanced_image_metadata_enabled
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if image_log_group is not None:
            self._values["image_log_group"] = image_log_group
        if image_pipeline_log_group is not None:
            self._values["image_pipeline_log_group"] = image_pipeline_log_group
        if image_pipeline_name is not None:
            self._values["image_pipeline_name"] = image_pipeline_name
        if image_scanning_ecr_repository is not None:
            self._values["image_scanning_ecr_repository"] = image_scanning_ecr_repository
        if image_scanning_ecr_tags is not None:
            self._values["image_scanning_ecr_tags"] = image_scanning_ecr_tags
        if image_scanning_enabled is not None:
            self._values["image_scanning_enabled"] = image_scanning_enabled
        if image_tests_enabled is not None:
            self._values["image_tests_enabled"] = image_tests_enabled
        if infrastructure_configuration is not None:
            self._values["infrastructure_configuration"] = infrastructure_configuration
        if schedule is not None:
            self._values["schedule"] = schedule
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags
        if workflows is not None:
            self._values["workflows"] = workflows

    @builtins.property
    def recipe(self) -> IRecipeBase:
        '''(experimental) The recipe that defines the base image, components, and customizations used to build the image.

        This can either be
        an image recipe, or a container recipe.

        :stability: experimental
        '''
        result = self._values.get("recipe")
        assert result is not None, "Required property 'recipe' is missing"
        return typing.cast(IRecipeBase, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the image pipeline.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def distribution_configuration(self) -> typing.Optional[IDistributionConfiguration]:
        '''(experimental) The distribution configuration used for distributing the image.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("distribution_configuration")
        return typing.cast(typing.Optional[IDistributionConfiguration], result)

    @builtins.property
    def enhanced_image_metadata_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If enabled, collects additional information about the image being created, including the operating system (OS) version and package list for the AMI.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enhanced_image_metadata_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The execution role used to perform workflow actions to build this image.

        By default, the Image Builder Service Linked Role (SLR) will be created automatically and used as the execution
        role. However, when providing a custom set of image workflows for the pipeline, an execution role will be
        generated with the minimal permissions needed to execute the workflows.

        :default: - Image Builder will use the SLR if possible. Otherwise, an execution role will be generated

        :stability: experimental
        '''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def image_log_group(self) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup]:
        '''(experimental) The log group to use for images created from the image pipeline.

        By default, a log group will be created with the
        format ``/aws/imagebuilder/<image-name>``.

        :default: - a log group will be created

        :stability: experimental
        '''
        result = self._values.get("image_log_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup], result)

    @builtins.property
    def image_pipeline_log_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup]:
        '''(experimental) The log group to use for the image pipeline.

        By default, a log group will be created with the format
        ``/aws/imagebuilder/pipeline/<pipeline-name>``

        :default: - a log group will be created

        :stability: experimental
        '''
        result = self._values.get("image_pipeline_log_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup], result)

    @builtins.property
    def image_pipeline_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the image pipeline.

        :default: - a name is generated

        :stability: experimental
        '''
        result = self._values.get("image_pipeline_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_scanning_ecr_repository(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecr_ceddda9d.IRepository]:
        '''(experimental) The container repository that Amazon Inspector scans to identify findings for your container images.

        If a
        repository is not provided, Image Builder creates a repository named ``image-builder-image-scanning-repository``
        for vulnerability scanning.

        :default: - if scanning is enabled, a repository will be created by Image Builder if one is not provided

        :stability: experimental
        '''
        result = self._values.get("image_scanning_ecr_repository")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecr_ceddda9d.IRepository], result)

    @builtins.property
    def image_scanning_ecr_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The tags for Image Builder to apply to the output container image that Amazon Inspector scans.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("image_scanning_ecr_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def image_scanning_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether Image Builder keeps a snapshot of the vulnerability scans that Amazon Inspector runs against the build instance when you create a new image.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("image_scanning_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def image_tests_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to run tests after building an image.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("image_tests_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def infrastructure_configuration(
        self,
    ) -> typing.Optional[IInfrastructureConfiguration]:
        '''(experimental) The infrastructure configuration used for building the image.

        A default infrastructure configuration will be used if one is not provided.

        The default configuration will create an instance profile and role with minimal permissions needed to build the
        image, attached to the EC2 instance.

        :default: - an infrastructure configuration will be created with the default settings

        :stability: experimental
        '''
        result = self._values.get("infrastructure_configuration")
        return typing.cast(typing.Optional[IInfrastructureConfiguration], result)

    @builtins.property
    def schedule(self) -> typing.Optional["ImagePipelineSchedule"]:
        '''(experimental) The schedule of the image pipeline.

        This configures how often and when a pipeline automatically creates a new
        image.

        :default: - none, a manual image pipeline will be created

        :stability: experimental
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["ImagePipelineSchedule"], result)

    @builtins.property
    def status(self) -> typing.Optional["ImagePipelineStatus"]:
        '''(experimental) Indicates whether the pipeline is enabled to be triggered by the provided schedule.

        :default: ImagePipelineStatus.ENABLED

        :stability: experimental
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional["ImagePipelineStatus"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The tags to apply to the image pipeline.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def workflows(self) -> typing.Optional[typing.List["WorkflowConfiguration"]]:
        '''(experimental) The list of workflow configurations used to build the image.

        :default: - Image Builder will use a default set of workflows for the build to build, test, and distribute the image

        :stability: experimental
        '''
        result = self._values.get("workflows")
        return typing.cast(typing.Optional[typing.List["WorkflowConfiguration"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagePipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ImagePipelineSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "auto_disable_failure_count": "autoDisableFailureCount",
        "start_condition": "startCondition",
    },
)
class ImagePipelineSchedule:
    def __init__(
        self,
        *,
        expression: _aws_cdk_aws_events_ceddda9d.Schedule,
        auto_disable_failure_count: typing.Optional[jsii.Number] = None,
        start_condition: typing.Optional["ScheduleStartCondition"] = None,
    ) -> None:
        '''(experimental) The schedule settings for the image pipeline, which defines when a pipeline should be triggered.

        :param expression: (experimental) The schedule expression to use. This can either be a cron expression or a rate expression.
        :param auto_disable_failure_count: (experimental) The number of consecutive failures allowed before the pipeline is automatically disabled. This value must be between 1 and 10. Default: - no auto-disable policy is configured and the pipeline is not automatically disabled on consecutive failures
        :param start_condition: (experimental) The start condition for the pipeline, indicating the condition under which a pipeline should be triggered. Default: ScheduleStartCondition.EXPRESSION_MATCH_AND_DEPENDENCY_UPDATES_AVAILABLE

        :stability: experimental
        :exampleMetadata: infused

        Example::

            daily_pipeline = imagebuilder.ImagePipeline(self, "DailyPipeline",
                recipe=example_container_recipe,
                schedule=imagebuilder.ImagePipelineSchedule(
                    expression=events.Schedule.rate(Duration.days(1))
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d90009cac3814f6853f63afe41943fed9768ffe8575410bb897f8d1fb491877)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument auto_disable_failure_count", value=auto_disable_failure_count, expected_type=type_hints["auto_disable_failure_count"])
            check_type(argname="argument start_condition", value=start_condition, expected_type=type_hints["start_condition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }
        if auto_disable_failure_count is not None:
            self._values["auto_disable_failure_count"] = auto_disable_failure_count
        if start_condition is not None:
            self._values["start_condition"] = start_condition

    @builtins.property
    def expression(self) -> _aws_cdk_aws_events_ceddda9d.Schedule:
        '''(experimental) The schedule expression to use.

        This can either be a cron expression or a rate expression.

        :stability: experimental
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(_aws_cdk_aws_events_ceddda9d.Schedule, result)

    @builtins.property
    def auto_disable_failure_count(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of consecutive failures allowed before the pipeline is automatically disabled.

        This value must be
        between 1 and 10.

        :default:

        - no auto-disable policy is configured and the pipeline is not automatically disabled on consecutive
        failures

        :stability: experimental
        '''
        result = self._values.get("auto_disable_failure_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_condition(self) -> typing.Optional["ScheduleStartCondition"]:
        '''(experimental) The start condition for the pipeline, indicating the condition under which a pipeline should be triggered.

        :default: ScheduleStartCondition.EXPRESSION_MATCH_AND_DEPENDENCY_UPDATES_AVAILABLE

        :stability: experimental
        '''
        result = self._values.get("start_condition")
        return typing.cast(typing.Optional["ScheduleStartCondition"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagePipelineSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.ImagePipelineStatus")
class ImagePipelineStatus(enum.Enum):
    '''(experimental) Indicates whether the pipeline is enabled to be triggered by the provided schedule.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        advanced_schedule_pipeline = imagebuilder.ImagePipeline(self, "AdvancedSchedulePipeline",
            recipe=example_image_recipe,
            schedule=imagebuilder.ImagePipelineSchedule(
                expression=events.Schedule.rate(Duration.days(7)),
                # Only trigger when dependencies are updated (new base images, components, etc.)
                start_condition=imagebuilder.ScheduleStartCondition.EXPRESSION_MATCH_AND_DEPENDENCY_UPDATES_AVAILABLE,
                # Automatically disable after 3 consecutive failures
                auto_disable_failure_count=3
            ),
            # Start enabled
            status=imagebuilder.ImagePipelineStatus.ENABLED
        )
    '''

    ENABLED = "ENABLED"
    '''(experimental) Indicates that the pipeline is enabled for scheduling.

    :stability: experimental
    '''
    DISABLED = "DISABLED"
    '''(experimental) Indicates that the pipeline is disabled and will not be triggered on the schedule.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ImageProps",
    jsii_struct_bases=[],
    name_mapping={
        "recipe": "recipe",
        "deletion_execution_role": "deletionExecutionRole",
        "distribution_configuration": "distributionConfiguration",
        "enhanced_image_metadata_enabled": "enhancedImageMetadataEnabled",
        "execution_role": "executionRole",
        "image_scanning_ecr_repository": "imageScanningEcrRepository",
        "image_scanning_ecr_tags": "imageScanningEcrTags",
        "image_scanning_enabled": "imageScanningEnabled",
        "image_tests_enabled": "imageTestsEnabled",
        "infrastructure_configuration": "infrastructureConfiguration",
        "log_group": "logGroup",
        "tags": "tags",
        "workflows": "workflows",
    },
)
class ImageProps:
    def __init__(
        self,
        *,
        recipe: IRecipeBase,
        deletion_execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        distribution_configuration: typing.Optional[IDistributionConfiguration] = None,
        enhanced_image_metadata_enabled: typing.Optional[builtins.bool] = None,
        execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        image_scanning_ecr_repository: typing.Optional[_aws_cdk_aws_ecr_ceddda9d.IRepository] = None,
        image_scanning_ecr_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_scanning_enabled: typing.Optional[builtins.bool] = None,
        image_tests_enabled: typing.Optional[builtins.bool] = None,
        infrastructure_configuration: typing.Optional[IInfrastructureConfiguration] = None,
        log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workflows: typing.Optional[typing.Sequence[typing.Union["WorkflowConfiguration", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Properties for creating an Image resource.

        :param recipe: (experimental) The recipe that defines the base image, components, and customizations used to build the image. This can either be an image recipe, or a container recipe.
        :param deletion_execution_role: (experimental) The execution role to use for deleting the image as well as the underlying resources, such as the AMIs, snapshots, and containers. This role should contain resource lifecycle permissions required to delete the underlying AMIs/containers. Default: - no execution role. Only the Image Builder image will be deleted.
        :param distribution_configuration: (experimental) The distribution configuration used for distributing the image. Default: None
        :param enhanced_image_metadata_enabled: (experimental) If enabled, collects additional information about the image being created, including the operating system (OS) version and package list for the AMI. Default: true
        :param execution_role: (experimental) The execution role used to perform workflow actions to build the image. By default, the Image Builder Service Linked Role (SLR) will be created automatically and used as the execution role. However, when providing a custom set of image workflows for the image, an execution role will be generated with the minimal permissions needed to execute the workflows. Default: - Image Builder will use the SLR if possible. Otherwise, an execution role will be generated
        :param image_scanning_ecr_repository: (experimental) The container repository that Amazon Inspector scans to identify findings for your container images. If a repository is not provided, Image Builder creates a repository named ``image-builder-image-scanning-repository`` for vulnerability scanning. Default: - if scanning is enabled, a repository will be created by Image Builder if one is not provided
        :param image_scanning_ecr_tags: (experimental) The tags for Image Builder to apply to the output container image that Amazon Inspector scans. Default: None
        :param image_scanning_enabled: (experimental) Indicates whether Image Builder keeps a snapshot of the vulnerability scans that Amazon Inspector runs against the build instance when you create a new image. Default: false
        :param image_tests_enabled: (experimental) Whether to run tests after building an image. Default: true
        :param infrastructure_configuration: (experimental) The infrastructure configuration used for building the image. A default infrastructure configuration will be used if one is not provided. The default configuration will create an instance profile and role with minimal permissions needed to build the image, attached to the EC2 instance. IMDSv2 will be required by default on the instances used to build and test the image. Default: - an infrastructure configuration will be created with the default settings
        :param log_group: (experimental) The log group to use for the image. By default, a log group will be created with the format ``/aws/imagebuilder/<image-name>`` Default: - a log group will be created
        :param tags: (experimental) The tags to apply to the image. Default: None
        :param workflows: (experimental) The list of workflow configurations used to build the image. Default: - Image Builder will use a default set of workflows for the build to build, test, and distribute the image

        :stability: experimental
        :exampleMetadata: infused

        Example::

            container_recipe = imagebuilder.ContainerRecipe(self, "MyContainerRecipe",
                base_image=imagebuilder.BaseContainerImage.from_docker_hub("amazonlinux", "latest"),
                target_repository=imagebuilder.Repository.from_ecr(
                    ecr.Repository.from_repository_name(self, "Repository", "my-container-repo"))
            )
            
            container_image = imagebuilder.Image(self, "MyContainerImage",
                recipe=container_recipe
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7a30a589b05ea8fe5afc9710649c4fb14c5b638999f1db9faa746a058ab1e4f)
            check_type(argname="argument recipe", value=recipe, expected_type=type_hints["recipe"])
            check_type(argname="argument deletion_execution_role", value=deletion_execution_role, expected_type=type_hints["deletion_execution_role"])
            check_type(argname="argument distribution_configuration", value=distribution_configuration, expected_type=type_hints["distribution_configuration"])
            check_type(argname="argument enhanced_image_metadata_enabled", value=enhanced_image_metadata_enabled, expected_type=type_hints["enhanced_image_metadata_enabled"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument image_scanning_ecr_repository", value=image_scanning_ecr_repository, expected_type=type_hints["image_scanning_ecr_repository"])
            check_type(argname="argument image_scanning_ecr_tags", value=image_scanning_ecr_tags, expected_type=type_hints["image_scanning_ecr_tags"])
            check_type(argname="argument image_scanning_enabled", value=image_scanning_enabled, expected_type=type_hints["image_scanning_enabled"])
            check_type(argname="argument image_tests_enabled", value=image_tests_enabled, expected_type=type_hints["image_tests_enabled"])
            check_type(argname="argument infrastructure_configuration", value=infrastructure_configuration, expected_type=type_hints["infrastructure_configuration"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workflows", value=workflows, expected_type=type_hints["workflows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "recipe": recipe,
        }
        if deletion_execution_role is not None:
            self._values["deletion_execution_role"] = deletion_execution_role
        if distribution_configuration is not None:
            self._values["distribution_configuration"] = distribution_configuration
        if enhanced_image_metadata_enabled is not None:
            self._values["enhanced_image_metadata_enabled"] = enhanced_image_metadata_enabled
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if image_scanning_ecr_repository is not None:
            self._values["image_scanning_ecr_repository"] = image_scanning_ecr_repository
        if image_scanning_ecr_tags is not None:
            self._values["image_scanning_ecr_tags"] = image_scanning_ecr_tags
        if image_scanning_enabled is not None:
            self._values["image_scanning_enabled"] = image_scanning_enabled
        if image_tests_enabled is not None:
            self._values["image_tests_enabled"] = image_tests_enabled
        if infrastructure_configuration is not None:
            self._values["infrastructure_configuration"] = infrastructure_configuration
        if log_group is not None:
            self._values["log_group"] = log_group
        if tags is not None:
            self._values["tags"] = tags
        if workflows is not None:
            self._values["workflows"] = workflows

    @builtins.property
    def recipe(self) -> IRecipeBase:
        '''(experimental) The recipe that defines the base image, components, and customizations used to build the image.

        This can either be
        an image recipe, or a container recipe.

        :stability: experimental
        '''
        result = self._values.get("recipe")
        assert result is not None, "Required property 'recipe' is missing"
        return typing.cast(IRecipeBase, result)

    @builtins.property
    def deletion_execution_role(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The execution role to use for deleting the image as well as the underlying resources, such as the AMIs, snapshots, and containers.

        This role should contain resource lifecycle permissions required to delete the underlying
        AMIs/containers.

        :default: - no execution role. Only the Image Builder image will be deleted.

        :stability: experimental
        '''
        result = self._values.get("deletion_execution_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def distribution_configuration(self) -> typing.Optional[IDistributionConfiguration]:
        '''(experimental) The distribution configuration used for distributing the image.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("distribution_configuration")
        return typing.cast(typing.Optional[IDistributionConfiguration], result)

    @builtins.property
    def enhanced_image_metadata_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If enabled, collects additional information about the image being created, including the operating system (OS) version and package list for the AMI.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enhanced_image_metadata_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The execution role used to perform workflow actions to build the image.

        By default, the Image Builder Service Linked Role (SLR) will be created automatically and used as the execution
        role. However, when providing a custom set of image workflows for the image, an execution role will be
        generated with the minimal permissions needed to execute the workflows.

        :default: - Image Builder will use the SLR if possible. Otherwise, an execution role will be generated

        :stability: experimental
        '''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def image_scanning_ecr_repository(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecr_ceddda9d.IRepository]:
        '''(experimental) The container repository that Amazon Inspector scans to identify findings for your container images.

        If a
        repository is not provided, Image Builder creates a repository named ``image-builder-image-scanning-repository``
        for vulnerability scanning.

        :default: - if scanning is enabled, a repository will be created by Image Builder if one is not provided

        :stability: experimental
        '''
        result = self._values.get("image_scanning_ecr_repository")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecr_ceddda9d.IRepository], result)

    @builtins.property
    def image_scanning_ecr_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The tags for Image Builder to apply to the output container image that Amazon Inspector scans.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("image_scanning_ecr_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def image_scanning_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether Image Builder keeps a snapshot of the vulnerability scans that Amazon Inspector runs against the build instance when you create a new image.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("image_scanning_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def image_tests_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to run tests after building an image.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("image_tests_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def infrastructure_configuration(
        self,
    ) -> typing.Optional[IInfrastructureConfiguration]:
        '''(experimental) The infrastructure configuration used for building the image.

        A default infrastructure configuration will be used if one is not provided.

        The default configuration will create an instance profile and role with minimal permissions needed to build the
        image, attached to the EC2 instance.

        IMDSv2 will be required by default on the instances used to build and test the image.

        :default: - an infrastructure configuration will be created with the default settings

        :stability: experimental
        '''
        result = self._values.get("infrastructure_configuration")
        return typing.cast(typing.Optional[IInfrastructureConfiguration], result)

    @builtins.property
    def log_group(self) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup]:
        '''(experimental) The log group to use for the image.

        By default, a log group will be created with the format
        ``/aws/imagebuilder/<image-name>``

        :default: - a log group will be created

        :stability: experimental
        '''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The tags to apply to the image.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def workflows(self) -> typing.Optional[typing.List["WorkflowConfiguration"]]:
        '''(experimental) The list of workflow configurations used to build the image.

        :default:

        - Image Builder will use a default set of workflows for the build to build, test, and distribute the
        image

        :stability: experimental
        '''
        result = self._values.get("workflows")
        return typing.cast(typing.Optional[typing.List["WorkflowConfiguration"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ImageRecipeAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "image_recipe_arn": "imageRecipeArn",
        "image_recipe_name": "imageRecipeName",
        "image_recipe_version": "imageRecipeVersion",
    },
)
class ImageRecipeAttributes:
    def __init__(
        self,
        *,
        image_recipe_arn: typing.Optional[builtins.str] = None,
        image_recipe_name: typing.Optional[builtins.str] = None,
        image_recipe_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for an EC2 Image Builder image recipe.

        :param image_recipe_arn: (experimental) The ARN of the image recipe. Default: - derived from the imageRecipeName
        :param image_recipe_name: (experimental) The name of the image recipe. Default: - derived from the imageRecipeArn
        :param image_recipe_version: (experimental) The version of the image recipe. Default: - derived from imageRecipeArn. if a imageRecipeName is provided, the latest version, x.x.x, will be used

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
            
            image_recipe_attributes = imagebuilder_alpha.ImageRecipeAttributes(
                image_recipe_arn="imageRecipeArn",
                image_recipe_name="imageRecipeName",
                image_recipe_version="imageRecipeVersion"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25d6cb317a11ae5d32daa6a7eebcee461a9487b2855e894be98b6c1cddc9add0)
            check_type(argname="argument image_recipe_arn", value=image_recipe_arn, expected_type=type_hints["image_recipe_arn"])
            check_type(argname="argument image_recipe_name", value=image_recipe_name, expected_type=type_hints["image_recipe_name"])
            check_type(argname="argument image_recipe_version", value=image_recipe_version, expected_type=type_hints["image_recipe_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if image_recipe_arn is not None:
            self._values["image_recipe_arn"] = image_recipe_arn
        if image_recipe_name is not None:
            self._values["image_recipe_name"] = image_recipe_name
        if image_recipe_version is not None:
            self._values["image_recipe_version"] = image_recipe_version

    @builtins.property
    def image_recipe_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the image recipe.

        :default: - derived from the imageRecipeName

        :stability: experimental
        '''
        result = self._values.get("image_recipe_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_recipe_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the image recipe.

        :default: - derived from the imageRecipeArn

        :stability: experimental
        '''
        result = self._values.get("image_recipe_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_recipe_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the image recipe.

        :default:

        - derived from imageRecipeArn. if a imageRecipeName is provided, the latest version, x.x.x, will
        be used

        :stability: experimental
        '''
        result = self._values.get("image_recipe_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageRecipeAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ImageRecipeProps",
    jsii_struct_bases=[],
    name_mapping={
        "base_image": "baseImage",
        "ami_tags": "amiTags",
        "block_devices": "blockDevices",
        "components": "components",
        "description": "description",
        "image_recipe_name": "imageRecipeName",
        "image_recipe_version": "imageRecipeVersion",
        "tags": "tags",
        "uninstall_ssm_agent_after_build": "uninstallSsmAgentAfterBuild",
        "user_data_override": "userDataOverride",
        "working_directory": "workingDirectory",
    },
)
class ImageRecipeProps:
    def __init__(
        self,
        *,
        base_image: BaseImage,
        ami_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
        components: typing.Optional[typing.Sequence[typing.Union[ComponentConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        image_recipe_name: typing.Optional[builtins.str] = None,
        image_recipe_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        uninstall_ssm_agent_after_build: typing.Optional[builtins.bool] = None,
        user_data_override: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for creating an Image Recipe resource.

        :param base_image: (experimental) The base image for customizations specified in the image recipe.
        :param ami_tags: (experimental) The additional tags to assign to the output AMI generated by the build. Default: None
        :param block_devices: (experimental) The block devices to attach to the instance used for building the image. Default: None
        :param components: (experimental) The list of component configurations to apply in the image build. Default: None
        :param description: (experimental) The description of the image recipe. Default: None
        :param image_recipe_name: (experimental) The name of the image recipe. Default: - a name is generated
        :param image_recipe_version: (experimental) The version of the image recipe. Default: 1.0.x
        :param tags: (experimental) The tags to apply to the image recipe. Default: None
        :param uninstall_ssm_agent_after_build: (experimental) Whether to uninstall the Systems Manager agent from your final build image, prior to creating the new AMI. Default: - this is false if the Systems Manager agent is pre-installed on the base image. Otherwise, this is true.
        :param user_data_override: (experimental) The user data commands to pass to Image Builder build and test EC2 instances. For Linux and macOS, Image Builder uses a default user data script to install the Systems Manager agent. If you override the user data, you must ensure to add commands to install Systems Manager agent, if it is not pre-installed on your base image. Default: None
        :param working_directory: (experimental) The working directory for use during build and test workflows. Default: - the Image Builder default working directory is used. For Linux and macOS builds, this would be /tmp. For Windows builds, this would be C:/

        :stability: experimental
        :exampleMetadata: infused

        Example::

            parameterized_component = imagebuilder.Component.from_component_name(self, "ParameterizedComponent", "my-parameterized-component")
            
            image_recipe = imagebuilder.ImageRecipe(self, "ParameterizedImageRecipe",
                base_image=imagebuilder.BaseImage.from_ssm_parameter_name("/aws/service/ami-amazon-linux-latest/al2023-ami-minimal-kernel-default-x86_64"),
                components=[imagebuilder.ComponentConfiguration(
                    component=parameterized_component,
                    parameters={
                        "environment": imagebuilder.ComponentParameterValue.from_string("production"),
                        "version": imagebuilder.ComponentParameterValue.from_string("1.0.0")
                    }
                )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ba5b495abe1897e0704d43888c87d03025aec08e1d07a8acc0ce089932c6a6)
            check_type(argname="argument base_image", value=base_image, expected_type=type_hints["base_image"])
            check_type(argname="argument ami_tags", value=ami_tags, expected_type=type_hints["ami_tags"])
            check_type(argname="argument block_devices", value=block_devices, expected_type=type_hints["block_devices"])
            check_type(argname="argument components", value=components, expected_type=type_hints["components"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument image_recipe_name", value=image_recipe_name, expected_type=type_hints["image_recipe_name"])
            check_type(argname="argument image_recipe_version", value=image_recipe_version, expected_type=type_hints["image_recipe_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument uninstall_ssm_agent_after_build", value=uninstall_ssm_agent_after_build, expected_type=type_hints["uninstall_ssm_agent_after_build"])
            check_type(argname="argument user_data_override", value=user_data_override, expected_type=type_hints["user_data_override"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "base_image": base_image,
        }
        if ami_tags is not None:
            self._values["ami_tags"] = ami_tags
        if block_devices is not None:
            self._values["block_devices"] = block_devices
        if components is not None:
            self._values["components"] = components
        if description is not None:
            self._values["description"] = description
        if image_recipe_name is not None:
            self._values["image_recipe_name"] = image_recipe_name
        if image_recipe_version is not None:
            self._values["image_recipe_version"] = image_recipe_version
        if tags is not None:
            self._values["tags"] = tags
        if uninstall_ssm_agent_after_build is not None:
            self._values["uninstall_ssm_agent_after_build"] = uninstall_ssm_agent_after_build
        if user_data_override is not None:
            self._values["user_data_override"] = user_data_override
        if working_directory is not None:
            self._values["working_directory"] = working_directory

    @builtins.property
    def base_image(self) -> BaseImage:
        '''(experimental) The base image for customizations specified in the image recipe.

        :stability: experimental
        '''
        result = self._values.get("base_image")
        assert result is not None, "Required property 'base_image' is missing"
        return typing.cast(BaseImage, result)

    @builtins.property
    def ami_tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The additional tags to assign to the output AMI generated by the build.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("ami_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def block_devices(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.BlockDevice]]:
        '''(experimental) The block devices to attach to the instance used for building the image.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("block_devices")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.BlockDevice]], result)

    @builtins.property
    def components(self) -> typing.Optional[typing.List[ComponentConfiguration]]:
        '''(experimental) The list of component configurations to apply in the image build.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("components")
        return typing.cast(typing.Optional[typing.List[ComponentConfiguration]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the image recipe.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_recipe_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the image recipe.

        :default: - a name is generated

        :stability: experimental
        '''
        result = self._values.get("image_recipe_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_recipe_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the image recipe.

        :default: 1.0.x

        :stability: experimental
        '''
        result = self._values.get("image_recipe_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The tags to apply to the image recipe.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def uninstall_ssm_agent_after_build(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to uninstall the Systems Manager agent from your final build image, prior to creating the new AMI.

        :default: - this is false if the Systems Manager agent is pre-installed on the base image. Otherwise, this is true.

        :stability: experimental
        '''
        result = self._values.get("uninstall_ssm_agent_after_build")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def user_data_override(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData]:
        '''(experimental) The user data commands to pass to Image Builder build and test EC2 instances.

        For Linux and macOS, Image Builder
        uses a default user data script to install the Systems Manager agent. If you override the user data, you must
        ensure to add commands to install Systems Manager agent, if it is not pre-installed on your base image.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("user_data_override")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) The working directory for use during build and test workflows.

        :default:

        - the Image Builder default working directory is used. For Linux and macOS builds, this would be /tmp. For
        Windows builds, this would be C:/

        :stability: experimental
        '''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageRecipeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.ImageType")
class ImageType(enum.Enum):
    '''(experimental) The type of the image.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Amazon Linux 2023 AMI for x86_64
        amazon_linux2023_ami = imagebuilder.AmazonManagedImage.amazon_linux2023(self, "AmazonLinux2023",
            image_type=imagebuilder.ImageType.AMI,
            image_architecture=imagebuilder.ImageArchitecture.X86_64
        )
        
        # Ubuntu 22.04 AMI for ARM64
        ubuntu2204_ami = imagebuilder.AmazonManagedImage.ubuntu_server2204(self, "Ubuntu2204",
            image_type=imagebuilder.ImageType.AMI,
            image_architecture=imagebuilder.ImageArchitecture.ARM64
        )
        
        # Windows Server 2022 Full AMI
        windows2022_ami = imagebuilder.AmazonManagedImage.windows_server2022_full(self, "Windows2022",
            image_type=imagebuilder.ImageType.AMI,
            image_architecture=imagebuilder.ImageArchitecture.X86_64
        )
        
        # Use as base image in recipe
        managed_image_recipe = imagebuilder.ImageRecipe(self, "ManagedImageRecipe",
            base_image=amazon_linux2023_ami.to_base_image()
        )
    '''

    AMI = "AMI"
    '''(experimental) Indicates the image produced is an AMI.

    :stability: experimental
    '''
    DOCKER = "DOCKER"
    '''(experimental) Indicates the image produced is a Docker image.

    :stability: experimental
    '''


@jsii.implements(IInfrastructureConfiguration)
class InfrastructureConfiguration(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.InfrastructureConfiguration",
):
    '''(experimental) Represents an EC2 Image Builder Infrastructure Configuration.

    :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/manage-infra-config.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        infrastructure_configuration = imagebuilder.InfrastructureConfiguration(self, "Infrastructure",
            infrastructure_configuration_name="production-infrastructure",
            instance_types=[
                ec2.InstanceType.of(ec2.InstanceClass.COMPUTE7_INTEL, ec2.InstanceSize.LARGE)
            ],
            vpc=vpc,
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
        )
        
        distribution_configuration = imagebuilder.DistributionConfiguration(self, "Distribution")
        distribution_configuration.add_ami_distributions(
            ami_name="production-ami-{{ imagebuilder:buildDate }}",
            ami_target_account_ids=["123456789012", "098765432109"]
        )
        
        production_pipeline = imagebuilder.ImagePipeline(self, "ProductionPipeline",
            recipe=example_image_recipe,
            infrastructure_configuration=infrastructure_configuration,
            distribution_configuration=distribution_configuration
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        ec2_instance_availability_zone: typing.Optional[builtins.str] = None,
        ec2_instance_host_id: typing.Optional[builtins.str] = None,
        ec2_instance_host_resource_group_arn: typing.Optional[builtins.str] = None,
        ec2_instance_tenancy: typing.Optional["Tenancy"] = None,
        http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
        http_tokens: typing.Optional[HttpTokens] = None,
        infrastructure_configuration_name: typing.Optional[builtins.str] = None,
        instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IInstanceProfile] = None,
        instance_types: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceType]] = None,
        key_pair: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IKeyPair] = None,
        logging: typing.Optional[typing.Union["InfrastructureConfigurationLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        notification_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
        resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        terminate_instance_on_failure: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param description: (experimental) The description of the infrastructure configuration. Default: None
        :param ec2_instance_availability_zone: (experimental) The availability zone to place Image Builder build and test EC2 instances. Default: EC2 will select a random zone
        :param ec2_instance_host_id: (experimental) The ID of the Dedicated Host on which build and test instances run. This only applies if the instance tenancy is ``host``. This cannot be used with the ``ec2InstanceHostResourceGroupArn`` parameter. Default: None
        :param ec2_instance_host_resource_group_arn: (experimental) The ARN of the host resource group on which build and test instances run. This only applies if the instance tenancy is ``host``. This cannot be used with the ``ec2InstanceHostId`` parameter. Default: None
        :param ec2_instance_tenancy: (experimental) The tenancy of the instance. Dedicated tenancy runs instances on single-tenant hardware, while host tenancy runs instances on a dedicated host. Shared tenancy is used by default. Default: Tenancy.DEFAULT
        :param http_put_response_hop_limit: (experimental) The maximum number of hops that an instance metadata request can traverse to reach its destination. By default, this is set to 2. Default: 2
        :param http_tokens: (experimental) Indicates whether a signed token header is required for instance metadata retrieval requests. By default, this is set to ``required`` to require IMDSv2 on build and test EC2 instances. Default: HttpTokens.REQUIRED
        :param infrastructure_configuration_name: (experimental) The name of the infrastructure configuration. This name must be normalized by transforming all alphabetical characters to lowercase, and replacing all spaces and underscores with hyphens. Default: A name is generated
        :param instance_profile: (experimental) The instance profile to associate with the instance used to customize the AMI. By default, an instance profile and role will be created with minimal permissions needed to build the image, attached to the EC2 instance. If an S3 logging bucket and key prefix is provided, an IAM inline policy will be attached to the instance profile's role, allowing s3:PutObject permissions on the bucket. Default: An instance profile will be generated
        :param instance_types: (experimental) The instance types to launch build and test EC2 instances with. Default: Image Builder will choose from a default set of instance types compatible with the AMI
        :param key_pair: (experimental) The key pair used to connect to the build and test EC2 instances. The key pair can be used to log into the build or test instances for troubleshooting any failures. Default: None
        :param logging: (experimental) The log settings for detailed build logging. Default: None
        :param notification_topic: (experimental) The SNS topic on which notifications are sent when an image build completes. Default: No notifications are sent
        :param resource_tags: (experimental) The additional tags to assign to the Amazon EC2 instance that Image Builder launches during the build process. Default: None
        :param role: (experimental) An IAM role to associate with the instance profile used by Image Builder. The role must be assumable by the service principal ``ec2.amazonaws.com``: Note: You can provide an instanceProfile or a role, but not both. Default: A role will automatically be created, it can be accessed via the ``role`` property
        :param security_groups: (experimental) The security groups to associate with the instance used to customize the AMI. Default: The default security group for the VPC will be used
        :param subnet_selection: (experimental) Select which subnet to place the instance used to customize the AMI. The first subnet that is selected will be used. You must specify the VPC to customize the subnet selection. Default: The first subnet selected from the provided VPC will be used
        :param tags: (experimental) The tags to apply to the infrastructure configuration. Default: None
        :param terminate_instance_on_failure: (experimental) Whether to terminate the EC2 instance when the build or test workflow fails. Default: true
        :param vpc: (experimental) The VPC to place the instance used to customize the AMI. Default: The default VPC will be used

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8672dd2c6991d2ba23136620a37140cb449f0b7606cfe5538649d44bc009387)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = InfrastructureConfigurationProps(
            description=description,
            ec2_instance_availability_zone=ec2_instance_availability_zone,
            ec2_instance_host_id=ec2_instance_host_id,
            ec2_instance_host_resource_group_arn=ec2_instance_host_resource_group_arn,
            ec2_instance_tenancy=ec2_instance_tenancy,
            http_put_response_hop_limit=http_put_response_hop_limit,
            http_tokens=http_tokens,
            infrastructure_configuration_name=infrastructure_configuration_name,
            instance_profile=instance_profile,
            instance_types=instance_types,
            key_pair=key_pair,
            logging=logging,
            notification_topic=notification_topic,
            resource_tags=resource_tags,
            role=role,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            tags=tags,
            terminate_instance_on_failure=terminate_instance_on_failure,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromInfrastructureConfigurationArn")
    @builtins.classmethod
    def from_infrastructure_configuration_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        infrastructure_configuration_arn: builtins.str,
    ) -> IInfrastructureConfiguration:
        '''(experimental) Import an existing infrastructure configuration given its ARN.

        :param scope: -
        :param id: -
        :param infrastructure_configuration_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35015fe2e49bc142df9482904b92351bbc9b41c560cac1ac06713b2b564cd982)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument infrastructure_configuration_arn", value=infrastructure_configuration_arn, expected_type=type_hints["infrastructure_configuration_arn"])
        return typing.cast(IInfrastructureConfiguration, jsii.sinvoke(cls, "fromInfrastructureConfigurationArn", [scope, id, infrastructure_configuration_arn]))

    @jsii.member(jsii_name="fromInfrastructureConfigurationName")
    @builtins.classmethod
    def from_infrastructure_configuration_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        infrastructure_configuration_name: builtins.str,
    ) -> IInfrastructureConfiguration:
        '''(experimental) Import an existing infrastructure configuration given its name.

        The provided name must be normalized by converting
        all alphabetical characters to lowercase, and replacing all spaces and underscores with hyphens.

        :param scope: -
        :param id: -
        :param infrastructure_configuration_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d30c941bd6f0f1b07145f10c999bbeef38a9fbbc483fdfb4e54de8301a42bd6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument infrastructure_configuration_name", value=infrastructure_configuration_name, expected_type=type_hints["infrastructure_configuration_name"])
        return typing.cast(IInfrastructureConfiguration, jsii.sinvoke(cls, "fromInfrastructureConfigurationName", [scope, id, infrastructure_configuration_name]))

    @jsii.member(jsii_name="isInfrastructureConfiguration")
    @builtins.classmethod
    def is_infrastructure_configuration(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Return whether the given object is an InfrastructureConfiguration.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__653ebae43bf6b6e095ea87727d122e7cab0c8786387877992a5a7e642a846e02)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isInfrastructureConfiguration", [x]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the infrastructure configuration.

        :param grantee: - The principal.
        :param actions: - The list of actions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d73bd89218669ef1c777360509401b7db5901968dd024b757f3c75f85ccd1228)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the infrastructure configuration.

        :param grantee: - The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61c74f957e8c879932590c0d74b45224a68ab6d8eca577948a171e837ccc4cda)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureConfigurationArn")
    def infrastructure_configuration_arn(self) -> builtins.str:
        '''(experimental) The ARN of the infrastructure configuration.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "infrastructureConfigurationArn"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureConfigurationName")
    def infrastructure_configuration_name(self) -> builtins.str:
        '''(experimental) The name of the infrastructure configuration.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "infrastructureConfigurationName"))

    @builtins.property
    @jsii.member(jsii_name="instanceProfile")
    def instance_profile(self) -> _aws_cdk_aws_iam_ceddda9d.IInstanceProfile:
        '''(experimental) The EC2 instance profile to use for the build.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IInstanceProfile, jsii.get(self, "instanceProfile"))

    @builtins.property
    @jsii.member(jsii_name="logBucket")
    def log_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''(experimental) The bucket used to upload image build logs.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], jsii.get(self, "logBucket"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role associated with the EC2 instance profile used for the build.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "role"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.InfrastructureConfigurationLogging",
    jsii_struct_bases=[],
    name_mapping={"s3_bucket": "s3Bucket", "s3_key_prefix": "s3KeyPrefix"},
)
class InfrastructureConfigurationLogging:
    def __init__(
        self,
        *,
        s3_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        s3_key_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The log settings for detailed build logging.

        :param s3_bucket: (experimental) The S3 logging bucket to use for detailed build logging.
        :param s3_key_prefix: (experimental) The S3 logging prefix to use for detailed build logging. Default: No prefix

        :stability: experimental
        :exampleMetadata: infused

        Example::

            infrastructure_configuration = imagebuilder.InfrastructureConfiguration(self, "InfrastructureConfiguration",
                infrastructure_configuration_name="test-infrastructure-configuration",
                description="An Infrastructure Configuration",
                # Optional - instance types to use for build/test
                instance_types=[
                    ec2.InstanceType.of(ec2.InstanceClass.STANDARD7_INTEL, ec2.InstanceSize.LARGE),
                    ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.LARGE)
                ],
                # Optional - create an instance profile with necessary permissions
                instance_profile=iam.InstanceProfile(self, "InstanceProfile",
                    instance_profile_name="test-instance-profile",
                    role=iam.Role(self, "InstanceProfileRole",
                        assumed_by=iam.ServicePrincipal.from_static_service_principle_name("ec2.amazonaws.com"),
                        managed_policies=[
                            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"),
                            iam.ManagedPolicy.from_aws_managed_policy_name("EC2InstanceProfileForImageBuilder")
                        ]
                    )
                ),
                # Use VPC network configuration
                vpc=vpc,
                subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                security_groups=[ec2.SecurityGroup.from_security_group_id(self, "SecurityGroup", vpc.vpc_default_security_group)],
                key_pair=ec2.KeyPair.from_key_pair_name(self, "KeyPair", "imagebuilder-instance-key-pair"),
                terminate_instance_on_failure=True,
                # Optional - IMDSv2 settings
                http_tokens=imagebuilder.HttpTokens.REQUIRED,
                http_put_response_hop_limit=1,
                # Optional - publish image completion messages to an SNS topic
                notification_topic=sns.Topic.from_topic_arn(self, "Topic",
                    self.format_arn(service="sns", resource="image-builder-topic")),
                # Optional - log settings. Logging is enabled by default
                logging=imagebuilder.InfrastructureConfigurationLogging(
                    s3_bucket=s3.Bucket.from_bucket_name(self, "LogBucket", f"imagebuilder-logging-{Aws.ACCOUNT_ID}"),
                    s3_key_prefix="imagebuilder-logs"
                ),
                # Optional - host placement settings
                ec2_instance_availability_zone=Stack.of(self).availability_zones[0],
                ec2_instance_host_id=dedicated_host.attr_host_id,
                ec2_instance_tenancy=imagebuilder.Tenancy.HOST,
                resource_tags={
                    "Environment": "production"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74cffe7aa25819eaef361f450e04e7112a9f46a9d0138a9696f9723b55a1d31d)
            check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            check_type(argname="argument s3_key_prefix", value=s3_key_prefix, expected_type=type_hints["s3_key_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_bucket": s3_bucket,
        }
        if s3_key_prefix is not None:
            self._values["s3_key_prefix"] = s3_key_prefix

    @builtins.property
    def s3_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''(experimental) The S3 logging bucket to use for detailed build logging.

        :stability: experimental
        '''
        result = self._values.get("s3_bucket")
        assert result is not None, "Required property 's3_bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def s3_key_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The S3 logging prefix to use for detailed build logging.

        :default: No prefix

        :stability: experimental
        '''
        result = self._values.get("s3_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InfrastructureConfigurationLogging(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.InfrastructureConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "ec2_instance_availability_zone": "ec2InstanceAvailabilityZone",
        "ec2_instance_host_id": "ec2InstanceHostId",
        "ec2_instance_host_resource_group_arn": "ec2InstanceHostResourceGroupArn",
        "ec2_instance_tenancy": "ec2InstanceTenancy",
        "http_put_response_hop_limit": "httpPutResponseHopLimit",
        "http_tokens": "httpTokens",
        "infrastructure_configuration_name": "infrastructureConfigurationName",
        "instance_profile": "instanceProfile",
        "instance_types": "instanceTypes",
        "key_pair": "keyPair",
        "logging": "logging",
        "notification_topic": "notificationTopic",
        "resource_tags": "resourceTags",
        "role": "role",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "tags": "tags",
        "terminate_instance_on_failure": "terminateInstanceOnFailure",
        "vpc": "vpc",
    },
)
class InfrastructureConfigurationProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        ec2_instance_availability_zone: typing.Optional[builtins.str] = None,
        ec2_instance_host_id: typing.Optional[builtins.str] = None,
        ec2_instance_host_resource_group_arn: typing.Optional[builtins.str] = None,
        ec2_instance_tenancy: typing.Optional["Tenancy"] = None,
        http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
        http_tokens: typing.Optional[HttpTokens] = None,
        infrastructure_configuration_name: typing.Optional[builtins.str] = None,
        instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IInstanceProfile] = None,
        instance_types: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceType]] = None,
        key_pair: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IKeyPair] = None,
        logging: typing.Optional[typing.Union[InfrastructureConfigurationLogging, typing.Dict[builtins.str, typing.Any]]] = None,
        notification_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
        resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        terminate_instance_on_failure: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''(experimental) Properties for creating an Infrastructure Configuration resource.

        :param description: (experimental) The description of the infrastructure configuration. Default: None
        :param ec2_instance_availability_zone: (experimental) The availability zone to place Image Builder build and test EC2 instances. Default: EC2 will select a random zone
        :param ec2_instance_host_id: (experimental) The ID of the Dedicated Host on which build and test instances run. This only applies if the instance tenancy is ``host``. This cannot be used with the ``ec2InstanceHostResourceGroupArn`` parameter. Default: None
        :param ec2_instance_host_resource_group_arn: (experimental) The ARN of the host resource group on which build and test instances run. This only applies if the instance tenancy is ``host``. This cannot be used with the ``ec2InstanceHostId`` parameter. Default: None
        :param ec2_instance_tenancy: (experimental) The tenancy of the instance. Dedicated tenancy runs instances on single-tenant hardware, while host tenancy runs instances on a dedicated host. Shared tenancy is used by default. Default: Tenancy.DEFAULT
        :param http_put_response_hop_limit: (experimental) The maximum number of hops that an instance metadata request can traverse to reach its destination. By default, this is set to 2. Default: 2
        :param http_tokens: (experimental) Indicates whether a signed token header is required for instance metadata retrieval requests. By default, this is set to ``required`` to require IMDSv2 on build and test EC2 instances. Default: HttpTokens.REQUIRED
        :param infrastructure_configuration_name: (experimental) The name of the infrastructure configuration. This name must be normalized by transforming all alphabetical characters to lowercase, and replacing all spaces and underscores with hyphens. Default: A name is generated
        :param instance_profile: (experimental) The instance profile to associate with the instance used to customize the AMI. By default, an instance profile and role will be created with minimal permissions needed to build the image, attached to the EC2 instance. If an S3 logging bucket and key prefix is provided, an IAM inline policy will be attached to the instance profile's role, allowing s3:PutObject permissions on the bucket. Default: An instance profile will be generated
        :param instance_types: (experimental) The instance types to launch build and test EC2 instances with. Default: Image Builder will choose from a default set of instance types compatible with the AMI
        :param key_pair: (experimental) The key pair used to connect to the build and test EC2 instances. The key pair can be used to log into the build or test instances for troubleshooting any failures. Default: None
        :param logging: (experimental) The log settings for detailed build logging. Default: None
        :param notification_topic: (experimental) The SNS topic on which notifications are sent when an image build completes. Default: No notifications are sent
        :param resource_tags: (experimental) The additional tags to assign to the Amazon EC2 instance that Image Builder launches during the build process. Default: None
        :param role: (experimental) An IAM role to associate with the instance profile used by Image Builder. The role must be assumable by the service principal ``ec2.amazonaws.com``: Note: You can provide an instanceProfile or a role, but not both. Default: A role will automatically be created, it can be accessed via the ``role`` property
        :param security_groups: (experimental) The security groups to associate with the instance used to customize the AMI. Default: The default security group for the VPC will be used
        :param subnet_selection: (experimental) Select which subnet to place the instance used to customize the AMI. The first subnet that is selected will be used. You must specify the VPC to customize the subnet selection. Default: The first subnet selected from the provided VPC will be used
        :param tags: (experimental) The tags to apply to the infrastructure configuration. Default: None
        :param terminate_instance_on_failure: (experimental) Whether to terminate the EC2 instance when the build or test workflow fails. Default: true
        :param vpc: (experimental) The VPC to place the instance used to customize the AMI. Default: The default VPC will be used

        :stability: experimental
        :exampleMetadata: infused

        Example::

            infrastructure_configuration = imagebuilder.InfrastructureConfiguration(self, "Infrastructure",
                infrastructure_configuration_name="production-infrastructure",
                instance_types=[
                    ec2.InstanceType.of(ec2.InstanceClass.COMPUTE7_INTEL, ec2.InstanceSize.LARGE)
                ],
                vpc=vpc,
                subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
            )
            
            distribution_configuration = imagebuilder.DistributionConfiguration(self, "Distribution")
            distribution_configuration.add_ami_distributions(
                ami_name="production-ami-{{ imagebuilder:buildDate }}",
                ami_target_account_ids=["123456789012", "098765432109"]
            )
            
            production_pipeline = imagebuilder.ImagePipeline(self, "ProductionPipeline",
                recipe=example_image_recipe,
                infrastructure_configuration=infrastructure_configuration,
                distribution_configuration=distribution_configuration
            )
        '''
        if isinstance(logging, dict):
            logging = InfrastructureConfigurationLogging(**logging)
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07545a4f62a3521f9640beafa4b4d7cc1fbe20fc1df54541287ed96ffe7f8e4e)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument ec2_instance_availability_zone", value=ec2_instance_availability_zone, expected_type=type_hints["ec2_instance_availability_zone"])
            check_type(argname="argument ec2_instance_host_id", value=ec2_instance_host_id, expected_type=type_hints["ec2_instance_host_id"])
            check_type(argname="argument ec2_instance_host_resource_group_arn", value=ec2_instance_host_resource_group_arn, expected_type=type_hints["ec2_instance_host_resource_group_arn"])
            check_type(argname="argument ec2_instance_tenancy", value=ec2_instance_tenancy, expected_type=type_hints["ec2_instance_tenancy"])
            check_type(argname="argument http_put_response_hop_limit", value=http_put_response_hop_limit, expected_type=type_hints["http_put_response_hop_limit"])
            check_type(argname="argument http_tokens", value=http_tokens, expected_type=type_hints["http_tokens"])
            check_type(argname="argument infrastructure_configuration_name", value=infrastructure_configuration_name, expected_type=type_hints["infrastructure_configuration_name"])
            check_type(argname="argument instance_profile", value=instance_profile, expected_type=type_hints["instance_profile"])
            check_type(argname="argument instance_types", value=instance_types, expected_type=type_hints["instance_types"])
            check_type(argname="argument key_pair", value=key_pair, expected_type=type_hints["key_pair"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument notification_topic", value=notification_topic, expected_type=type_hints["notification_topic"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument terminate_instance_on_failure", value=terminate_instance_on_failure, expected_type=type_hints["terminate_instance_on_failure"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if ec2_instance_availability_zone is not None:
            self._values["ec2_instance_availability_zone"] = ec2_instance_availability_zone
        if ec2_instance_host_id is not None:
            self._values["ec2_instance_host_id"] = ec2_instance_host_id
        if ec2_instance_host_resource_group_arn is not None:
            self._values["ec2_instance_host_resource_group_arn"] = ec2_instance_host_resource_group_arn
        if ec2_instance_tenancy is not None:
            self._values["ec2_instance_tenancy"] = ec2_instance_tenancy
        if http_put_response_hop_limit is not None:
            self._values["http_put_response_hop_limit"] = http_put_response_hop_limit
        if http_tokens is not None:
            self._values["http_tokens"] = http_tokens
        if infrastructure_configuration_name is not None:
            self._values["infrastructure_configuration_name"] = infrastructure_configuration_name
        if instance_profile is not None:
            self._values["instance_profile"] = instance_profile
        if instance_types is not None:
            self._values["instance_types"] = instance_types
        if key_pair is not None:
            self._values["key_pair"] = key_pair
        if logging is not None:
            self._values["logging"] = logging
        if notification_topic is not None:
            self._values["notification_topic"] = notification_topic
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags
        if role is not None:
            self._values["role"] = role
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if tags is not None:
            self._values["tags"] = tags
        if terminate_instance_on_failure is not None:
            self._values["terminate_instance_on_failure"] = terminate_instance_on_failure
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the infrastructure configuration.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_instance_availability_zone(self) -> typing.Optional[builtins.str]:
        '''(experimental) The availability zone to place Image Builder build and test EC2 instances.

        :default: EC2 will select a random zone

        :stability: experimental
        '''
        result = self._values.get("ec2_instance_availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_instance_host_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ID of the Dedicated Host on which build and test instances run.

        This only applies if the instance tenancy is
        ``host``. This cannot be used with the ``ec2InstanceHostResourceGroupArn`` parameter.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("ec2_instance_host_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_instance_host_resource_group_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the host resource group on which build and test instances run.

        This only applies if the instance tenancy
        is ``host``. This cannot be used with the ``ec2InstanceHostId`` parameter.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("ec2_instance_host_resource_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_instance_tenancy(self) -> typing.Optional["Tenancy"]:
        '''(experimental) The tenancy of the instance.

        Dedicated tenancy runs instances on single-tenant hardware, while host tenancy runs
        instances on a dedicated host. Shared tenancy is used by default.

        :default: Tenancy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("ec2_instance_tenancy")
        return typing.cast(typing.Optional["Tenancy"], result)

    @builtins.property
    def http_put_response_hop_limit(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of hops that an instance metadata request can traverse to reach its destination.

        By default,
        this is set to 2.

        :default: 2

        :stability: experimental
        '''
        result = self._values.get("http_put_response_hop_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def http_tokens(self) -> typing.Optional[HttpTokens]:
        '''(experimental) Indicates whether a signed token header is required for instance metadata retrieval requests.

        By default, this is
        set to ``required`` to require IMDSv2 on build and test EC2 instances.

        :default: HttpTokens.REQUIRED

        :stability: experimental
        '''
        result = self._values.get("http_tokens")
        return typing.cast(typing.Optional[HttpTokens], result)

    @builtins.property
    def infrastructure_configuration_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the infrastructure configuration.

        This name must be normalized by transforming all alphabetical
        characters to lowercase, and replacing all spaces and underscores with hyphens.

        :default: A name is generated

        :stability: experimental
        '''
        result = self._values.get("infrastructure_configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_profile(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IInstanceProfile]:
        '''(experimental) The instance profile to associate with the instance used to customize the AMI.

        By default, an instance profile and role will be created with minimal permissions needed to build the image,
        attached to the EC2 instance.

        If an S3 logging bucket and key prefix is provided, an IAM inline policy will be attached to the instance profile's
        role, allowing s3:PutObject permissions on the bucket.

        :default: An instance profile will be generated

        :stability: experimental
        '''
        result = self._values.get("instance_profile")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IInstanceProfile], result)

    @builtins.property
    def instance_types(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceType]]:
        '''(experimental) The instance types to launch build and test EC2 instances with.

        :default: Image Builder will choose from a default set of instance types compatible with the AMI

        :stability: experimental
        '''
        result = self._values.get("instance_types")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceType]], result)

    @builtins.property
    def key_pair(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IKeyPair]:
        '''(experimental) The key pair used to connect to the build and test EC2 instances.

        The key pair can be used to log into the build
        or test instances for troubleshooting any failures.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("key_pair")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IKeyPair], result)

    @builtins.property
    def logging(self) -> typing.Optional[InfrastructureConfigurationLogging]:
        '''(experimental) The log settings for detailed build logging.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[InfrastructureConfigurationLogging], result)

    @builtins.property
    def notification_topic(self) -> typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic]:
        '''(experimental) The SNS topic on which notifications are sent when an image build completes.

        :default: No notifications are sent

        :stability: experimental
        '''
        result = self._values.get("notification_topic")
        return typing.cast(typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic], result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The additional tags to assign to the Amazon EC2 instance that Image Builder launches during the build process.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) An IAM role to associate with the instance profile used by Image Builder.

        The role must be assumable by the service principal ``ec2.amazonaws.com``:
        Note: You can provide an instanceProfile or a role, but not both.

        :default: A role will automatically be created, it can be accessed via the ``role`` property

        :stability: experimental

        Example::

            instance_profile_role = iam.Role(self, "MyRole",
                assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
            )
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''(experimental) The security groups to associate with the instance used to customize the AMI.

        :default: The default security group for the VPC will be used

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) Select which subnet to place the instance used to customize the AMI.

        The first subnet that is selected will be used.
        You must specify the VPC to customize the subnet selection.

        :default: The first subnet selected from the provided VPC will be used

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The tags to apply to the infrastructure configuration.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def terminate_instance_on_failure(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to terminate the EC2 instance when the build or test workflow fails.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("terminate_instance_on_failure")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''(experimental) The VPC to place the instance used to customize the AMI.

        :default: The default VPC will be used

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InfrastructureConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.LaunchTemplateConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "launch_template": "launchTemplate",
        "account_id": "accountId",
        "set_default_version": "setDefaultVersion",
    },
)
class LaunchTemplateConfiguration:
    def __init__(
        self,
        *,
        launch_template: _aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate,
        account_id: typing.Optional[builtins.str] = None,
        set_default_version: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) The launch template to apply the distributed AMI to.

        :param launch_template: (experimental) The launch template to apply the distributed AMI to. A new launch template version will be created for the provided launch template with the distributed AMI applied. *Note:* The launch template should expose a ``launchTemplateId``. Templates imported by name only are not supported.
        :param account_id: (experimental) The AWS account ID that owns the launch template. Default: The current account is used
        :param set_default_version: (experimental) Whether to set the new launch template version that is created as the default launch template version. After creation of the launch template version containing the distributed AMI, it will be automatically set as the default version for the launch template. Default: false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
            from aws_cdk import aws_ec2 as ec2
            
            # launch_template: ec2.LaunchTemplate
            
            launch_template_configuration = imagebuilder_alpha.LaunchTemplateConfiguration(
                launch_template=launch_template,
            
                # the properties below are optional
                account_id="accountId",
                set_default_version=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7488a156223bbf9e56775eef019a0bfc54d1cbe34be84e101b6775196600d51d)
            check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument set_default_version", value=set_default_version, expected_type=type_hints["set_default_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "launch_template": launch_template,
        }
        if account_id is not None:
            self._values["account_id"] = account_id
        if set_default_version is not None:
            self._values["set_default_version"] = set_default_version

    @builtins.property
    def launch_template(self) -> _aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate:
        '''(experimental) The launch template to apply the distributed AMI to.

        A new launch template version will be created for the
        provided launch template with the distributed AMI applied.

        *Note:* The launch template should expose a ``launchTemplateId``. Templates
        imported by name only are not supported.

        :stability: experimental
        '''
        result = self._values.get("launch_template")
        assert result is not None, "Required property 'launch_template' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate, result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS account ID that owns the launch template.

        :default: The current account is used

        :stability: experimental
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def set_default_version(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to set the new launch template version that is created as the default launch template version.

        After
        creation of the launch template version containing the distributed AMI, it will be automatically set as the
        default version for the launch template.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("set_default_version")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LaunchTemplateConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ILifecyclePolicy)
class LifecyclePolicy(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.LifecyclePolicy",
):
    '''(experimental) Represents an EC2 Image Builder Lifecycle Policy.

    :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/manage-image-lifecycles.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        disabled_policy = imagebuilder.LifecyclePolicy(self, "DisabledPolicy",
            lifecycle_policy_name="my-disabled-policy",
            description="A lifecycle policy that is temporarily disabled",
            status=imagebuilder.LifecyclePolicyStatus.DISABLED,
            resource_type=imagebuilder.LifecyclePolicyResourceType.AMI_IMAGE,
            details=[imagebuilder.LifecyclePolicyDetail(
                action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
                filter=imagebuilder.LifecyclePolicyFilter(age_filter=imagebuilder.LifecyclePolicyAgeFilter(age=Duration.days(30)))
            )
            ],
            resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
                tags={"Environment": "testing"}
            ),
            tags={
                "Owner": "DevOps",
                "CostCenter": "Engineering"
            }
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        details: typing.Sequence[typing.Union["LifecyclePolicyDetail", typing.Dict[builtins.str, typing.Any]]],
        resource_selection: typing.Union["LifecyclePolicyResourceSelection", typing.Dict[builtins.str, typing.Any]],
        resource_type: "LifecyclePolicyResourceType",
        description: typing.Optional[builtins.str] = None,
        execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        lifecycle_policy_name: typing.Optional[builtins.str] = None,
        status: typing.Optional["LifecyclePolicyStatus"] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param details: (experimental) Configuration details for the lifecycle policy rules.
        :param resource_selection: (experimental) Selection criteria for the resources that the lifecycle policy applies to.
        :param resource_type: (experimental) The type of Image Builder resource that the lifecycle policy applies to.
        :param description: (experimental) The description of the lifecycle policy. Default: None
        :param execution_role: (experimental) The execution role that grants Image Builder access to run lifecycle actions. By default, an execution role will be created with the minimal permissions needed to execute the lifecycle policy actions. Default: - an execution role will be generated
        :param lifecycle_policy_name: (experimental) The name of the lifecycle policy. Default: - a name is generated
        :param status: (experimental) The status of the lifecycle policy. Default: LifecyclePolicyStatus.ENABLED
        :param tags: (experimental) The tags to apply to the lifecycle policy. Default: - none

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__271dd3ac2c3d06c33753c4bf70e5cd28cce1cef2dbee876e788d779ae69dfa38)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LifecyclePolicyProps(
            details=details,
            resource_selection=resource_selection,
            resource_type=resource_type,
            description=description,
            execution_role=execution_role,
            lifecycle_policy_name=lifecycle_policy_name,
            status=status,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromLifecyclePolicyArn")
    @builtins.classmethod
    def from_lifecycle_policy_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        lifecycle_policy_arn: builtins.str,
    ) -> ILifecyclePolicy:
        '''(experimental) Import an existing lifecycle policy given its ARN.

        :param scope: -
        :param id: -
        :param lifecycle_policy_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8d6e9555d5d1ae0956ec47cedab74a03b2ed708cc29831d6e57521697d93b3a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lifecycle_policy_arn", value=lifecycle_policy_arn, expected_type=type_hints["lifecycle_policy_arn"])
        return typing.cast(ILifecyclePolicy, jsii.sinvoke(cls, "fromLifecyclePolicyArn", [scope, id, lifecycle_policy_arn]))

    @jsii.member(jsii_name="fromLifecyclePolicyName")
    @builtins.classmethod
    def from_lifecycle_policy_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        lifecycle_policy_name: builtins.str,
    ) -> ILifecyclePolicy:
        '''(experimental) Import an existing lifecycle policy given its name.

        If the name is a token representing a dynamic CloudFormation
        expression, you must ensure all alphabetic characters in the expression are already lowercased

        :param scope: -
        :param id: -
        :param lifecycle_policy_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0ec60504dec766447fdf4acbcc8d3442ac7e4399d368f43fe3bd752231252ff)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lifecycle_policy_name", value=lifecycle_policy_name, expected_type=type_hints["lifecycle_policy_name"])
        return typing.cast(ILifecyclePolicy, jsii.sinvoke(cls, "fromLifecyclePolicyName", [scope, id, lifecycle_policy_name]))

    @jsii.member(jsii_name="isLifecyclePolicy")
    @builtins.classmethod
    def is_lifecycle_policy(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Return whether the given object is a LifecyclePolicy.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bc873f1fcffad5dc3ac5e61b579399350b520d1989d5d72b322ed9ecb69dd7d)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isLifecyclePolicy", [x]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the lifecycle policy.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19112552930af6d7588f60ce65a10af56c59c57151ecdd169cc3d9b3de262d14)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the lifecycle policy.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__043e3753fbd001f82f0190c1f88995921a471ef4ef3025996236713cc912f5b6)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The execution role used for lifecycle policy executions.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "executionRole"))

    @builtins.property
    @jsii.member(jsii_name="lifecyclePolicyArn")
    def lifecycle_policy_arn(self) -> builtins.str:
        '''(experimental) The ARN of the lifecycle policy.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "lifecyclePolicyArn"))

    @builtins.property
    @jsii.member(jsii_name="lifecyclePolicyName")
    def lifecycle_policy_name(self) -> builtins.str:
        '''(experimental) The name of the lifecycle policy.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "lifecyclePolicyName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.LifecyclePolicyAction",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "include_amis": "includeAmis",
        "include_containers": "includeContainers",
        "include_snapshots": "includeSnapshots",
    },
)
class LifecyclePolicyAction:
    def __init__(
        self,
        *,
        type: "LifecyclePolicyActionType",
        include_amis: typing.Optional[builtins.bool] = None,
        include_containers: typing.Optional[builtins.bool] = None,
        include_snapshots: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) The action to perform in the lifecycle policy rule.

        :param type: (experimental) The action to perform on the resources selected in the lifecycle policy rule.
        :param include_amis: (experimental) Whether to include AMIs in the scope of the lifecycle rule. Default: - true for AMI-based policies, false otherwise
        :param include_containers: (experimental) Whether to include containers in the scope of the lifecycle rule. Default: - true for container-based policies, false otherwise
        :param include_snapshots: (experimental) Whether to include snapshots in the scope of the lifecycle rule. Default: - true for AMI-based policies, false otherwise

        :stability: experimental
        :exampleMetadata: infused

        Example::

            disabled_policy = imagebuilder.LifecyclePolicy(self, "DisabledPolicy",
                lifecycle_policy_name="my-disabled-policy",
                description="A lifecycle policy that is temporarily disabled",
                status=imagebuilder.LifecyclePolicyStatus.DISABLED,
                resource_type=imagebuilder.LifecyclePolicyResourceType.AMI_IMAGE,
                details=[imagebuilder.LifecyclePolicyDetail(
                    action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
                    filter=imagebuilder.LifecyclePolicyFilter(age_filter=imagebuilder.LifecyclePolicyAgeFilter(age=Duration.days(30)))
                )
                ],
                resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
                    tags={"Environment": "testing"}
                ),
                tags={
                    "Owner": "DevOps",
                    "CostCenter": "Engineering"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6575e02812d62404e6b9df0d628cc5ab29363e1a59d64b7eaa21161ce95e3cdc)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument include_amis", value=include_amis, expected_type=type_hints["include_amis"])
            check_type(argname="argument include_containers", value=include_containers, expected_type=type_hints["include_containers"])
            check_type(argname="argument include_snapshots", value=include_snapshots, expected_type=type_hints["include_snapshots"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if include_amis is not None:
            self._values["include_amis"] = include_amis
        if include_containers is not None:
            self._values["include_containers"] = include_containers
        if include_snapshots is not None:
            self._values["include_snapshots"] = include_snapshots

    @builtins.property
    def type(self) -> "LifecyclePolicyActionType":
        '''(experimental) The action to perform on the resources selected in the lifecycle policy rule.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("LifecyclePolicyActionType", result)

    @builtins.property
    def include_amis(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to include AMIs in the scope of the lifecycle rule.

        :default: - true for AMI-based policies, false otherwise

        :stability: experimental
        '''
        result = self._values.get("include_amis")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def include_containers(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to include containers in the scope of the lifecycle rule.

        :default: - true for container-based policies, false otherwise

        :stability: experimental
        '''
        result = self._values.get("include_containers")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def include_snapshots(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to include snapshots in the scope of the lifecycle rule.

        :default: - true for AMI-based policies, false otherwise

        :stability: experimental
        '''
        result = self._values.get("include_snapshots")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LifecyclePolicyAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.LifecyclePolicyActionType")
class LifecyclePolicyActionType(enum.Enum):
    '''(experimental) The action to perform on the resources which the policy applies to.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        disabled_policy = imagebuilder.LifecyclePolicy(self, "DisabledPolicy",
            lifecycle_policy_name="my-disabled-policy",
            description="A lifecycle policy that is temporarily disabled",
            status=imagebuilder.LifecyclePolicyStatus.DISABLED,
            resource_type=imagebuilder.LifecyclePolicyResourceType.AMI_IMAGE,
            details=[imagebuilder.LifecyclePolicyDetail(
                action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
                filter=imagebuilder.LifecyclePolicyFilter(age_filter=imagebuilder.LifecyclePolicyAgeFilter(age=Duration.days(30)))
            )
            ],
            resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
                tags={"Environment": "testing"}
            ),
            tags={
                "Owner": "DevOps",
                "CostCenter": "Engineering"
            }
        )
    '''

    DELETE = "DELETE"
    '''(experimental) Indicates that the rule should delete the resource when it is applied.

    :stability: experimental
    '''
    DEPRECATE = "DEPRECATE"
    '''(experimental) Indicates that the rule should deprecate the resource when it is applied.

    :stability: experimental
    '''
    DISABLE = "DISABLE"
    '''(experimental) Indicates that the rule should disable the resource when it is applied.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.LifecyclePolicyAgeFilter",
    jsii_struct_bases=[],
    name_mapping={"age": "age", "retain_at_least": "retainAtLeast"},
)
class LifecyclePolicyAgeFilter:
    def __init__(
        self,
        *,
        age: _aws_cdk_ceddda9d.Duration,
        retain_at_least: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) The age-based filtering to apply in a lifecycle policy rule.

        :param age: (experimental) The minimum age of the resource to filter. The provided duration will be rounded up to the nearest day/week/month/year value.
        :param retain_at_least: (experimental) For age-based filters, the number of EC2 Image Builder images to keep on hand once the rule is applied. The value must be between 1 and 10. Default: 0

        :stability: experimental
        :exampleMetadata: infused

        Example::

            disabled_policy = imagebuilder.LifecyclePolicy(self, "DisabledPolicy",
                lifecycle_policy_name="my-disabled-policy",
                description="A lifecycle policy that is temporarily disabled",
                status=imagebuilder.LifecyclePolicyStatus.DISABLED,
                resource_type=imagebuilder.LifecyclePolicyResourceType.AMI_IMAGE,
                details=[imagebuilder.LifecyclePolicyDetail(
                    action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
                    filter=imagebuilder.LifecyclePolicyFilter(age_filter=imagebuilder.LifecyclePolicyAgeFilter(age=Duration.days(30)))
                )
                ],
                resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
                    tags={"Environment": "testing"}
                ),
                tags={
                    "Owner": "DevOps",
                    "CostCenter": "Engineering"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__183f6aac6170e6f01f4103a4405e21b1793e7f5802b375799ec3c20b24901e5b)
            check_type(argname="argument age", value=age, expected_type=type_hints["age"])
            check_type(argname="argument retain_at_least", value=retain_at_least, expected_type=type_hints["retain_at_least"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "age": age,
        }
        if retain_at_least is not None:
            self._values["retain_at_least"] = retain_at_least

    @builtins.property
    def age(self) -> _aws_cdk_ceddda9d.Duration:
        '''(experimental) The minimum age of the resource to filter.

        The provided duration will be rounded up to the nearest
        day/week/month/year value.

        :stability: experimental
        '''
        result = self._values.get("age")
        assert result is not None, "Required property 'age' is missing"
        return typing.cast(_aws_cdk_ceddda9d.Duration, result)

    @builtins.property
    def retain_at_least(self) -> typing.Optional[jsii.Number]:
        '''(experimental) For age-based filters, the number of EC2 Image Builder images to keep on hand once the rule is applied.

        The value
        must be between 1 and 10.

        :default: 0

        :stability: experimental
        '''
        result = self._values.get("retain_at_least")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LifecyclePolicyAgeFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.LifecyclePolicyAmiExclusionRules",
    jsii_struct_bases=[],
    name_mapping={
        "is_public": "isPublic",
        "last_launched": "lastLaunched",
        "regions": "regions",
        "shared_accounts": "sharedAccounts",
        "tags": "tags",
    },
)
class LifecyclePolicyAmiExclusionRules:
    def __init__(
        self,
        *,
        is_public: typing.Optional[builtins.bool] = None,
        last_launched: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        shared_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) The rules to apply for excluding AMIs from the lifecycle policy rule.

        :param is_public: (experimental) Excludes public AMIs from the lifecycle policy rule if true. Default: false
        :param last_launched: (experimental) Excludes AMIs which were launched from within the provided duration. Default: None
        :param regions: (experimental) Excludes AMIs which reside in any of the provided regions. Default: None
        :param shared_accounts: (experimental) Excludes AMIs which are shared with any of the provided shared accounts. Default: None
        :param tags: (experimental) Excludes AMIs which have any of the provided tags applied to it. Default: None

        :stability: experimental
        :exampleMetadata: infused

        Example::

            exclude_amis_policy = imagebuilder.LifecyclePolicy(self, "ExcludeAmisPolicy",
                resource_type=imagebuilder.LifecyclePolicyResourceType.AMI_IMAGE,
                details=[imagebuilder.LifecyclePolicyDetail(
                    action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
                    filter=imagebuilder.LifecyclePolicyFilter(age_filter=imagebuilder.LifecyclePolicyAgeFilter(age=Duration.days(30))),
                    exclusion_rules=imagebuilder.LifecyclePolicyExclusionRules(
                        ami_exclusion_rules=imagebuilder.LifecyclePolicyAmiExclusionRules(
                            is_public=True,  # Exclude public AMIs
                            last_launched=Duration.days(7),  # Exclude AMIs launched in last 7 days
                            regions=["us-west-2", "eu-west-1"],  # Exclude AMIs in specific regions
                            shared_accounts=["123456789012"],  # Exclude AMIs shared with specific accounts
                            tags={
                                "Protected": "true",
                                "Environment": "production"
                            }
                        )
                    )
                )
                ],
                resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
                    tags={"Team": "infrastructure"}
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e57835a73ae082e18c324554f09925609de5a9e0d340221eb13c812a7a5b96e)
            check_type(argname="argument is_public", value=is_public, expected_type=type_hints["is_public"])
            check_type(argname="argument last_launched", value=last_launched, expected_type=type_hints["last_launched"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument shared_accounts", value=shared_accounts, expected_type=type_hints["shared_accounts"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_public is not None:
            self._values["is_public"] = is_public
        if last_launched is not None:
            self._values["last_launched"] = last_launched
        if regions is not None:
            self._values["regions"] = regions
        if shared_accounts is not None:
            self._values["shared_accounts"] = shared_accounts
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def is_public(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Excludes public AMIs from the lifecycle policy rule if true.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("is_public")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def last_launched(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) Excludes AMIs which were launched from within the provided duration.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("last_launched")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Excludes AMIs which reside in any of the provided regions.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def shared_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Excludes AMIs which are shared with any of the provided shared accounts.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("shared_accounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Excludes AMIs which have any of the provided tags applied to it.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LifecyclePolicyAmiExclusionRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.LifecyclePolicyCountFilter",
    jsii_struct_bases=[],
    name_mapping={"count": "count"},
)
class LifecyclePolicyCountFilter:
    def __init__(self, *, count: jsii.Number) -> None:
        '''(experimental) The count-based filtering to apply in a lifecycle policy rule.

        :param count: (experimental) The minimum number of resources to keep on hand as part of resource filtering.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            exclude_images_policy = imagebuilder.LifecyclePolicy(self, "ExcludeImagesPolicy",
                resource_type=imagebuilder.LifecyclePolicyResourceType.CONTAINER_IMAGE,
                details=[imagebuilder.LifecyclePolicyDetail(
                    action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
                    filter=imagebuilder.LifecyclePolicyFilter(count_filter=imagebuilder.LifecyclePolicyCountFilter(count=20)),
                    exclusion_rules=imagebuilder.LifecyclePolicyExclusionRules(
                        image_exclusion_rules=imagebuilder.LifecyclePolicyImageExclusionRules(
                            tags={
                                "DoNotDelete": "true",
                                "Critical": "baseline"
                            }
                        )
                    )
                )
                ],
                resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
                    tags={"Application": "frontend"}
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e92b96d7974adf6a33269bb31e7e79b100ba6b4ded4c01a47f51153348a0c0eb)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''(experimental) The minimum number of resources to keep on hand as part of resource filtering.

        :stability: experimental
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LifecyclePolicyCountFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.LifecyclePolicyDetail",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "filter": "filter",
        "exclusion_rules": "exclusionRules",
    },
)
class LifecyclePolicyDetail:
    def __init__(
        self,
        *,
        action: typing.Union[LifecyclePolicyAction, typing.Dict[builtins.str, typing.Any]],
        filter: typing.Union["LifecyclePolicyFilter", typing.Dict[builtins.str, typing.Any]],
        exclusion_rules: typing.Optional[typing.Union["LifecyclePolicyExclusionRules", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Configuration details for the lifecycle policy rules.

        :param action: (experimental) The action to perform in the lifecycle policy rule.
        :param filter: (experimental) The resource filtering to apply in the lifecycle policy rule.
        :param exclusion_rules: (experimental) The rules to apply for excluding resources from the lifecycle policy rule. Default: - no exclusion rules are applied on any resource

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
            import aws_cdk as cdk
            
            lifecycle_policy_detail = imagebuilder_alpha.LifecyclePolicyDetail(
                action=imagebuilder_alpha.LifecyclePolicyAction(
                    type=imagebuilder_alpha.LifecyclePolicyActionType.DELETE,
            
                    # the properties below are optional
                    include_amis=False,
                    include_containers=False,
                    include_snapshots=False
                ),
                filter=imagebuilder_alpha.LifecyclePolicyFilter(
                    age_filter=imagebuilder_alpha.LifecyclePolicyAgeFilter(
                        age=cdk.Duration.minutes(30),
            
                        # the properties below are optional
                        retain_at_least=123
                    ),
                    count_filter=imagebuilder_alpha.LifecyclePolicyCountFilter(
                        count=123
                    )
                ),
            
                # the properties below are optional
                exclusion_rules=imagebuilder_alpha.LifecyclePolicyExclusionRules(
                    ami_exclusion_rules=imagebuilder_alpha.LifecyclePolicyAmiExclusionRules(
                        is_public=False,
                        last_launched=cdk.Duration.minutes(30),
                        regions=["regions"],
                        shared_accounts=["sharedAccounts"],
                        tags={
                            "tags_key": "tags"
                        }
                    ),
                    image_exclusion_rules=imagebuilder_alpha.LifecyclePolicyImageExclusionRules(
                        tags={
                            "tags_key": "tags"
                        }
                    )
                )
            )
        '''
        if isinstance(action, dict):
            action = LifecyclePolicyAction(**action)
        if isinstance(filter, dict):
            filter = LifecyclePolicyFilter(**filter)
        if isinstance(exclusion_rules, dict):
            exclusion_rules = LifecyclePolicyExclusionRules(**exclusion_rules)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d529b43dd44a438161a3bc5f50e2f1d1073b31e4e5fd63a57e350b93e453c17)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument exclusion_rules", value=exclusion_rules, expected_type=type_hints["exclusion_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "filter": filter,
        }
        if exclusion_rules is not None:
            self._values["exclusion_rules"] = exclusion_rules

    @builtins.property
    def action(self) -> LifecyclePolicyAction:
        '''(experimental) The action to perform in the lifecycle policy rule.

        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(LifecyclePolicyAction, result)

    @builtins.property
    def filter(self) -> "LifecyclePolicyFilter":
        '''(experimental) The resource filtering to apply in the lifecycle policy rule.

        :stability: experimental
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast("LifecyclePolicyFilter", result)

    @builtins.property
    def exclusion_rules(self) -> typing.Optional["LifecyclePolicyExclusionRules"]:
        '''(experimental) The rules to apply for excluding resources from the lifecycle policy rule.

        :default: - no exclusion rules are applied on any resource

        :stability: experimental
        '''
        result = self._values.get("exclusion_rules")
        return typing.cast(typing.Optional["LifecyclePolicyExclusionRules"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LifecyclePolicyDetail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.LifecyclePolicyExclusionRules",
    jsii_struct_bases=[],
    name_mapping={
        "ami_exclusion_rules": "amiExclusionRules",
        "image_exclusion_rules": "imageExclusionRules",
    },
)
class LifecyclePolicyExclusionRules:
    def __init__(
        self,
        *,
        ami_exclusion_rules: typing.Optional[typing.Union[LifecyclePolicyAmiExclusionRules, typing.Dict[builtins.str, typing.Any]]] = None,
        image_exclusion_rules: typing.Optional[typing.Union["LifecyclePolicyImageExclusionRules", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) The rules to apply for excluding resources from the lifecycle policy rule.

        :param ami_exclusion_rules: (experimental) The rules to apply for excluding AMIs from the lifecycle policy rule. Default: - no exclusion rules are applied on the AMI
        :param image_exclusion_rules: (experimental) The rules to apply for excluding EC2 Image Builder images from the lifecycle policy rule. Default: - no exclusion rules are applied on the image

        :stability: experimental
        :exampleMetadata: infused

        Example::

            exclude_amis_policy = imagebuilder.LifecyclePolicy(self, "ExcludeAmisPolicy",
                resource_type=imagebuilder.LifecyclePolicyResourceType.AMI_IMAGE,
                details=[imagebuilder.LifecyclePolicyDetail(
                    action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
                    filter=imagebuilder.LifecyclePolicyFilter(age_filter=imagebuilder.LifecyclePolicyAgeFilter(age=Duration.days(30))),
                    exclusion_rules=imagebuilder.LifecyclePolicyExclusionRules(
                        ami_exclusion_rules=imagebuilder.LifecyclePolicyAmiExclusionRules(
                            is_public=True,  # Exclude public AMIs
                            last_launched=Duration.days(7),  # Exclude AMIs launched in last 7 days
                            regions=["us-west-2", "eu-west-1"],  # Exclude AMIs in specific regions
                            shared_accounts=["123456789012"],  # Exclude AMIs shared with specific accounts
                            tags={
                                "Protected": "true",
                                "Environment": "production"
                            }
                        )
                    )
                )
                ],
                resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
                    tags={"Team": "infrastructure"}
                )
            )
        '''
        if isinstance(ami_exclusion_rules, dict):
            ami_exclusion_rules = LifecyclePolicyAmiExclusionRules(**ami_exclusion_rules)
        if isinstance(image_exclusion_rules, dict):
            image_exclusion_rules = LifecyclePolicyImageExclusionRules(**image_exclusion_rules)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be32a843ef901862ea30ac304ea2b78ca608e710fee49030a9131a7e35b3cd2c)
            check_type(argname="argument ami_exclusion_rules", value=ami_exclusion_rules, expected_type=type_hints["ami_exclusion_rules"])
            check_type(argname="argument image_exclusion_rules", value=image_exclusion_rules, expected_type=type_hints["image_exclusion_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ami_exclusion_rules is not None:
            self._values["ami_exclusion_rules"] = ami_exclusion_rules
        if image_exclusion_rules is not None:
            self._values["image_exclusion_rules"] = image_exclusion_rules

    @builtins.property
    def ami_exclusion_rules(self) -> typing.Optional[LifecyclePolicyAmiExclusionRules]:
        '''(experimental) The rules to apply for excluding AMIs from the lifecycle policy rule.

        :default: - no exclusion rules are applied on the AMI

        :stability: experimental
        '''
        result = self._values.get("ami_exclusion_rules")
        return typing.cast(typing.Optional[LifecyclePolicyAmiExclusionRules], result)

    @builtins.property
    def image_exclusion_rules(
        self,
    ) -> typing.Optional["LifecyclePolicyImageExclusionRules"]:
        '''(experimental) The rules to apply for excluding EC2 Image Builder images from the lifecycle policy rule.

        :default: - no exclusion rules are applied on the image

        :stability: experimental
        '''
        result = self._values.get("image_exclusion_rules")
        return typing.cast(typing.Optional["LifecyclePolicyImageExclusionRules"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LifecyclePolicyExclusionRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.LifecyclePolicyFilter",
    jsii_struct_bases=[],
    name_mapping={"age_filter": "ageFilter", "count_filter": "countFilter"},
)
class LifecyclePolicyFilter:
    def __init__(
        self,
        *,
        age_filter: typing.Optional[typing.Union[LifecyclePolicyAgeFilter, typing.Dict[builtins.str, typing.Any]]] = None,
        count_filter: typing.Optional[typing.Union[LifecyclePolicyCountFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) The resource filtering to apply in the lifecycle policy rule.

        :param age_filter: (experimental) The resource age filter to apply in the lifecycle policy rule. Default: - none if a count filter is provided. Otherwise, an age filter is required.
        :param count_filter: (experimental) The resource count filter to apply in the lifecycle policy rule. Default: - none if an age filter is provided. Otherwise, a count filter is required.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            disabled_policy = imagebuilder.LifecyclePolicy(self, "DisabledPolicy",
                lifecycle_policy_name="my-disabled-policy",
                description="A lifecycle policy that is temporarily disabled",
                status=imagebuilder.LifecyclePolicyStatus.DISABLED,
                resource_type=imagebuilder.LifecyclePolicyResourceType.AMI_IMAGE,
                details=[imagebuilder.LifecyclePolicyDetail(
                    action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
                    filter=imagebuilder.LifecyclePolicyFilter(age_filter=imagebuilder.LifecyclePolicyAgeFilter(age=Duration.days(30)))
                )
                ],
                resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
                    tags={"Environment": "testing"}
                ),
                tags={
                    "Owner": "DevOps",
                    "CostCenter": "Engineering"
                }
            )
        '''
        if isinstance(age_filter, dict):
            age_filter = LifecyclePolicyAgeFilter(**age_filter)
        if isinstance(count_filter, dict):
            count_filter = LifecyclePolicyCountFilter(**count_filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6943d9f9d76b975de1d1f68fa0018543edfef85f0d47efad320e7af88787188)
            check_type(argname="argument age_filter", value=age_filter, expected_type=type_hints["age_filter"])
            check_type(argname="argument count_filter", value=count_filter, expected_type=type_hints["count_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if age_filter is not None:
            self._values["age_filter"] = age_filter
        if count_filter is not None:
            self._values["count_filter"] = count_filter

    @builtins.property
    def age_filter(self) -> typing.Optional[LifecyclePolicyAgeFilter]:
        '''(experimental) The resource age filter to apply in the lifecycle policy rule.

        :default: - none if a count filter is provided. Otherwise, an age filter is required.

        :stability: experimental
        '''
        result = self._values.get("age_filter")
        return typing.cast(typing.Optional[LifecyclePolicyAgeFilter], result)

    @builtins.property
    def count_filter(self) -> typing.Optional[LifecyclePolicyCountFilter]:
        '''(experimental) The resource count filter to apply in the lifecycle policy rule.

        :default: - none if an age filter is provided. Otherwise, a count filter is required.

        :stability: experimental
        '''
        result = self._values.get("count_filter")
        return typing.cast(typing.Optional[LifecyclePolicyCountFilter], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LifecyclePolicyFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.LifecyclePolicyImageExclusionRules",
    jsii_struct_bases=[],
    name_mapping={"tags": "tags"},
)
class LifecyclePolicyImageExclusionRules:
    def __init__(self, *, tags: typing.Mapping[builtins.str, builtins.str]) -> None:
        '''(experimental) The rules to apply for excluding EC2 Image Builder images from the lifecycle policy rule.

        :param tags: (experimental) Excludes EC2 Image Builder images with any of the provided tags from the lifecycle policy rule.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            exclude_images_policy = imagebuilder.LifecyclePolicy(self, "ExcludeImagesPolicy",
                resource_type=imagebuilder.LifecyclePolicyResourceType.CONTAINER_IMAGE,
                details=[imagebuilder.LifecyclePolicyDetail(
                    action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
                    filter=imagebuilder.LifecyclePolicyFilter(count_filter=imagebuilder.LifecyclePolicyCountFilter(count=20)),
                    exclusion_rules=imagebuilder.LifecyclePolicyExclusionRules(
                        image_exclusion_rules=imagebuilder.LifecyclePolicyImageExclusionRules(
                            tags={
                                "DoNotDelete": "true",
                                "Critical": "baseline"
                            }
                        )
                    )
                )
                ],
                resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
                    tags={"Application": "frontend"}
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73d1e60b18534f0b200268d994e117596c824c5090cccc95264352f6ee9764af)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tags": tags,
        }

    @builtins.property
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) Excludes EC2 Image Builder images with any of the provided tags from the lifecycle policy rule.

        :stability: experimental
        '''
        result = self._values.get("tags")
        assert result is not None, "Required property 'tags' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LifecyclePolicyImageExclusionRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.LifecyclePolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "details": "details",
        "resource_selection": "resourceSelection",
        "resource_type": "resourceType",
        "description": "description",
        "execution_role": "executionRole",
        "lifecycle_policy_name": "lifecyclePolicyName",
        "status": "status",
        "tags": "tags",
    },
)
class LifecyclePolicyProps:
    def __init__(
        self,
        *,
        details: typing.Sequence[typing.Union[LifecyclePolicyDetail, typing.Dict[builtins.str, typing.Any]]],
        resource_selection: typing.Union["LifecyclePolicyResourceSelection", typing.Dict[builtins.str, typing.Any]],
        resource_type: "LifecyclePolicyResourceType",
        description: typing.Optional[builtins.str] = None,
        execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        lifecycle_policy_name: typing.Optional[builtins.str] = None,
        status: typing.Optional["LifecyclePolicyStatus"] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Properties for creating a Lifecycle Policy resource.

        :param details: (experimental) Configuration details for the lifecycle policy rules.
        :param resource_selection: (experimental) Selection criteria for the resources that the lifecycle policy applies to.
        :param resource_type: (experimental) The type of Image Builder resource that the lifecycle policy applies to.
        :param description: (experimental) The description of the lifecycle policy. Default: None
        :param execution_role: (experimental) The execution role that grants Image Builder access to run lifecycle actions. By default, an execution role will be created with the minimal permissions needed to execute the lifecycle policy actions. Default: - an execution role will be generated
        :param lifecycle_policy_name: (experimental) The name of the lifecycle policy. Default: - a name is generated
        :param status: (experimental) The status of the lifecycle policy. Default: LifecyclePolicyStatus.ENABLED
        :param tags: (experimental) The tags to apply to the lifecycle policy. Default: - none

        :stability: experimental
        :exampleMetadata: infused

        Example::

            disabled_policy = imagebuilder.LifecyclePolicy(self, "DisabledPolicy",
                lifecycle_policy_name="my-disabled-policy",
                description="A lifecycle policy that is temporarily disabled",
                status=imagebuilder.LifecyclePolicyStatus.DISABLED,
                resource_type=imagebuilder.LifecyclePolicyResourceType.AMI_IMAGE,
                details=[imagebuilder.LifecyclePolicyDetail(
                    action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
                    filter=imagebuilder.LifecyclePolicyFilter(age_filter=imagebuilder.LifecyclePolicyAgeFilter(age=Duration.days(30)))
                )
                ],
                resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
                    tags={"Environment": "testing"}
                ),
                tags={
                    "Owner": "DevOps",
                    "CostCenter": "Engineering"
                }
            )
        '''
        if isinstance(resource_selection, dict):
            resource_selection = LifecyclePolicyResourceSelection(**resource_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96a0fa69ee38b571f992d146893360a20d2cdedddaaa132dc7696ef2d64792a9)
            check_type(argname="argument details", value=details, expected_type=type_hints["details"])
            check_type(argname="argument resource_selection", value=resource_selection, expected_type=type_hints["resource_selection"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument lifecycle_policy_name", value=lifecycle_policy_name, expected_type=type_hints["lifecycle_policy_name"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "details": details,
            "resource_selection": resource_selection,
            "resource_type": resource_type,
        }
        if description is not None:
            self._values["description"] = description
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if lifecycle_policy_name is not None:
            self._values["lifecycle_policy_name"] = lifecycle_policy_name
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def details(self) -> typing.List[LifecyclePolicyDetail]:
        '''(experimental) Configuration details for the lifecycle policy rules.

        :stability: experimental
        '''
        result = self._values.get("details")
        assert result is not None, "Required property 'details' is missing"
        return typing.cast(typing.List[LifecyclePolicyDetail], result)

    @builtins.property
    def resource_selection(self) -> "LifecyclePolicyResourceSelection":
        '''(experimental) Selection criteria for the resources that the lifecycle policy applies to.

        :stability: experimental
        '''
        result = self._values.get("resource_selection")
        assert result is not None, "Required property 'resource_selection' is missing"
        return typing.cast("LifecyclePolicyResourceSelection", result)

    @builtins.property
    def resource_type(self) -> "LifecyclePolicyResourceType":
        '''(experimental) The type of Image Builder resource that the lifecycle policy applies to.

        :stability: experimental
        '''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast("LifecyclePolicyResourceType", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the lifecycle policy.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The execution role that grants Image Builder access to run lifecycle actions.

        By default, an execution role will be created with the minimal permissions needed to execute the lifecycle policy
        actions.

        :default: - an execution role will be generated

        :stability: experimental
        '''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def lifecycle_policy_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the lifecycle policy.

        :default: - a name is generated

        :stability: experimental
        '''
        result = self._values.get("lifecycle_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional["LifecyclePolicyStatus"]:
        '''(experimental) The status of the lifecycle policy.

        :default: LifecyclePolicyStatus.ENABLED

        :stability: experimental
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional["LifecyclePolicyStatus"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The tags to apply to the lifecycle policy.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LifecyclePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.LifecyclePolicyResourceSelection",
    jsii_struct_bases=[],
    name_mapping={"recipes": "recipes", "tags": "tags"},
)
class LifecyclePolicyResourceSelection:
    def __init__(
        self,
        *,
        recipes: typing.Optional[typing.Sequence[IRecipeBase]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Selection criteria for the resources that the lifecycle policy applies to.

        :param recipes: (experimental) The list of image recipes or container recipes to apply the lifecycle policy to. Default: - none if tag selections are provided. Otherwise, at least one recipe or tag selection must be provided
        :param tags: (experimental) Selects EC2 Image Builder images containing any of the provided tags. Default: - none if recipe selections are provided. Otherwise, at least one recipe or tag selection must be provided

        :stability: experimental
        :exampleMetadata: infused

        Example::

            disabled_policy = imagebuilder.LifecyclePolicy(self, "DisabledPolicy",
                lifecycle_policy_name="my-disabled-policy",
                description="A lifecycle policy that is temporarily disabled",
                status=imagebuilder.LifecyclePolicyStatus.DISABLED,
                resource_type=imagebuilder.LifecyclePolicyResourceType.AMI_IMAGE,
                details=[imagebuilder.LifecyclePolicyDetail(
                    action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
                    filter=imagebuilder.LifecyclePolicyFilter(age_filter=imagebuilder.LifecyclePolicyAgeFilter(age=Duration.days(30)))
                )
                ],
                resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
                    tags={"Environment": "testing"}
                ),
                tags={
                    "Owner": "DevOps",
                    "CostCenter": "Engineering"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec4ef8fa30361e9ec41e2180c6c210ea22ae393bbfe7d6a9df335ed9b980d38e)
            check_type(argname="argument recipes", value=recipes, expected_type=type_hints["recipes"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if recipes is not None:
            self._values["recipes"] = recipes
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def recipes(self) -> typing.Optional[typing.List[IRecipeBase]]:
        '''(experimental) The list of image recipes or container recipes to apply the lifecycle policy to.

        :default: - none if tag selections are provided. Otherwise, at least one recipe or tag selection must be provided

        :stability: experimental
        '''
        result = self._values.get("recipes")
        return typing.cast(typing.Optional[typing.List[IRecipeBase]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Selects EC2 Image Builder images containing any of the provided tags.

        :default: - none if recipe selections are provided. Otherwise, at least one recipe or tag selection must be provided

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LifecyclePolicyResourceSelection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.LifecyclePolicyResourceType")
class LifecyclePolicyResourceType(enum.Enum):
    '''(experimental) The resource type which the lifecycle policy is applied to.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        disabled_policy = imagebuilder.LifecyclePolicy(self, "DisabledPolicy",
            lifecycle_policy_name="my-disabled-policy",
            description="A lifecycle policy that is temporarily disabled",
            status=imagebuilder.LifecyclePolicyStatus.DISABLED,
            resource_type=imagebuilder.LifecyclePolicyResourceType.AMI_IMAGE,
            details=[imagebuilder.LifecyclePolicyDetail(
                action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
                filter=imagebuilder.LifecyclePolicyFilter(age_filter=imagebuilder.LifecyclePolicyAgeFilter(age=Duration.days(30)))
            )
            ],
            resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
                tags={"Environment": "testing"}
            ),
            tags={
                "Owner": "DevOps",
                "CostCenter": "Engineering"
            }
        )
    '''

    AMI_IMAGE = "AMI_IMAGE"
    '''(experimental) Indicates the policy applies to AMI-based images.

    :stability: experimental
    '''
    CONTAINER_IMAGE = "CONTAINER_IMAGE"
    '''(experimental) Indicates the policy applies to container images.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.LifecyclePolicyStatus")
class LifecyclePolicyStatus(enum.Enum):
    '''(experimental) The status of the lifecycle policy, indicating whether it will run.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        disabled_policy = imagebuilder.LifecyclePolicy(self, "DisabledPolicy",
            lifecycle_policy_name="my-disabled-policy",
            description="A lifecycle policy that is temporarily disabled",
            status=imagebuilder.LifecyclePolicyStatus.DISABLED,
            resource_type=imagebuilder.LifecyclePolicyResourceType.AMI_IMAGE,
            details=[imagebuilder.LifecyclePolicyDetail(
                action=imagebuilder.LifecyclePolicyAction(type=imagebuilder.LifecyclePolicyActionType.DELETE),
                filter=imagebuilder.LifecyclePolicyFilter(age_filter=imagebuilder.LifecyclePolicyAgeFilter(age=Duration.days(30)))
            )
            ],
            resource_selection=imagebuilder.LifecyclePolicyResourceSelection(
                tags={"Environment": "testing"}
            ),
            tags={
                "Owner": "DevOps",
                "CostCenter": "Engineering"
            }
        )
    '''

    ENABLED = "ENABLED"
    '''(experimental) Indicates that the lifecycle policy should be enabled.

    :stability: experimental
    '''
    DISABLED = "DISABLED"
    '''(experimental) Indicates that the lifecycle policy should be disabled.

    :stability: experimental
    '''


class OSVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.OSVersion",
):
    '''(experimental) Represents an OS version for an EC2 Image Builder image.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
        
        o_sVersion = imagebuilder_alpha.OSVersion.AMAZON_LINUX
    '''

    def __init__(
        self,
        platform: "Platform",
        os_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param platform: -
        :param os_version: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e835db1a09fe43e2d622f4324c6ace2e9dbd991bf060bc80994a8c7f278814)
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument os_version", value=os_version, expected_type=type_hints["os_version"])
        jsii.create(self.__class__, self, [platform, os_version])

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(
        cls,
        platform: "Platform",
        os_version: typing.Optional[builtins.str] = None,
    ) -> "OSVersion":
        '''(experimental) Constructs an OS version with a custom name.

        :param platform: The platform of the OS version.
        :param os_version: The custom OS version to use.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff5a2c2e2f508c6ffd9d7b790056aed4fb62718c2288d6565e09783a7327d151)
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument os_version", value=os_version, expected_type=type_hints["os_version"])
        return typing.cast("OSVersion", jsii.sinvoke(cls, "custom", [platform, os_version]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_LINUX")
    def AMAZON_LINUX(cls) -> "OSVersion":
        '''(experimental) OS version for all Amazon Linux images.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "AMAZON_LINUX"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_LINUX_2")
    def AMAZON_LINUX_2(cls) -> "OSVersion":
        '''(experimental) OS version for Amazon Linux 2.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "AMAZON_LINUX_2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_LINUX_2023")
    def AMAZON_LINUX_2023(cls) -> "OSVersion":
        '''(experimental) OS version for Amazon Linux 2023.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "AMAZON_LINUX_2023"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX")
    def LINUX(cls) -> "OSVersion":
        '''(experimental) OS version for all Linux images.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "LINUX"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MAC_OS")
    def MAC_OS(cls) -> "OSVersion":
        '''(experimental) OS version for all macOS images.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "MAC_OS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MAC_OS_14")
    def MAC_OS_14(cls) -> "OSVersion":
        '''(experimental) OS version for macOS 14.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "MAC_OS_14"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MAC_OS_15")
    def MAC_OS_15(cls) -> "OSVersion":
        '''(experimental) OS version for macOS 15.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "MAC_OS_15"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REDHAT_ENTERPRISE_LINUX")
    def REDHAT_ENTERPRISE_LINUX(cls) -> "OSVersion":
        '''(experimental) OS version for all Red Hat Enterprise Linux images.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "REDHAT_ENTERPRISE_LINUX"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REDHAT_ENTERPRISE_LINUX_10")
    def REDHAT_ENTERPRISE_LINUX_10(cls) -> "OSVersion":
        '''(experimental) OS version for Red Hat Enterprise Linux 10.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "REDHAT_ENTERPRISE_LINUX_10"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REDHAT_ENTERPRISE_LINUX_8")
    def REDHAT_ENTERPRISE_LINUX_8(cls) -> "OSVersion":
        '''(experimental) OS version for Red Hat Enterprise Linux 8.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "REDHAT_ENTERPRISE_LINUX_8"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REDHAT_ENTERPRISE_LINUX_9")
    def REDHAT_ENTERPRISE_LINUX_9(cls) -> "OSVersion":
        '''(experimental) OS version for Red Hat Enterprise Linux 9.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "REDHAT_ENTERPRISE_LINUX_9"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SLES")
    def SLES(cls) -> "OSVersion":
        '''(experimental) OS version for all SLES images.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "SLES"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SLES_15")
    def SLES_15(cls) -> "OSVersion":
        '''(experimental) OS version for SLES 15.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "SLES_15"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU")
    def UBUNTU(cls) -> "OSVersion":
        '''(experimental) OS version for all Ubuntu images.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "UBUNTU"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_22_04")
    def UBUNTU_22_04(cls) -> "OSVersion":
        '''(experimental) OS version for Ubuntu 22.04.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "UBUNTU_22_04"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_24_04")
    def UBUNTU_24_04(cls) -> "OSVersion":
        '''(experimental) OS version for Ubuntu 24.04.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "UBUNTU_24_04"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="WINDOWS")
    def WINDOWS(cls) -> "OSVersion":
        '''(experimental) OS version for all Windows images.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "WINDOWS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="WINDOWS_SERVER")
    def WINDOWS_SERVER(cls) -> "OSVersion":
        '''(experimental) OS version for all Windows server images.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "WINDOWS_SERVER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="WINDOWS_SERVER_2016")
    def WINDOWS_SERVER_2016(cls) -> "OSVersion":
        '''(experimental) OS version for Windows Server 2016.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "WINDOWS_SERVER_2016"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="WINDOWS_SERVER_2019")
    def WINDOWS_SERVER_2019(cls) -> "OSVersion":
        '''(experimental) OS version for Windows Server 2019.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "WINDOWS_SERVER_2019"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="WINDOWS_SERVER_2022")
    def WINDOWS_SERVER_2022(cls) -> "OSVersion":
        '''(experimental) OS version for Windows Server 2022.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "WINDOWS_SERVER_2022"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="WINDOWS_SERVER_2025")
    def WINDOWS_SERVER_2025(cls) -> "OSVersion":
        '''(experimental) OS version for Windows Server 2025.

        :stability: experimental
        '''
        return typing.cast("OSVersion", jsii.sget(cls, "WINDOWS_SERVER_2025"))

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> "Platform":
        '''(experimental) The Platform of the OS version.

        :stability: experimental
        '''
        return typing.cast("Platform", jsii.get(self, "platform"))

    @builtins.property
    @jsii.member(jsii_name="osVersion")
    def os_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The OS version name.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osVersion"))


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.Platform")
class Platform(enum.Enum):
    '''(experimental) Represents a platform for an EC2 Image Builder image.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        component = imagebuilder.Component(self, "JsonComponent",
            platform=imagebuilder.Platform.LINUX,
            data=imagebuilder.ComponentData.from_json_object({
                "schema_version": imagebuilder.ComponentSchemaVersion.V1_0,
                "phases": [{
                    "name": imagebuilder.ComponentPhaseName.BUILD,
                    "steps": [{
                        "name": "configure-app",
                        "action": imagebuilder.ComponentAction.CREATE_FILE,
                        "inputs": {
                            "path": "/etc/myapp/config.json",
                            "content": "{\"env\": \"production\"}"
                        }
                    }
                    ]
                }
                ]
            })
        )
    '''

    LINUX = "LINUX"
    '''(experimental) Platform for Linux.

    :stability: experimental
    '''
    WINDOWS = "WINDOWS"
    '''(experimental) Platform for Windows.

    :stability: experimental
    '''
    MAC_OS = "MAC_OS"
    '''(experimental) Platform for macOS.

    :stability: experimental
    '''


class Repository(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.Repository",
):
    '''(experimental) A container repository used to distribute container images in EC2 Image Builder.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        parameterized_component = imagebuilder.Component.from_component_name(self, "ParameterizedComponent", "my-parameterized-component")
        
        image_recipe = imagebuilder.ImageRecipe(self, "ParameterizedImageRecipe",
            base_image=imagebuilder.BaseImage.from_ssm_parameter_name("/aws/service/ami-amazon-linux-latest/al2023-ami-minimal-kernel-default-x86_64"),
            components=[imagebuilder.ComponentConfiguration(
                component=parameterized_component,
                parameters={
                    "environment": imagebuilder.ComponentParameterValue.from_string("production"),
                    "version": imagebuilder.ComponentParameterValue.from_string("1.0.0")
                }
            )
            ]
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromEcr")
    @builtins.classmethod
    def from_ecr(
        cls,
        repository: _aws_cdk_aws_ecr_ceddda9d.IRepository,
    ) -> "Repository":
        '''(experimental) The ECR repository to use as the target container repository.

        :param repository: The ECR repository to use.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf80e8cbc35b94d36db54f92df03bee46b372adfb0f2a76712eaf0f716c17c3e)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
        return typing.cast("Repository", jsii.sinvoke(cls, "fromEcr", [repository]))

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    @abc.abstractmethod
    def repository_name(self) -> builtins.str:
        '''(experimental) The name of the container repository where the output container image is stored.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="service")
    @abc.abstractmethod
    def service(self) -> "RepositoryService":
        '''(experimental) The service in which the container repository is hosted.

        :stability: experimental
        '''
        ...


class _RepositoryProxy(Repository):
    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        '''(experimental) The name of the container repository where the output container image is stored.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryName"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> "RepositoryService":
        '''(experimental) The service in which the container repository is hosted.

        :stability: experimental
        '''
        return typing.cast("RepositoryService", jsii.get(self, "service"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Repository).__jsii_proxy_class__ = lambda : _RepositoryProxy


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.RepositoryService")
class RepositoryService(enum.Enum):
    '''(experimental) The service in which a container should be registered.

    :stability: experimental
    '''

    ECR = "ECR"
    '''(experimental) Indicates the container should be registered in ECR.

    :stability: experimental
    '''


class S3ComponentData(
    ComponentData,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.S3ComponentData",
):
    '''(experimental) Helper class for S3-based component data references, containing additional permission grant methods on the S3 object.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
        import aws_cdk as cdk
        from aws_cdk import aws_iam as iam
        from aws_cdk.interfaces import aws_kms as interfaces_kms
        
        # docker_image: cdk.DockerImage
        # grantable: iam.IGrantable
        # key_ref: interfaces_kms.IKeyRef
        # local_bundling: cdk.ILocalBundling
        
        s3_component_data = imagebuilder_alpha.S3ComponentData.from_asset(self, "MyS3ComponentData", "path",
            asset_hash="assetHash",
            asset_hash_type=cdk.AssetHashType.SOURCE,
            bundling=cdk.BundlingOptions(
                image=docker_image,
        
                # the properties below are optional
                bundling_file_access=cdk.BundlingFileAccess.VOLUME_COPY,
                command=["command"],
                entrypoint=["entrypoint"],
                environment={
                    "environment_key": "environment"
                },
                local=local_bundling,
                network="network",
                output_type=cdk.BundlingOutput.ARCHIVED,
                platform="platform",
                security_opt="securityOpt",
                user="user",
                volumes=[cdk.DockerVolume(
                    container_path="containerPath",
                    host_path="hostPath",
        
                    # the properties below are optional
                    consistency=cdk.DockerVolumeConsistency.CONSISTENT
                )],
                volumes_from=["volumesFrom"],
                working_directory="workingDirectory"
            ),
            deploy_time=False,
            display_name="displayName",
            exclude=["exclude"],
            follow_symlinks=cdk.SymlinkFollowMode.NEVER,
            ignore_mode=cdk.IgnoreMode.GLOB,
            readers=[grantable],
            source_kMSKey=key_ref
        )
    '''

    def __init__(
        self,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        key: builtins.str,
    ) -> None:
        '''
        :param bucket: -
        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8cfdd61801a768cf18184f1eb0737a88d90c072ea930a509e6fe06fcff393d8)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        jsii.create(self.__class__, self, [bucket, key])

    @jsii.member(jsii_name="grantPut")
    def grant_put(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant put permissions to the given grantee for the component data in S3.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc38fb84d23f869830d4eb53138914295325097f770e7d5bd62c28c8cedaaa0c)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantPut", [grantee]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the component data in S3.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__022e6141b2cc124364e4bd232e91e64e60212165c7aca9e98a54c50a7b0e1bb7)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def _bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, jsii.get(self, "bucket"))

    @builtins.property
    @jsii.member(jsii_name="isS3Reference")
    def is_s3_reference(self) -> builtins.bool:
        '''(experimental) Indicates that the provided component data is an S3 reference.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isS3Reference"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def _key(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "key"))


class _S3ComponentDataProxy(
    S3ComponentData,
    jsii.proxy_for(ComponentData), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, S3ComponentData).__jsii_proxy_class__ = lambda : _S3ComponentDataProxy


class S3DockerfileData(
    DockerfileData,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.S3DockerfileData",
):
    '''(experimental) Helper class for S3-based dockerfile data references, containing additional permission grant methods on the S3 object.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
        import aws_cdk as cdk
        from aws_cdk import aws_iam as iam
        from aws_cdk.interfaces import aws_kms as interfaces_kms
        
        # docker_image: cdk.DockerImage
        # grantable: iam.IGrantable
        # key_ref: interfaces_kms.IKeyRef
        # local_bundling: cdk.ILocalBundling
        
        s3_dockerfile_data = imagebuilder_alpha.S3DockerfileData.from_asset(self, "MyS3DockerfileData", "path",
            asset_hash="assetHash",
            asset_hash_type=cdk.AssetHashType.SOURCE,
            bundling=cdk.BundlingOptions(
                image=docker_image,
        
                # the properties below are optional
                bundling_file_access=cdk.BundlingFileAccess.VOLUME_COPY,
                command=["command"],
                entrypoint=["entrypoint"],
                environment={
                    "environment_key": "environment"
                },
                local=local_bundling,
                network="network",
                output_type=cdk.BundlingOutput.ARCHIVED,
                platform="platform",
                security_opt="securityOpt",
                user="user",
                volumes=[cdk.DockerVolume(
                    container_path="containerPath",
                    host_path="hostPath",
        
                    # the properties below are optional
                    consistency=cdk.DockerVolumeConsistency.CONSISTENT
                )],
                volumes_from=["volumesFrom"],
                working_directory="workingDirectory"
            ),
            deploy_time=False,
            display_name="displayName",
            exclude=["exclude"],
            follow_symlinks=cdk.SymlinkFollowMode.NEVER,
            ignore_mode=cdk.IgnoreMode.GLOB,
            readers=[grantable],
            source_kMSKey=key_ref
        )
    '''

    def __init__(
        self,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        key: builtins.str,
    ) -> None:
        '''
        :param bucket: -
        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0acb3c5cf678b9df02a383da86cbaad019f8c0ef0a4d5c4581796756291bcce1)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        jsii.create(self.__class__, self, [bucket, key])

    @jsii.member(jsii_name="grantPut")
    def grant_put(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant put permissions to the given grantee for the dockerfile data in S3.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__404b4072c58a96918f411d53482b980373a8a636b91cfcee714b014077b4d944)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantPut", [grantee]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the dockerfile data in S3.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c5016d23b88559064fded2374377862c2b2efde220704d938420b4822d4af53)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="render")
    def render(self) -> DockerfileTemplateConfig:
        '''(experimental) The rendered Dockerfile S3 URL, for use in CloudFormation.

        :stability: experimental
        '''
        return typing.cast(DockerfileTemplateConfig, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def _bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, jsii.get(self, "bucket"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def _key(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "key"))


class _S3DockerfileDataProxy(
    S3DockerfileData,
    jsii.proxy_for(DockerfileData), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, S3DockerfileData).__jsii_proxy_class__ = lambda : _S3DockerfileDataProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.SSMParameterConfigurations",
    jsii_struct_bases=[],
    name_mapping={
        "parameter": "parameter",
        "ami_account": "amiAccount",
        "data_type": "dataType",
    },
)
class SSMParameterConfigurations:
    def __init__(
        self,
        *,
        parameter: _aws_cdk_aws_ssm_ceddda9d.IStringParameter,
        ami_account: typing.Optional[builtins.str] = None,
        data_type: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterDataType] = None,
    ) -> None:
        '''(experimental) The SSM parameters to create or update for the distributed AMIs.

        :param parameter: (experimental) The SSM parameter to create or update.
        :param ami_account: (experimental) The AWS account ID that will own the SSM parameter in the given region. This must be one of the target accounts that was included in the list of AMI distribution target accounts Default: The current account is used
        :param data_type: (experimental) The data type of the SSM parameter. Default: ssm.ParameterDataType.AWS_EC2_IMAGE

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
            from aws_cdk import aws_ssm as ssm
            
            # string_parameter: ssm.StringParameter
            
            s_sMParameter_configurations = imagebuilder_alpha.SSMParameterConfigurations(
                parameter=string_parameter,
            
                # the properties below are optional
                ami_account="amiAccount",
                data_type=ssm.ParameterDataType.TEXT
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8c69f6418914aecbc11661f47678dc487ec81badbe17d0b392aff21a8c9943f)
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
            check_type(argname="argument ami_account", value=ami_account, expected_type=type_hints["ami_account"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parameter": parameter,
        }
        if ami_account is not None:
            self._values["ami_account"] = ami_account
        if data_type is not None:
            self._values["data_type"] = data_type

    @builtins.property
    def parameter(self) -> _aws_cdk_aws_ssm_ceddda9d.IStringParameter:
        '''(experimental) The SSM parameter to create or update.

        :stability: experimental
        '''
        result = self._values.get("parameter")
        assert result is not None, "Required property 'parameter' is missing"
        return typing.cast(_aws_cdk_aws_ssm_ceddda9d.IStringParameter, result)

    @builtins.property
    def ami_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS account ID that will own the SSM parameter in the given region.

        This must be one of the target accounts
        that was included in the list of AMI distribution target accounts

        :default: The current account is used

        :stability: experimental
        '''
        result = self._values.get("ami_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_type(self) -> typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterDataType]:
        '''(experimental) The data type of the SSM parameter.

        :default: ssm.ParameterDataType.AWS_EC2_IMAGE

        :stability: experimental
        '''
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterDataType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SSMParameterConfigurations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.ScheduleStartCondition")
class ScheduleStartCondition(enum.Enum):
    '''(experimental) The start condition for the pipeline, indicating the condition under which a pipeline should be triggered.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        advanced_schedule_pipeline = imagebuilder.ImagePipeline(self, "AdvancedSchedulePipeline",
            recipe=example_image_recipe,
            schedule=imagebuilder.ImagePipelineSchedule(
                expression=events.Schedule.rate(Duration.days(7)),
                # Only trigger when dependencies are updated (new base images, components, etc.)
                start_condition=imagebuilder.ScheduleStartCondition.EXPRESSION_MATCH_AND_DEPENDENCY_UPDATES_AVAILABLE,
                # Automatically disable after 3 consecutive failures
                auto_disable_failure_count=3
            ),
            # Start enabled
            status=imagebuilder.ImagePipelineStatus.ENABLED
        )
    '''

    EXPRESSION_MATCH_ONLY = "EXPRESSION_MATCH_ONLY"
    '''(experimental) Indicates to trigger a pipeline whenever its schedule is met.

    :stability: experimental
    '''
    EXPRESSION_MATCH_AND_DEPENDENCY_UPDATES_AVAILABLE = "EXPRESSION_MATCH_AND_DEPENDENCY_UPDATES_AVAILABLE"
    '''(experimental) Indicates to trigger a pipeline whenever its schedule is met, and there are matching dependency updates available, such as new versions of components or images to use in the pipeline build.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.Tenancy")
class Tenancy(enum.Enum):
    '''(experimental) The tenancy to use for an instance.

    :see: https://docs.aws.amazon.com/imagebuilder/latest/APIReference/API_Placement.html#imagebuilder-Type-Placement-tenancy
    :stability: experimental
    :exampleMetadata: infused

    Example::

        infrastructure_configuration = imagebuilder.InfrastructureConfiguration(self, "InfrastructureConfiguration",
            infrastructure_configuration_name="test-infrastructure-configuration",
            description="An Infrastructure Configuration",
            # Optional - instance types to use for build/test
            instance_types=[
                ec2.InstanceType.of(ec2.InstanceClass.STANDARD7_INTEL, ec2.InstanceSize.LARGE),
                ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.LARGE)
            ],
            # Optional - create an instance profile with necessary permissions
            instance_profile=iam.InstanceProfile(self, "InstanceProfile",
                instance_profile_name="test-instance-profile",
                role=iam.Role(self, "InstanceProfileRole",
                    assumed_by=iam.ServicePrincipal.from_static_service_principle_name("ec2.amazonaws.com"),
                    managed_policies=[
                        iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"),
                        iam.ManagedPolicy.from_aws_managed_policy_name("EC2InstanceProfileForImageBuilder")
                    ]
                )
            ),
            # Use VPC network configuration
            vpc=vpc,
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_groups=[ec2.SecurityGroup.from_security_group_id(self, "SecurityGroup", vpc.vpc_default_security_group)],
            key_pair=ec2.KeyPair.from_key_pair_name(self, "KeyPair", "imagebuilder-instance-key-pair"),
            terminate_instance_on_failure=True,
            # Optional - IMDSv2 settings
            http_tokens=imagebuilder.HttpTokens.REQUIRED,
            http_put_response_hop_limit=1,
            # Optional - publish image completion messages to an SNS topic
            notification_topic=sns.Topic.from_topic_arn(self, "Topic",
                self.format_arn(service="sns", resource="image-builder-topic")),
            # Optional - log settings. Logging is enabled by default
            logging=imagebuilder.InfrastructureConfigurationLogging(
                s3_bucket=s3.Bucket.from_bucket_name(self, "LogBucket", f"imagebuilder-logging-{Aws.ACCOUNT_ID}"),
                s3_key_prefix="imagebuilder-logs"
            ),
            # Optional - host placement settings
            ec2_instance_availability_zone=Stack.of(self).availability_zones[0],
            ec2_instance_host_id=dedicated_host.attr_host_id,
            ec2_instance_tenancy=imagebuilder.Tenancy.HOST,
            resource_tags={
                "Environment": "production"
            }
        )
    '''

    DEFAULT = "DEFAULT"
    '''(experimental) Instances will be launched with default tenancy.

    :stability: experimental
    '''
    DEDICATED = "DEDICATED"
    '''(experimental) Instances will be launched with dedicated tenancy.

    :stability: experimental
    '''
    HOST = "HOST"
    '''(experimental) Instances will be launched on a dedicated host.

    :stability: experimental
    '''


@jsii.implements(IWorkflow)
class Workflow(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.Workflow",
):
    '''(experimental) Represents an EC2 Image Builder Workflow.

    :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/manage-image-workflows.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        workflow = imagebuilder.Workflow(self, "EncryptedWorkflow",
            workflow_type=imagebuilder.WorkflowType.BUILD,
            kms_key=kms.Key(self, "WorkflowKey"),
            data=imagebuilder.WorkflowData.from_json_object({
                "schema_version": imagebuilder.WorkflowSchemaVersion.V1_0,
                "steps": [{
                    "name": "LaunchBuildInstance",
                    "action": imagebuilder.WorkflowAction.LAUNCH_INSTANCE,
                    "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
                    "inputs": {
                        "wait_for": "ssmAgent"
                    }
                }, {
                    "name": "CreateImage",
                    "action": imagebuilder.WorkflowAction.CREATE_IMAGE,
                    "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
                    "inputs": {
                        "instance_id": "i-123"
                    }
                }, {
                    "name": "TerminateInstance",
                    "action": imagebuilder.WorkflowAction.TERMINATE_INSTANCE,
                    "on_failure": imagebuilder.WorkflowOnFailure.CONTINUE,
                    "inputs": {
                        "instance_id": "i-123"
                    }
                }
                ],
                "outputs": [{
                    "name": "ImageId",
                    "value": "$.stepOutputs.CreateImage.imageId"
                }
                ]
            })
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        data: "WorkflowData",
        workflow_type: "WorkflowType",
        change_description: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workflow_name: typing.Optional[builtins.str] = None,
        workflow_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param data: (experimental) The workflow document content that defines the image creation process.
        :param workflow_type: (experimental) The phase in the image build process for which the workflow resource is responsible.
        :param change_description: (experimental) The change description of the workflow. Describes what change has been made in this version of the workflow, or what makes this version different from other versions. Default: None
        :param description: (experimental) The description of the workflow. Default: None
        :param kms_key: (experimental) The KMS key used to encrypt this workflow. Default: - an Image Builder owned key will be used to encrypt the workflow.
        :param tags: (experimental) The tags to apply to the workflow. Default: None
        :param workflow_name: (experimental) The name of the workflow. Default: - a name is generated
        :param workflow_version: (experimental) The version of the workflow. Default: 1.0.0

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33f61e84e71eb204b9e3eba30cf8cb65b6e523efac1baff856e35fc1d8a7674b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WorkflowProps(
            data=data,
            workflow_type=workflow_type,
            change_description=change_description,
            description=description,
            kms_key=kms_key,
            tags=tags,
            workflow_name=workflow_name,
            workflow_version=workflow_version,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromWorkflowArn")
    @builtins.classmethod
    def from_workflow_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        workflow_arn: builtins.str,
    ) -> IWorkflow:
        '''(experimental) Import an existing workflow given its ARN.

        :param scope: -
        :param id: -
        :param workflow_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb2978b6779771efb1902d7ba54f2188438a2e979f75f5e32738f71e4096f5d8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument workflow_arn", value=workflow_arn, expected_type=type_hints["workflow_arn"])
        return typing.cast(IWorkflow, jsii.sinvoke(cls, "fromWorkflowArn", [scope, id, workflow_arn]))

    @jsii.member(jsii_name="fromWorkflowAttributes")
    @builtins.classmethod
    def from_workflow_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        workflow_arn: typing.Optional[builtins.str] = None,
        workflow_name: typing.Optional[builtins.str] = None,
        workflow_type: typing.Optional["WorkflowType"] = None,
        workflow_version: typing.Optional[builtins.str] = None,
    ) -> IWorkflow:
        '''(experimental) Import an existing workflow by providing its attributes.

        The provided name must be normalized by converting
        all alphabetical characters to lowercase, and replacing all spaces and underscores with hyphens. You may not
        provide a dynamic expression for the workflowArn or workflowType

        :param scope: -
        :param id: -
        :param workflow_arn: (experimental) The ARN of the workflow. Default: - the ARN is automatically constructed if a workflowName and workflowType is provided, otherwise a workflowArn is required
        :param workflow_name: (experimental) The name of the workflow. Default: - the name is automatically constructed if a workflowArn is provided, otherwise a workflowName is required
        :param workflow_type: (experimental) The type of the workflow. Default: - the type is automatically constructed if a workflowArn is provided, otherwise a workflowType is required
        :param workflow_version: (experimental) The version of the workflow. Default: x.x.x

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5edf9d7cc79b93c3f1a190b9f26e05f09ff1aff7e6f4061d5468b4337d5b469c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = WorkflowAttributes(
            workflow_arn=workflow_arn,
            workflow_name=workflow_name,
            workflow_type=workflow_type,
            workflow_version=workflow_version,
        )

        return typing.cast(IWorkflow, jsii.sinvoke(cls, "fromWorkflowAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="isWorkflow")
    @builtins.classmethod
    def is_workflow(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Return whether the given object is a Workflow.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c33f638af75f2cf96769ae23ad4899df1b36f64fdae79266ecd17f0f6980474)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isWorkflow", [x]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the workflow.

        :param grantee: The principal.
        :param actions: The list of actions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a50f18b2739cb8fc10502cd31849c39c3268dd0fe52af6086df0b09b20168c0c)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the workflow.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c88f0daf052ccf8229d67eb15fdb5ebfbb9650208e655dccf3ed29c06592f378)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="workflowArn")
    def workflow_arn(self) -> builtins.str:
        '''(experimental) The ARN of the workflow.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "workflowArn"))

    @builtins.property
    @jsii.member(jsii_name="workflowName")
    def workflow_name(self) -> builtins.str:
        '''(experimental) The name of the workflow.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "workflowName"))

    @builtins.property
    @jsii.member(jsii_name="workflowType")
    def workflow_type(self) -> builtins.str:
        '''(experimental) The type of the workflow.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "workflowType"))

    @builtins.property
    @jsii.member(jsii_name="workflowVersion")
    def workflow_version(self) -> builtins.str:
        '''(experimental) The version of the workflow.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "workflowVersion"))


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.WorkflowAction")
class WorkflowAction(enum.Enum):
    '''(experimental) The action for a step within the workflow document.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        workflow = imagebuilder.Workflow(self, "MyWorkflow",
            workflow_type=imagebuilder.WorkflowType.BUILD,
            data=imagebuilder.WorkflowData.from_json_object({
                "schema_version": imagebuilder.WorkflowSchemaVersion.V1_0,
                "steps": [{
                    "name": "LaunchBuildInstance",
                    "action": imagebuilder.WorkflowAction.LAUNCH_INSTANCE,
                    "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
                    "inputs": {
                        "wait_for": "ssmAgent"
                    }
                }, {
                    "name": "ExecuteComponents",
                    "action": imagebuilder.WorkflowAction.EXECUTE_COMPONENTS,
                    "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
                    "inputs": {
                        "instance_id": "i-123"
                    }
                }, {
                    "name": "CreateImage",
                    "action": imagebuilder.WorkflowAction.CREATE_IMAGE,
                    "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
                    "inputs": {
                        "instance_id": "i-123"
                    }
                }, {
                    "name": "TerminateInstance",
                    "action": imagebuilder.WorkflowAction.TERMINATE_INSTANCE,
                    "on_failure": imagebuilder.WorkflowOnFailure.CONTINUE,
                    "inputs": {
                        "instance_id": "i-123"
                    }
                }
                ],
                "outputs": [{
                    "name": "ImageId",
                    "value": "$.stepOutputs.CreateImage.imageId"
                }
                ]
            })
        )
    '''

    APPLY_IMAGE_CONFIGURATIONS = "APPLY_IMAGE_CONFIGURATIONS"
    '''(experimental) Applies customizations and configurations to the input AMIs, such as publishing the AMI to SSM Parameter Store, or creating launch template versions with the AMI IDs provided in the input.

    :stability: experimental
    '''
    BOOTSTRAP_INSTANCE_FOR_CONTAINER = "BOOTSTRAP_INSTANCE_FOR_CONTAINER"
    '''(experimental) The BootstrapInstanceForContainer action runs a service script to bootstrap the instance with minimum requirements to run container workflows.

    :stability: experimental
    '''
    COLLECT_IMAGE_METADATA = "COLLECT_IMAGE_METADATA"
    '''(experimental) The CollectImageMetadata action collects additional information about the instance, such as the list of packages and their respective versions.

    :stability: experimental
    '''
    COLLECT_IMAGE_SCAN_FINDINGS = "COLLECT_IMAGE_SCAN_FINDINGS"
    '''(experimental) The CollectImageScanFindings action collects findings reported by Amazon Inspector for the provided instance.

    :stability: experimental
    '''
    CREATE_IMAGE = "CREATE_IMAGE"
    '''(experimental) The CreateImage action creates an AMI from a running instance with the ec2:CreateImage API.

    :stability: experimental
    '''
    DISTRIBUTE_IMAGE = "DISTRIBUTE_IMAGE"
    '''(experimental) The DistributeImage action copies an AMI using the image's distribution configuration, or using the distribution settings in the step input.

    :stability: experimental
    '''
    EXECUTE_COMPONENTS = "EXECUTE_COMPONENTS"
    '''(experimental) The ExecuteComponents action runs components that are specified in the recipe for the current image being built.

    :stability: experimental
    '''
    EXECUTE_STATE_MACHINE = "EXECUTE_STATE_MACHINE"
    '''(experimental) The ExecuteStateMachine action executes a the state machine provided and waits for completion as part of the workflow.

    :stability: experimental
    '''
    LAUNCH_INSTANCE = "LAUNCH_INSTANCE"
    '''(experimental) The LaunchInstance action launches an instance using the settings from your recipe and infrastructure configuration resources.

    :stability: experimental
    '''
    MODIFY_IMAGE_ATTRIBUTES = "MODIFY_IMAGE_ATTRIBUTES"
    '''(experimental) Applies attribute updates to the provided set of distributed images, such as launch permission updates.

    :stability: experimental
    '''
    RUN_COMMAND = "RUN_COMMAND"
    '''(experimental) The RunCommand action runs a command document against the provided instance.

    :stability: experimental
    '''
    REGISTER_IMAGE = "REGISTER_IMAGE"
    '''(experimental) The RegisterImage action creates an AMI from a set of snapshots with the ec2:RegisterImage API.

    :stability: experimental
    '''
    RUN_SYS_PREP = "RUN_SYS_PREP"
    '''(experimental) The RunSysprep action runs the Sysprep document on the provided Windows instance.

    :stability: experimental
    '''
    SANITIZE_INSTANCE = "SANITIZE_INSTANCE"
    '''(experimental) The SanitizeInstance action runs a recommended sanitization script on Linux instances.

    :stability: experimental
    '''
    TERMINATE_INSTANCE = "TERMINATE_INSTANCE"
    '''(experimental) The TerminateInstance action terminates the provided instance.

    :stability: experimental
    '''
    WAIT_FOR_ACTION = "WAIT_FOR_ACTION"
    '''(experimental) The WaitForAction action pauses the workflow and waits to receive an external signal from the imagebuilder:SendWorkflowStepAction API.

    :stability: experimental
    '''
    WAIT_FOR_SSM_AGENT = "WAIT_FOR_SSM_AGENT"
    '''(experimental) The WaitForSSMAgent action waits for the given instance to have connectivity with SSM before proceeding.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.WorkflowAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "workflow_arn": "workflowArn",
        "workflow_name": "workflowName",
        "workflow_type": "workflowType",
        "workflow_version": "workflowVersion",
    },
)
class WorkflowAttributes:
    def __init__(
        self,
        *,
        workflow_arn: typing.Optional[builtins.str] = None,
        workflow_name: typing.Optional[builtins.str] = None,
        workflow_type: typing.Optional["WorkflowType"] = None,
        workflow_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for an EC2 Image Builder Workflow.

        :param workflow_arn: (experimental) The ARN of the workflow. Default: - the ARN is automatically constructed if a workflowName and workflowType is provided, otherwise a workflowArn is required
        :param workflow_name: (experimental) The name of the workflow. Default: - the name is automatically constructed if a workflowArn is provided, otherwise a workflowName is required
        :param workflow_type: (experimental) The type of the workflow. Default: - the type is automatically constructed if a workflowArn is provided, otherwise a workflowType is required
        :param workflow_version: (experimental) The version of the workflow. Default: x.x.x

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
            
            workflow_attributes = imagebuilder_alpha.WorkflowAttributes(
                workflow_arn="workflowArn",
                workflow_name="workflowName",
                workflow_type=imagebuilder_alpha.WorkflowType.BUILD,
                workflow_version="workflowVersion"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b490bf0126bb9e20ec92b9fc145bcff9bfc9e5981bdb9d4e82b8770c1c28fa5f)
            check_type(argname="argument workflow_arn", value=workflow_arn, expected_type=type_hints["workflow_arn"])
            check_type(argname="argument workflow_name", value=workflow_name, expected_type=type_hints["workflow_name"])
            check_type(argname="argument workflow_type", value=workflow_type, expected_type=type_hints["workflow_type"])
            check_type(argname="argument workflow_version", value=workflow_version, expected_type=type_hints["workflow_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if workflow_arn is not None:
            self._values["workflow_arn"] = workflow_arn
        if workflow_name is not None:
            self._values["workflow_name"] = workflow_name
        if workflow_type is not None:
            self._values["workflow_type"] = workflow_type
        if workflow_version is not None:
            self._values["workflow_version"] = workflow_version

    @builtins.property
    def workflow_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the workflow.

        :default:

        - the ARN is automatically constructed if a workflowName and workflowType is provided, otherwise a
        workflowArn is required

        :stability: experimental
        '''
        result = self._values.get("workflow_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the workflow.

        :default: - the name is automatically constructed if a workflowArn is provided, otherwise a workflowName is required

        :stability: experimental
        '''
        result = self._values.get("workflow_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_type(self) -> typing.Optional["WorkflowType"]:
        '''(experimental) The type of the workflow.

        :default: - the type is automatically constructed if a workflowArn is provided, otherwise a workflowType is required

        :stability: experimental
        '''
        result = self._values.get("workflow_type")
        return typing.cast(typing.Optional["WorkflowType"], result)

    @builtins.property
    def workflow_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the workflow.

        :default: x.x.x

        :stability: experimental
        '''
        result = self._values.get("workflow_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.WorkflowConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "workflow": "workflow",
        "on_failure": "onFailure",
        "parallel_group": "parallelGroup",
        "parameters": "parameters",
    },
)
class WorkflowConfiguration:
    def __init__(
        self,
        *,
        workflow: IWorkflow,
        on_failure: typing.Optional["WorkflowOnFailure"] = None,
        parallel_group: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, "WorkflowParameterValue"]] = None,
    ) -> None:
        '''(experimental) Configuration details for a workflow.

        :param workflow: (experimental) The workflow to execute in the image build.
        :param on_failure: (experimental) The action to take if the workflow fails. Default: WorkflowOnFailure.ABORT
        :param parallel_group: (experimental) The named parallel group to include this workflow in. Workflows in the same parallel group run in parallel of each other. Default: None
        :param parameters: (experimental) The parameters to pass to the workflow at execution time. Default: - none if the workflow has no parameters, otherwise the default parameter values are used

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
            
            # workflow: imagebuilder_alpha.Workflow
            # workflow_parameter_value: imagebuilder_alpha.WorkflowParameterValue
            
            workflow_configuration = imagebuilder_alpha.WorkflowConfiguration(
                workflow=workflow,
            
                # the properties below are optional
                on_failure=imagebuilder_alpha.WorkflowOnFailure.ABORT,
                parallel_group="parallelGroup",
                parameters={
                    "parameters_key": workflow_parameter_value
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae5d30bc53a91c868756c58068d5a287081b77df55c64df09f3498063a378b1b)
            check_type(argname="argument workflow", value=workflow, expected_type=type_hints["workflow"])
            check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
            check_type(argname="argument parallel_group", value=parallel_group, expected_type=type_hints["parallel_group"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "workflow": workflow,
        }
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if parallel_group is not None:
            self._values["parallel_group"] = parallel_group
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def workflow(self) -> IWorkflow:
        '''(experimental) The workflow to execute in the image build.

        :stability: experimental
        '''
        result = self._values.get("workflow")
        assert result is not None, "Required property 'workflow' is missing"
        return typing.cast(IWorkflow, result)

    @builtins.property
    def on_failure(self) -> typing.Optional["WorkflowOnFailure"]:
        '''(experimental) The action to take if the workflow fails.

        :default: WorkflowOnFailure.ABORT

        :stability: experimental
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional["WorkflowOnFailure"], result)

    @builtins.property
    def parallel_group(self) -> typing.Optional[builtins.str]:
        '''(experimental) The named parallel group to include this workflow in.

        Workflows in the same parallel group run in parallel of each
        other.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("parallel_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "WorkflowParameterValue"]]:
        '''(experimental) The parameters to pass to the workflow at execution time.

        :default: - none if the workflow has no parameters, otherwise the default parameter values are used

        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "WorkflowParameterValue"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkflowData(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.WorkflowData",
):
    '''(experimental) Helper class for referencing and uploading workflow data.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        workflow = imagebuilder.Workflow(self, "EncryptedWorkflow",
            workflow_type=imagebuilder.WorkflowType.BUILD,
            kms_key=kms.Key(self, "WorkflowKey"),
            data=imagebuilder.WorkflowData.from_json_object({
                "schema_version": imagebuilder.WorkflowSchemaVersion.V1_0,
                "steps": [{
                    "name": "LaunchBuildInstance",
                    "action": imagebuilder.WorkflowAction.LAUNCH_INSTANCE,
                    "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
                    "inputs": {
                        "wait_for": "ssmAgent"
                    }
                }, {
                    "name": "CreateImage",
                    "action": imagebuilder.WorkflowAction.CREATE_IMAGE,
                    "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
                    "inputs": {
                        "instance_id": "i-123"
                    }
                }, {
                    "name": "TerminateInstance",
                    "action": imagebuilder.WorkflowAction.TERMINATE_INSTANCE,
                    "on_failure": imagebuilder.WorkflowOnFailure.CONTINUE,
                    "inputs": {
                        "instance_id": "i-123"
                    }
                }
                ],
                "outputs": [{
                    "name": "ImageId",
                    "value": "$.stepOutputs.CreateImage.imageId"
                }
                ]
            })
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        path: builtins.str,
        *,
        deploy_time: typing.Optional[builtins.bool] = None,
        display_name: typing.Optional[builtins.str] = None,
        readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IGrantable]] = None,
        source_kms_key: typing.Optional[_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef] = None,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[_aws_cdk_ceddda9d.AssetHashType] = None,
        bundling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow_symlinks: typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode] = None,
        ignore_mode: typing.Optional[_aws_cdk_ceddda9d.IgnoreMode] = None,
    ) -> "S3WorkflowData":
        '''(experimental) Uploads workflow data from a local file to S3 to use as the workflow data.

        :param scope: The construct scope.
        :param id: Identifier of the construct.
        :param path: The local path to the workflow data file.
        :param deploy_time: Whether or not the asset needs to exist beyond deployment time; i.e. are copied over to a different location and not needed afterwards. Setting this property to true has an impact on the lifecycle of the asset, because we will assume that it is safe to delete after the CloudFormation deployment succeeds. For example, Lambda Function assets are copied over to Lambda during deployment. Therefore, it is not necessary to store the asset in S3, so we consider those deployTime assets. Default: false
        :param display_name: A display name for this asset. If supplied, the display name will be used in locations where the asset identifier is printed, like in the CLI progress information. If the same asset is added multiple times, the display name of the first occurrence is used. The default is the construct path of the Asset construct, with respect to the enclosing stack. If the asset is produced by a construct helper function (such as ``lambda.Code.fromAsset()``), this will look like ``MyFunction/Code``. We use the stack-relative construct path so that in the common case where you have multiple stacks with the same asset, we won't show something like ``/MyBetaStack/MyFunction/Code`` when you are actually deploying to production. Default: - Stack-relative construct path
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_kms_key: The ARN of the KMS key used to encrypt the handler code. Default: - the default server-side encryption with Amazon S3 managed keys(SSE-S3) key will be used.
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container or a custom bundling provider. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise
        :param exclude: File paths matching the patterns will be excluded. See ``ignoreMode`` to set the matching behavior. Has no effect on Assets bundled using the ``bundling`` property. Default: - nothing is excluded
        :param follow_symlinks: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param ignore_mode: The ignore behavior to use for ``exclude`` patterns. Default: IgnoreMode.GLOB

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__913a79b6c888d75f8a4ef320c4d6e729ded50f49d548a5cc790dd9ea0c01afff)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        options = _aws_cdk_aws_s3_assets_ceddda9d.AssetOptions(
            deploy_time=deploy_time,
            display_name=display_name,
            readers=readers,
            source_kms_key=source_kms_key,
            asset_hash=asset_hash,
            asset_hash_type=asset_hash_type,
            bundling=bundling,
            exclude=exclude,
            follow_symlinks=follow_symlinks,
            ignore_mode=ignore_mode,
        )

        return typing.cast("S3WorkflowData", jsii.sinvoke(cls, "fromAsset", [scope, id, path, options]))

    @jsii.member(jsii_name="fromInline")
    @builtins.classmethod
    def from_inline(cls, data: builtins.str) -> "WorkflowData":
        '''(experimental) Uses an inline JSON or YAML string as the workflow data.

        :param data: An inline JSON or YAML string representing the workflow data.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cf7dbab53cec8587f90a9f949a9adea406f4b9ca97d2e9302a7d42a735b369f)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        return typing.cast("WorkflowData", jsii.sinvoke(cls, "fromInline", [data]))

    @jsii.member(jsii_name="fromJsonObject")
    @builtins.classmethod
    def from_json_object(
        cls,
        data: typing.Mapping[builtins.str, typing.Any],
    ) -> "WorkflowData":
        '''(experimental) Uses an inline JSON object as the workflow data.

        :param data: An inline JSON object representing the workflow data.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fe6f14c77eadc4671cb27e0c94bdd34f4db1c9033c9c4ed2af36137f2207d98)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        return typing.cast("WorkflowData", jsii.sinvoke(cls, "fromJsonObject", [data]))

    @jsii.member(jsii_name="fromS3")
    @builtins.classmethod
    def from_s3(
        cls,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        key: builtins.str,
    ) -> "S3WorkflowData":
        '''(experimental) References workflow data from a pre-existing S3 object.

        :param bucket: The S3 bucket where the workflow data is stored.
        :param key: The S3 key of the workflow data file.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e65bf6cf6bbd09caf29fbd63b408e6ab154058a71515c02091d3a3dc26448614)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast("S3WorkflowData", jsii.sinvoke(cls, "fromS3", [bucket, key]))

    @jsii.member(jsii_name="render")
    @abc.abstractmethod
    def render(self) -> "WorkflowDataConfig":
        '''(experimental) The rendered workflow data value, for use in CloudFormation.

        - For inline workflows, data is the workflow text
        - For S3-backed workflows, uri is the S3 URL

        :stability: experimental
        '''
        ...


class _WorkflowDataProxy(WorkflowData):
    @jsii.member(jsii_name="render")
    def render(self) -> "WorkflowDataConfig":
        '''(experimental) The rendered workflow data value, for use in CloudFormation.

        - For inline workflows, data is the workflow text
        - For S3-backed workflows, uri is the S3 URL

        :stability: experimental
        '''
        return typing.cast("WorkflowDataConfig", jsii.invoke(self, "render", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, WorkflowData).__jsii_proxy_class__ = lambda : _WorkflowDataProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.WorkflowDataConfig",
    jsii_struct_bases=[],
    name_mapping={"data": "data", "uri": "uri"},
)
class WorkflowDataConfig:
    def __init__(
        self,
        *,
        data: typing.Optional[builtins.str] = None,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The rendered workflow data value, for use in CloudFormation.

        - For inline workflows, data is the workflow text
        - For S3-backed workflows, uri is the S3 URL

        :param data: (experimental) The rendered workflow data, for use in CloudFormation. Default: - none if uri is set
        :param uri: (experimental) The rendered workflow data URI, for use in CloudFormation. Default: - none if data is set

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
            
            workflow_data_config = imagebuilder_alpha.WorkflowDataConfig(
                data="data",
                uri="uri"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abca9452ae65d500dee03120f5a8897cddba519688cb7df2c35f7808b1b0a78d)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data is not None:
            self._values["data"] = data
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def data(self) -> typing.Optional[builtins.str]:
        '''(experimental) The rendered workflow data, for use in CloudFormation.

        :default: - none if uri is set

        :stability: experimental
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''(experimental) The rendered workflow data URI, for use in CloudFormation.

        :default: - none if data is set

        :stability: experimental
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowDataConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.WorkflowOnFailure")
class WorkflowOnFailure(enum.Enum):
    '''(experimental) The action to take if the workflow fails.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        workflow = imagebuilder.Workflow(self, "MyWorkflow",
            workflow_type=imagebuilder.WorkflowType.BUILD,
            data=imagebuilder.WorkflowData.from_json_object({
                "schema_version": imagebuilder.WorkflowSchemaVersion.V1_0,
                "steps": [{
                    "name": "LaunchBuildInstance",
                    "action": imagebuilder.WorkflowAction.LAUNCH_INSTANCE,
                    "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
                    "inputs": {
                        "wait_for": "ssmAgent"
                    }
                }, {
                    "name": "ExecuteComponents",
                    "action": imagebuilder.WorkflowAction.EXECUTE_COMPONENTS,
                    "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
                    "inputs": {
                        "instance_id": "i-123"
                    }
                }, {
                    "name": "CreateImage",
                    "action": imagebuilder.WorkflowAction.CREATE_IMAGE,
                    "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
                    "inputs": {
                        "instance_id": "i-123"
                    }
                }, {
                    "name": "TerminateInstance",
                    "action": imagebuilder.WorkflowAction.TERMINATE_INSTANCE,
                    "on_failure": imagebuilder.WorkflowOnFailure.CONTINUE,
                    "inputs": {
                        "instance_id": "i-123"
                    }
                }
                ],
                "outputs": [{
                    "name": "ImageId",
                    "value": "$.stepOutputs.CreateImage.imageId"
                }
                ]
            })
        )
    '''

    ABORT = "ABORT"
    '''(experimental) Fails the image build if the workflow fails.

    :stability: experimental
    '''
    CONTINUE = "CONTINUE"
    '''(experimental) Continues with the image build if the workflow fails.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.WorkflowParameterType")
class WorkflowParameterType(enum.Enum):
    '''(experimental) The parameter type for the workflow parameter.

    :stability: experimental
    '''

    BOOLEAN = "BOOLEAN"
    '''(experimental) Indicates the workflow parameter has a boolean value.

    :stability: experimental
    '''
    INTEGER = "INTEGER"
    '''(experimental) Indicates the workflow parameter has an integer value.

    :stability: experimental
    '''
    STRING = "STRING"
    '''(experimental) Indicates the workflow parameter has a string value.

    :stability: experimental
    '''
    STRING_LIST = "STRING_LIST"
    '''(experimental) Indicates the workflow parameter has a string list value.

    :stability: experimental
    '''


class WorkflowParameterValue(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.WorkflowParameterValue",
):
    '''(experimental) The parameter value for a workflow parameter.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
        
        workflow_parameter_value = imagebuilder_alpha.WorkflowParameterValue.from_boolean(False)
    '''

    def __init__(self, value: typing.Sequence[builtins.str]) -> None:
        '''
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8390658566480506f37646356b689906719e0fc8ddc32d148d22b3ab3f1c542a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.create(self.__class__, self, [value])

    @jsii.member(jsii_name="fromBoolean")
    @builtins.classmethod
    def from_boolean(cls, value: builtins.bool) -> "WorkflowParameterValue":
        '''(experimental) The value of the parameter as a boolean.

        :param value: The boolean value of the parameter.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__773718d93193fbd15f3a843e768afddc055e8f29bef57e745d13d237c40e45f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("WorkflowParameterValue", jsii.sinvoke(cls, "fromBoolean", [value]))

    @jsii.member(jsii_name="fromInteger")
    @builtins.classmethod
    def from_integer(cls, value: jsii.Number) -> "WorkflowParameterValue":
        '''(experimental) The value of the parameter as an integer.

        :param value: The integer value of the parameter.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__005a2ac7bb593fef8596de2c7606b93ada71b8997a22c2a51229c0e5c2cfe8ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("WorkflowParameterValue", jsii.sinvoke(cls, "fromInteger", [value]))

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, value: builtins.str) -> "WorkflowParameterValue":
        '''(experimental) The value of the parameter as a string.

        :param value: The string value of the parameter.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d10499aad16ad33480a7b70976859f27c7f34b4bb04c017bbcc764105e694bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("WorkflowParameterValue", jsii.sinvoke(cls, "fromString", [value]))

    @jsii.member(jsii_name="fromStringList")
    @builtins.classmethod
    def from_string_list(
        cls,
        values: typing.Sequence[builtins.str],
    ) -> "WorkflowParameterValue":
        '''(experimental) The value of the parameter as a string list.

        :param values: The string list value of the parameter.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86f18020b47f3928303c21a98584964c8d1cf0a2004826f17073b1fdea4e8cf1)
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        return typing.cast("WorkflowParameterValue", jsii.sinvoke(cls, "fromStringList", [values]))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.List[builtins.str]:
        '''(experimental) The rendered parameter value.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "value"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.WorkflowProps",
    jsii_struct_bases=[],
    name_mapping={
        "data": "data",
        "workflow_type": "workflowType",
        "change_description": "changeDescription",
        "description": "description",
        "kms_key": "kmsKey",
        "tags": "tags",
        "workflow_name": "workflowName",
        "workflow_version": "workflowVersion",
    },
)
class WorkflowProps:
    def __init__(
        self,
        *,
        data: WorkflowData,
        workflow_type: "WorkflowType",
        change_description: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workflow_name: typing.Optional[builtins.str] = None,
        workflow_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for creating a Workflow resource.

        :param data: (experimental) The workflow document content that defines the image creation process.
        :param workflow_type: (experimental) The phase in the image build process for which the workflow resource is responsible.
        :param change_description: (experimental) The change description of the workflow. Describes what change has been made in this version of the workflow, or what makes this version different from other versions. Default: None
        :param description: (experimental) The description of the workflow. Default: None
        :param kms_key: (experimental) The KMS key used to encrypt this workflow. Default: - an Image Builder owned key will be used to encrypt the workflow.
        :param tags: (experimental) The tags to apply to the workflow. Default: None
        :param workflow_name: (experimental) The name of the workflow. Default: - a name is generated
        :param workflow_version: (experimental) The version of the workflow. Default: 1.0.0

        :stability: experimental
        :exampleMetadata: infused

        Example::

            workflow = imagebuilder.Workflow(self, "EncryptedWorkflow",
                workflow_type=imagebuilder.WorkflowType.BUILD,
                kms_key=kms.Key(self, "WorkflowKey"),
                data=imagebuilder.WorkflowData.from_json_object({
                    "schema_version": imagebuilder.WorkflowSchemaVersion.V1_0,
                    "steps": [{
                        "name": "LaunchBuildInstance",
                        "action": imagebuilder.WorkflowAction.LAUNCH_INSTANCE,
                        "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
                        "inputs": {
                            "wait_for": "ssmAgent"
                        }
                    }, {
                        "name": "CreateImage",
                        "action": imagebuilder.WorkflowAction.CREATE_IMAGE,
                        "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
                        "inputs": {
                            "instance_id": "i-123"
                        }
                    }, {
                        "name": "TerminateInstance",
                        "action": imagebuilder.WorkflowAction.TERMINATE_INSTANCE,
                        "on_failure": imagebuilder.WorkflowOnFailure.CONTINUE,
                        "inputs": {
                            "instance_id": "i-123"
                        }
                    }
                    ],
                    "outputs": [{
                        "name": "ImageId",
                        "value": "$.stepOutputs.CreateImage.imageId"
                    }
                    ]
                })
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__274786ee77c88aed437f6a3906db52d1f1368518de0534e4edd1c94a4a8299ea)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument workflow_type", value=workflow_type, expected_type=type_hints["workflow_type"])
            check_type(argname="argument change_description", value=change_description, expected_type=type_hints["change_description"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workflow_name", value=workflow_name, expected_type=type_hints["workflow_name"])
            check_type(argname="argument workflow_version", value=workflow_version, expected_type=type_hints["workflow_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data": data,
            "workflow_type": workflow_type,
        }
        if change_description is not None:
            self._values["change_description"] = change_description
        if description is not None:
            self._values["description"] = description
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if tags is not None:
            self._values["tags"] = tags
        if workflow_name is not None:
            self._values["workflow_name"] = workflow_name
        if workflow_version is not None:
            self._values["workflow_version"] = workflow_version

    @builtins.property
    def data(self) -> WorkflowData:
        '''(experimental) The workflow document content that defines the image creation process.

        :stability: experimental
        '''
        result = self._values.get("data")
        assert result is not None, "Required property 'data' is missing"
        return typing.cast(WorkflowData, result)

    @builtins.property
    def workflow_type(self) -> "WorkflowType":
        '''(experimental) The phase in the image build process for which the workflow resource is responsible.

        :stability: experimental
        '''
        result = self._values.get("workflow_type")
        assert result is not None, "Required property 'workflow_type' is missing"
        return typing.cast("WorkflowType", result)

    @builtins.property
    def change_description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The change description of the workflow.

        Describes what change has been made in this version of the workflow, or
        what makes this version different from other versions.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("change_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the workflow.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key used to encrypt this workflow.

        :default: - an Image Builder owned key will be used to encrypt the workflow.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The tags to apply to the workflow.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def workflow_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the workflow.

        :default: - a name is generated

        :stability: experimental
        '''
        result = self._values.get("workflow_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the workflow.

        :default: 1.0.0

        :stability: experimental
        '''
        result = self._values.get("workflow_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.WorkflowSchemaVersion")
class WorkflowSchemaVersion(enum.Enum):
    '''(experimental) The schema version of the workflow.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        workflow = imagebuilder.Workflow(self, "MyWorkflow",
            workflow_type=imagebuilder.WorkflowType.BUILD,
            data=imagebuilder.WorkflowData.from_json_object({
                "schema_version": imagebuilder.WorkflowSchemaVersion.V1_0,
                "steps": [{
                    "name": "LaunchBuildInstance",
                    "action": imagebuilder.WorkflowAction.LAUNCH_INSTANCE,
                    "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
                    "inputs": {
                        "wait_for": "ssmAgent"
                    }
                }, {
                    "name": "ExecuteComponents",
                    "action": imagebuilder.WorkflowAction.EXECUTE_COMPONENTS,
                    "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
                    "inputs": {
                        "instance_id": "i-123"
                    }
                }, {
                    "name": "CreateImage",
                    "action": imagebuilder.WorkflowAction.CREATE_IMAGE,
                    "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
                    "inputs": {
                        "instance_id": "i-123"
                    }
                }, {
                    "name": "TerminateInstance",
                    "action": imagebuilder.WorkflowAction.TERMINATE_INSTANCE,
                    "on_failure": imagebuilder.WorkflowOnFailure.CONTINUE,
                    "inputs": {
                        "instance_id": "i-123"
                    }
                }
                ],
                "outputs": [{
                    "name": "ImageId",
                    "value": "$.stepOutputs.CreateImage.imageId"
                }
                ]
            })
        )
    '''

    V1_0 = "V1_0"
    '''(experimental) Schema version 1.0 for the workflow document.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-imagebuilder-alpha.WorkflowType")
class WorkflowType(enum.Enum):
    '''(experimental) The type of the workflow.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        workflow = imagebuilder.Workflow(self, "EncryptedWorkflow",
            workflow_type=imagebuilder.WorkflowType.BUILD,
            kms_key=kms.Key(self, "WorkflowKey"),
            data=imagebuilder.WorkflowData.from_json_object({
                "schema_version": imagebuilder.WorkflowSchemaVersion.V1_0,
                "steps": [{
                    "name": "LaunchBuildInstance",
                    "action": imagebuilder.WorkflowAction.LAUNCH_INSTANCE,
                    "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
                    "inputs": {
                        "wait_for": "ssmAgent"
                    }
                }, {
                    "name": "CreateImage",
                    "action": imagebuilder.WorkflowAction.CREATE_IMAGE,
                    "on_failure": imagebuilder.WorkflowOnFailure.ABORT,
                    "inputs": {
                        "instance_id": "i-123"
                    }
                }, {
                    "name": "TerminateInstance",
                    "action": imagebuilder.WorkflowAction.TERMINATE_INSTANCE,
                    "on_failure": imagebuilder.WorkflowOnFailure.CONTINUE,
                    "inputs": {
                        "instance_id": "i-123"
                    }
                }
                ],
                "outputs": [{
                    "name": "ImageId",
                    "value": "$.stepOutputs.CreateImage.imageId"
                }
                ]
            })
        )
    '''

    BUILD = "BUILD"
    '''(experimental) Indicates the workflow is for building images.

    :stability: experimental
    '''
    TEST = "TEST"
    '''(experimental) Indicates the workflow is for testing images.

    :stability: experimental
    '''
    DISTRIBUTION = "DISTRIBUTION"
    '''(experimental) Indicates the workflow is for distributing images.

    :stability: experimental
    '''


@jsii.implements(IComponent)
class Component(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.Component",
):
    '''(experimental) Represents an EC2 Image Builder Component.

    :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/manage-components.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        component = imagebuilder.Component(self, "EncryptedComponent",
            platform=imagebuilder.Platform.LINUX,
            kms_key=kms.Key(self, "ComponentKey"),
            data=imagebuilder.ComponentData.from_json_object({
                "schema_version": imagebuilder.ComponentSchemaVersion.V1_0,
                "phases": [{
                    "name": imagebuilder.ComponentPhaseName.BUILD,
                    "steps": [{
                        "name": "secure-setup",
                        "action": imagebuilder.ComponentAction.EXECUTE_BASH,
                        "inputs": {
                            "commands": ["echo \"This component data is encrypted with KMS\""]
                        }
                    }
                    ]
                }
                ]
            })
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        data: ComponentData,
        platform: Platform,
        change_description: typing.Optional[builtins.str] = None,
        component_name: typing.Optional[builtins.str] = None,
        component_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        supported_os_versions: typing.Optional[typing.Sequence[OSVersion]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param data: (experimental) The component document content that defines the build, validation, or test steps to be executed during the image building process.
        :param platform: (experimental) The operating system platform of the component.
        :param change_description: (experimental) The change description of the component. Describes what change has been made in this version of the component, or what makes this version different from other versions. Default: None
        :param component_name: (experimental) The name of the component. Default: - a name is generated
        :param component_version: (experimental) The version of the component. Default: 1.0.0
        :param description: (experimental) The description of the component. Default: None
        :param kms_key: (experimental) The KMS key used to encrypt this component. Default: - an Image Builder owned key will be used to encrypt the component.
        :param supported_os_versions: (experimental) The operating system versions supported by the component. Default: None
        :param tags: (experimental) The tags to apply to the component. Default: None

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__821af830fe4669e7ab6c5b515ddf450036e43237ed7a7ea4daa79141efaecef1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ComponentProps(
            data=data,
            platform=platform,
            change_description=change_description,
            component_name=component_name,
            component_version=component_version,
            description=description,
            kms_key=kms_key,
            supported_os_versions=supported_os_versions,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromComponentArn")
    @builtins.classmethod
    def from_component_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        component_arn: builtins.str,
    ) -> IComponent:
        '''(experimental) Import an existing component given its ARN.

        :param scope: -
        :param id: -
        :param component_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfd3696ebfc0965153ddc80c27294aa75eba17b75effa00c9bb472513a1c896f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument component_arn", value=component_arn, expected_type=type_hints["component_arn"])
        return typing.cast(IComponent, jsii.sinvoke(cls, "fromComponentArn", [scope, id, component_arn]))

    @jsii.member(jsii_name="fromComponentAttributes")
    @builtins.classmethod
    def from_component_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        component_arn: typing.Optional[builtins.str] = None,
        component_name: typing.Optional[builtins.str] = None,
        component_version: typing.Optional[builtins.str] = None,
    ) -> IComponent:
        '''(experimental) Import an existing component by providing its attributes.

        If the component name is provided as an attribute, it
        must be normalized by converting all alphabetical characters to lowercase, and replacing all spaces and underscores
        with hyphens.

        :param scope: -
        :param id: -
        :param component_arn: (experimental) The ARN of the component. Default: - the ARN is automatically constructed if a componentName is provided, otherwise a componentArn is required
        :param component_name: (experimental) The name of the component. Default: - the name is automatically constructed if a componentArn is provided, otherwise a componentName is required
        :param component_version: (experimental) The version of the component. Default: - the latest version of the component, x.x.x

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__855ab91348e9a8f975e485b8a62a964df50c942f63ab667e01e7d63dbb4c7a0e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = ComponentAttributes(
            component_arn=component_arn,
            component_name=component_name,
            component_version=component_version,
        )

        return typing.cast(IComponent, jsii.sinvoke(cls, "fromComponentAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromComponentName")
    @builtins.classmethod
    def from_component_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        component_name: builtins.str,
    ) -> IComponent:
        '''(experimental) Import an existing component given its name.

        The provided name must be normalized by converting all alphabetical
        characters to lowercase, and replacing all spaces and underscores with hyphens.

        :param scope: -
        :param id: -
        :param component_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc6fec412b104b8ebb0eb1becd579dd790fd8b15f8a325c62a139498c1c1e16f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument component_name", value=component_name, expected_type=type_hints["component_name"])
        return typing.cast(IComponent, jsii.sinvoke(cls, "fromComponentName", [scope, id, component_name]))

    @jsii.member(jsii_name="isComponent")
    @builtins.classmethod
    def is_component(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Return whether the given object is a Component.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e53a5c2eecca10be8fe0de193fb3e2a0e5fd9773e5f63ad62b925d179b954fb)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isComponent", [x]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the component.

        :param grantee: The principal.
        :param actions: The list of actions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b5b31f435c4629c89b4f258618167515bf0149ce8e4a65bc41d5edfe8e6e30a)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the component.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42a34b26472675ab353df57d1bba08682c320d94f42e392d792c8cc9e26064be)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="componentArn")
    def component_arn(self) -> builtins.str:
        '''(experimental) The ARN of the component.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "componentArn"))

    @builtins.property
    @jsii.member(jsii_name="componentName")
    def component_name(self) -> builtins.str:
        '''(experimental) The name of the component.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "componentName"))

    @builtins.property
    @jsii.member(jsii_name="componentType")
    def component_type(self) -> builtins.str:
        '''(experimental) The type of the component.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "componentType"))

    @builtins.property
    @jsii.member(jsii_name="componentVersion")
    def component_version(self) -> builtins.str:
        '''(experimental) The version of the component.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "componentVersion"))

    @builtins.property
    @jsii.member(jsii_name="encrypted")
    def encrypted(self) -> builtins.bool:
        '''(experimental) Whether the component is encrypted.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "encrypted"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def _kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "kmsKey"))


@jsii.implements(IDistributionConfiguration)
class DistributionConfiguration(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.DistributionConfiguration",
):
    '''(experimental) Represents an EC2 Image Builder Distribution Configuration.

    :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/manage-distribution-settings.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        infrastructure_configuration = imagebuilder.InfrastructureConfiguration(self, "Infrastructure",
            infrastructure_configuration_name="production-infrastructure",
            instance_types=[
                ec2.InstanceType.of(ec2.InstanceClass.COMPUTE7_INTEL, ec2.InstanceSize.LARGE)
            ],
            vpc=vpc,
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
        )
        
        distribution_configuration = imagebuilder.DistributionConfiguration(self, "Distribution")
        distribution_configuration.add_ami_distributions(
            ami_name="production-ami-{{ imagebuilder:buildDate }}",
            ami_target_account_ids=["123456789012", "098765432109"]
        )
        
        production_pipeline = imagebuilder.ImagePipeline(self, "ProductionPipeline",
            recipe=example_image_recipe,
            infrastructure_configuration=infrastructure_configuration,
            distribution_configuration=distribution_configuration
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        ami_distributions: typing.Optional[typing.Sequence[typing.Union[AmiDistribution, typing.Dict[builtins.str, typing.Any]]]] = None,
        container_distributions: typing.Optional[typing.Sequence[typing.Union[ContainerDistribution, typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        distribution_configuration_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param ami_distributions: (experimental) The list of target regions and associated AMI distribution settings where the built AMI will be distributed. AMI distributions may also be added with the ``addAmiDistributions`` method. Default: None if container distributions are provided. Otherwise, at least one AMI or container distribution must be provided
        :param container_distributions: (experimental) The list of target regions and associated container distribution settings where the built container will be distributed. Container distributions may also be added with the ``addContainerDistributions`` method. Default: None if AMI distributions are provided. Otherwise, at least one AMI or container distribution must be provided
        :param description: (experimental) The description of the distribution configuration. Default: None
        :param distribution_configuration_name: (experimental) The name of the distribution configuration. Default: A name is generated
        :param tags: (experimental) The tags to apply to the distribution configuration. Default: None

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11d3b64e9f6b2ee2d3b14d4e9e47b654d28b8b1fc3fa8dea006c45f12fca43a4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DistributionConfigurationProps(
            ami_distributions=ami_distributions,
            container_distributions=container_distributions,
            description=description,
            distribution_configuration_name=distribution_configuration_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromDistributionConfigurationArn")
    @builtins.classmethod
    def from_distribution_configuration_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        distribution_configuration_arn: builtins.str,
    ) -> IDistributionConfiguration:
        '''(experimental) Import an existing distribution configuration given its ARN.

        :param scope: -
        :param id: -
        :param distribution_configuration_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af172824cb5c143f0efbf3117bc59db39ad72fce677d46a164a9e803d61ec34f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument distribution_configuration_arn", value=distribution_configuration_arn, expected_type=type_hints["distribution_configuration_arn"])
        return typing.cast(IDistributionConfiguration, jsii.sinvoke(cls, "fromDistributionConfigurationArn", [scope, id, distribution_configuration_arn]))

    @jsii.member(jsii_name="fromDistributionConfigurationName")
    @builtins.classmethod
    def from_distribution_configuration_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        distribution_configuration_name: builtins.str,
    ) -> IDistributionConfiguration:
        '''(experimental) Import an existing distribution configuration given its name.

        The provided name must be normalized by converting
        all alphabetical characters to lowercase, and replacing all spaces and underscores with hyphens.

        :param scope: -
        :param id: -
        :param distribution_configuration_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79a8c170425f7540a2fdc34caebbab7f83b2b5dad9f689bd2c9bb8fef61df566)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument distribution_configuration_name", value=distribution_configuration_name, expected_type=type_hints["distribution_configuration_name"])
        return typing.cast(IDistributionConfiguration, jsii.sinvoke(cls, "fromDistributionConfigurationName", [scope, id, distribution_configuration_name]))

    @jsii.member(jsii_name="isDistributionConfiguration")
    @builtins.classmethod
    def is_distribution_configuration(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Return whether the given object is a DistributionConfiguration.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e875d815d7fce8de551a2b7ca7d67241b9174bff80334d12c760431295c2b620)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isDistributionConfiguration", [x]))

    @jsii.member(jsii_name="addAmiDistributions")
    def add_ami_distributions(self, *ami_distributions: AmiDistribution) -> None:
        '''(experimental) Adds AMI distribution settings to the distribution configuration.

        :param ami_distributions: The list of AMI distribution settings to apply.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf357449b11fb13199b1274b1f2ecc286d438f3066b3854934da18ccd64a988)
            check_type(argname="argument ami_distributions", value=ami_distributions, expected_type=typing.Tuple[type_hints["ami_distributions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addAmiDistributions", [*ami_distributions]))

    @jsii.member(jsii_name="addContainerDistributions")
    def add_container_distributions(
        self,
        *container_distributions: ContainerDistribution,
    ) -> None:
        '''(experimental) Adds container distribution settings to the distribution configuration.

        :param container_distributions: The list of container distribution settings to apply.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b84d6f6541e69607800d8d08bd8a584f1abf3776893226fd8020fab23dfb21ac)
            check_type(argname="argument container_distributions", value=container_distributions, expected_type=typing.Tuple[type_hints["container_distributions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addContainerDistributions", [*container_distributions]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the distribution configuration.

        :param grantee: The principal.
        :param actions: The list of actions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b0fd339a1dc53ecc72e60e1ff7801f259edf211b35356c71fbf6f5c32d6367c)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the distribution configuration.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90ca521312fb50ebc6b1949574749352f71bd6afecb49058e89da3130e5b8f73)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="distributionConfigurationArn")
    def distribution_configuration_arn(self) -> builtins.str:
        '''(experimental) The ARN of the distribution configuration.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "distributionConfigurationArn"))

    @builtins.property
    @jsii.member(jsii_name="distributionConfigurationName")
    def distribution_configuration_name(self) -> builtins.str:
        '''(experimental) The name of the distribution configuration.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "distributionConfigurationName"))


@jsii.interface(jsii_type="@aws-cdk/aws-imagebuilder-alpha.IContainerRecipe")
class IContainerRecipe(IRecipeBase, typing_extensions.Protocol):
    '''(experimental) An EC2 Image Builder Container Recipe.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="containerRecipeArn")
    def container_recipe_arn(self) -> builtins.str:
        '''(experimental) The ARN of the container recipe.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="containerRecipeName")
    def container_recipe_name(self) -> builtins.str:
        '''(experimental) The name of the container recipe.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="containerRecipeVersion")
    def container_recipe_version(self) -> builtins.str:
        '''(experimental) The version of the container recipe.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IContainerRecipeProxy(
    jsii.proxy_for(IRecipeBase), # type: ignore[misc]
):
    '''(experimental) An EC2 Image Builder Container Recipe.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-imagebuilder-alpha.IContainerRecipe"

    @builtins.property
    @jsii.member(jsii_name="containerRecipeArn")
    def container_recipe_arn(self) -> builtins.str:
        '''(experimental) The ARN of the container recipe.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "containerRecipeArn"))

    @builtins.property
    @jsii.member(jsii_name="containerRecipeName")
    def container_recipe_name(self) -> builtins.str:
        '''(experimental) The name of the container recipe.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "containerRecipeName"))

    @builtins.property
    @jsii.member(jsii_name="containerRecipeVersion")
    def container_recipe_version(self) -> builtins.str:
        '''(experimental) The version of the container recipe.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "containerRecipeVersion"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IContainerRecipe).__jsii_proxy_class__ = lambda : _IContainerRecipeProxy


@jsii.interface(jsii_type="@aws-cdk/aws-imagebuilder-alpha.IImageRecipe")
class IImageRecipe(IRecipeBase, typing_extensions.Protocol):
    '''(experimental) An EC2 Image Builder Image Recipe.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="imageRecipeArn")
    def image_recipe_arn(self) -> builtins.str:
        '''(experimental) The ARN of the image recipe.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="imageRecipeName")
    def image_recipe_name(self) -> builtins.str:
        '''(experimental) The name of the image recipe.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="imageRecipeVersion")
    def image_recipe_version(self) -> builtins.str:
        '''(experimental) The version of the image recipe.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IImageRecipeProxy(
    jsii.proxy_for(IRecipeBase), # type: ignore[misc]
):
    '''(experimental) An EC2 Image Builder Image Recipe.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-imagebuilder-alpha.IImageRecipe"

    @builtins.property
    @jsii.member(jsii_name="imageRecipeArn")
    def image_recipe_arn(self) -> builtins.str:
        '''(experimental) The ARN of the image recipe.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageRecipeArn"))

    @builtins.property
    @jsii.member(jsii_name="imageRecipeName")
    def image_recipe_name(self) -> builtins.str:
        '''(experimental) The name of the image recipe.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageRecipeName"))

    @builtins.property
    @jsii.member(jsii_name="imageRecipeVersion")
    def image_recipe_version(self) -> builtins.str:
        '''(experimental) The version of the image recipe.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageRecipeVersion"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IImageRecipe).__jsii_proxy_class__ = lambda : _IImageRecipeProxy


@jsii.implements(IImageRecipe)
class ImageRecipe(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ImageRecipe",
):
    '''(experimental) Represents an EC2 Image Builder Image Recipe.

    :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/manage-recipes.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        parameterized_component = imagebuilder.Component.from_component_name(self, "ParameterizedComponent", "my-parameterized-component")
        
        image_recipe = imagebuilder.ImageRecipe(self, "ParameterizedImageRecipe",
            base_image=imagebuilder.BaseImage.from_ssm_parameter_name("/aws/service/ami-amazon-linux-latest/al2023-ami-minimal-kernel-default-x86_64"),
            components=[imagebuilder.ComponentConfiguration(
                component=parameterized_component,
                parameters={
                    "environment": imagebuilder.ComponentParameterValue.from_string("production"),
                    "version": imagebuilder.ComponentParameterValue.from_string("1.0.0")
                }
            )
            ]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        base_image: BaseImage,
        ami_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
        components: typing.Optional[typing.Sequence[typing.Union[ComponentConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        image_recipe_name: typing.Optional[builtins.str] = None,
        image_recipe_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        uninstall_ssm_agent_after_build: typing.Optional[builtins.bool] = None,
        user_data_override: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param base_image: (experimental) The base image for customizations specified in the image recipe.
        :param ami_tags: (experimental) The additional tags to assign to the output AMI generated by the build. Default: None
        :param block_devices: (experimental) The block devices to attach to the instance used for building the image. Default: None
        :param components: (experimental) The list of component configurations to apply in the image build. Default: None
        :param description: (experimental) The description of the image recipe. Default: None
        :param image_recipe_name: (experimental) The name of the image recipe. Default: - a name is generated
        :param image_recipe_version: (experimental) The version of the image recipe. Default: 1.0.x
        :param tags: (experimental) The tags to apply to the image recipe. Default: None
        :param uninstall_ssm_agent_after_build: (experimental) Whether to uninstall the Systems Manager agent from your final build image, prior to creating the new AMI. Default: - this is false if the Systems Manager agent is pre-installed on the base image. Otherwise, this is true.
        :param user_data_override: (experimental) The user data commands to pass to Image Builder build and test EC2 instances. For Linux and macOS, Image Builder uses a default user data script to install the Systems Manager agent. If you override the user data, you must ensure to add commands to install Systems Manager agent, if it is not pre-installed on your base image. Default: None
        :param working_directory: (experimental) The working directory for use during build and test workflows. Default: - the Image Builder default working directory is used. For Linux and macOS builds, this would be /tmp. For Windows builds, this would be C:/

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__377f1255d9b2bf64253588fc57c03a1f7ecce539b30fa201a7a56594cf739272)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ImageRecipeProps(
            base_image=base_image,
            ami_tags=ami_tags,
            block_devices=block_devices,
            components=components,
            description=description,
            image_recipe_name=image_recipe_name,
            image_recipe_version=image_recipe_version,
            tags=tags,
            uninstall_ssm_agent_after_build=uninstall_ssm_agent_after_build,
            user_data_override=user_data_override,
            working_directory=working_directory,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromImageRecipeArn")
    @builtins.classmethod
    def from_image_recipe_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        image_recipe_arn: builtins.str,
    ) -> IImageRecipe:
        '''(experimental) Import an existing image recipe given its ARN.

        :param scope: -
        :param id: -
        :param image_recipe_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fecdc8fa3e2d91789f55e7eaeb1b82a788a201b50b912e81abaf713601252844)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_recipe_arn", value=image_recipe_arn, expected_type=type_hints["image_recipe_arn"])
        return typing.cast(IImageRecipe, jsii.sinvoke(cls, "fromImageRecipeArn", [scope, id, image_recipe_arn]))

    @jsii.member(jsii_name="fromImageRecipeAttributes")
    @builtins.classmethod
    def from_image_recipe_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_recipe_arn: typing.Optional[builtins.str] = None,
        image_recipe_name: typing.Optional[builtins.str] = None,
        image_recipe_version: typing.Optional[builtins.str] = None,
    ) -> IImageRecipe:
        '''(experimental) Import an existing image recipe by providing its attributes.

        If the image recipe name is provided as an attribute,
        it must be normalized by converting all alphabetical characters to lowercase, and replacing all spaces and
        underscores with hyphens.

        :param scope: -
        :param id: -
        :param image_recipe_arn: (experimental) The ARN of the image recipe. Default: - derived from the imageRecipeName
        :param image_recipe_name: (experimental) The name of the image recipe. Default: - derived from the imageRecipeArn
        :param image_recipe_version: (experimental) The version of the image recipe. Default: - derived from imageRecipeArn. if a imageRecipeName is provided, the latest version, x.x.x, will be used

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__246e07386c6c0484a1464b945468555fa45c87a2061bf6aa4034c2490aed7ca7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = ImageRecipeAttributes(
            image_recipe_arn=image_recipe_arn,
            image_recipe_name=image_recipe_name,
            image_recipe_version=image_recipe_version,
        )

        return typing.cast(IImageRecipe, jsii.sinvoke(cls, "fromImageRecipeAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromImageRecipeName")
    @builtins.classmethod
    def from_image_recipe_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        image_recipe_name: builtins.str,
    ) -> IImageRecipe:
        '''(experimental) Import the latest version of an existing image recipe given its name.

        The provided name must be normalized by
        converting all alphabetical characters to lowercase, and replacing all spaces and underscores with hyphens.

        :param scope: -
        :param id: -
        :param image_recipe_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__933ab55f764c78a5f7d7f57303070f1ee38ba91b264a44d2122acd96faa78eb1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_recipe_name", value=image_recipe_name, expected_type=type_hints["image_recipe_name"])
        return typing.cast(IImageRecipe, jsii.sinvoke(cls, "fromImageRecipeName", [scope, id, image_recipe_name]))

    @jsii.member(jsii_name="isImageRecipe")
    @builtins.classmethod
    def is_image_recipe(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Return whether the given object is an ImageRecipe.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4572f5f31fa83dee1ccd58aa102d2bbe0386114cc11f857c3a55dacd29480f1f)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isImageRecipe", [x]))

    @jsii.member(jsii_name="addBlockDevice")
    def add_block_device(
        self,
        *block_devices: _aws_cdk_aws_ec2_ceddda9d.BlockDevice,
    ) -> None:
        '''(experimental) Adds block devices to attach to the instance used for building the image.

        :param block_devices: The list of block devices to attach.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__703b21331388ff1203716594a7d9d938583810ad7cf13c35e311e4600de1d312)
            check_type(argname="argument block_devices", value=block_devices, expected_type=typing.Tuple[type_hints["block_devices"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addBlockDevice", [*block_devices]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the image recipe.

        :param grantee: The principal.
        :param actions: The list of actions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e47afe7dd47a321f5a6cf3c8306a65f7d60cf3661ad72670edd5917ee1b9760)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the image recipe.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7983b53652829dfb75f2107ad2c4f294630c861b138aa4f76b98814c74d22c7d)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="imageRecipeArn")
    def image_recipe_arn(self) -> builtins.str:
        '''(experimental) The ARN of the image recipe.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageRecipeArn"))

    @builtins.property
    @jsii.member(jsii_name="imageRecipeName")
    def image_recipe_name(self) -> builtins.str:
        '''(experimental) The name of the image recipe.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageRecipeName"))

    @builtins.property
    @jsii.member(jsii_name="imageRecipeVersion")
    def image_recipe_version(self) -> builtins.str:
        '''(experimental) The version of the image recipe.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageRecipeVersion"))


class S3WorkflowData(
    WorkflowData,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.S3WorkflowData",
):
    '''(experimental) Helper class for S3-based workflow data references, containing additional permission grant methods on the S3 object.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_imagebuilder_alpha as imagebuilder_alpha
        import aws_cdk as cdk
        from aws_cdk import aws_iam as iam
        from aws_cdk.interfaces import aws_kms as interfaces_kms
        
        # docker_image: cdk.DockerImage
        # grantable: iam.IGrantable
        # key_ref: interfaces_kms.IKeyRef
        # local_bundling: cdk.ILocalBundling
        
        s3_workflow_data = imagebuilder_alpha.S3WorkflowData.from_asset(self, "MyS3WorkflowData", "path",
            asset_hash="assetHash",
            asset_hash_type=cdk.AssetHashType.SOURCE,
            bundling=cdk.BundlingOptions(
                image=docker_image,
        
                # the properties below are optional
                bundling_file_access=cdk.BundlingFileAccess.VOLUME_COPY,
                command=["command"],
                entrypoint=["entrypoint"],
                environment={
                    "environment_key": "environment"
                },
                local=local_bundling,
                network="network",
                output_type=cdk.BundlingOutput.ARCHIVED,
                platform="platform",
                security_opt="securityOpt",
                user="user",
                volumes=[cdk.DockerVolume(
                    container_path="containerPath",
                    host_path="hostPath",
        
                    # the properties below are optional
                    consistency=cdk.DockerVolumeConsistency.CONSISTENT
                )],
                volumes_from=["volumesFrom"],
                working_directory="workingDirectory"
            ),
            deploy_time=False,
            display_name="displayName",
            exclude=["exclude"],
            follow_symlinks=cdk.SymlinkFollowMode.NEVER,
            ignore_mode=cdk.IgnoreMode.GLOB,
            readers=[grantable],
            source_kMSKey=key_ref
        )
    '''

    def __init__(
        self,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        key: builtins.str,
    ) -> None:
        '''
        :param bucket: -
        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98d8491030d8583ac988370c8afc0d793cfde844ad98e26e57bd7b6b711c0a91)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        jsii.create(self.__class__, self, [bucket, key])

    @jsii.member(jsii_name="grantPut")
    def grant_put(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant put permissions to the given grantee for the workflow data in S3.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c6e83526d3b09335919570ad32399de5dd58dbb25aa7ceb261c6b1f6d4bcecf)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantPut", [grantee]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the workflow data in S3.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d4261d3dda500682580e7e1aa1fb68e0bc07199cf41489a866d06f89d98ec66)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="render")
    def render(self) -> WorkflowDataConfig:
        '''(experimental) The rendered workflow data text, for use in CloudFormation.

        :stability: experimental
        '''
        return typing.cast(WorkflowDataConfig, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def _bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, jsii.get(self, "bucket"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def _key(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "key"))


class _S3WorkflowDataProxy(
    S3WorkflowData,
    jsii.proxy_for(WorkflowData), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, S3WorkflowData).__jsii_proxy_class__ = lambda : _S3WorkflowDataProxy


@jsii.implements(IContainerRecipe)
class ContainerRecipeBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ContainerRecipeBase",
):
    '''(experimental) A new or imported Container Recipe.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__208c8eabb8214736ffb40d737cad760649652aa7f2cb5fea48e1475a3fd356f7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant custom actions to the given grantee for the container recipe.

        :param grantee: The principal.
        :param actions: The list of actions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4d7f25e7544c4c73596e565467ab7657c05c81b07a1391cb57c824d00a78cbb)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given grantee for the container recipe.

        :param grantee: The principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e30c9448f74f3feea4ad45c6735400c7d7a8964226d0a4d2909de6e92a1c0f2)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="containerRecipeArn")
    @abc.abstractmethod
    def container_recipe_arn(self) -> builtins.str:
        '''(experimental) The ARN of the container recipe.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="containerRecipeName")
    @abc.abstractmethod
    def container_recipe_name(self) -> builtins.str:
        '''(experimental) The name of the container recipe.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="containerRecipeVersion")
    @abc.abstractmethod
    def container_recipe_version(self) -> builtins.str:
        '''(experimental) The version of the container recipe.

        :stability: experimental
        '''
        ...


class _ContainerRecipeBaseProxy(
    ContainerRecipeBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="containerRecipeArn")
    def container_recipe_arn(self) -> builtins.str:
        '''(experimental) The ARN of the container recipe.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "containerRecipeArn"))

    @builtins.property
    @jsii.member(jsii_name="containerRecipeName")
    def container_recipe_name(self) -> builtins.str:
        '''(experimental) The name of the container recipe.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "containerRecipeName"))

    @builtins.property
    @jsii.member(jsii_name="containerRecipeVersion")
    def container_recipe_version(self) -> builtins.str:
        '''(experimental) The version of the container recipe.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "containerRecipeVersion"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ContainerRecipeBase).__jsii_proxy_class__ = lambda : _ContainerRecipeBaseProxy


class ContainerRecipe(
    ContainerRecipeBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-imagebuilder-alpha.ContainerRecipe",
):
    '''(experimental) Represents an EC2 Image Builder Container Recipe.

    :see: https://docs.aws.amazon.com/imagebuilder/latest/userguide/manage-recipes.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        container_recipe = imagebuilder.ContainerRecipe(self, "MyContainerRecipe",
            base_image=imagebuilder.BaseContainerImage.from_docker_hub("amazonlinux", "latest"),
            target_repository=imagebuilder.Repository.from_ecr(
                ecr.Repository.from_repository_name(self, "Repository", "my-container-repo"))
        )
        
        container_pipeline = imagebuilder.ImagePipeline(self, "MyContainerPipeline",
            recipe=example_container_recipe
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        base_image: BaseContainerImage,
        target_repository: Repository,
        components: typing.Optional[typing.Sequence[typing.Union[ComponentConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
        container_recipe_name: typing.Optional[builtins.str] = None,
        container_recipe_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        dockerfile: typing.Optional[DockerfileData] = None,
        instance_block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_image: typing.Optional[ContainerInstanceImage] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        os_version: typing.Optional[OSVersion] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param base_image: (experimental) The base image for customizations specified in the container recipe.
        :param target_repository: (experimental) The container repository where the output container image is stored.
        :param components: (experimental) The list of component configurations to apply in the image build. Default: None
        :param container_recipe_name: (experimental) The name of the container recipe. Default: a name is generated
        :param container_recipe_version: (experimental) The version of the container recipe. Default: 1.0.x
        :param description: (experimental) The description of the container recipe. Default: None
        :param dockerfile: (experimental) The dockerfile template used to build the container image. Default: - a standard dockerfile template will be generated to pull the base image, perform environment setup, and run all components in the recipe
        :param instance_block_devices: (experimental) The block devices to attach to the instance used for building, testing, and distributing the container image. Default: the block devices of the instance image will be used
        :param instance_image: (experimental) The image to use to launch the instance used for building, testing, and distributing the container image. Default: Image Builder will use the appropriate ECS-optimized AMI
        :param kms_key: (experimental) The KMS key used to encrypt the dockerfile template. Default: None
        :param os_version: (experimental) The operating system (OS) version of the base image. Default: - Image Builder will determine the OS version of the base image, if sourced from a third-party container registry. Otherwise, the OS version of the base image is required.
        :param tags: (experimental) The tags to apply to the container recipe. Default: None
        :param working_directory: (experimental) The working directory for use during build and test workflows. Default: - the Image Builder default working directory is used. For Linux and macOS builds, this would be /tmp. For Windows builds, this would be C:/

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c43f0e93330477cda649da83e59cb360ca0991bdd11d598853a607c0bc8d81db)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ContainerRecipeProps(
            base_image=base_image,
            target_repository=target_repository,
            components=components,
            container_recipe_name=container_recipe_name,
            container_recipe_version=container_recipe_version,
            description=description,
            dockerfile=dockerfile,
            instance_block_devices=instance_block_devices,
            instance_image=instance_image,
            kms_key=kms_key,
            os_version=os_version,
            tags=tags,
            working_directory=working_directory,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromContainerRecipeArn")
    @builtins.classmethod
    def from_container_recipe_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        container_recipe_arn: builtins.str,
    ) -> IContainerRecipe:
        '''(experimental) Import an existing container recipe given its ARN.

        :param scope: -
        :param id: -
        :param container_recipe_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca435b5c344f1c145569303085e9457987de3af99669751c0686e929edeb2fb1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument container_recipe_arn", value=container_recipe_arn, expected_type=type_hints["container_recipe_arn"])
        return typing.cast(IContainerRecipe, jsii.sinvoke(cls, "fromContainerRecipeArn", [scope, id, container_recipe_arn]))

    @jsii.member(jsii_name="fromContainerRecipeAttributes")
    @builtins.classmethod
    def from_container_recipe_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        container_recipe_arn: typing.Optional[builtins.str] = None,
        container_recipe_name: typing.Optional[builtins.str] = None,
        container_recipe_version: typing.Optional[builtins.str] = None,
    ) -> IContainerRecipe:
        '''(experimental) Import an existing container recipe by providing its attributes.

        If the container recipe name is provided as an
        attribute, it must be normalized by converting all alphabetical characters to lowercase, and replacing all spaces
        and underscores with hyphens.

        :param scope: -
        :param id: -
        :param container_recipe_arn: (experimental) The ARN of the container recipe. Default: - derived from containerRecipeName
        :param container_recipe_name: (experimental) The name of the container recipe. Default: - derived from containerRecipeArn
        :param container_recipe_version: (experimental) The version of the container recipe. Default: - derived from containerRecipeArn. if a containerRecipeName is provided, the latest version, x.x.x, will be used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__489199a8433daef7e6806e6132b5ee569bef3d83a5e88388f9cbcc6a1e87ad52)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = ContainerRecipeAttributes(
            container_recipe_arn=container_recipe_arn,
            container_recipe_name=container_recipe_name,
            container_recipe_version=container_recipe_version,
        )

        return typing.cast(IContainerRecipe, jsii.sinvoke(cls, "fromContainerRecipeAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromContainerRecipeName")
    @builtins.classmethod
    def from_container_recipe_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        container_recipe_name: builtins.str,
    ) -> IContainerRecipe:
        '''(experimental) Import the latest version of an existing container recipe given its name.

        The provided name must be normalized by
        converting all alphabetical characters to lowercase, and replacing all spaces and underscores with hyphens.

        :param scope: -
        :param id: -
        :param container_recipe_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66314fe7983c78c5c557a72fe2742ed61fe210cb1a6f8d50652919475653ccfa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument container_recipe_name", value=container_recipe_name, expected_type=type_hints["container_recipe_name"])
        return typing.cast(IContainerRecipe, jsii.sinvoke(cls, "fromContainerRecipeName", [scope, id, container_recipe_name]))

    @jsii.member(jsii_name="isContainerRecipe")
    @builtins.classmethod
    def is_container_recipe(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Return whether the given object is a ContainerRecipe.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6d587699a76f61f7846ce75688ae4688097bac85e94778eeb0f061d2e755eb)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isContainerRecipe", [x]))

    @jsii.member(jsii_name="addInstanceBlockDevice")
    def add_instance_block_device(
        self,
        *instance_block_devices: _aws_cdk_aws_ec2_ceddda9d.BlockDevice,
    ) -> None:
        '''(experimental) Adds block devices to attach to the instance used for building, testing, and distributing the container image.

        :param instance_block_devices: - The list of block devices to attach.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9f5aaf67b2cdb98ad2d3866469c208f6ad586fd1cdcaba963fc0572cbd6040)
            check_type(argname="argument instance_block_devices", value=instance_block_devices, expected_type=typing.Tuple[type_hints["instance_block_devices"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addInstanceBlockDevice", [*instance_block_devices]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="containerRecipeArn")
    def container_recipe_arn(self) -> builtins.str:
        '''(experimental) The ARN of the container recipe.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "containerRecipeArn"))

    @builtins.property
    @jsii.member(jsii_name="containerRecipeName")
    def container_recipe_name(self) -> builtins.str:
        '''(experimental) The name of the container recipe.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "containerRecipeName"))

    @builtins.property
    @jsii.member(jsii_name="containerRecipeVersion")
    def container_recipe_version(self) -> builtins.str:
        '''(experimental) The version of the container recipe.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "containerRecipeVersion"))


__all__ = [
    "AmazonManagedImage",
    "AmazonManagedImageAttributes",
    "AmazonManagedImageOptions",
    "AmiDistribution",
    "AmiLaunchPermission",
    "AwsManagedComponent",
    "AwsManagedComponentAttributes",
    "AwsManagedWorkflow",
    "AwsManagedWorkflowAttributes",
    "AwsMarketplaceComponent",
    "AwsMarketplaceComponentAttributes",
    "BaseContainerImage",
    "BaseImage",
    "Component",
    "ComponentAction",
    "ComponentAttributes",
    "ComponentConfiguration",
    "ComponentConstantValue",
    "ComponentData",
    "ComponentDocument",
    "ComponentDocumentForLoop",
    "ComponentDocumentLoop",
    "ComponentDocumentParameterDefinition",
    "ComponentDocumentPhase",
    "ComponentDocumentStep",
    "ComponentOnFailure",
    "ComponentParameterType",
    "ComponentParameterValue",
    "ComponentPhaseName",
    "ComponentProps",
    "ComponentSchemaVersion",
    "ComponentStepIfCondition",
    "ComponentStepInputs",
    "ContainerDistribution",
    "ContainerInstanceImage",
    "ContainerRecipe",
    "ContainerRecipeAttributes",
    "ContainerRecipeBase",
    "ContainerRecipeProps",
    "ContainerType",
    "DistributionConfiguration",
    "DistributionConfigurationProps",
    "DockerfileData",
    "DockerfileTemplateConfig",
    "FastLaunchConfiguration",
    "HttpTokens",
    "IComponent",
    "IContainerRecipe",
    "IDistributionConfiguration",
    "IImage",
    "IImagePipeline",
    "IImageRecipe",
    "IInfrastructureConfiguration",
    "ILifecyclePolicy",
    "IRecipeBase",
    "IWorkflow",
    "Image",
    "ImageArchitecture",
    "ImageAttributes",
    "ImagePipeline",
    "ImagePipelineProps",
    "ImagePipelineSchedule",
    "ImagePipelineStatus",
    "ImageProps",
    "ImageRecipe",
    "ImageRecipeAttributes",
    "ImageRecipeProps",
    "ImageType",
    "InfrastructureConfiguration",
    "InfrastructureConfigurationLogging",
    "InfrastructureConfigurationProps",
    "LaunchTemplateConfiguration",
    "LifecyclePolicy",
    "LifecyclePolicyAction",
    "LifecyclePolicyActionType",
    "LifecyclePolicyAgeFilter",
    "LifecyclePolicyAmiExclusionRules",
    "LifecyclePolicyCountFilter",
    "LifecyclePolicyDetail",
    "LifecyclePolicyExclusionRules",
    "LifecyclePolicyFilter",
    "LifecyclePolicyImageExclusionRules",
    "LifecyclePolicyProps",
    "LifecyclePolicyResourceSelection",
    "LifecyclePolicyResourceType",
    "LifecyclePolicyStatus",
    "OSVersion",
    "Platform",
    "Repository",
    "RepositoryService",
    "S3ComponentData",
    "S3DockerfileData",
    "S3WorkflowData",
    "SSMParameterConfigurations",
    "ScheduleStartCondition",
    "Tenancy",
    "Workflow",
    "WorkflowAction",
    "WorkflowAttributes",
    "WorkflowConfiguration",
    "WorkflowData",
    "WorkflowDataConfig",
    "WorkflowOnFailure",
    "WorkflowParameterType",
    "WorkflowParameterValue",
    "WorkflowProps",
    "WorkflowSchemaVersion",
    "WorkflowType",
]

publication.publish()

def _typecheckingstub__7947700e1122d5aa4d0d7d9b637c3b9bd5948401fff18ddf1422d9d999866961(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_architecture: ImageArchitecture,
    image_type: ImageType,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d6bd3dc3695283fd4d95f78be62c5a0657d8b9ae95743a91a31109e52c761f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_architecture: ImageArchitecture,
    image_type: ImageType,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b66d2662230092726641e7e4836619556bd9e4b713a6fc4529a28b947f78b58(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_name: builtins.str,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063769c3bafee118e66089b0f686c22bca6dc78fe974fe2edac626a19dfe8ebc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    amazon_managed_image_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a90e0540bc8af83339fcb4098a61e8ec9f39158584ff8fb17117a8fe360fe3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_architecture: ImageArchitecture,
    image_type: ImageType,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0fc5bb0d6de80813a16eb2998d0611a274a576256375f31b472e02f80d78571(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_architecture: ImageArchitecture,
    image_type: ImageType,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__249c269acb30f26f021ece47976db26ca8237f4a85754bfb451ab6e90b553eac(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_architecture: ImageArchitecture,
    image_type: ImageType,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89450646b941985086d014d2c31fe96ddacad781ad42b07676f74f1e017d1ba3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_architecture: ImageArchitecture,
    image_type: ImageType,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f79c89eeed43e42c3aecf4cbbe3d75f1454077443edd9d827a142f4c53e7ee11(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_architecture: ImageArchitecture,
    image_type: ImageType,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f55fa360510b50813985792d1c6504ed9c557eda04ffd0aeae52275952ceb3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_architecture: ImageArchitecture,
    image_type: ImageType,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__259375d42f13f9fadb8c5a63cf0ee57d1f37478062e2d18c6208a89c67bd0bb3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_architecture: ImageArchitecture,
    image_type: ImageType,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020643b3889e3e4a8e90e663491955ea5e8e406ba2fff268471b7c49eae26cc4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_architecture: ImageArchitecture,
    image_type: ImageType,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc810e858fab1db87e4b0c2348c64c1cb5fe9f4079825f70cdbfdfe298c76249(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_architecture: ImageArchitecture,
    image_type: ImageType,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17fe12aaec5fb10118a69b960cf85c1e0779655f8dfb3671c264cdca3d64afa4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_architecture: ImageArchitecture,
    image_type: ImageType,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e78c9c813e22a826ec7fff531cbea709a35dcb0969f8c81e8b00de3c996093(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_architecture: ImageArchitecture,
    image_type: ImageType,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ba66c48751044fc285ce087542041940238dcd0ee33f909aa3970e9d5feced(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_architecture: ImageArchitecture,
    image_type: ImageType,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ea4f3fc7629d971e5d2679cb3e6679b795f4723fbc7a56ac489a030fd4ea81(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_architecture: ImageArchitecture,
    image_type: ImageType,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe55b3cafe893bb3dd918aa59cf063319e9956fd385f2c3e07cd7b17d7b4c24(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_architecture: ImageArchitecture,
    image_type: ImageType,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6c580216396266e53e26e73fe91034e57c6ded616ace3f4f3ffd74c548c8e3(
    *,
    image_name: builtins.str,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ec2d910a894edc13dfa7e84a3c18d579d4c6177a5d686f7deaa9fdc2bff83c8(
    *,
    image_architecture: ImageArchitecture,
    image_type: ImageType,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bbb50c8ed5cb401fdf362f5d0a7b629c2c082dbdaadf32bcf6aef95e968f20b(
    *,
    ami_description: typing.Optional[builtins.str] = None,
    ami_kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ami_launch_permission: typing.Optional[typing.Union[AmiLaunchPermission, typing.Dict[builtins.str, typing.Any]]] = None,
    ami_name: typing.Optional[builtins.str] = None,
    ami_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ami_target_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    fast_launch_configurations: typing.Optional[typing.Sequence[typing.Union[FastLaunchConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
    launch_templates: typing.Optional[typing.Sequence[typing.Union[LaunchTemplateConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
    license_configuration_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    ssm_parameters: typing.Optional[typing.Sequence[typing.Union[SSMParameterConfigurations, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c99475ef38f88d24e515c5d4cfe68b2b801bf8855b6659a379ba52bbf9fc1a2e(
    *,
    account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    is_public_user_group: typing.Optional[builtins.bool] = None,
    organizational_unit_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    organization_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a85b2f57e866c107d58316256ca41b5310ce1316357a3af47fb8c9be257978(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    component_name: typing.Optional[builtins.str] = None,
    component_version: typing.Optional[builtins.str] = None,
    platform: typing.Optional[Platform] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb8b88fb01463e77d65e8b3815c5fe4a9d52d5ed7d626bea7c9e5bdd7e3c933(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    component_name: typing.Optional[builtins.str] = None,
    component_version: typing.Optional[builtins.str] = None,
    platform: typing.Optional[Platform] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1627b69c7ba0f04ae9ab6f1180bac6dcb468a367c684ce2ad9e056fe1b690dd7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    aws_managed_component_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e95cc80beec8557aaefdf226beed47b803646d97e987b28db9a477824f800fe7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    component_name: typing.Optional[builtins.str] = None,
    component_version: typing.Optional[builtins.str] = None,
    platform: typing.Optional[Platform] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b92acbc29e4089fea8f68555361bc22819eb5f63eadda40faf19d3a828fb29fc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    component_name: typing.Optional[builtins.str] = None,
    component_version: typing.Optional[builtins.str] = None,
    platform: typing.Optional[Platform] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69ab4d7f7fe572f41496187a8f5fd08b3dfdbbe78d1aa9cf5265d61d84e8ecbe(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    component_name: typing.Optional[builtins.str] = None,
    component_version: typing.Optional[builtins.str] = None,
    platform: typing.Optional[Platform] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee53616f10cfba26195e210fe4dc7bcff71fa4a63c9e6648e4025ee62fafedcc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    component_name: typing.Optional[builtins.str] = None,
    component_version: typing.Optional[builtins.str] = None,
    platform: typing.Optional[Platform] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19311b8326a0517457ce310fe53e0167cc068a7f8d5c49cc1a577e6fa7d0cd2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    component_name: typing.Optional[builtins.str] = None,
    component_version: typing.Optional[builtins.str] = None,
    platform: typing.Optional[Platform] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32e146149e9a0c45e3993363b6a87d969c0d980b08ea6bb731b42f52f28c04dd(
    *,
    component_name: typing.Optional[builtins.str] = None,
    component_version: typing.Optional[builtins.str] = None,
    platform: typing.Optional[Platform] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a155f9cb076a38ddb30dd0e7f35bafb4d217fd6c93b9a6444aefb8e6c1cc987(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa82bb2164b9cfa3afb41b7c6b512a4c8280e516924674003c4470e1795b483a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7f482a2f0e84d1dca7a602a36a7c76a13441da4fc906eb2f8336be8421fd0f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__912196f13b00352d038c885488f6bfd1c05df8ba4a91cdc34fa1d6116baacc91(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    workflow_name: builtins.str,
    workflow_type: WorkflowType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428931e5241250f9049063f6a8ae1a8929009cefd1a6a9a6c4d357c793a307b4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cfe7323a7ef8ba146a1ddf02e1541eb79936f6f1e05cc1af64ba803c4e98d48(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b9473566d3a776b877c50ed7ed69f1975be749b5da768cabbfb17555871f24(
    *,
    workflow_name: builtins.str,
    workflow_type: WorkflowType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72fea4585ffbd64de79c39d71516ff9636b95dece6fff22dc33683909474b7ea(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    component_name: builtins.str,
    marketplace_product_id: builtins.str,
    component_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7239391743877da3432bdb2ba2d1e3c8b1e460c607e06086757dd481b60551dc(
    *,
    component_name: builtins.str,
    marketplace_product_id: builtins.str,
    component_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f33e6e4838f756e4f6d1484519ed8cda5186a57f5a24b153b4f78b80a4079dd(
    image: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48005f580635b80c73674c7e0c85c6bf5b0a544c29e84be5ee9596eccd9be266(
    repository: builtins.str,
    tag: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5680334c19570bfa7dbe1efa3db41983dfd9a17d9a5cdbeca4c275bd7f83b20a(
    repository: _aws_cdk_aws_ecr_ceddda9d.IRepository,
    tag: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83b8eff102d8e64797bd198891174985269faba6c5197d5b48de485a4c548ed(
    registry_alias: builtins.str,
    repository_name: builtins.str,
    tag: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c454c4618efb367d2f7ae32dcb02cd045d92bb792ff0c83ff7fff3e63d4d9fa3(
    image: IImage,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebf155a76d591443840415d8905e10ede75195d0a4f0adc38e3421e0501ea18d(
    base_container_image_string: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36dd4f2e58924418174005f93bb4ca0a48a8a6821e91ebabcd4caece94d57920(
    image: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2183ddda9c4be9f7f4d3b9c8284f458011b99a2fd8cdb08d3fca5360979b5526(
    ami_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b4bc4ef847aa19f559cc5a935a3e212c4324770f3541b35ece7c02d61706e6(
    image: IImage,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c595dcdab9a4c781c9ad18ce78da524b051e4de8d12c26a390bf96b5ae4574c(
    product_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc8c265a90648821cebcd7fe9c4979868fd28ab3126cbede2318ae61298c484(
    parameter: _aws_cdk_aws_ssm_ceddda9d.IParameter,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__234840a8fb1e1cfb3f78458b770d74f46dd279f3ebef8cf5922473b295655177(
    parameter_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c8c49a907e420333bd6f88018ea7e3635e275a97ef17b77b6272f39e04b9ba(
    base_image_string: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a111ce6a3cc980fdfd78a9c04008d2621e0cdb5a73ac895dcac5188565ad834a(
    *,
    component_arn: typing.Optional[builtins.str] = None,
    component_name: typing.Optional[builtins.str] = None,
    component_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db17d444fe5fcbbca45d94785f2ae1499dd8f616813840a72a68e10c146b1bb8(
    *,
    component: IComponent,
    parameters: typing.Optional[typing.Mapping[builtins.str, ComponentParameterValue]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a022302a19d26bbe18edf3fafb69d72fca2ee4e1f292dafa9ce24d08a9455c(
    type: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963a239c9c403fc6b5a4313e8e62b5aa83e3dfcb87d450ca08bbee183cbac1d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edbe027f8c3d7062dfc1c03bb55eb927c328b9cd602143575a35fa311f551f29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3dd9994d6bd946b1ceac062da8831ad7f0ab68167221bcb1de2b5bf4f1b9389(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    path: builtins.str,
    *,
    deploy_time: typing.Optional[builtins.bool] = None,
    display_name: typing.Optional[builtins.str] = None,
    readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IGrantable]] = None,
    source_kms_key: typing.Optional[_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef] = None,
    asset_hash: typing.Optional[builtins.str] = None,
    asset_hash_type: typing.Optional[_aws_cdk_ceddda9d.AssetHashType] = None,
    bundling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow_symlinks: typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_ceddda9d.IgnoreMode] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5c968d474a4be4f05abdfab6bd5b4d52a49ade7db8a0614bd22bc59fe1dbb4(
    data: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e62d9de5f9eddd59dcfb4d4419326a2af5a8035493101b1595b1a55234425ab(
    data: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__502ae41b418b170f33bf886f3f817d134270c2d3c6d326d7017b7da013816b35(
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4737aa013938586441da1b86dab7eebc204c3816be9ffb4b4666db7f4c154a3c(
    *,
    phases: typing.Sequence[typing.Union[ComponentDocumentPhase, typing.Dict[builtins.str, typing.Any]]],
    schema_version: ComponentSchemaVersion,
    constants: typing.Optional[typing.Mapping[builtins.str, ComponentConstantValue]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, typing.Union[ComponentDocumentParameterDefinition, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7545616e7ad4244bf8e5212a06dc04473a71fef0517840bdfaf4168ea419c44(
    *,
    end: jsii.Number,
    start: jsii.Number,
    update_by: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016c7a2af8ebcf03286820555388bbfa1ccb89028f5f37b87fa3f7cb9dceded7(
    *,
    for_: typing.Optional[typing.Union[ComponentDocumentForLoop, typing.Dict[builtins.str, typing.Any]]] = None,
    for_each: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b765c0d6f7d805699670929833be905f563259a2aec778f1d09ab1ac16f76c5(
    *,
    type: ComponentParameterType,
    default: typing.Any = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3717a69557789288ecb2866be7254e9e0d4db1c92bd936b8be1466c3858d8a51(
    *,
    name: ComponentPhaseName,
    steps: typing.Sequence[typing.Union[ComponentDocumentStep, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da991558ffc8ca306ecc6999d0b287568416629c1073bde551fb7c089193ce5c(
    *,
    action: ComponentAction,
    inputs: ComponentStepInputs,
    name: builtins.str,
    if_: typing.Optional[ComponentStepIfCondition] = None,
    loop: typing.Optional[typing.Union[ComponentDocumentLoop, typing.Dict[builtins.str, typing.Any]]] = None,
    on_failure: typing.Optional[ComponentOnFailure] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e92686cd7276bf6fbf1757d82345ea962a18e656b80715db13df6e5965fd52d6(
    value: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc9ffc8841ac8c6b276316e4a6162663a25683c16942020ec08483a48230b50f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dafb5f8cd0f4ef40e1c882755f37fc5dc1a69e4a81d5826049e0c91bf971be3a(
    *,
    data: ComponentData,
    platform: Platform,
    change_description: typing.Optional[builtins.str] = None,
    component_name: typing.Optional[builtins.str] = None,
    component_version: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    supported_os_versions: typing.Optional[typing.Sequence[OSVersion]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e9b0814cd916ca01f8a7cf48021bfcd01d4c17be3ae2253fe86dd86f93d671(
    if_condition: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7bb86c499fa1670bd8e78f1bd8542abc56e983e69f40e47d32019e6656ffcc(
    if_object: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e53ae7d6d8c31ee6012880e97dd97ea37ce68d0a35e0216830ea8ab676a9ec3(
    input: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e97a2950e23ff264bda320a66d7ece7c77f491b953c2d2b71cb4ece4c553e4(
    inputs_object_list: typing.Sequence[typing.Mapping[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61535270ffc68df1496f99af681d722e10151c09b0576885b939d7919cfb56b2(
    inputs_object: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e915667467bed957a52d2238405ebf79ca421c029bc891bb818483871e32a658(
    *,
    container_repository: Repository,
    container_description: typing.Optional[builtins.str] = None,
    container_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8065edc35db44571f3272fa2f5d9aae7fbbfb5d16c9357f32e5a658c405c1a0f(
    image: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d93b2dfc09202ba4ae97724b390f56f404845aea745c90fe04cb4d3e5fc0ebc(
    ami_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6cd09b34db089ebfb47e92fc0fd184732208254e705dfd87bcd078e1c2e3bed(
    parameter: _aws_cdk_aws_ssm_ceddda9d.IStringParameter,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56573a7aa687996e1d992967b202a4504f01f439a99a85965911ec50d4e46818(
    parameter_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b8ad82c04f1a1c3051ab529af538511f6d05832ca4e51853d741ab13cff44f(
    container_instance_image_string: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__587fb8aeeb95698cf041c0d967899d6df448fbd1674d9c8a635b4ec267fba6d1(
    *,
    container_recipe_arn: typing.Optional[builtins.str] = None,
    container_recipe_name: typing.Optional[builtins.str] = None,
    container_recipe_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96339edaee9e503b1e793c320e5750414456d8a53a1c668b01572bf0b445d29(
    *,
    base_image: BaseContainerImage,
    target_repository: Repository,
    components: typing.Optional[typing.Sequence[typing.Union[ComponentConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
    container_recipe_name: typing.Optional[builtins.str] = None,
    container_recipe_version: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    dockerfile: typing.Optional[DockerfileData] = None,
    instance_block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_image: typing.Optional[ContainerInstanceImage] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    os_version: typing.Optional[OSVersion] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00a08291003318bd50149ef24f2bb14662ca021351848559c22243f8c7a24a58(
    *,
    ami_distributions: typing.Optional[typing.Sequence[typing.Union[AmiDistribution, typing.Dict[builtins.str, typing.Any]]]] = None,
    container_distributions: typing.Optional[typing.Sequence[typing.Union[ContainerDistribution, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    distribution_configuration_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e465c40a4e54b23940290f080c08cfb4e6ed15f3d514e7bdd79e3d61defa78(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    path: builtins.str,
    *,
    deploy_time: typing.Optional[builtins.bool] = None,
    display_name: typing.Optional[builtins.str] = None,
    readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IGrantable]] = None,
    source_kms_key: typing.Optional[_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef] = None,
    asset_hash: typing.Optional[builtins.str] = None,
    asset_hash_type: typing.Optional[_aws_cdk_ceddda9d.AssetHashType] = None,
    bundling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow_symlinks: typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_ceddda9d.IgnoreMode] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33cede864df4d22e89991676d6f5b1c4f6b58443d12df72b1654ba2c708233aa(
    data: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e93bd18936e56d5825914dd93f6f2ebb38b36fbb87c932ff9ab8247a5b6f4ef(
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d3d0c12c8b9d7ab3a72a82829a53da6567d2c621b4751c8ba673fb699f4ce0(
    *,
    dockerfile_template_data: typing.Optional[builtins.str] = None,
    dockerfile_template_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90ae1e7cf235ef00d4a47bdf413ccd7ca19785b18e7f91a75464655f60195df(
    *,
    enabled: typing.Optional[builtins.bool] = None,
    launch_template: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate] = None,
    max_parallel_launches: typing.Optional[jsii.Number] = None,
    target_snapshot_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c05d6ee1a3eb8c5f9b0d715b586bd51b2a253ebbcc8dae51c78ae2c159bf057(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__841448c6baa993d7b4b3033a5490d19f411b8aebe362b78bd7e0490c73bd22d1(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9dae8c4b2356a5fed2efe8df76a59819e04e2a8562b9fe922537ca4b6313be(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e644849da79fab144eff75407555da79d5543225778e3d852909fa3b1a1d2933(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3276ee979b27952851d2f36b668b4bf2f4378adf7731f6e1232dc543a6e49a07(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c182cbdd5bc65235c36e534dba1aa8f309e3c27cf3cbeb87e37885969292af6f(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9a7780ef73c14556994f6fa8819e22a8467694dda3f89e55e75049834c32dc(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd1ad72d6c4a34306ef21742f859f00b83e5f860e5c8f0635b42613c748bd08(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa895de47b9cf1a63c6d30b4d4ad2b01ddb6ce62da9325fd3c7b0690ef173fe(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880ec80536c3f2c5824d0ec9dc299d46bc0d287296538ba1055d8067d2485f7d(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5f38ae4b97b44d57cd707bacec18195907141dfd0a6a91ecc557de931ede97a(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58710cc3d4336254e0af45eff2cdb81c60bd51b9de82d103acaa0231e11de37(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ed6ed74909416a5bc8e1370b5c1b5323a1bd28fa4c06bc20be9b6e44b65cab(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34d3df73810d33135be008062f2a8d78392d9d6f1ba4a4f913358b865df7122(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c481d4265c4c0633be2bc92a50918cf26005b82a53d1963ff1267b8ef2ac8a(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397042635617cd97dddc7588edef7f9dccb7f68ca854c1cc47d962fea44afbf4(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a289aeda75eae7ca4c17b26ae7c52ea260ca4a3a67a382bd19f4f662d99c075d(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8212807ebda9a9c367c21684bb2e3108004d395720b50f556f78ce624e2eeea4(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94429e836818b23a640507fa54b60c37e9aba1345e1ae71b7ca42ec0e323a9e3(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f4ed7436405bcfb3a075aa5c93725806206943d8dbaa96c5cef8dd4d46cae37(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2582830fbd4fc0772d12414b5d2346ecedd7b1bb8582db47fa079012ef22197(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc13bfedf536aa32a04f1ae979b0cdaa79e62a91830c859a47e1f3d9a2f761a(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5899e69104590e773d3aed63c9f3c694bdeb14392efdc65b0fc19700402c68e(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b23a51e11415232274c8ba996b5aa565e9e2abe2f40f1151b846ada69dc201(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d6e4867e55c2c8ef84e31eb5367502ec1ffdb65877ecfdd2caac1ad06699196(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5a2a7384fc07f344d9ad883137648bc3f9d66145ca25702ad1e61d89b6176d(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6302fac9559d479e26025ee1e3d3f2a0a68dd3dc6e7b461db24dc1c755c86162(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030f15c77b2bbcd41794165ded225e1182616669caf96b4f1552a7847a910ea4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    recipe: IRecipeBase,
    deletion_execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    distribution_configuration: typing.Optional[IDistributionConfiguration] = None,
    enhanced_image_metadata_enabled: typing.Optional[builtins.bool] = None,
    execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    image_scanning_ecr_repository: typing.Optional[_aws_cdk_aws_ecr_ceddda9d.IRepository] = None,
    image_scanning_ecr_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_scanning_enabled: typing.Optional[builtins.bool] = None,
    image_tests_enabled: typing.Optional[builtins.bool] = None,
    infrastructure_configuration: typing.Optional[IInfrastructureConfiguration] = None,
    log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workflows: typing.Optional[typing.Sequence[typing.Union[WorkflowConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e00da4d4aafb3e96b734592b50a5507669f6f8282023fea353c83fe9c1e564e5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    image_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56fc3a16ff529463d8b0ab8962cd6f1ebf3f608762e39adbcf06065ecf1034f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_arn: typing.Optional[builtins.str] = None,
    image_name: typing.Optional[builtins.str] = None,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b680e7f46fa34bb4cb6edac51de1a19e1feb086b48d927fa79da1085403365e8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    image_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7fb4700ccff258247b59db28a7c2655a5d913e22e589c292238904f7086ff9d(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__865d936fa059acad61d6ff14ffdfefd15f23d87430302056e830dffa7b486b38(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c15936fdca36c2becea19d37ef971f2656d0b7813cd6a09384905fc9df866fe(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9051a94b754d203fc043136113c5d4ae1992b65e093a7c6d07320e74b29fb3f4(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ed11a9ec065fecf71481ca69df8a28cb8144ba021f0148629a9be5d38ccdab(
    *,
    image_arn: typing.Optional[builtins.str] = None,
    image_name: typing.Optional[builtins.str] = None,
    image_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be256ce26470dd7ce99d85d182fed712c84ad063411b79a3fa8356a67e08da0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    recipe: IRecipeBase,
    description: typing.Optional[builtins.str] = None,
    distribution_configuration: typing.Optional[IDistributionConfiguration] = None,
    enhanced_image_metadata_enabled: typing.Optional[builtins.bool] = None,
    execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    image_log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
    image_pipeline_log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
    image_pipeline_name: typing.Optional[builtins.str] = None,
    image_scanning_ecr_repository: typing.Optional[_aws_cdk_aws_ecr_ceddda9d.IRepository] = None,
    image_scanning_ecr_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_scanning_enabled: typing.Optional[builtins.bool] = None,
    image_tests_enabled: typing.Optional[builtins.bool] = None,
    infrastructure_configuration: typing.Optional[IInfrastructureConfiguration] = None,
    schedule: typing.Optional[typing.Union[ImagePipelineSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[ImagePipelineStatus] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workflows: typing.Optional[typing.Sequence[typing.Union[WorkflowConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8335134c462cc84e1f47b31b9c90894b85ff3b208c66d1c7ad33f21a30dcc75(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    image_pipeline_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3cfc55a44581fac1d29db8a08b9e65bcc8a20bfb45aa6a2b1847c1ae51f057(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    image_pipeline_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d891818b696c2dd9c1b14607b5b4a1d4836d8d38ee7c1ee23a256b28d8034b5e(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5bd77b1c63ad1dc271d0d0ecd4a832c3f5c52bd37a5e803f4725c241fc86af4(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56199255193a2219bb1c8fdd69cf53dcfa094f8133bf9336c26279f6a370af8b(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a9687a4f2667c95aa42534de951075cdd9565d2053d0460f71f89f3630bb16(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe0bb818b71b7f18b19a1dcf3f5addd085a4d3222e3038517cfb3fe2f2c4870(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c699424e12fee7bb387a499563fc8d745b1f9960b9fde89c970a085d73f4d6a2(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd8c06e734f1dfff99b88ca46b23f6ca9d7c17e3c4a92c8840d24b95105307cb(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e7732ef851dae9bf19ad0516fc9c22a37e4b7db10ed679eb6487882d3458ff(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__646672c252d0e8b44005b72edac02caf1fec6e450563792904f586b53881c343(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd5f7c6f1fac7bba012ce49a070a25ba21023d4be1497621395602e1fd557a8(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc825e4f0f338e19e53d39a6529ef7df6b3ffd11090bd2ee19a2bde279c5c885(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82aaa4bd4e0bc03d082c6b8ae3dab095fd8ccf0b642493805a37b078c2d399b(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__313f641cb1f2a65155332a5ecfa65d8620094ba181089054cc5139134f3a5201(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9e2b7ca1149caaaa96b4d3f527cb5b23241d30446acf045fcacf461e8c08a3(
    *,
    recipe: IRecipeBase,
    description: typing.Optional[builtins.str] = None,
    distribution_configuration: typing.Optional[IDistributionConfiguration] = None,
    enhanced_image_metadata_enabled: typing.Optional[builtins.bool] = None,
    execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    image_log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
    image_pipeline_log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
    image_pipeline_name: typing.Optional[builtins.str] = None,
    image_scanning_ecr_repository: typing.Optional[_aws_cdk_aws_ecr_ceddda9d.IRepository] = None,
    image_scanning_ecr_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_scanning_enabled: typing.Optional[builtins.bool] = None,
    image_tests_enabled: typing.Optional[builtins.bool] = None,
    infrastructure_configuration: typing.Optional[IInfrastructureConfiguration] = None,
    schedule: typing.Optional[typing.Union[ImagePipelineSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[ImagePipelineStatus] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workflows: typing.Optional[typing.Sequence[typing.Union[WorkflowConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d90009cac3814f6853f63afe41943fed9768ffe8575410bb897f8d1fb491877(
    *,
    expression: _aws_cdk_aws_events_ceddda9d.Schedule,
    auto_disable_failure_count: typing.Optional[jsii.Number] = None,
    start_condition: typing.Optional[ScheduleStartCondition] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7a30a589b05ea8fe5afc9710649c4fb14c5b638999f1db9faa746a058ab1e4f(
    *,
    recipe: IRecipeBase,
    deletion_execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    distribution_configuration: typing.Optional[IDistributionConfiguration] = None,
    enhanced_image_metadata_enabled: typing.Optional[builtins.bool] = None,
    execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    image_scanning_ecr_repository: typing.Optional[_aws_cdk_aws_ecr_ceddda9d.IRepository] = None,
    image_scanning_ecr_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_scanning_enabled: typing.Optional[builtins.bool] = None,
    image_tests_enabled: typing.Optional[builtins.bool] = None,
    infrastructure_configuration: typing.Optional[IInfrastructureConfiguration] = None,
    log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workflows: typing.Optional[typing.Sequence[typing.Union[WorkflowConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d6cb317a11ae5d32daa6a7eebcee461a9487b2855e894be98b6c1cddc9add0(
    *,
    image_recipe_arn: typing.Optional[builtins.str] = None,
    image_recipe_name: typing.Optional[builtins.str] = None,
    image_recipe_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ba5b495abe1897e0704d43888c87d03025aec08e1d07a8acc0ce089932c6a6(
    *,
    base_image: BaseImage,
    ami_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
    components: typing.Optional[typing.Sequence[typing.Union[ComponentConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    image_recipe_name: typing.Optional[builtins.str] = None,
    image_recipe_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    uninstall_ssm_agent_after_build: typing.Optional[builtins.bool] = None,
    user_data_override: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8672dd2c6991d2ba23136620a37140cb449f0b7606cfe5538649d44bc009387(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    ec2_instance_availability_zone: typing.Optional[builtins.str] = None,
    ec2_instance_host_id: typing.Optional[builtins.str] = None,
    ec2_instance_host_resource_group_arn: typing.Optional[builtins.str] = None,
    ec2_instance_tenancy: typing.Optional[Tenancy] = None,
    http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
    http_tokens: typing.Optional[HttpTokens] = None,
    infrastructure_configuration_name: typing.Optional[builtins.str] = None,
    instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IInstanceProfile] = None,
    instance_types: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceType]] = None,
    key_pair: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IKeyPair] = None,
    logging: typing.Optional[typing.Union[InfrastructureConfigurationLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    notification_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
    resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    terminate_instance_on_failure: typing.Optional[builtins.bool] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35015fe2e49bc142df9482904b92351bbc9b41c560cac1ac06713b2b564cd982(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    infrastructure_configuration_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d30c941bd6f0f1b07145f10c999bbeef38a9fbbc483fdfb4e54de8301a42bd6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    infrastructure_configuration_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653ebae43bf6b6e095ea87727d122e7cab0c8786387877992a5a7e642a846e02(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73bd89218669ef1c777360509401b7db5901968dd024b757f3c75f85ccd1228(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c74f957e8c879932590c0d74b45224a68ab6d8eca577948a171e837ccc4cda(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74cffe7aa25819eaef361f450e04e7112a9f46a9d0138a9696f9723b55a1d31d(
    *,
    s3_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    s3_key_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07545a4f62a3521f9640beafa4b4d7cc1fbe20fc1df54541287ed96ffe7f8e4e(
    *,
    description: typing.Optional[builtins.str] = None,
    ec2_instance_availability_zone: typing.Optional[builtins.str] = None,
    ec2_instance_host_id: typing.Optional[builtins.str] = None,
    ec2_instance_host_resource_group_arn: typing.Optional[builtins.str] = None,
    ec2_instance_tenancy: typing.Optional[Tenancy] = None,
    http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
    http_tokens: typing.Optional[HttpTokens] = None,
    infrastructure_configuration_name: typing.Optional[builtins.str] = None,
    instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IInstanceProfile] = None,
    instance_types: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceType]] = None,
    key_pair: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IKeyPair] = None,
    logging: typing.Optional[typing.Union[InfrastructureConfigurationLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    notification_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
    resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    terminate_instance_on_failure: typing.Optional[builtins.bool] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7488a156223bbf9e56775eef019a0bfc54d1cbe34be84e101b6775196600d51d(
    *,
    launch_template: _aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate,
    account_id: typing.Optional[builtins.str] = None,
    set_default_version: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271dd3ac2c3d06c33753c4bf70e5cd28cce1cef2dbee876e788d779ae69dfa38(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    details: typing.Sequence[typing.Union[LifecyclePolicyDetail, typing.Dict[builtins.str, typing.Any]]],
    resource_selection: typing.Union[LifecyclePolicyResourceSelection, typing.Dict[builtins.str, typing.Any]],
    resource_type: LifecyclePolicyResourceType,
    description: typing.Optional[builtins.str] = None,
    execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    lifecycle_policy_name: typing.Optional[builtins.str] = None,
    status: typing.Optional[LifecyclePolicyStatus] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8d6e9555d5d1ae0956ec47cedab74a03b2ed708cc29831d6e57521697d93b3a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    lifecycle_policy_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ec60504dec766447fdf4acbcc8d3442ac7e4399d368f43fe3bd752231252ff(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    lifecycle_policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bc873f1fcffad5dc3ac5e61b579399350b520d1989d5d72b322ed9ecb69dd7d(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19112552930af6d7588f60ce65a10af56c59c57151ecdd169cc3d9b3de262d14(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__043e3753fbd001f82f0190c1f88995921a471ef4ef3025996236713cc912f5b6(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6575e02812d62404e6b9df0d628cc5ab29363e1a59d64b7eaa21161ce95e3cdc(
    *,
    type: LifecyclePolicyActionType,
    include_amis: typing.Optional[builtins.bool] = None,
    include_containers: typing.Optional[builtins.bool] = None,
    include_snapshots: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183f6aac6170e6f01f4103a4405e21b1793e7f5802b375799ec3c20b24901e5b(
    *,
    age: _aws_cdk_ceddda9d.Duration,
    retain_at_least: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e57835a73ae082e18c324554f09925609de5a9e0d340221eb13c812a7a5b96e(
    *,
    is_public: typing.Optional[builtins.bool] = None,
    last_launched: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    shared_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e92b96d7974adf6a33269bb31e7e79b100ba6b4ded4c01a47f51153348a0c0eb(
    *,
    count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d529b43dd44a438161a3bc5f50e2f1d1073b31e4e5fd63a57e350b93e453c17(
    *,
    action: typing.Union[LifecyclePolicyAction, typing.Dict[builtins.str, typing.Any]],
    filter: typing.Union[LifecyclePolicyFilter, typing.Dict[builtins.str, typing.Any]],
    exclusion_rules: typing.Optional[typing.Union[LifecyclePolicyExclusionRules, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be32a843ef901862ea30ac304ea2b78ca608e710fee49030a9131a7e35b3cd2c(
    *,
    ami_exclusion_rules: typing.Optional[typing.Union[LifecyclePolicyAmiExclusionRules, typing.Dict[builtins.str, typing.Any]]] = None,
    image_exclusion_rules: typing.Optional[typing.Union[LifecyclePolicyImageExclusionRules, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6943d9f9d76b975de1d1f68fa0018543edfef85f0d47efad320e7af88787188(
    *,
    age_filter: typing.Optional[typing.Union[LifecyclePolicyAgeFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    count_filter: typing.Optional[typing.Union[LifecyclePolicyCountFilter, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73d1e60b18534f0b200268d994e117596c824c5090cccc95264352f6ee9764af(
    *,
    tags: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96a0fa69ee38b571f992d146893360a20d2cdedddaaa132dc7696ef2d64792a9(
    *,
    details: typing.Sequence[typing.Union[LifecyclePolicyDetail, typing.Dict[builtins.str, typing.Any]]],
    resource_selection: typing.Union[LifecyclePolicyResourceSelection, typing.Dict[builtins.str, typing.Any]],
    resource_type: LifecyclePolicyResourceType,
    description: typing.Optional[builtins.str] = None,
    execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    lifecycle_policy_name: typing.Optional[builtins.str] = None,
    status: typing.Optional[LifecyclePolicyStatus] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec4ef8fa30361e9ec41e2180c6c210ea22ae393bbfe7d6a9df335ed9b980d38e(
    *,
    recipes: typing.Optional[typing.Sequence[IRecipeBase]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e835db1a09fe43e2d622f4324c6ace2e9dbd991bf060bc80994a8c7f278814(
    platform: Platform,
    os_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff5a2c2e2f508c6ffd9d7b790056aed4fb62718c2288d6565e09783a7327d151(
    platform: Platform,
    os_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf80e8cbc35b94d36db54f92df03bee46b372adfb0f2a76712eaf0f716c17c3e(
    repository: _aws_cdk_aws_ecr_ceddda9d.IRepository,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8cfdd61801a768cf18184f1eb0737a88d90c072ea930a509e6fe06fcff393d8(
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc38fb84d23f869830d4eb53138914295325097f770e7d5bd62c28c8cedaaa0c(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__022e6141b2cc124364e4bd232e91e64e60212165c7aca9e98a54c50a7b0e1bb7(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0acb3c5cf678b9df02a383da86cbaad019f8c0ef0a4d5c4581796756291bcce1(
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__404b4072c58a96918f411d53482b980373a8a636b91cfcee714b014077b4d944(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c5016d23b88559064fded2374377862c2b2efde220704d938420b4822d4af53(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c69f6418914aecbc11661f47678dc487ec81badbe17d0b392aff21a8c9943f(
    *,
    parameter: _aws_cdk_aws_ssm_ceddda9d.IStringParameter,
    ami_account: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterDataType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f61e84e71eb204b9e3eba30cf8cb65b6e523efac1baff856e35fc1d8a7674b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    data: WorkflowData,
    workflow_type: WorkflowType,
    change_description: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workflow_name: typing.Optional[builtins.str] = None,
    workflow_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2978b6779771efb1902d7ba54f2188438a2e979f75f5e32738f71e4096f5d8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    workflow_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5edf9d7cc79b93c3f1a190b9f26e05f09ff1aff7e6f4061d5468b4337d5b469c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    workflow_arn: typing.Optional[builtins.str] = None,
    workflow_name: typing.Optional[builtins.str] = None,
    workflow_type: typing.Optional[WorkflowType] = None,
    workflow_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c33f638af75f2cf96769ae23ad4899df1b36f64fdae79266ecd17f0f6980474(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a50f18b2739cb8fc10502cd31849c39c3268dd0fe52af6086df0b09b20168c0c(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88f0daf052ccf8229d67eb15fdb5ebfbb9650208e655dccf3ed29c06592f378(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b490bf0126bb9e20ec92b9fc145bcff9bfc9e5981bdb9d4e82b8770c1c28fa5f(
    *,
    workflow_arn: typing.Optional[builtins.str] = None,
    workflow_name: typing.Optional[builtins.str] = None,
    workflow_type: typing.Optional[WorkflowType] = None,
    workflow_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae5d30bc53a91c868756c58068d5a287081b77df55c64df09f3498063a378b1b(
    *,
    workflow: IWorkflow,
    on_failure: typing.Optional[WorkflowOnFailure] = None,
    parallel_group: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, WorkflowParameterValue]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__913a79b6c888d75f8a4ef320c4d6e729ded50f49d548a5cc790dd9ea0c01afff(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    path: builtins.str,
    *,
    deploy_time: typing.Optional[builtins.bool] = None,
    display_name: typing.Optional[builtins.str] = None,
    readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IGrantable]] = None,
    source_kms_key: typing.Optional[_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef] = None,
    asset_hash: typing.Optional[builtins.str] = None,
    asset_hash_type: typing.Optional[_aws_cdk_ceddda9d.AssetHashType] = None,
    bundling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow_symlinks: typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_ceddda9d.IgnoreMode] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf7dbab53cec8587f90a9f949a9adea406f4b9ca97d2e9302a7d42a735b369f(
    data: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe6f14c77eadc4671cb27e0c94bdd34f4db1c9033c9c4ed2af36137f2207d98(
    data: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e65bf6cf6bbd09caf29fbd63b408e6ab154058a71515c02091d3a3dc26448614(
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abca9452ae65d500dee03120f5a8897cddba519688cb7df2c35f7808b1b0a78d(
    *,
    data: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8390658566480506f37646356b689906719e0fc8ddc32d148d22b3ab3f1c542a(
    value: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773718d93193fbd15f3a843e768afddc055e8f29bef57e745d13d237c40e45f1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005a2ac7bb593fef8596de2c7606b93ada71b8997a22c2a51229c0e5c2cfe8ed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d10499aad16ad33480a7b70976859f27c7f34b4bb04c017bbcc764105e694bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86f18020b47f3928303c21a98584964c8d1cf0a2004826f17073b1fdea4e8cf1(
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__274786ee77c88aed437f6a3906db52d1f1368518de0534e4edd1c94a4a8299ea(
    *,
    data: WorkflowData,
    workflow_type: WorkflowType,
    change_description: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workflow_name: typing.Optional[builtins.str] = None,
    workflow_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821af830fe4669e7ab6c5b515ddf450036e43237ed7a7ea4daa79141efaecef1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    data: ComponentData,
    platform: Platform,
    change_description: typing.Optional[builtins.str] = None,
    component_name: typing.Optional[builtins.str] = None,
    component_version: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    supported_os_versions: typing.Optional[typing.Sequence[OSVersion]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd3696ebfc0965153ddc80c27294aa75eba17b75effa00c9bb472513a1c896f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    component_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__855ab91348e9a8f975e485b8a62a964df50c942f63ab667e01e7d63dbb4c7a0e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    component_arn: typing.Optional[builtins.str] = None,
    component_name: typing.Optional[builtins.str] = None,
    component_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc6fec412b104b8ebb0eb1becd579dd790fd8b15f8a325c62a139498c1c1e16f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    component_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e53a5c2eecca10be8fe0de193fb3e2a0e5fd9773e5f63ad62b925d179b954fb(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b5b31f435c4629c89b4f258618167515bf0149ce8e4a65bc41d5edfe8e6e30a(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a34b26472675ab353df57d1bba08682c320d94f42e392d792c8cc9e26064be(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d3b64e9f6b2ee2d3b14d4e9e47b654d28b8b1fc3fa8dea006c45f12fca43a4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    ami_distributions: typing.Optional[typing.Sequence[typing.Union[AmiDistribution, typing.Dict[builtins.str, typing.Any]]]] = None,
    container_distributions: typing.Optional[typing.Sequence[typing.Union[ContainerDistribution, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    distribution_configuration_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af172824cb5c143f0efbf3117bc59db39ad72fce677d46a164a9e803d61ec34f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    distribution_configuration_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79a8c170425f7540a2fdc34caebbab7f83b2b5dad9f689bd2c9bb8fef61df566(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    distribution_configuration_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e875d815d7fce8de551a2b7ca7d67241b9174bff80334d12c760431295c2b620(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf357449b11fb13199b1274b1f2ecc286d438f3066b3854934da18ccd64a988(
    *ami_distributions: AmiDistribution,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b84d6f6541e69607800d8d08bd8a584f1abf3776893226fd8020fab23dfb21ac(
    *container_distributions: ContainerDistribution,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0fd339a1dc53ecc72e60e1ff7801f259edf211b35356c71fbf6f5c32d6367c(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ca521312fb50ebc6b1949574749352f71bd6afecb49058e89da3130e5b8f73(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377f1255d9b2bf64253588fc57c03a1f7ecce539b30fa201a7a56594cf739272(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    base_image: BaseImage,
    ami_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
    components: typing.Optional[typing.Sequence[typing.Union[ComponentConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    image_recipe_name: typing.Optional[builtins.str] = None,
    image_recipe_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    uninstall_ssm_agent_after_build: typing.Optional[builtins.bool] = None,
    user_data_override: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fecdc8fa3e2d91789f55e7eaeb1b82a788a201b50b912e81abaf713601252844(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    image_recipe_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__246e07386c6c0484a1464b945468555fa45c87a2061bf6aa4034c2490aed7ca7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_recipe_arn: typing.Optional[builtins.str] = None,
    image_recipe_name: typing.Optional[builtins.str] = None,
    image_recipe_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__933ab55f764c78a5f7d7f57303070f1ee38ba91b264a44d2122acd96faa78eb1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    image_recipe_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4572f5f31fa83dee1ccd58aa102d2bbe0386114cc11f857c3a55dacd29480f1f(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703b21331388ff1203716594a7d9d938583810ad7cf13c35e311e4600de1d312(
    *block_devices: _aws_cdk_aws_ec2_ceddda9d.BlockDevice,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e47afe7dd47a321f5a6cf3c8306a65f7d60cf3661ad72670edd5917ee1b9760(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7983b53652829dfb75f2107ad2c4f294630c861b138aa4f76b98814c74d22c7d(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d8491030d8583ac988370c8afc0d793cfde844ad98e26e57bd7b6b711c0a91(
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6e83526d3b09335919570ad32399de5dd58dbb25aa7ceb261c6b1f6d4bcecf(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d4261d3dda500682580e7e1aa1fb68e0bc07199cf41489a866d06f89d98ec66(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__208c8eabb8214736ffb40d737cad760649652aa7f2cb5fea48e1475a3fd356f7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d7f25e7544c4c73596e565467ab7657c05c81b07a1391cb57c824d00a78cbb(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e30c9448f74f3feea4ad45c6735400c7d7a8964226d0a4d2909de6e92a1c0f2(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c43f0e93330477cda649da83e59cb360ca0991bdd11d598853a607c0bc8d81db(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    base_image: BaseContainerImage,
    target_repository: Repository,
    components: typing.Optional[typing.Sequence[typing.Union[ComponentConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
    container_recipe_name: typing.Optional[builtins.str] = None,
    container_recipe_version: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    dockerfile: typing.Optional[DockerfileData] = None,
    instance_block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_image: typing.Optional[ContainerInstanceImage] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    os_version: typing.Optional[OSVersion] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca435b5c344f1c145569303085e9457987de3af99669751c0686e929edeb2fb1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    container_recipe_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489199a8433daef7e6806e6132b5ee569bef3d83a5e88388f9cbcc6a1e87ad52(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    container_recipe_arn: typing.Optional[builtins.str] = None,
    container_recipe_name: typing.Optional[builtins.str] = None,
    container_recipe_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66314fe7983c78c5c557a72fe2742ed61fe210cb1a6f8d50652919475653ccfa(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    container_recipe_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6d587699a76f61f7846ce75688ae4688097bac85e94778eeb0f061d2e755eb(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9f5aaf67b2cdb98ad2d3866469c208f6ad586fd1cdcaba963fc0572cbd6040(
    *instance_block_devices: _aws_cdk_aws_ec2_ceddda9d.BlockDevice,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IComponent, IContainerRecipe, IDistributionConfiguration, IImage, IImagePipeline, IImageRecipe, IInfrastructureConfiguration, ILifecyclePolicy, IRecipeBase, IWorkflow]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
