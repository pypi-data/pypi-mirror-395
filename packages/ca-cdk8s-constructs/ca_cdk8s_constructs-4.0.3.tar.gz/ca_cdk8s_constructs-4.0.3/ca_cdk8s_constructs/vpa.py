import enum

from cdk8s_plus_32 import Cpu, Workload
from constructs import Construct

from ca_cdk8s_constructs.imports.io.k8s.autoscaling import (
    VerticalPodAutoscaler,
    VerticalPodAutoscalerSpec,
    VerticalPodAutoscalerSpecResourcePolicy,
    VerticalPodAutoscalerSpecResourcePolicyContainerPolicies,
    VerticalPodAutoscalerSpecResourcePolicyContainerPoliciesMinAllowed,
    VerticalPodAutoscalerSpecTargetRef,
    VerticalPodAutoscalerSpecUpdatePolicy,
    VerticalPodAutoscalerSpecUpdatePolicyUpdateMode,
)


class VpaUpdateMode(enum.Enum):
    """Update modes for Vertical Pod Autoscaler.

    The different modes are:
    - OFF: VPA will only provide the recommendations, and it will not automatically change resource requirements.
    - INITIAL: VPA only assigns resource requests on pod creation and never changes them later.
    - RECREATE: VPA assigns resource requests on pod creation time and updates them on existing pods by evicting and recreating them.
    - AUTO: It recreates the pod based on the recommendation.
    """

    OFF = "off"
    INITIAL = "initial"
    RECREATE = "recreate"
    AUTO = "auto"

    def to_vpa_mode(self) -> VerticalPodAutoscalerSpecUpdatePolicyUpdateMode:
        """Convert to the underlying VPA update mode enum."""
        mode_map = {
            VpaUpdateMode.OFF: VerticalPodAutoscalerSpecUpdatePolicyUpdateMode.OFF,
            VpaUpdateMode.INITIAL: VerticalPodAutoscalerSpecUpdatePolicyUpdateMode.INITIAL,
            VpaUpdateMode.RECREATE: VerticalPodAutoscalerSpecUpdatePolicyUpdateMode.RECREATE,
            VpaUpdateMode.AUTO: VerticalPodAutoscalerSpecUpdatePolicyUpdateMode.AUTO,
        }
        return mode_map[self]


def ca_vpa(
    scope: Construct,
    id: str,
    target: Workload,
    min_allowed_cpu: Cpu = Cpu.millis(100),
    update_mode: VpaUpdateMode = VpaUpdateMode.AUTO,
) -> VerticalPodAutoscaler:
    """Returns a VerticalPodAutoscaler for a target.

    The minimum allowed CPU is the minimum CPU that the VPA will assign to the pod. This is applied to all containers in the pod.

    Args:
        scope: The scope of the construct.
        id: The id of the construct.
        target: The target to autoscale.
        min_allowed_cpu: The minimum allowed CPU in millicores. Defaults to 100.
        update_mode: The update mode to use. Defaults to VpaUpdateMode.AUTO.

    Returns:
        A VerticalPodAutoscaler.
    """

    return VerticalPodAutoscaler(
        scope,
        id,
        spec=VerticalPodAutoscalerSpec(
            target_ref=VerticalPodAutoscalerSpecTargetRef(
                api_version=target.api_version,
                kind=target.kind,
                name=target.name,
            ),
            update_policy=VerticalPodAutoscalerSpecUpdatePolicy(
                update_mode=update_mode.to_vpa_mode()
            ),
            resource_policy=VerticalPodAutoscalerSpecResourcePolicy(
                container_policies=[
                    VerticalPodAutoscalerSpecResourcePolicyContainerPolicies(
                        container_name=container.name,
                        min_allowed={
                            "cpu": VerticalPodAutoscalerSpecResourcePolicyContainerPoliciesMinAllowed.from_string(
                                min_allowed_cpu.amount
                            )
                        },
                    )
                    for container in target.containers
                ]
            ),
        ),
    )
