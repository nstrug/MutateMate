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

cnst_pipeline = "PipelineRun"
cnst_notebook = "Notebook"

cnst_kube_url = os.getenv("BASE_URL")
cnst_kube_access_token = os.getenv("ACCESS_TOKEN")

crd_name_list = [ cnst_pipeline, cnst_notebook ]

notebook_mutater = NotebookMutaterService()
pipeline_mutater = PipelineRunMutaterService()
jsonService = JsonHelperService()

@app.route('/mutate', methods=['POST'])
def mutate_pod():
    #try catch will be added here:
    return main_flow(request)
    return send_response(request.json)

def main_flow(request):
    print("********************** Mutate **********************")
    print(request.json)

    #For Emergency. By pass everything; uncomment this return:
    return send_response(request.json)
    #

    payload = [{"op": "add", "path": "/metadata/labels", "value": {"thy.editedby": "MutateMate" }}]

    data_req = jsonService.get_dict(request.json)
    print(data_req)
    
    #return send_response(request.json, payload)

    #################

    val_kind = data_req["kind"]
    val_namespace = data_req["namespace"]
    if val_kind not in crd_name_list : return send_response(request.json)

    kube_service = KubeWrapperService(cnst_kube_url, cnst_kube_access_token)

    payload_extra = []

    if val_kind == cnst_notebook: 
        payload_extra = notebook_mutater.generate_mutation(request.json, kube_service)

    if val_kind == cnst_pipeline: 
        payload_extra = flow_pipeline(request.json, kube_service)

    return send_response(request.json, payload + payload_extra)


def flow_pipeline(request_json : json, kube_service : KubeWrapperService) -> list:
    val_cpu, val_ram, val_gpu = kube_service.get_all_resources()
    nb_pipeline = []
    return nb_pipeline

def send_response(req_json, payload : list = None):
    #https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#response
    response = req_json.copy()
    uid = req_json['request']['uid']

    response.pop('request', None)

    response["response"] = {
            "uid": uid,
            "allowed": True
    }

    if (payload is not None) and (len(payload) > 0):
        tmp_ser = base64.b64encode(json.dumps(payload).encode('utf-8')).decode()
        response["response"]["patchType"] = "JSONPatch"
        response["response"]["patch"] = tmp_ser
    
    
    print(">>>>>")
    print(response)
    print("<<<<<")

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)