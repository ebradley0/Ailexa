from RealtimeSTT import AudioToTextRecorder
from Ollama import Querry_AI
import time

class STT:
    def __init__(self):
        self.active = True
        self.recorder = None
        self.response = None
        self.responseRecorder = None
        self.responseActive = False
        self.currentTime = None
        
    
    def responseListen(self):
        self.currentTime = time.time()
        while time.time() - self.currentTime < 5:
            self.responseRecorder.listen()
            self.responseRecorder.text(self.process_text)
            
        self.active = True
        print("Response concluded, waiting for wake word again")
        
        
        
    
    def process_text(self, text):
        print(text)
        print("Process finished")
        self.active = False
        self.response = Querry_AI(text)
        print(self.response)
        self.responseListen()




    def recordingStarted(self):
        print("Recording Started")
        

    def recordingEnded(self):
        print("Recording Ended")
        #This will shut off the recorder while Ollama processes the data
        self.active = False


    def init_recorder(self):
        
        self.recorder = AudioToTextRecorder(wake_words="computer", on_recording_start=self.recordingStarted, on_recording_stop=self.recordingEnded, post_speech_silence_duration=1)
        self.responseRecorder = AudioToTextRecorder() #This way the user can respond without a wake word, more conversational
        print("Listening... for wake word")
        while True:
            if self.active:
                self.recorder.listen()
                self.recorder.text(self.process_text)
            


        
            

        
        
            
