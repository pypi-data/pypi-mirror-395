from enum import Enum
from typing import Sequence

from cdk8s import JsonPatch
from cdk8s_plus_32 import Deployment, StatefulSet, Topology


class WhenUnsatisfiable(Enum):
    """Specifies how to deal with a pod if it doesn't satisfy the spread constraint.

    DO_NOT_SCHEDULE: Don't schedule the pod at all.
    SCHEDULE_ANYWAY: Schedule the pod anyway.
    """

    DO_NOT_SCHEDULE = "DoNotSchedule"
    SCHEDULE_ANYWAY = "ScheduleAnyway"


def set_topology_spread(
    target: Deployment | StatefulSet,
    topology_keys: Sequence[Topology] = (Topology.ZONE, Topology.HOSTNAME),
    when_unsatisfiable: WhenUnsatisfiable = WhenUnsatisfiable.SCHEDULE_ANYWAY,
    max_skew: int = 1,
    min_domains: int = 3,
):
    """Set topology spread constraints on a Deployment or StatefulSet.

    This function applies a topology spread constraint to a Deployment or
    StatefulSet to ensure pods are distributed across different Availability
    Zones and Nodes to improve high availability and fault tolerance.

    This function will replace any existing topology spread constraints on the
    Deployment or StatefulSet.

    It will set the maxSkew and minDomains to the provided values for all
    topology keys.

    Args:
        target: The Deployment or StatefulSet to apply the topology spread constraint to.
        topology_keys: The topology keys to spread the pods across.
        when_unsatisfiable: What to do if the pod doesn't satisfy the spread constraint.
        max_skew: The max difference between the number of pods in the most populated domain and the least populated domain.
        min_domains: The minimum number of domains to spread the pods across.
    """

    target._api_object.add_json_patch(
        JsonPatch.replace(
            path="/spec/template/spec/topologySpreadConstraints",
            value=[
                {
                    "maxSkew": max_skew,
                    "minDomains": min_domains,
                    "topologyKey": topology_key.key,
                    "whenUnsatisfiable": when_unsatisfiable.value,
                    "labelSelector": {
                        "matchLabels": target.match_labels,
                    },
                }
                for topology_key in topology_keys
            ],
        )
    )
