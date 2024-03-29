
import json


class JsonBag():
    def __init__(self, json_data : json) -> None:
        self.assign_values(json_data)
        pass
    
    def to_json(self):
        return {
            'kind': self.kind,
            'name': self.name,
            "namespace": self.namespace,
            "workbench_description": self.workbench_description
        }

    def assign_values(self, json_data):
        tmp_obj = json_data["request"]["object"]
        
        self.kind = tmp_obj["kind"]
        self.name = tmp_obj["metadata"]["name"]
        self.namespace = tmp_obj["metadata"]["namespace"]
        self.workbench_description = tmp_obj["metadata"]["annotations"].get("openshift.io/description")