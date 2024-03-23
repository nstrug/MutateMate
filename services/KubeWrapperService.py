import re

class KubeWrapperService:
    def __init__(self, kube_base_url : str, kube_access_token : str) -> None:
        self.base_url = kube_base_url
        self.access_token = kube_access_token
        
        self.gather_all_resources(kube_base_url, kube_access_token)
        
        pass

    # CPU, RAM, GPU all values related part:

    def gather_all_resources(self, url, access_token):
        pass

    def get_cpu_value(self) -> str:
        pass

    def get_ram_value(self) -> str:
        pass

    def get_gpu_value(self) -> str:
        pass

    def get_all_resources(self) -> str:
        return self.get_cpu_value(), self.get_ram_value(), self.get_gpu_value()

    ###

    def get_all_secrets(self) -> dict:
        #keys are names of secret
        #values are all key/value pairs inside that secret
        pass

    def get_namespace_definition(self, name_space : str) -> str:
        pass

    def get_namespace_definition_hashtags(self, name_space : str) -> list:
        tmp_desc = self.get_namespace_definition(name_space)
        return re.findall(r"#(\w+)", tmp_desc)
    
    def rearrange_by_names(self, allowed_names : list, whole_secret : dict) -> dict:
        tmp = { }
        for itm in allowed_names:
            if(itm in whole_secret):
                vals = whole_secret[itm]
                for key, val in vals:
                    tmp[key] = val

        return tmp