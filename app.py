from flask import Flask, request, jsonify
from services.KubeWrapperService import KubeWrapperService
from services.NotebookMutaterService import NotebookMutaterService
from services.PipelineRunMutaterService import PipelineRunMutaterService

app = Flask(__name__)

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

    kube_service = KubeWrapperService()

    if val_kind == cnst_pipeline: 
        return mtt_pipeline.mutate(req_json)
    elif val_kind == cnst_notebook: 
        return mtt_notebook.mutate(req_json)

    return req_json

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)