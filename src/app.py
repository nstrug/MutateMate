import os
import base64
import copy
import json

from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

from services.JsonHelperService import JsonHelperService
from services.KubeWrapperService import KubeWrapperService
from services.NotebookMutaterService import NotebookMutaterService
from services.PipelineRunMutaterService import PipelineRunMutaterService

app = Flask(__name__)

cnst_kube_url = os.getenv("BASE_URL")
cnst_kube_access_token = os.getenv("ACCESS_TOKEN")
cnst_pipeline = "PipelineRun"
cnst_notebook = "Notebook"
crd_name_list = [ cnst_pipeline, cnst_notebook ]

notebook_mutater = NotebookMutaterService()
pipeline_mutater = PipelineRunMutaterService()
jsonService = JsonHelperService()

@app.route('/mutate', methods=['POST'])
def mutate_pod():
    print("********************** Mutate **********************")
    print(request.json)

    #For Emergency. By pass everything
    #return send_response(request.json)
    #

    payload = [{"op": "add", "path": "/metadata/labels", "value": {"thy.editedby": "MutateMate" }}]
    payload.append({"op": "add", "path": "/spec/template/spec/containers/0/env/-", "value": {"name": "thy1", "value": "thyvalue2"}})

    json_data = jsonService.get_dict(request.json)
    print(json_data)
    
    return send_response(request.json, payload)

    #################

    req_json = request.json.copy()

    val_kind = req_json["kind"]
    if val_kind not in crd_name_list : return req_json
    
    val_namespace = req_json["metadata"]["namespace"]

    kube_service = KubeWrapperService(cnst_kube_url, cnst_kube_access_token)
    hashtags = kube_service.get_namespace_definition_hashtags(val_namespace)
    all_secret_infos = kube_service.get_all_secrets()
    secrets_targeted = kube_service.rearrange_by_names(hashtags, all_secret_infos)

    val_cpu, val_ram, val_gpu = kube_service.get_all_resources()

    if val_kind == cnst_pipeline: 
        return pipeline_mutater.mutate(req_json, secrets_targeted, val_cpu, val_ram, val_gpu)
    elif val_kind == cnst_notebook: 
        return notebook_mutater.mutate(req_json, secrets_targeted, val_cpu, val_ram, val_gpu)

    return req_json

def send_response(req_json, payload : list = None):
    #https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#response
    response = req_json.copy()
    uid = req_json['request']['uid']

    response.pop('request', None)
    # tmp1 =  [{"op": "add", "path": "/spec/replicas", "value": 3}]
    # tmp2 = base64.b64encode(json.dumps(tmp1).encode('utf-8')).decode()
    # tmp3 = base64.b64encode(json.dumps(tmp1).encode()).decode()
    # tmp4 = base64.b64encode(str(tmp1).encode()).decode()    
    # isequal = tmp2 == "W3sib3AiOiAiYWRkIiwgInBhdGgiOiAiL3NwZWMvcmVwbGljYXMiLCAidmFsdWUiOiAzfV0="

    response["response"] = {
            "uid": uid,
            "allowed": True
    }

    if(payload is not None):
        tmp_ser = base64.b64encode(json.dumps(payload).encode('utf-8')).decode()
        response["response"]["patchType"] = "JSONPatch"
        response["response"]["patch"] = tmp_ser
    
    
    print(">>>>>")
    print(response)
    print("<<<<<")

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)