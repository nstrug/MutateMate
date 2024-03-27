
class JsonHelperService():
    def __init__(self) -> None:
        pass

    def get_dict(self, json_data):
        target = {}

        tmp_obj = json_data["request"]["object"]

        target["kind"] = tmp_obj["kind"]
        target["name"] = tmp_obj["metadata"]["name"]
        target["namespace"] = tmp_obj["metadata"]["namespace"]

        return target