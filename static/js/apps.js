//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream;                      //stream from getUserMedia()
var rec;                            //Recorder.js object
var input;                          //MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");


//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);

function startRecording() {
    console.log("recordButton clicked");

    /*
        Simple constraints object, for more advanced audio features see
        https://addpipe.com/blog/audio-constraints-getusermedia/
    */

    var constraints = { audio: true, video:false }

    /*
        Disable the record button until we get a success or fail from getUserMedia() 
    */

    recordButton.disabled = true;
    stopButton.disabled = false;
   

    /*
        We're using the standard promise based getUserMedia() 
        https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
    */

navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

        /*
            create an audio context after getUserMedia is called
            sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
            the sampleRate defaults to the one set in your OS for your playback device

        */
        audioContext = new AudioContext();

        //update the format 
        document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"

        /*  assign to gumStream for later use  */
        gumStream = stream;

        /* use the stream */
        input = audioContext.createMediaStreamSource(stream);

        /* 
            Create the Recorder object and configure to record mono sound (1 channel)
            Recording 2 channels  will double the file size
        */
        rec = new Recorder(input,{numChannels:1})

        //start the recording process
        rec.record()

        console.log("Recording started");

    }).catch(function(err) {
        //enable the record button if getUserMedia() fails
        recordButton.disabled = false;
        stopButton.disabled = true;
        
    });
}



function stopRecording() {
    console.log("stopButton clicked");

    //disable the stop button, enable the record to allow for new recordings
    stopButton.disabled = true;
    recordButton.disabled = false;
    
    //tell the recorder to stop the recording
    rec.stop();

    //stop microphone access
    gumStream.getAudioTracks()[0].stop();

    //create the wav blob and pass it on to createDownloadLink
    rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {
    //name of .wav file to use during upload and download (without extendion)
    var filename = new Date().toISOString();
    //upload link
    
    
   
    var xhr=new XMLHttpRequest();
    xhr.onload=function(e) {
      if(this.readyState === 4) {
          console.log("Server returned: ",e.target.responseText);
      }
    };
    var fd=new FormData();
    fd.append("audio_data",blob, filename);
    xhr.open("POST","/",true);
    xhr.send(fd);
}


var latest = document.getElementById('latest');
var output = document.getElementById('output');

var xhr = new XMLHttpRequest();
xhr.open('GET', '/text_stream');
xhr.send();
var position = 0;

function handleNewData() {
    // the response text include the entire response so far
    // split the messages, then take the messages that haven't been handled yet
    // position tracks how many messages have been handled
    // messages end with a newline, so split will always show one extra empty message at the end
    var messages = xhr.responseText.split('\n');
    messages.slice(position, -1).forEach(function(value) {
        latest.textContent = value;  // update the latest value in place
        // build and append a new item to a list to log all output
        var item = document.createElement('li');
        item.textContent = value;
        output.appendChild(item);
    });
    position = messages.length - 1;
}

var timer;
timer = setInterval(function() {
    // check the response for new data
    handleNewData();
    // stop checking once the response has ended
    if (xhr.readyState == XMLHttpRequest.DONE) {
        clearInterval(timer);
        latest.textContent = 'Done';
    }
}, 1000);
 