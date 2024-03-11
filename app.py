from flask import Flask, request
from pose_format import Pose
from pose_format.pose_visualizer import PoseVisualizer
import requests

app = Flask(__name__)

@app.route("/textToASL", methods=['GET'])
def textToASL():
    inputText = request.args.get('inputText')
    apiForTextForASL = f"https://us-central1-sign-mt.cloudfunctions.net/spoken_text_to_signed_pose?text={inputText}&spoken=en&signed=ase"
    print(inputText)
    
    response = requests.get(apiForTextForASL)
    
    if(response.status_code == 200):
        
        # with open('downloaded_file.pose', 'wb') as file:
        #     file.write(response.content)
        
        # with open(response.content, "rb") as poseFile:
        #     pose = Pose.read(poseFile.read())
    
        # read pose file  
        pose = Pose.read(response.content)
        v = PoseVisualizer(pose)
        v.save_video("pose.mp4", v.draw())
           
    else:
        print(f"Error in Get Requests Error Code :{response.status_code} ") 
    return "video"

if __name__ == '__main__':
    app.run(debug=True)