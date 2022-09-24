from flask import Flask,render_template,request
import ibm_db


app = Flask(__name__)


conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=8e359033-a1c9-4643-82ef-8ac06f5107eb.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30120;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=lpf74710;PWD=G6pXqWOb8Pf0NXeG",'','')


@app.route("/")

def main():
    return render_template("index.html",user="")

@app.route("/signin", methods=["GET","POST"])

def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
       
        select = ("select * from signup where email = '{}' and password = '{}';".format(email,password))
        get = ibm_db.prepare(conn, select)
        ibm_db.execute(get)
        user = ibm_db.fetch_assoc(get)
        print(user)
        if email in user["EMAIL"]:
            return render_template("index.html", user= user["USERNAME"] + " logged in")
    return render_template("signin.html")

@app.route("/signup", methods=["GET","POST"])

def signup():
    if request.method == "POST":
        try:
            username = request.form.get("Userame")
            email = request.form.get("email")
            password = request.form.get("password")
            a = ("INSERT INTO signup (username,email,password) VALUES ('{}','{}','{}')".format(username,email,password))
            load = ibm_db.prepare(conn, a)
            ibm_db.execute(load)
            return render_template("index.html" ,user= "register successful")
        except:
            message = "Mail is already registered"
            return render_template("signup.html",message=message)
    return render_template("signup.html")



if __name__ == "__main__":
    app.run(debug=True)