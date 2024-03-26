import os
import base64
import copy

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

notebook_mutater = NotebookMutaterService()
pipeline_mutater = PipelineRunMutaterService()

@app.route("/validate", methods=["POST"])
def validate():
    print("*** validate")
    allowed = True
    try:
        for container_spec in request.json["request"]["object"]["spec"]["containers"]:
            if "env" in container_spec:
                allowed = False
    except KeyError:
        pass
    return jsonify(
        {
            "response": {
                "allowed": allowed,
                "uid": request.json["request"]["uid"],
                "status": {"message": "env keys are prohibited"},
            }
        }
    )


@app.route('/mutate', methods=['POST'])
def mutate_pod():
    print("*** mutate")
    print(request.json)
    spec = request.json["request"]["object"]
    print("-----------")
    print(spec)
    modified_spec = copy.deepcopy(spec)

    #For Emergency. By pass everything
    return send_reponse(request.json, modified_spec)
    #

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

def send_reponse(req_json, req_inside):
    #return jsonify(req_json)
    
    uid = req_json['request']['uid']
    print(f"uid => {uid}")
    response = {
            "response": {
                "allowed": True,
                "uid": request.json["request"]["uid"],
                "patch": base64.b64encode(str(req_inside).encode()).decode(),
                "patchtype": "JSONPatch",
            }
    }
    
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)