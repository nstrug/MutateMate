
import json

from services.KubeWrapperService import KubeWrapperService
from services.MutatingHelperService import MutatingHelperService


class PipelineRunMutaterService:
    def __init__(self) -> None:
        pass

    def mutate(self, data_req : json, kube_service : KubeWrapperService) -> json:
        pr_payload = []

        mwh_service = MutatingHelperService()
        kube_secrets, kube_cpu, kube_ram, kube_gpu = kube_service.get_notebook_info(data_req)

        #Secret commands:
        for itm_key, itm_value in kube_secrets.getitems():
            pr_payload.append(mwh_service.add_secret_notation(itm_key, itm_value))
        
        #resource commands:

        return pr_payload