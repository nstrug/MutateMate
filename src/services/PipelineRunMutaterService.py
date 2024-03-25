
import json


class PipelineRunMutaterService:
    def __init__(self) -> None:
        pass

    def mutate(self, data : json, secrets : dict, cpu : str, ram : str, gpu : str) -> json:
        data["metadata"]["labels"]["MutatingMate"] = "PipelineRunMutater"
        data = self.assign_secrets(data, secrets)

        return data

    def assign_secrets(self, data_json : json, secrets : dict) -> json:
        tmp_tasks = data_json["spec"]["pipelineSpec"]["tasks"]

        for itm_task in tmp_tasks:
            tmp_env = itm_task["taskSpec"]["steps"][0]["env"]            

            for secret_key, secret_value in secrets.items():
                tmp_env.append({ "name":secret_key, "value": secret_value })
        
        return data_json