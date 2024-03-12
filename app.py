from flask import Flask, request, Response
from pose_format import Pose
from pose_format.pose_visualizer import PoseVisualizer
import requests
import cv2

app = Flask(__name__)



def generate_frames():
    vid = cv2.VideoCapture("pose.mp4")
    while True:
            
        ## read the camera frame
        success,frame=vid.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    # Generate the response with the video stream
    response = Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    # Set the CORS headers to allow all origins
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

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
        # for frame in v.draw():
        
           
    else:
        print(f"Error in Get Requests Error Code :{response.status_code}") 
    # return "video"
    


if __name__ == '__main__':
    app.run(debug=True)