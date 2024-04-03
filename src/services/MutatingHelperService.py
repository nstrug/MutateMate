
class MutatingHelperService:
    def __init__(self) -> None:
        pass

    def add_secret_for_notebook(self, key_name : str, real_value : str):
        return {"op": "add", "path": "/spec/template/spec/containers/0/env/-", "value": {"name": key_name, "value": real_value}}
    
    def add_secret_for_pipeline(self, task_index : int, key_name : str, real_value : str):
        return {"op": "add", "path": f"/spec/pipelineSpec/tasks/{task_index}/taskSpec/steps/0/env/-", "value": {"name": key_name, "value": real_value}}
    
    def add_resource_for_pipeline(self, task_index : int, cpu_limit : str, ram_limit : str, gpu_limit : str):
        return {
            "op": "add", "path": f"/spec/pipelineSpec/tasks/{task_index}/taskSpec/steps/0/computeResources" , 
                "value": { "limits": { "nvidia.com/gpu": gpu_limit, "cpu": cpu_limit, "memory": ram_limit }
            }
        }