import re
from kubernetes import client, config

class KubeWrapperService:
    def __init__(self, kube_base_url : str, kube_access_token : str) -> None:
        self.base_url = kube_base_url
        self.access_token = kube_access_token
        
        self.core_api = self.set_client(kube_base_url, kube_access_token)
        
        pass

    def set_client(self, kube_url, access_token):
        if (kube_url is not None) and (len(kube_url) > 0):
            configuration = client.Configuration()
            configuration.api_key["authorization"] = access_token
            configuration.api_key_prefix['authorization'] = 'Bearer'
            configuration.host = kube_url
            configuration.verify_ssl = False
            #configuration.ssl_ca_cert = '<path_to_cluster_ca_certificate>'

            return client.CoreV1Api(client.ApiClient(configuration))

        config.load_incluster_config()

        return client.CoreV1Api()

    # CPU, RAM, GPU all values related part:
    
    def get_cpu_value(self) -> str:
        return "1"

    def get_ram_value(self) -> str:
        return "1G"

    def get_gpu_value(self) -> str:
        return "1"

    def get_all_resources(self) -> str:
        return self.get_cpu_value(), self.get_ram_value(), self.get_gpu_value()

    ### Secret Part =>

    def get_all_secrets_by_filter(self, secret_namespace : str, filter_names = []) -> dict:
        if(len(filter_names) == 0): return { }
        
        secret_list = { }
        kube_secret_data = self.core_api.list_namespaced_secret(secret_namespace)
        for itm in kube_secret_data.items:
            tmp_name = itm.metadata.name
            if(tmp_name not in filter_names): continue

            secret_list.update(itm.data)
        
        return secret_list

    def get_namespace_definition_hashtags(self, request_json : str) -> list:
        return re.findall(r"#(\w+)", request_json)