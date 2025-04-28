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
        self.timer = None
        self.text_buffer = []
       
        
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

        
        
    def stop_response(self):
        print("Stopping response")
        self.responseRecorder.stop()
        self.responseActive = False
        text = self.responseRecorder.text() # Get the text from the recorder
        self.text_buffer.append(text) # Append the text to the buffer
        print("Text buffer: ", self.text_buffer)
        
        full_text = " ".join(self.text_buffer).strip() # Join the text in the buffer to a single string
        
        if (full_text==""): ## If no response is detected, return to main loop by setting active to true
            print("No response detected")
            self.responseActive = False
            self.active = True

        else: #Repeat the process_text function with the response text
            self.process_text(text)
   
       
    def responseWindow(self):

        self.responseRecorder.start() # Set the text function to process_text, this actively transcribes the audio to text
        self.responseActive = True
        self.timer = threading.Timer(5, self.stop_response) # Set a timer for 5 seconds to stop the response window
        
        self.timer.start() # Start the timer

        self.responseRecorder.on_realtime_transcription_update = self.resetTimer # Reset the timer if there is a response detected
        
    def resetTimer(self, text):
        if (text.strip() != ""): # If the text is not empty, append it to the buffer
            self.text_buffer.append(text) # Append the text to the buffer


        if self.timer:
            print("Resetting timer")
            self.timer.cancel() # Cancel the previous timer
            self.timer = None # Reset the timer to None
            self.timer = threading.Timer(5, self.stop_response) # Reset the timer to 5 seconds
            self.timer.start()
    
    def process_text(self, text):
        print(text)
        self.active = False
        self.response = Querry_AI(text)
        print(self.response)
        #self.speak(self.response)
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

                

            


        
            

        
        
            
