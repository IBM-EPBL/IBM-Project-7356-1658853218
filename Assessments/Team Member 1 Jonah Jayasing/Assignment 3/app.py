from flask import Flask,render_template
import ibm_boto3
from ibm_botocore.client import Config, ClientError


COS_ENDPOINT ="https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
COS_API_KEY_ID = "1lPy2Y0UcYE0TfGrRKMV7tkjVy0KPU3I6hJLpGYMAQeW"
COS_INSTANCE_CRN= "crn:v1:bluemix:public:cloud-object-storage:global:a/4ec5ba80b0824b1abc11c1c9aa888211:d41fd821-4f07-4e21-869f-81475069fb58::"
COS_BUCKET_LOCATION="jp-tok-Storage"
cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

app = Flask(__name__)

def get_bucket_contents(bucket_name):
    try:
        files = cos.Bucket(bucket_name).objects.all()
        edit_file = []
        for file in files:
            edit_file.append(file.key)
        return edit_file
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))




@app.route("/")

def home():
    # get_bucket_contents("jonahjayasingh")
    return render_template("home.html",image=get_bucket_contents("jonahjayasingh"))

if __name__ == "__main__":
    app.run(debug=True)