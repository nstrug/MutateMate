
import json


class JsonBag():
    def __init__(self, json_data : json) -> None:
        self.assign_values(json_data)

    def assign_values(self, json_data):
        tmp_obj = json_data["request"]["object"]
        
        self.kind = tmp_obj["kind"]
        self.name = tmp_obj["metadata"]["name"]
        self.namespace = tmp_obj["metadata"]["namespace"]
        self.workbench_description = tmp_obj["metadata"]["annotations"]["openshift.io/description"]