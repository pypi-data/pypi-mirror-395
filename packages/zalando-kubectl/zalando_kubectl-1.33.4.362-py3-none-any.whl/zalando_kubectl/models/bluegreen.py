import json


BACKEND_WEIGHTS = "zalando.org/backend-weights"


class BlueGreen:
    def __init__(self, definition):
        self.definition = definition
        self.stacks = {}
        self.stacks_status = {}
        self.to_annotate = {}

        self.weights_annotation = BACKEND_WEIGHTS

        if "annotations" in self.definition["metadata"]:
            backend_weights = self.definition["metadata"]["annotations"].get(
                self.weights_annotation
            )
            if backend_weights:
                self.stacks_status = json.loads(backend_weights)

    def get_name(self):
        return self.definition["metadata"]["name"]

    def get_traffic(self):
        if not self.stacks:
            return []

        traffic = []

        for name, desired in self.stacks.items():
            stack_weights = {"name": name, "actual": self.stacks_status.get(name, 0)}
            if (
                isinstance(desired, int) or isinstance(desired, float)
            ) and desired >= 0:
                stack_weights["desired"] = desired
            traffic.append(stack_weights)

        return traffic

    def set_traffic_weight(self, stack_name: str, weight: float):
        stackset_name = self.get_name()
        if not stack_name.startswith(stackset_name):
            stack_name = stackset_name + "-" + stack_name

        self.validate_traffic_weight(stack_name, weight)

        new_weights = {stack_name: weight}
        new_weight_remain = 100.0 - weight

        to_update = self.get_stacks_to_update()

        traffic_complement = self.get_traffic_complement(stack_name)
        for name in to_update:
            if name != stack_name and to_update[name] != 0.0:
                new_weights[name] = round(
                    to_update[name] * new_weight_remain / traffic_complement
                )

        self.update_stacks(new_weights)

    def validate_traffic_weight(self, stack_name: str, weight: float):
        if stack_name not in self.get_all_stacks():
            raise ValueError(f"Backend {stack_name} does not exist.")

        if len(self.stacks_status) == 1 and weight != 100:
            raise ValueError(f"Stack {stack_name} is the only stack; weight must 100.")

        if self.get_traffic_complement(stack_name) == 0:
            raise ValueError(
                f"All stacks other than {stack_name} have no weight. Please choose a different one."
            )

    def get_stacks_to_update(self):
        return self.stacks

    def get_all_stacks(self):
        return self.stacks_status

    def get_traffic_complement(self, stack_name: str):
        stacks_complement = self.get_stacks_to_update()
        return sum(
            stacks_complement[name] for name in stacks_complement if name != stack_name
        )

    def update_stacks(self, new_weights):
        if new_weights:
            to_update = self.get_stacks_to_update()

            for name in new_weights:
                to_update[name] = new_weights[name]

            new_weights_string = json.dumps(new_weights)
            self.to_annotate[self.weights_annotation] = new_weights_string
            self.definition["metadata"]["annotations"][self.weights_annotation] = (
                new_weights_string
            )

    def get_traffic_cmd(self):
        if self.to_annotate:
            annotations = [f"{k}={self.to_annotate[k]}" for k in self.to_annotate]
            return ("annotate", "ingress", self.get_name(), "--overwrite", *annotations)
