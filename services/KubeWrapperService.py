
class KubeWrapperService:
    def __init__(self, kube_base_url : str, kube_access_token : str) -> None:
        self.base_url = kube_base_url
        self.access_token = kube_access_token
        
        self.gather_all_resources(kube_base_url, kube_access_token)
        
        pass

    def gather_all_resources(self, url, access_token):
        pass

    def get_cpu_value(self) -> str:
        pass

    def get_ram_value(self) -> str:
        pass

    def get_gpu_value(self) -> str:
        pass

    def get_all_secrets(self) -> dict:
        #keys are names of secret
        #values are all key/value pairs inside that secret
        pass