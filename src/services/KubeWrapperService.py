import re
import base64
from kubernetes import client, config

from services.JsonBag import JsonBag

class KubeWrapperService:
    def __init__(self, kube_base_url : str, kube_access_token : str) -> None:
        self.base_url = kube_base_url
        self.access_token = kube_access_token
        
        self.set_client(kube_base_url, kube_access_token)
        
        pass

    def set_client(self, kube_url, access_token):
        if (kube_url is not None) and (len(kube_url) > 0):
            configuration = client.Configuration()
            configuration.api_key["authorization"] = access_token
            configuration.api_key_prefix['authorization'] = 'Bearer'
            configuration.host = kube_url
            configuration.verify_ssl = False

            self.custom_api = client.CustomObjectsApi(client.ApiClient(configuration))
            self.core_api =  client.CoreV1Api(client.ApiClient(configuration))
        else:
            config.load_incluster_config()

            self.core_api =  client.CoreV1Api()
            self.custom_api = client.CustomObjectsApi()
        
        pass

    # CPU, RAM, GPU all values related part:
    
    def get_cpu_value(self) -> str:
        return "1"

    def get_ram_value(self) -> str:
        return "1G"

    def get_gpu_value(self) -> str:
        return "1"

    def get_all_resources(self) -> str:
        return self.get_cpu_value(), self.get_ram_value(), self.get_gpu_value()
    
    ### Notebook Info Retreival =>

    def get_notebook_info(self, request_data : JsonBag):
        filter_nms =f'metadata.namespace={request_data.namespace}'
        tmp_notebooks = self.custom_api.list_cluster_custom_object(group="kubeflow.org", version="v1", plural="notebooks", field_selector=filter_nms)

        all_secrets = []
        all_cpu = []
        all_ram = []
        all_gpu =[]

        for itm in tmp_notebooks.get("items"):
            tmp_desc = itm["metadata"]["annotations"].get("openshift.io/description")
            if(len(tmp_desc) > 0): 
                tmp_spltd = self.get_hashtags_from_description(tmp_desc)
                all_secrets = all_secrets + tmp_spltd

            tmp_container = itm["spec"]["template"]["spec"]["containers"][0]

            tmp_cpu = tmp_container["resources"]["limits"]["cpu"]
            all_cpu.append(tmp_cpu)

            tmp_ram = tmp_container["resources"]["limits"]["memory"]
            all_ram.append(tmp_ram)

            tmp_gpu = tmp_container["resources"]["limits"].get("nvidia.com/gpu")
            if (tmp_gpu is not None) and (len(tmp_gpu) > 0): all_gpu.append(tmp_gpu)

            pass
        
        pass

    ### Secret Part =>

    def get_all_secrets_by_filter(self, secret_namespace : str, filter_names = []) -> dict:
        if(len(filter_names) == 0): return { }
        
        secret_list = { }
        kube_secret_data = self.core_api.list_namespaced_secret(secret_namespace)
        for itm in kube_secret_data.items:
            tmp_name = itm.metadata.name
            if(tmp_name not in filter_names): continue

            secret_list.update(itm.data)
        
        for itm_key, itm_value in secret_list.items():
            secret_list[itm_key] = base64.b64decode(itm_value).decode('utf-8')
        
        return secret_list

    def get_hashtags_from_description(self, description_text : str) -> list:
        return re.findall(r"#(\w+)", description_text)