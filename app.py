from cgitb import text
from flask import Flask, render_template,request,jsonify
from chat import get_response
#from fileinput import filename
#import csv
app=Flask(__name__)
@app . get("/")
def index_get() :
    return render_template ("base.html")
#filename="dataset2.csv";
#fields=["Questions"]
#a=[]
@app.post ("/predict")
def predict() :
    text = request.get_json().get("message")
    # TODO: check if text is valid
    response = get_response(text)
    message = {"answer": response}
    #a.append(text)
    return jsonify(message)
#a.append(text)
'''''def dataset(a):
    with open(filename, 'a') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(fields) 
            
        # writing the data rows 
        csvwriter.writerows(a)
    #with open('Pages.txt', 'w) as f:
    #    f.write("Questions="+'str(a)+"\n")
    #f.close()'''''

if __name__=="__main__":
    app.run(debug=True)
    #dataset(a)
    