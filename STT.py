from RealtimeSTT import AudioToTextRecorder
import threading
from Ollama import Querry_AI
class STT:
    def __init__(self):
        self.active = True
        self.Wakerecorder = None
        self.response = None
        self.currentTime = None
        self.responseActive = False
        self.p1 = None
        self.p2 = None
        self.responseRecorder = None
        
    def listen_for_response(self):
        print("Listening for response")
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
        print("Response Window")

        self.responseRecorder.start()
        self.responseActive = True
        threading.Timer(5, self.stop_response).start() # Set a timer for 5 seconds to stop the response window)
        
    
    def process_text(self, text):
        print(text)
        self.active = False
        self.response = Querry_AI(text)
        print(self.response)
        self.responseWindow()



    def recordingStarted(self):
        print("Recording Started")
        

    def recordingEnded(self):
        print("Recording Ended")
        #This will shut off the recorder while Ollama processes the data
        self.active = False


    def init_recorder(self):
        
        self.Wakerecorder = AudioToTextRecorder(wake_words="computer", on_recording_start=self.recordingStarted, on_recording_stop=self.recordingEnded, post_speech_silence_duration=1)
        print("Listening... for wake word")
        self.responseRecorder = AudioToTextRecorder(post_speech_silence_duration=1)
        self.Wakerecorder.listen()
        while True:
            if self.active:
                self.Wakerecorder.text(self.process_text)

                

            


        
            

        
        
            
