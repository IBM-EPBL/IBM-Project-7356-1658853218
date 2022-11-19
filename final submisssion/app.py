from flask import Flask,render_template,request
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 
from random import randint
import ibm_db
import ibm_boto3,os
from ibm_botocore.client import Config, ClientError
from werkzeug.utils import secure_filename 

COS_ENDPOINT ="https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
COS_API_KEY_ID = "1lPy2Y0UcYE0TfGrRKMV7tkjVy0KPU3I6hJLpGYMAQeW"
COS_INSTANCE_CRN= "crn:v1:bluemix:public:cloud-object-storage:global:a/4ec5ba80b0824b1abc11c1c9aa888211:d41fd821-4f07-4e21-869f-81475069fb58::"
COS_BUCKET_LOCATION="jp-tok-Storage"
COS_SERVICE_CRN = "crn:v1:bluemix:public:iam-identity::a/4ec5ba80b0824b1abc11c1c9aa888211::serviceid:ServiceId-2e88964b-b66a-471b-acba-96d385465204"

cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

UPLOAD_FOLDER = 'static/uploads' 

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=8e359033-a1c9-4643-82ef-8ac06f5107eb.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30120;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=lpf74710;PWD=G6pXqWOb8Pf0NXeG",'','')


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

OTP = 0

def send_otp(email):
    global OTP
    OTP = randint(100000,999999)
    sender_email = "mailt5523@gmail.com"
    receiver_email = email
    password = "ltupioflbirzddvf"
    message = MIMEMultipart("alternative")
    message["Subject"] = "This a OTP From Plasma Donating Website "
    message["From"] = sender_email
    message["To"] = receiver_email
    html = """\
            <html>
            <body>
                <h3>Your OTP is {}</h3>
            </body>
            </html>
    """.format(OTP)

    part2 = MIMEText(html, "html")
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

def confirmation_mail(email,username):
    sender_email = "mailt5523@gmail.com"
    receiver_email = email
    password = "ltupioflbirzddvf"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Plasma Donating Website "
    message["From"] = sender_email
    message["To"] = receiver_email
    html = """\
            <html lang="en">
            <body>
                <h1>Hello {}</h1>
                <h2>Thank you for joining</h2><br>
                <p>Your account is created successfully.To access the website login</p>
            </body>
            </html>
    """.format(username)

    part2 = MIMEText(html, "html")
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

def send_requestmail(remail,demail,hospitalname,phoneno,Address):
    sender_email = "mailt5523@gmail.com"
    receiver_email = demail
    password = "ltupioflbirzddvf"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Request for Plasma donation"
    message["From"] = sender_email
    message["To"] = receiver_email
    html = """\
            <html lang="en">
            
            <body>
                <h3>We from {} request you to come forward to donate blood plasma and save a life.</h3>
                <h3>For more information Email: {} or <br> Phone No: {} ,<br>Address: {}</h3>
            </body>
            </html>
    """.format(hospitalname,remail,phoneno,Address)

    part2 = MIMEText(html, "html")
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

def send_choice(email,choice):
    sender_email = "mailt5523@gmail.com"
    receiver_email = email
    password = "ltupioflbirzddvf"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Plasma donation"
    message["From"] = sender_email
    message["To"] = receiver_email
    html = """\
            <html lang="en">
            
            <body>
                <h3>The Donor {} your request {}</h3>
            </body>
            </html>
    """.format(choice,email)

    part2 = MIMEText(html, "html")
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )



def upload_large_file(bucket_name, item_name, file_path):
    print("Starting large file upload for {0} to bucket: {1}".format(item_name, bucket_name))

    # set the chunk size to 5 MB
    part_size = 1024 * 1024 * 5

    # set threadhold to 5 MB
    file_threshold = 1024 * 1024 * 5

    # Create client connection
    cos_cli = ibm_boto3.client("s3",
        ibm_api_key_id=COS_API_KEY_ID,
        ibm_service_instance_id=COS_SERVICE_CRN,
        config=Config(signature_version="oauth"),
        endpoint_url=COS_ENDPOINT
    )

    # set the transfer threshold and chunk size in config settings
    transfer_config = ibm_boto3.s3.transfer.TransferConfig(
        multipart_threshold=file_threshold,
        multipart_chunksize=part_size
    )

    # create transfer manager
    transfer_mgr = ibm_boto3.s3.transfer.TransferManager(cos_cli, config=transfer_config)

    try:
        # initiate file upload
        future = transfer_mgr.upload(file_path, bucket_name, item_name)

        # wait for upload to complete
        future.result()

        print ("Large file upload complete!")
    except Exception as e:
        print("Unable to complete large file upload: {0}".format(e))
    finally:
        transfer_mgr.shutdown()
        


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/otp",methods=['GET','POST'])
def otp():
    if request.method == 'POST':
        email = request.form.get("email")
        choice = request.form.get("choice")
        if email == "":
            return render_template("otp.html")
        else:
            send_otp(email)
            return render_template("verfication.html", email=email,choice=choice)
    return render_template('otp.html')

@app.route("/verfication",methods=['GET','POST'])
def verfication():
    if request.method == 'POST':
        email = request.form.get("email")
        otp = request.form.get('otp')
        choice = request.form.get("choice")
        global OTP
        if OTP == int(otp):
            if choice == "Donor":
                return render_template('register.html',choice=choice,email=email)
            elif choice == "Requester":
                return render_template('register.html',choice=choice ,email=email)
        else:
            message = "You entered a wrong OTP"
            send_otp(email)
            return render_template("verfication.html",otp=OTP,choice=choice, email=email,message=message)   
    return render_template("verfication.html")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice == 'Donor':
            username = request.form.get("username")
            firstname = request.form.get("firstname")
            lastname = request.form.get("lastname")
            email = request.form.get("email")
            password = request.form.get("password")
            bloodgroup = request.form.get("bloodgroup")
            date = request.form.get("date")
            photo = request.files['photo']
            phoneno = request.form.get("phoneno")
            Address = request.form.get("Address")
            date = date.split("-")
            date = date[2]+'/'+date[1]+'/'+date[0]
            daccept = 0
            dreject = 0
            filename = secure_filename(photo.filename) 
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            bucket_name = "projectdonor"
            item_name = filename
            file_path ="{}/{}".format(UPLOAD_FOLDER,filename)
            upload_large_file(bucket_name, item_name, file_path)
            os.remove(file_path)

            insert_sql = "INSERT INTO PD VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, firstname)
            ibm_db.bind_param(prep_stmt, 3, lastname)
            ibm_db.bind_param(prep_stmt, 4, email)
            ibm_db.bind_param(prep_stmt, 5, password)
            ibm_db.bind_param(prep_stmt, 6, bloodgroup)
            ibm_db.bind_param(prep_stmt, 7, date)
            ibm_db.bind_param(prep_stmt, 8, filename)
            ibm_db.bind_param(prep_stmt, 9, phoneno)
            ibm_db.bind_param(prep_stmt, 10, Address)
            ibm_db.bind_param(prep_stmt, 11, daccept)
            ibm_db.bind_param(prep_stmt, 12, dreject)
            ibm_db.execute(prep_stmt)
            confirmation_mail(email,username)
            return render_template('home.html')
        elif choice == 'Requester':
            username = request.form.get("username")
            firstname = request.form.get("firstname")
            lastname = request.form.get("lastname")
            email = request.form.get("email")
            password = request.form.get("password")
            photo = request.files['photo']
            phoneno = request.form.get("phoneno")
            hospitalname = request.form.get("hospitalname")
            Address = request.form.get("Address")
            
            filename = secure_filename(photo.filename) 
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            bucket_name = "projectdonor"
            item_name = filename
            file_path ="{}/{}".format(UPLOAD_FOLDER,filename)
            upload_large_file(bucket_name, item_name, file_path)
            os.remove(file_path)

            insert_sql = "INSERT INTO PR VALUES (?,?,?,?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, firstname)
            ibm_db.bind_param(prep_stmt, 3, lastname)
            ibm_db.bind_param(prep_stmt, 4, email)
            ibm_db.bind_param(prep_stmt, 5, password)
            ibm_db.bind_param(prep_stmt, 6, hospitalname)
            ibm_db.bind_param(prep_stmt, 7, filename)
            ibm_db.bind_param(prep_stmt, 8, phoneno)
            ibm_db.bind_param(prep_stmt, 9, Address)
            ibm_db.execute(prep_stmt)
            confirmation_mail(email,username)
            return render_template('home.html')
    return render_template("register.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == "POST":
        choice = request.form.get('choice')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if choice == 'Donor':
            sql = "SELECT * FROM PD WHERE email =? and password = ?"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt,1,email)
            ibm_db.bind_param(stmt,2,password)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)
            if account:
                sql = "select * from PD where email=?;"
                ibm_db.bind_param(stmt,1,email)                
                ibm_db.execute(stmt)
                account = ibm_db.fetch_assoc(stmt)
                imgname = account["IMGNAME"]
                account.pop("PASSWORD")
                account.pop("IMGNAME")
                
                return render_template("pdashboard.html",choice=choice,data = account,imgname=imgname)
            else:
                sql = "SELECT * FROM PD WHERE email =?"
                stmt = ibm_db.prepare(conn, sql)
                ibm_db.bind_param(stmt,1,email)
                ibm_db.execute(stmt)
                account = ibm_db.fetch_assoc(stmt)
                
                if account:
                    message = "You entered a wrong password"
                    return render_template("login.html",message=message)
                else:
                    message = "You don't have a donor account"
                    return render_template("home.html",message=message)
        elif choice == 'Requester':
            sql = "SELECT * FROM PR WHERE email =? and password = ?"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt,1,email)
            ibm_db.bind_param(stmt,2,password)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)
            if account:
                sql = "select * from PR where email=?;"
                ibm_db.bind_param(stmt,1,email)                
                ibm_db.execute(stmt)
                account = ibm_db.fetch_assoc(stmt)
                imgname = account["IMGNAME"]
                account.pop("PASSWORD")
                account.pop("IMGNAME")
                
                return render_template("rdashboard.html",choice=choice,data = account,length=len(account),imgname=imgname)
            else:
                sql = "SELECT * FROM PR WHERE email =?"
                stmt = ibm_db.prepare(conn, sql)
                ibm_db.bind_param(stmt,1,email)
                ibm_db.execute(stmt)
                account = ibm_db.fetch_assoc(stmt)
                if account:
                    message = "You entered a wrong password"
                    return render_template("login.html",message=message)
                else:
                    message = "You don't have a Requester account"
                    return render_template("home.html",message=message)
        
    return render_template("login.html")

@app.route('/password',methods=['GET','POST'])
def password():
    if request.method == 'POST':
        email = request.form.get("email")
        choice = request.form.get("choice")
        if email == "":
            return render_template("password.html")
        else:
            if choice == "Donor":
                sql = "SELECT * FROM PD WHERE email =?"
                stmt = ibm_db.prepare(conn, sql)
                ibm_db.bind_param(stmt,1,email)
                ibm_db.execute(stmt)
                account = ibm_db.fetch_assoc(stmt)
                if account:
                    send_otp(email)
                    return render_template("update.html", email=email,choice=choice)
                else:
                    message = "You don't have to account recover password"
                    return render_template("home.html",message=message)
            elif choice == "Requester":
                sql = "SELECT * FROM PD WHERE email =?"
                stmt = ibm_db.prepare(conn, sql)
                ibm_db.bind_param(stmt,1,email)
                ibm_db.execute(stmt)
                account = ibm_db.fetch_assoc(stmt)
                if account:
                    send_otp(email)
                    return render_template("update.html", email=email,choice=choice)
                else:
                    message = "You don't have to account recover password"
                    return render_template("home.html",message=message)
            
    return render_template('password.html')

@app.route('/update',methods=['GET','POST'])
def update():
    if request.method == 'POST':
        email = request.form.get("email")
        otp = request.form.get('otp')
        choice = request.form.get("choice")
        global OTP
        if OTP == int(otp):
            if choice == "Donor":
                return render_template('change.html',email=email,choice=choice)
            elif choice == "Requester":
                return render_template('change.html',email=email,choice=choice)
        else:
            message = "You entered a wrong OTP"
            send_otp(email)
            return render_template("change.html",choice=choice, email=email,message=message)   
    return render_template("update.html")

@app.route('/change',methods=['GET','POST'])
def change():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        choice = request.form.get("choice")
        if choice == "Donor":
            sql = "update PD set password= ? where email= ?;"
            prep_stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(prep_stmt,1,password)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.execute(prep_stmt)
            return render_template("home.html")
        elif choice == "Requester":
            sql = "update PR set password= ? where email= ?;"
            prep_stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(prep_stmt,1,password)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.execute(prep_stmt)
            return render_template("home.html")
        
    return render_template('change.html')

@app.route("/dashboard" ,methods=['GET','POST'])
def dashboard():
    if request.method == "POST":
        choice = request.form.get("choice")
        data = request.form.get("data")
        imgname = request.form.get("imgname")
        if choice == "Donor":
            return render_template("pdashboard.html", data=data,imgname=imgname)
        elif choice == "Reqruester":
            return render_template("rdashboard.html", data=data,imgname=imgname)
            
    return render_template("dashboard.html")

@app.route("/drequest",methods=['GET','POST'])
def drequest():
    if request.method == "POST":
        email = request.form.get('email')
        data=[]
        sql = "SELECT * FROM PD"
        stmt = ibm_db.exec_immediate(conn, sql)
        dictionary = ibm_db.fetch_assoc(stmt)
        while dictionary != False:
            data.append(dictionary)
            dictionary = ibm_db.fetch_assoc(stmt)
        length = len(data)
        return render_template("request.html" ,data=data,length=length,email=email)
    return render_template("request.html")

@app.route("/info",methods=['POST','GET'])
def info():
    if request.method == "POST":
        remail = request.form.get("remail")
        email = request.form.get("email")
        sql = "SELECT * FROM PD WHERE email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        imgname = account["IMGNAME"]
        account.pop("PASSWORD")
        account.pop("IMGNAME")
        return render_template("info.html",data=account,imgname=imgname,email=remail)
    return render_template("info.html")

@app.route("/back",methods=['POST','GET'])
def back():
    if request.method =="POST":
        remail = request.form.get("remail")
        demail = request.form.get("demail")
        button = request.form.get("button")
        choice = "Requester"
        sql = "select * from PR where email=?;"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,remail)                
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        imgname = account["IMGNAME"]
        hospitalname = account["HOSPITALNAME"]
        phoneno = account["PHONENO"]
        Address = account["ADDRESS"]
        account.pop("PASSWORD")
        account.pop("IMGNAME")
        if button == "Back":        
            return render_template("rdashboard.html",choice=choice,data = account,length=len(account),imgname=imgname)
        elif button == "Request":
            insert_sql = "INSERT INTO notification VALUES (?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, demail)
            ibm_db.bind_param(prep_stmt, 2, hospitalname)
            ibm_db.bind_param(prep_stmt, 3, remail)
            ibm_db.execute(prep_stmt)
            send_requestmail(remail,demail,hospitalname,phoneno,Address)
            return render_template("rdashboard.html",choice=choice,data = account,length=len(account),imgname=imgname)
    
@app.route("/notification",methods=['POST','GET'])
def notification():
    if request.method =="POST":
        email = request.form.get("email")
        sql = "select * from notification where email= ?;"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        return render_template("notification.html",data=account,email=email)
    return render_template("notification.html")

def update(a,demail):
    sql = "update PD set daccept= ? where email= ?;"
    prep_stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(prep_stmt,1,a)
    ibm_db.bind_param(prep_stmt,2,demail)
    ibm_db.execute(prep_stmt)


@app.route("/choice",methods=['POST','GET'])
def choice():
    if request.method == 'POST':
        email = request.form.get("email")
        demail = request.form.get("demail")
        choice = request.form.get("value")
        if choice == "Accept":
            send_choice(email,choice)
            sql = "select daccept from PD where email = ?;"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt,1,demail)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)
            a =account["DACCEPT"]+1
            update(a,demail)            
            return render_template("home.html")
        elif choice == "Reject":
            send_choice(email,choice)
            sql = "select dreject from PD where email = ?;"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt,1,demail)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)
            a =account["DREJECT"]+1
            update(a,demail) 
            return render_template("home.html")
        



if __name__ == "__main__":
    app.run(host="0.0.0.0" , port=5000 ,debug=True)
