from flask import Flask,render_template
app=Flask(__name__)

@app.route('/',methods=["GET"])
def index():
    details={'name':"Amit",'age':24}
    return  render_template("index.html",detail=details)



if __name__=="__main__":
    app.run(debug=True)
