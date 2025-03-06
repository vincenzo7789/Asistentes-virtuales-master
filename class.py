import google.generativeai as genai
import playsound
from vosk import Model,KaldiRecognizer
import os
import json, sys, queue, sounddevice, requests
from gtts import gTTS
import docx
import subprocess
import pptx
from pptx import Presentation
import yt_dlp 

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

    def crear_un_proyecto_wed(self,caracteristicas_pagina:str,nombre:str,ruta_proyecto:str):
        nombre_proyecto= nombre
        nombre_ruta_proyecto= ruta_proyecto
        carpeta_nativa= os.path.join(os.path.expanduser("~"),nombre_proyecto)
        carpeta_final=os.path.join(carpeta_nativa, nombre_proyecto)
        os.makedirs(carpeta_final,exist_ok=True)
        codigo_html= self.model.generate_content([caracteristicas_pagina,"crea una pagina web referente al tema que te de el usuario, no uses caracteres especiales, no des indicaciones, solo devuelve el codigo HTML, este lo haras usando bootstrap y css en el mismo index HTML"])
        codigo_html= codigo_html.text.split("``html")[1].split('```')[0]
        with open(os.path.join(carpeta_final,"index.html"),"w",encoding="utf-8") as archivo_html:
            archivo_html.write(codigo_html)
        os.system(f"start msedge {carpeta_final}") 
        os.system(f"start Code {carpeta_final}")

    def escribir_un_documento(self,tema:str):

    
        """"
        descripcion:
        esta funcion redacta un ensayo del tema que te indique el usuario, 
        evitnado usar caracteres especiales

        args:
        tema: es el tema del documento
        """
        result=self.model.generate_content([tema,"redacta un ensayo del tema que te indique el usuario, evita usar caracteres especiales"])
        codigo= result.text.slit("``")[1].replace("python","").replace("¬","")
        with open("documento.py","w") as f:
            f.write(codigo)
        subprocess.run(['python,documento.py'])

    def crear_una_presentacion(self, tema: str):
        """
        Esta es una función que crea una presentación de PowerPoint cuando el usuario dice
        "crea una presentación" o algo así.

        Args:
            tema: Es el tema de la presentación.
        """
        try:
            resultado = self.model.generate_content([
                f"Créame una presentación de PowerPoint sobre {tema} en español",
                "Recuerda que tu resultado será un script de Python que con la librería pptx genere una presentación de PowerPoint, SOLO DEVUELVE EL CÓDIGO y recuerda al final abrir dicho archivo pptx usando la librería OS.",
                "En las cadenas de textos ni en los comentarios no uses caracteres especiales ni uses acentos como 'ñ' o 'á' y no coloques imagenes."
            ])

            # Verifica si el resultado contiene un bloque de código
            if "```" in resultado.text:
                codigo = resultado.text.split("```")[1].replace("python", "").replace("�", "")
            else:
                codigo = resultado.text  # Si no hay bloque de código, usa el texto completo

            # Escribe el código en un archivo Python
            with open("presentacion2.py", "w", encoding="utf-8") as f:
                f.write(codigo)

            # Ejecuta el archivo Python generado
            subprocess.run([sys.executable, "presentacion2.py"])
        except Exception as e:
            print(f"Error al crear la presentación: {e}")

    def escribe_una_nota(self,directorio_principal:str,carpeta:str,tema:str):
        """
        description:
        esta funcion es para crear una nota txt cuando usuario expresa que quiere
        crear una nota sobre un tema, en un directorio indicado por el usuario 

        args:
        directorio_principal: es el directorio principal donde se creara la carpeta 
        carpeta: es el nombre de la carpeta 
        tema: es el tema de la nota 
        """
        result=self.model.generate_content(f"crea una nota sobre{tema}")
        carpeta_nativa= os.path.join(os.path.expanduser("~"),directorio_principal)
        carpeta_nota= os.path.join(carpeta_nativa, carpeta)
        os.makedirs(carpeta_nota,exist_ok=True)
        result= result.text.replace("#","").replace("*","")
        with open(os.path.join(carpeta_nota,f"{tema}.txt"),"w", encoding="utf-8") as archivo:
            archivo.write(result)
        subprocess.run(['notepad', os.path.join(carpeta_nota,f"{tema}.txt")])
    
    def buscar_un_video(self, busqueda:str):
        """"
        descrition:
        esta funcion busca un video en youtube 

        args:
        busqueda: es la busqueda que el ususario quiera hacer en youtube
        """
        url= f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={busqueda}&type=video&type=AIzaSyAcKEFPYeqQr9lpI7eCOYgouU9FGVkkooo&maxResults=1"
        reply= requests.get(url)
        data=reply.json()
        if reply.status_code==200:
            print("listo")
            if "items" in data and len(data["items"]) > 0:
                video_id=data["items"][0]["videoId"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                subprocess.run(['msedge',video_url])

    def descargar_un_video(self,busqueda:str, ruta:str):
        """
        description:
        esta funcion es para descargar un video de youtube
        
        args:
        busqueda: es el url del video que el ususario quiere descargar  
        ruta: es la ruta donde se guardara el video
        """
        yld_ops= {
            'format': 'bestvideo',
            'outtmpl':'%(title)s.%(ext)s',
            'mergue_output_format': 'mp4'
            }
        try:
            print("iniciando")
            url= f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={busqueda}&type=video&type=AIzaSyAcKEFPYeqQr9lpI7eCOYgouU9FGVkkooo&maxResults=1"
            reply= requests.get(url)
            data=reply.json()
            if reply.status_code == 200:
                print("listo")
                if "items" in data and len(data["items"]) > 0:
                    video_id =data["items"][0]["videoId"]
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    with yt_dlp.YoutubeDL(yld_ops) as ydl:
                        ydl.download([video_url])
        except Exception as e:
            print("error al descargar el video")

gemini= Asistente("genmini-2.0-flash",
                  "audio.mp3",
                  "./models/vosk-model-small-es-0.42",
                  "hola",
                  config={"temperature":0.8,
                  "top_p":0.95,"top_k":64,
                  "max_output_tokens":8192,
                  "response_mime_type":"text/plain",
                  },
                  system_intruction="",
                  API="AIzaSyD--kHOT3Vp6QiuaXNyBA_Zx0L6CQ-lUls",
                  vosk_model_lang="es")


