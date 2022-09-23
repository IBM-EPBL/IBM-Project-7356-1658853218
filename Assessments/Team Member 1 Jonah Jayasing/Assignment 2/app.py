
from email import message
from flask import Flask,render_template,request
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "project"

mysql = MySQL(app)

@app.route("/")

def main():
    return render_template("index.html",user="")

@app.route("/signin", methods=["GET","POST"])

def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        cur = mysql.connection.cursor()
        cur.execute("select * from signup where email = '{}' and password = '{}';".format(email,password))
        user = cur.fetchone()
        if email in user:
            print(user[1])
            return render_template("index.html" , user=user[0] + " logged in")
    return render_template("signin.html")

@app.route("/signup", methods=["GET","POST"])

def signup():
    if request.method == "POST":
        try:
            username = request.form.get("Userame")
            email = request.form.get("email")
            password = request.form.get("password")
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO signup(username,email,password) VALUES ('{}','{}','{}')".format(username,email,password))
            mysql.connection.commit()
            cur.close()
            return render_template("index.html" ,user= "register successful")
        except:
            message = "Mail is already registered"
            return render_template("signup.html",message=message)
    return render_template("signup.html")



if __name__ == "__main__":
    app.run(debug=True)