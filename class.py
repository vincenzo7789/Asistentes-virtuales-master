import google.generativeai as genai
import playsound
from vosk import Model,KaldiRecognizer
import os
import json, sys, queue, sounddevice
from gtts import gTTS

class Asistente:
    def __init__(self,model_name:str,audio_path:str,vosk_path:str,key_word="hola",config={},system_intruction="",API="",vosk_model_lang="es"):
        #recibimos los parametros necesarios para la creacion del asistente 
        self.model_name = model_name
        self.audio_path=audio_path
        self.vosk_path=vosk_path
        self.key_word=key_word
        self.config=config
        self.system_intruction=system_intruction
        self.API=API
        self.vosk_model_lang=vosk_model_lang
        #inicializando al modelo de ia de gemini
        if self.API =="" or self.model_name =="" or self.config =={}:
            raise Exception("error al configurar gemini ai")
        try:
            genai.configure(api_key=self.API)
            self.model=genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.config,
            )
            self.chat = self.model.start_chat()
        except Exception as e:
            raise Exception("error al configurar gemini ai")
        #configurando el modelo de reconocimineto de voz 
        self.q= queue.Queue()
        self.divece_id=None
        self.sample_rate=160000
        try:
            vosk_model=Model(self.vosk_path)
        except Exception as e:
            try:
                print("error al cargar el modelo de voz, cambiando en español...")
                self.vosk_model=Model(self.vosk_model_lang)
            except Exception as e:
                ("error al cargar el modelo de reconociomiento de voz")

    def anwer(self,text:str):
        result=self.chat.send_message(text)
        return result.text.replace("*","").replace("/","")

    def talk(self,talk:str):
        model =gTTS(talk,lang= self.vosk_model_lang)
        model.save(self.auido_path)
        try:
            playsound.playsound(self.audio_path)
        except Exception as e:
            print("no se pudo reproducir el audio")
        os.remove(self.audio_path)

    def trascrip(self):
        try:
            model=Model(self.vosk_path)
        except Exception as e:
            try:
                model= Model(self.vosk_model_lang)
            except Exception as e:
                print("error al cargar el modelo de voz")

        q=queue.Queue()
        def callback(indata,frames,time,status):
            q.put(bytes(indata))
        
        silence_duration= 2
        with sounddevice.RawInputStream(samplerate=16000, blocksize=8000,dtype="int16",channels=1,callback=callback):
            print("escuchando...")
            silence_counter= 0
            recognizer=KaldiRecognizer(model,16000)
            final_text=""
            while True:
                data=q.get()

                if recognizer.AcceptWaveform(data):
                    result= json.loads(recognizer.Result())['text']
                    silence_counter=0
                    final_text += f"{result}"
                else:
                    partial=json.loads(recognizer.PartialResult())['partial']
                    print(partial)
                    if partial=="":
                        silence_counter+=1

                if silence_counter >= silence_duration * (16000/8000):
                    print("silencio detectado")
                    break
            if final_text != "":
                print("listo")
            else:
                print("listo!")
                return ""
            
    def key_board(self):
        try:
            model=Model(self.vosk_path)
        except Exception as e:
            try:
                model= Model(self.vosk_model_lang)
            except Exception as e:
                print("error al cargar el modelo de voz")

        q=queue.Queue()
        def callback(indata,frames,time,status):
            q.put(bytes(indata))
        
        with sounddevice.RawInputStream(samplerate=16000, blocksize=8000,dtype="int16",channels=1,callback=callback):
            print("escuchando...")
            recognizer=KaldiRecognizer(model,16000)
            while True:
                data=q.get()

                if recognizer.AcceptWaveform(data):
                    result= json.loads(recognizer.Result())['text']
                
                else:
                    partial=json.loads(recognizer.PartialResult())['partial']
                    print(partial)
                
gemini= Asistente("genmini-1.5-flash",
                  "audio.mp3",
                  "./models/vosk-model-small-es-0.42",
                  "hola",
                  config={"temperature":0.8,"top_p":0.95,"top_k":64,"max_output_tokens":8192,"response_mime_type":"text/plain,"},
                  system_intruction="",
                  API="AIzaSyD--kHOT3Vp6QiuaXNyBA_Zx0L6CQ-lUls",
                  vosk_model_lang="es")

gemini.trascrip()