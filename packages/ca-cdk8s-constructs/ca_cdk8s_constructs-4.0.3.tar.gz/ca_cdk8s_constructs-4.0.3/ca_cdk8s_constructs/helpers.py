"""A collection of helper functions for cdk8s applications."""

import cdk8s
from constructs import Construct


def add_labels(construct: Construct, labels: dict[str, str]) -> None:
    """
    Recursively add the supplied labels to all resources in
    the construct and all its children that have a metadata
    property.

    args:
        construct: The construct to add labels to recursively.
        labels: The labels to add to the construct.
    """

    for resource in construct.node.children:
        if hasattr(resource, "metadata") and isinstance(
            resource.metadata, cdk8s.ApiObjectMetadataDefinition
        ):
            for key, value in labels.items():
                resource.metadata.add_label(key, value)
        add_labels(resource, labels)


def add_annotations(construct: Construct, annotations: dict[str, str]) -> None:
    """
    Recursively add the supplied labels to all resources in
    the construct and all its children that have a metadata
    property.

    args:
        construct: The construct to add labels to recursively.
        annotations: The annotations to add to the construct.
    """

    for resource in construct.node.children:
        if hasattr(resource, "metadata") and isinstance(
            resource.metadata, cdk8s.ApiObjectMetadataDefinition
        ):
            for key, value in annotations.items():
                resource.metadata.add_annotation(key, value)
        add_annotations(resource, annotations)
