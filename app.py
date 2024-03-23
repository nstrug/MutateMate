import os

from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

from services.KubeWrapperService import KubeWrapperService
from services.NotebookMutaterService import NotebookMutaterService
from services.PipelineRunMutaterService import PipelineRunMutaterService

app = Flask(__name__)

cnst_kube_url = os.getenv("BASE_URL")
cnst_kube_access_token = os.getenv("ACCESS_TOKEN")
cnst_pipeline = "PipelineRun"
cnst_notebook = "Notebook"
crd_name_list = [ cnst_pipeline, cnst_notebook ]

mtt_notebook = NotebookMutaterService()
mtt_pipeline = PipelineRunMutaterService()

@app.route('/mutate', methods=['POST'])
def mutate_pod():
    print(request.json)
    #For Emergency. By pass everything
    #return request.json
    #

    req_json = request.json

    val_kind = req_json["kind"]
    if val_kind not in crd_name_list : return req_json
    
    val_namespace = req_json["metadata"]["namespace"]

    kube_service = KubeWrapperService(cnst_kube_url, cnst_kube_access_token)
    hashtags = kube_service.get_namespace_definition_hashtags(val_namespace)
    all_secret_infos = kube_service.get_all_secrets()
    secrets_targeted = kube_service.rearrange_by_names(hashtags, all_secret_infos)

    val_cpu, val_ram, val_gpu = kube_service.get_all_resources()

    if val_kind == cnst_pipeline: 
        return mtt_pipeline.mutate(req_json, secrets_targeted, val_cpu, val_ram, val_gpu)
    elif val_kind == cnst_notebook: 
        return mtt_notebook.mutate(req_json, secrets_targeted, val_cpu, val_ram, val_gpu)

    return req_json


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)