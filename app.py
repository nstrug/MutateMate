from flask import Flask, request, jsonify

app = Flask(__name__)

cnst_pipeline = "Pipeline"
crd_name_list = [ cnst_pipeline ]

@app.route('/mutate', methods=['POST'])
def mutate_pod():
    print(request_data)
    if(request_data["name"] not in  crd_name_list): return request.json

    #description'dan hash bilgileri (#crmapdb) alınıp, bir de cpu/ram alınırsa,  

    request_data = request.json
    
    

    return request_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)