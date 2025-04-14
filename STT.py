from RealtimeSTT import AudioToTextRecorder
import threading
from TTS.api import TTS
import torch
import requests
import json
from Ollama import Querry_AI
import pyaudio
import wave
import shutil
class STT:
    def __init__(self):
        self.active = True
        self.Wakerecorder = None
        self.response = None
        self.currentTime = None
        self.responseActive = False
        self.responseRecorder = None
        self.URL = "http://localhost:7851/api/tts-generate"
       
        
    def speak(self, text):
        print("Speaking")
        
        payload = {
            "text_input": text,
        }
        print(json.dumps(payload))
        response = requests.post(self.URL, data=payload)
        if response.status_code == 200:
            audio_data = response.content
            source = response.json["output_file_path"]
            shutil.copyfile(source, "output.wav")
            print("Audio file saved as output.wav")
        else:
            print(f"Error: {response.status_code} - {response.text}")

        wavFile = wave.open("output.wav", 'rb')
        pyaud = pyaudio.PyAudio()
        stream = pyaud.open(format=pyaudio.paInt16, channels=1, rate=22050, output=True)
        data = wavFile.readframes(1024)
        while data:
            stream.write(data)
            data = wavFile.readframes(1024) # Keep reading from the file until it is empty
        wavFile.close()
        stream.close()
        pyaud.terminate()

        

    def listen_for_response(self):
        
        self.responseRecorder.listen()
        self.responseRecorder.text(self.process_text)
        
    def stop_response(self):
        print("Stopping response")
        self.responseRecorder.stop()
        self.responseActive = False
        text = self.responseRecorder.text() # Get the text from the recorder
        
        if (text==""): ## If no response is detected, return to main loop by setting active to true
            print("No response detected")
            self.responseActive = False
            self.active = True
            return
        else: #Repeat the process_text function with the response text
            self.process_text(text)
   
       
    def responseWindow(self):

        self.responseRecorder.start()
        self.responseActive = True
        threading.Timer(3, self.stop_response).start() # Set a timer for 5 seconds to stop the response window)
        
    
    def process_text(self, text):
        print(text)
        self.active = False
        self.response = Querry_AI(text)
        print(self.response)
        self.speak(self.response)
        self.responseWindow()



    def recordingStarted(self):
        pass
        

    def recordingEnded(self):
        pass
        #This will shut off the recorder while Ollama processes the data
        self.active = False


    def init_recorder(self):
        
        self.Wakerecorder = AudioToTextRecorder(wake_words="computer", on_recording_start=self.recordingStarted, on_recording_stop=self.recordingEnded, post_speech_silence_duration=1)
        self.responseRecorder = AudioToTextRecorder(post_speech_silence_duration=1)
        self.Wakerecorder.listen()
        while True:
            if self.active:
                self.Wakerecorder.text(self.process_text)

                

            


        
            

        
        
            
