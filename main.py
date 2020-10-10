#Import libraries
from flask import Flask
from flask import request
from flask import render_template
import os
from os import path
import speech_recognition as sr
import time
import socket

#Declare variables
global messageList
messageList = [] #Declare variable for message list on webpage

global messageCounter
messageCounter = 0 #Declare variable for message counter on webpage

global audioRecog
audioRecog = 0 #Declare variable for audio recognition

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    #IF user clicks "Stop and Upload" button, download the audio file and send to Google Speech Recognition.
    if request.method == "POST":
        #Download the audio file and save it.
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        print('File downloaded successfully.')
        audioFile = path.join(path.dirname(path.realpath(__file__)), "audio.wav")
        #Initialize the audio recognizer library.
        r = sr.Recognizer()
        with sr.AudioFile(audioFile) as source:
            audio = r.record(source)  # Read the entire audio file.
        #TRY to parse audio by sending it to Google Speech Recognition services.
        try:
            print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
            audioRecog = r.recognize_google(audio)
            #Split the text recieved from Google into a list.
            audioRecogList = audioRecog.split()
            print(audioRecogList)
            #Figure out what the user is saying, and if it a command, carry it out. In this version of the code, since there is no hardware connected to this script,
            #there is simply a messsage sent to the user.
            if audioRecogList[0] + audioRecogList[1] == "goforward" and len(audioRecogList) >= 3:
                #audioRecogList[2] --> number of seconds to move
                messageList.append("Google Speech Recognition thinks you said '" + audioRecog + "' so the imaginary robot went forward for " + audioRecogList[2] + " seconds.")
                print("Go forward for " + audioRecogList[2] + " seconds")
            if audioRecogList[0] + audioRecogList[1] == "goback" and len(audioRecogList) >= 3:
                #audioRecogList[2] --> number of seconds to move
                messageList.append("Google Speech Recognition thinks you said '" + audioRecog + "' so the imaginary robot went backwards for " + audioRecogList[2] + " seconds.")
                print("Go back for " + audioRecogList[2] + " seconds")
            if audioRecogList[0] + audioRecogList[1] == "turnleft":
                messageList.append("Google Speech Recognition thinks you said '" + audioRecog + "' so the imaginary robot turned left.")
                print("turn left")
            if audioRecogList[0] + audioRecogList[1] == "turnright":
                messageList.append("Google Speech Recognition thinks you said '" + audioRecog + "' so the imaginary robot turned right.")
                print("turn right")
            else:
                messageList.append("Google Speech Recognition thinks you said '" + audioRecog + "'.")
        #Handle errors or if the audio couldn't be understood.
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            audioRecog = "Audio could not be understood."
            mesageList.append(audioRecog)
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            audioRecog = "Error!"
            messageList.append(audioRecog)
        return render_template('index.html', request="POST")
    else:
        return render_template("index.html")
#Dynamic text updates: the user doesn't have to reload the webpage to see updates from the script.
@app.route('/text_stream')
def stream():
    def generate():
        while True:
            global messageCounter
            #If messageList is empty, restart loop.
            #If messageList has not been updated, restart loop.
            #If messageList has been updated, update the webpage.
            if not messageList:
                continue
            if len(messageList) == messageCounter:
                continue
            if len(messageList) != messageCounter:
                print(len(messageList), messageCounter)
                messageCounter = messageCounter + 1
                yield '{}\n'.format(messageList[-1])
            

    return app.response_class(generate(), mimetype="text/event-stream")

if __name__ == "__main__":
    #Start webserver with adhoc HTTPS so that the browser won't throw an error when the page tries to access the user's microphone.
    #Since the certificate isn't verified, the browser will show a notification that the webpage is insecure, but once the user clicks continue, the webpage functions as normal.
    print("Copy this link into your broswer to open this webpage: https://" + socket.gethostbyname(socket.gethostname()) + ":5000")
    print("NOTE: When you connect to the webserver, you will get a warning that this webserver is insecure. Please disregard this and click 'Advanced' and then 'Continue to website'.")
    print("This warning is caused by the adhoc (unverified) certificate I am using to allow for HTTPS communication. Without this, most browsers wouldn't allow this script to access the user's microphone.")
    app.run(host='0.0.0.0', port=5000, threaded=True, ssl_context='adhoc')
