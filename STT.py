from RealtimeSTT import AudioToTextRecorder
from Ollama import Querry_AI

class STT:
    def __init__(self):
        self.active = True
        self.recorder = None
        self.response = None
    
    
    def process_text(self, text):
        print(text)
        print("Process finished")
        self.active = False
        self.response = Querry_AI(text)
        print(self.response)
        self.active = True




    def recordingStarted(self):
        print("Recording Started")
        

    def recordingEnded(self):
        print("Recording Ended")
        #This will shut off the recorder while Ollama processes the data
        self.active = False


    def init_recorder(self):
        
        self.recorder = AudioToTextRecorder(wake_words="computer", on_recording_start=self.recordingStarted, on_recording_stop=self.recordingEnded, post_speech_silence_duration=1)
        print("Listening... for wake word")
        while True:
            if self.active:
                self.recorder.listen()
                self.recorder.text(self.process_text)
            


        
            

        
        
            
