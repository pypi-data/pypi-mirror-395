from cdk8s_plus_32 import Workload
from cdk8s_plus_32.k8s import (
    IntOrString,
    KubePodDisruptionBudget,
    LabelSelector,
    PodDisruptionBudgetSpec,
)
from constructs import Construct


def ca_pod_disruption_budget(
    scope: Construct,
    id: str,
    target: Workload,
    max_unavailable: int = 1,
) -> KubePodDisruptionBudget:
    """Create a PodDisruptionBudget for a deployment.

    The match_labels can be extracted from a Deployment or StatefulSet using the `match_labels` property.

    Args:
        scope: The scope of the construct.
        id: ID for the construct.
        target: The target to create a PodDisruptionBudget for. Usually a Deployment or StatefulSet.
        max_unavailable: The maximum number of unavailable pods. Defaults to 1.

    Returns:
        A PodDisruptionBudget.
    """
    return KubePodDisruptionBudget(
        scope,
        id,
        spec=PodDisruptionBudgetSpec(
            max_unavailable=IntOrString.from_number(max_unavailable),
            selector=LabelSelector(match_labels=target.match_labels),
        ),
    )
