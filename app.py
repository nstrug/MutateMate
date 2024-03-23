from flask import Flask, request, jsonify

app = Flask(__name__)

cnst_pipeline = "PipelineRun"
cnst_notebook = "Notebook"
crd_name_list = [ cnst_pipeline, cnst_notebook ]

@app.route('/mutate', methods=['POST'])
def mutate_pod():
    print(request.json)
    #For Emergency. By pass everything
    #return request.json
    #

    jsn = request.json
    if(jsn["kind"] not in  crd_name_list): return jsn

    #description'dan hash bilgileri (#crmapdb) alınıp, bir de cpu/ram alınırsa,  

    return jsn

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)