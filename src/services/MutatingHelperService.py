
class MutatingHelperService:
    def __init__(self) -> None:
        pass

    def add_secret_notation(self, key_name : str, real_value : str):
        return {"op": "add", "path": "/spec/template/spec/containers/0/env/-", "value": {"name": key_name, "value": real_value}}