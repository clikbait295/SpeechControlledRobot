# Speech Controlled Imaginary Robot
Created for MakeSPP 2020!
This Repo is for the version of my software which can run without any hardware, like a Raspberry Pi or motors. It simply removes motor functionality and replaces it with a message to the user saying an imaginary robot has moved.

**PREQUISITES:**

Before you run this code, you must make sure you have the following libraries/dependencies
- Flask
- SpeechRecognition
- Google-api-python-client
- Cryptography

To install these all on Python3, run the following command in your command prompt/terminal:
pip3 install SpeechRecognition Flask google-api-python-client cryptography

**HOW TO RUN:**

Now that you have all of the prequisites/dependencies installed, you should be able to run this program without any issues. Just run "main.py" and go to the IP address in the first line outputed from the script (you should probably use the IDLE for this). Remember to copy the "https://", otherwise you will get an error. READ THE NEXT SECTION BEFORE OPENING THE PAGE!

**IMPORTANT: **

WHEN YOU FIRST CONNECT TO THE WEBSERVER, YOU WILL GET A "Your connection is not private" MESSAGE FROM THE BROWSER. PLEASE DISREGARD THIS MESSAGE, IT IS APPEARING BECAUSE I AM USING AN UNVERIFIED CERTIFICATE TO GET HTTPS ON MY SERVER, WHICH ALLOWS ME TO ACCESS THE USER'S MICROPHONE. To continue to the website, click on "Advanced" and then click "Continue". YOU ARE NOT GETTING HACKED!

**HOW TO USE:**

Simply click the record button, allow access to your microphone, and say "go forward 10 seconds". Then click the stop button. After a few seconds, you will get a message on the website which says an imaginary robot has moved forward for ten seconds. Here is the command syntax:
- "go forward {number of seconds} seconds"
- "go back {number of seconds} seconds"
- "turn left"
- "turn right"

**CREDITS:**

- https://github.com/addpipe/simple-recorderjs-demo for the recording part of the webserver.
- https://www.raspberrypi-spy.co.uk/2012/07/stepper-motor-control-in-python/ for some of the stepper motor code.
- https://github.com/mattdiamond/Recorderjs for Recorder.js library.
