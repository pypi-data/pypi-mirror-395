import json

from zalando_kubectl.models.stackset_ingress_authoritative import (
    StackSetIngressAuthoritative,
)


def mock_get_stacksetingressauthoritative(name: str):
    ingress_def = {
        "apiVersion": "extensions/v1beta1",
        "kind": "Ingress",
        "metadata": {
            "labels": {"application": name, "stackset": name},
            "name": name,
            "ownerReferences": [
                {
                    "apiVersion": "zalando.org/v1",
                    "kind": "StackSet",
                    "name": name,
                    "uid": "7f3085af-9bea-11e8-a6a2-0ab150f5ed66",
                }
            ],
            "annotations": {
                "zalando.org/backend-weights": (
                    '{"' + name + '-v1":70,"' + name + '-v2":30,"' + name + '-v3":0}'
                ),
                "zalando.org/stack-traffic-weights": (
                    '{"' + name + '-v1":60,"' + name + '-v2":40,"' + name + '-v3":0}'
                ),
            },
        },
        "spec": {
            "rules": [
                {
                    "host": f"{name}.mock.zalan.do",
                    "http": {
                        "paths": [
                            {
                                "backend": {
                                    "serviceName": f"{name}-v1",
                                    "servicePort": 80,
                                }
                            },
                            {
                                "backend": {
                                    "serviceName": f"{name}-v2",
                                    "servicePort": 80,
                                }
                            },
                            {
                                "backend": {
                                    "serviceName": f"{name}-v3",
                                    "servicePort": 80,
                                }
                            },
                        ]
                    },
                }
            ]
        },
    }

    stacks_def = {
        "apiversion": "v1",
        "items": [
            {
                "apiversion": "zalando.org/v1",
                "kind": "Stack",
                "metadata": {"name": f"{name}-v1"},
            },
            {
                "apiversion": "zalando.org/v1",
                "kind": "Stack",
                "metadata": {"name": f"{name}-v2"},
            },
            {
                "apiversion": "zalando.org/v1",
                "kind": "Stack",
                "metadata": {"name": f"{name}-v3"},
            },
        ],
    }

    if name == "unusedstacks-ingress":
        ingress_def["metadata"]["annotations"]["zalando.org/backend-weights"] = (
            '{"' + name + '-v1":70,"' + name + '-v2":30}'
        )
        ingress_def["metadata"]["annotations"]["zalando.org/stack-traffic-weights"] = (
            '{"' + name + '-v1":60,"' + name + '-v2":40}'
        )

    return StackSetIngressAuthoritative(ingress_def, stacks_def)


def test_get_traffic_stackset():
    stackset_name = "standard-ingress"
    expected = {
        f"{stackset_name}-v1": {
            "name": f"{stackset_name}-v1",
            "desired": 60,
            "actual": 70,
        },
        f"{stackset_name}-v2": {
            "name": f"{stackset_name}-v2",
            "desired": 40,
            "actual": 30,
        },
        f"{stackset_name}-v3": {
            "name": f"{stackset_name}-v3",
            "desired": 0,
            "actual": 0,
        },
    }
    stackset = mock_get_stacksetingressauthoritative(stackset_name)

    traffic = stackset.get_traffic()
    assert len(traffic) == len(expected)
    for stack in traffic:
        for key in stack:
            assert stack[key] == expected[stack["name"]][key]


def test_get_traffic_unused_stacks():
    stackset_name = "unusedstacks-ingress"
    expected = {
        f"{stackset_name}-v1": {
            "name": f"{stackset_name}-v1",
            "desired": 60,
            "actual": 70,
        },
        f"{stackset_name}-v2": {
            "name": f"{stackset_name}-v2",
            "desired": 40,
            "actual": 30,
        },
        f"{stackset_name}-v3": {
            "name": f"{stackset_name}-v3",
            "desired": 0,
            "actual": 0,
        },
    }
    stackset = mock_get_stacksetingressauthoritative(stackset_name)

    traffic = stackset.get_traffic()
    assert len(traffic) == len(expected)
    for stack in traffic:
        for key in stack:
            assert stack[key] == expected[stack["name"]][key]


def test_set_traffic_weight():
    stackset_name = "standard-ingress"
    expected = {
        f"{stackset_name}-v1": {
            "name": f"{stackset_name}-v1",
            "desired": 80,
            "actual": 70,
        },
        f"{stackset_name}-v2": {
            "name": f"{stackset_name}-v2",
            "desired": 20,
            "actual": 30,
        },
        f"{stackset_name}-v3": {
            "name": f"{stackset_name}-v3",
            "desired": 0,
            "actual": 0,
        },
    }

    stackset = mock_get_stacksetingressauthoritative(stackset_name)

    stackset.set_traffic_weight("standard-ingress-v1", 80)

    traffic = stackset.get_traffic()
    for stack in traffic:
        for key in stack:
            assert stack[key] == expected[stack["name"]][key]


def test_set_traffic_weight_to_unused_stack():
    stackset_name = "unusedstacks-ingress"
    expected = {
        f"{stackset_name}-v1": {
            "name": f"{stackset_name}-v1",
            "desired": 0,
            "actual": 70,
        },
        f"{stackset_name}-v2": {
            "name": f"{stackset_name}-v2",
            "desired": 0,
            "actual": 30,
        },
        f"{stackset_name}-v3": {
            "name": f"{stackset_name}-v3",
            "desired": 100,
            "actual": 0,
        },
    }

    stackset = mock_get_stacksetingressauthoritative(stackset_name)
    stackset.set_traffic_weight(f"{stackset_name}-v3", 100)

    traffic = stackset.get_traffic()
    for stack in traffic:
        for key in stack:
            assert stack[key] == expected[stack["name"]][key]


def test_traffic_distribution():
    stackset_name = "standard-ingress"
    expected = {
        f"{stackset_name}-v1": {
            "name": f"{stackset_name}-v1",
            "desired": 48,
            "actual": 70,
        },
        f"{stackset_name}-v2": {
            "name": f"{stackset_name}-v2",
            "desired": 32,
            "actual": 30,
        },
        f"{stackset_name}-v3": {
            "name": f"{stackset_name}-v3",
            "desired": 20,
            "actual": 0,
        },
    }

    stackset = mock_get_stacksetingressauthoritative(stackset_name)
    stackset.set_traffic_weight("standard-ingress-v3", 20)

    traffic = stackset.get_traffic()
    for stack in traffic:
        for key in stack:
            assert stack[key] == expected[stack["name"]][key]


def test_get_traffic_cmd():
    stackset_name = "standard-ingress"
    stackset = mock_get_stacksetingressauthoritative(stackset_name)

    stackset.set_traffic_weight(f"{stackset_name}-v3", 100)
    _, _, name, _, annotation = stackset.get_traffic_cmd()
    annotation_name, annotation_value = annotation.split("=", 1)

    assert annotation_name == "zalando.org/stack-traffic-weights"
    assert json.loads(annotation_value) == {
        "standard-ingress-v1": 0,
        "standard-ingress-v2": 0,
        "standard-ingress-v3": 100,
    }


def test_force_traffic_option():
    stackset_name = "standard-ingress"
    stackset = mock_get_stacksetingressauthoritative(stackset_name)

    stackset.set_traffic_weight(f"{stackset_name}-v3", 100)
    stackset.force_traffic_weight()

    _, _, name, _, *raw_annotations = stackset.get_traffic_cmd()
    split_annotations = (annotation.split("=", 1) for annotation in raw_annotations)
    annotations = {name: json.loads(value) for name, value in split_annotations}

    expected_value = {
        "standard-ingress-v1": 0,
        "standard-ingress-v2": 0,
        "standard-ingress-v3": 100,
    }
    assert annotations == {
        "zalando.org/stack-traffic-weights": expected_value,
        "zalando.org/backend-weights": expected_value,
    }


def test_no_cmd_when_noupdate():
    stackset_name = "standard-ingress"
    stackset = mock_get_stacksetingressauthoritative(stackset_name)

    res = stackset.get_traffic_cmd()

    assert res is None
