from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/ls")
def ls():
    return render_template("ls.html")

@app.route("/lc")
def lc():
    return render_template("lc.html")

@app.route("/rs")
def rs():
    return render_template("rs.html")

@app.route("/rc")
def rc():
    return render_template("rc.html")

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)