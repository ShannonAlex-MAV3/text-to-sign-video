from flask import Flask, request, Response, send_file
from pose_format import Pose
from pose_format.pose_visualizer import PoseVisualizer
import requests
import cv2

app = Flask(__name__)

vid_name = "video.mp4"

# function to serve vid frames 
def generate_frames():
    vid = cv2.VideoCapture(vid_name)
    while True:
            
        # read frame
        success,frame=vid.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# route to serve vid frames
@app.route('/video')
def video():
    # Generate the response with the video stream
    response = Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    # Set the CORS headers to allow all origins
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# test vid file endpoint
@app.route('/pose')
def pose():
    return send_file(vid_name)

# route to server vid file
@app.route("/textToASL", methods=['GET'])
def textToASL():
    inputText = request.args.get('inputText')
    apiForTextForASL = f"https://us-central1-sign-mt.cloudfunctions.net/spoken_text_to_signed_pose?text={inputText}&spoken=en&signed=ase"
    # print(inputText)
    
    response = requests.get(apiForTextForASL)
    
    if(response.status_code == 200):
        # read pose file  
        pose = Pose.read(response.content)
        v = PoseVisualizer(pose)
        v.save_video(vid_name, v.draw())
        return send_file(vid_name)    
    else:
        print(f"Error in Get Requests Error Code :{response.status_code}") 
    

if __name__ == '__main__':
    app.run(debug=True)