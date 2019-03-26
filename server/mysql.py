from flask import Flask, jsonify,request,jsonify
from flask_mysqldb import MySQL
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token


app=Flask(__name__)

app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='medtronic'
app.config['MYSQL_DB']='crud_application_python'
app.config['MYSQL_HOST']='localhost'
#app.config['MYSQL_CURSORCLASS']='DictCursor'
#app.config['MYSQL_PORT']='3306'
app.config['JWT_SECRET_KEY']='secret'


mysql=MySQL(app)
bcrypt=Bcrypt(app)
jwt=JWTManager(app)
CORS(app)

@app.route('/')
def index():
    return "Hello crud"



@app.route('/user/register',methods=['POST'])
def register():
    try:
        cur=mysql.connection.cursor()
        print(cur)
        first=request.get_json()['first_name']
        last=request.get_json()['last_name']
        email=request.get_json()['email']
        password=bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
        created=datetime.utcnow()
        cur.execute('insert into users(first_name,last_name,email,password,created) values(%s,%s,%s,%s,%s)',(str(first),str(last),str(email),str(password),str(created)))
        query="insert into users(first_name,last_name,email,password,created) values('"+str(first)+"','"+str(last)+"','"+str(email)+"','"+str(password)+"','"+str(created)+"')"
        print(query)
        cur.execute(query)
        mysql.connection.commit()

        result={
             'first_name':first,
             'last_name':last,
             'email':email,
             'password':password,
             'created':created
         }
        print(result)
        return jsonify({'result':result})
        
    except Exception as e:
        print(e)
    

    #return jsonify({'result':result})


@app.route('/user/list')
def userList():
    try:
        cur=mysql.connection.cursor()
        #cur.execute('insert into users(first_name,last_name,email,password,created) values(%s,%s,%s,%s,%s)',(str(first),str(last),str(email),str(password),str(created)))
        query="select * from users"
        print(query)
        cur.execute(query)
        mysql.connection.commit()
        result = cur.fetchall()
        print(result)
        return jsonify({'result':result})
    except Exception as e:
        print(e)

@app.route('/user/delete/<id>',methods=['DELETE'])
def delete(id):
    try:
        cur=mysql.connection.cursor()
        response=cur.execute("delete from users where id="+id)
        mysql.connection.commit()

        if response>0:
            result={'message':'record deleted '}
        else :
            result={'message':'record not found'}
        
        return jsonify({'result':result})
    except Exception as e:
        print(e)

if __name__ == '__main__':
    app.run(debug=True)




