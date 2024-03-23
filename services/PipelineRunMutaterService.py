
import json


class PipelineRunMutaterService:
    def __init__(self) -> None:
        pass

    def mutate(self, data : json, secrets : dict, cpu : str, ram : str, gpu : str) -> json:
        data = self.assign_secrets(data, secrets)

        return data

    def assign_secrets(self, data_json : json, secrets : dict) -> json:
        tmp_tasks = data_json["spec"]["pipelineSpec"]["task"]

        for itm_task in tmp_tasks:
            tmp_env = itm_task["taskSpec"]["steps"]["0"]["env"]

            for secret_key, secret_value in secrets.items():
                tmp_env.append(secret_key, secret_value)
        
        return data_json