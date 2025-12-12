import builtins
import typing
from enum import Enum
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent
from typing import Sequence

import cdk8s
import cdk8s_plus_32
import yaml
from aws_cdk import Duration
from aws_cdk.aws_eks import HelmChart, ICluster
from aws_cdk.aws_s3_assets import Asset
from constructs import Construct


class HelmChartAsset(Construct):
    """
    Asset for a Helm chart that renders anything passed to `Values.resources` as a helm template.
    Not to be used directly, instead use `Cdk8sHelmChart` to deploy a cdk8s chart as a helm chart.
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        name: str,
        version: str,
        app_version: str,
    ) -> None:
        """
        Create an S3 asset for a cdk8s chart.
        """

        super().__init__(scope, id)

        # Create a temporary directory for the chart
        with TemporaryDirectory() as chart_folder:
            # Write the chart spec to the Chart.yaml file
            with open(Path(chart_folder, "Chart.yaml"), "w+") as chart_spec:
                chart_spec.write(
                    yaml.dump(
                        {
                            "apiVersion": "v2",
                            "name": name,
                            "description": f"Generated chart for {name}",
                            "type": "application",
                            "version": version,
                            "appVersion": app_version,
                        }
                    )
                )

            # Write the values.yaml file. This is a single key which will contain
            # the rendered cdk8s chart.
            with open(Path(chart_folder, "values.yaml"), "w+") as values:
                values.write("resources: {}")

            # Create the templates directory
            template_dir = Path(chart_folder, "templates")
            template_dir.mkdir(parents=True)

            # Write the resources.yaml file. This will contain the rendered cdk8s chart.
            with open(Path(template_dir, "resources.yaml"), "w+") as template:
                template.write(
                    dedent(
                        """\
                        {{- range $v := .Values.resources }}
                        ---
                        {{$v | toYaml }}
                        {{- end }}
                        """
                    )
                )

            # Create the chart asset
            self.asset = Asset(self, "Default", path=chart_folder)


class Cdk8sHelmChart(HelmChart):
    """Bundles a cdk8s chart as a Helm chart and deploys the resources it contains.

    Is used in the same way as the `aws-cdk.aws_eks.HelmChart` resource, but instead of `chart` or
    `chart_asset`, pass an instance of `cdk8s.Chart` to `cdk8s_chart`.\

    The cdk8s chart MUST have a namespace specified in the namespace field of the chart.

    Args:
        scope: The scope in which to define this construct.
        id: The scoped construct ID.
        chart_name: The name of the chart.
        app_version: The version of the app to be applied to the chart.
        cluster: The EKS cluster to apply this configuration to.
        cdk8s_chart: The cdk8s chart.
        atomic: Whether or not Helm should treat this operation as atomic; if set, upgrade process rolls back changes made in case of failed upgrade. The --wait flag will be set automatically if --atomic is used. Defaults to False.
        create_namespace: Create namespace if not exist. Defaults to True.
        release: The name of the release. If no release name is given, it will use the last 53 characters of the node's unique id.
        skip_crds: If set, no CRDs will be installed. By default, CRDs are installed if not already present.
        timeout: Amount of time to wait for any individual Kubernetes operation. Maximum 15 minutes. Defaults to Duration.minutes(5).
        version: The chart version to install. If not specified, 1.0 will be used.
        wait: Whether or not Helm should wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment, StatefulSet, or ReplicaSet are in a ready state before marking the release as successful. By default, Helm will not wait before marking release as successful.
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        chart_name: str,
        app_version: str,
        cluster: ICluster,
        cdk8s_chart: cdk8s.Chart,
        atomic: typing.Optional[builtins.bool] = None,
        create_namespace: typing.Optional[builtins.bool] = None,
        release: typing.Optional[builtins.str] = None,
        skip_crds: typing.Optional[builtins.bool] = None,
        timeout: typing.Optional[Duration] = None,
        version: typing.Optional[builtins.str] = None,
        wait: typing.Optional[builtins.bool] = None,
    ) -> None:
        chart_asset = HelmChartAsset(
            scope,
            "Package",
            name=chart_name,
            version=version or "1.0",
            app_version=app_version,
        ).asset

        super().__init__(
            scope,
            id,
            cluster=cluster,
            chart_asset=chart_asset,
            atomic=atomic,
            create_namespace=create_namespace,
            namespace=cdk8s_chart.namespace,
            release=release,
            skip_crds=skip_crds,
            timeout=timeout,
            values={"resources": cdk8s_chart.to_json()},
            wait=wait,
        )


class HelmHookType(Enum):
    """The type of hook to apply.

    pre-install: Executes after templates are rendered, but before any resources are created in Kubernetes
    post-install: Executes after all resources are loaded into Kubernetes
    pre-delete: Executes on a deletion request before any resources are deleted from Kubernetes
    post-delete: Executes on a deletion request after all of the release's resources have been deleted
    pre-upgrade: Executes on an upgrade request after templates are rendered, but before any resources are updated
    post-upgrade: Executes on an upgrade request after all resources have been upgraded
    pre-rollback: Executes on a rollback request after templates are rendered, but before any resources are rolled back
    post-rollback: Executes on a rollback request after all resources have been modified
    test: Executes when the Helm test subcommand is invoked
    """

    PRE_INSTALL = "pre-install"
    POST_INSTALL = "post-install"
    PRE_DELETE = "pre-delete"
    POST_DELETE = "post-delete"
    PRE_UPGRADE = "pre-upgrade"
    POST_UPGRADE = "post-upgrade"
    PRE_ROLLBACK = "pre-rollback"
    POST_ROLLBACK = "post-rollback"
    TEST = "test"


class HelmHookDeletePolicy(Enum):
    """The policy for deleting the hook resource after the hook has been executed.

    before-hook-creation: Delete the previous resource before a new hook is launched
    hook-succeeded: Delete the resource after the hook is successfully executed
    hook-failed: Delete the resource if the hook failed during execution
    """

    HOOK_SUCCEEDED = "hook-succeeded"
    BEFORE_HOOK_CREATION = "before-hook-creation"
    HOOK_FAILED = "hook-failed"


def apply_helm_hook(
    resource: cdk8s_plus_32.Resource,
    hook_types: Sequence[HelmHookType],
    hook_delete_policy: Sequence[HelmHookDeletePolicy] = [
        HelmHookDeletePolicy.BEFORE_HOOK_CREATION
    ],
    weight: int = 0,
) -> None:
    """Apply helm hook annotations to a resource.

    This applies the correct annotations to the resource to ensure that the resource is executed as
    a helm hook if the resource is deployed as a helm chart.

    Args:
        resource: The resource to apply the helm hook to. Must have a metadata attribute with add_annotation method.
        hook_types: The types of hook to apply.
        hook_delete_policy: The policy for deleting the hook resource after the hook has been executed.
        weight: The weight specifies the order in which hooks are executed.
    """

    if not hasattr(resource, "metadata") or not hasattr(resource.metadata, "add_annotation"):
        raise TypeError("Resource must have a metadata attribute with add_annotation method.")

    resource.metadata.add_annotation(
        "helm.sh/hook-delete-policy", ",".join([policy.value for policy in hook_delete_policy])
    )

    resource.metadata.add_annotation(
        "helm.sh/hook", ",".join([hook.value for hook in hook_types])
    )

    resource.metadata.add_annotation("helm.sh/hook-weight", str(weight))
