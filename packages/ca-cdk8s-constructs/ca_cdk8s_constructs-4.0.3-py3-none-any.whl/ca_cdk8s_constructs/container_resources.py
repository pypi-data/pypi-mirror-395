from cdk8s import Size
from cdk8s_plus_32 import ContainerResources, Cpu, CpuResources, MemoryResources


def ca_container_resources(cpu: Cpu, memory: Size):
    """Create a ContainerResources object.

    It is not recommended to set cpu limit so this value is not set by this construct.
    The memory limit will be set equal to the memory request.

    Args:
        cpu: The CPU request.
        memory: The memory request and limit.
    """

    return ContainerResources(
        cpu=CpuResources(
            request=cpu,
        ),
        memory=MemoryResources(
            limit=memory,
            request=memory,
        ),
    )
