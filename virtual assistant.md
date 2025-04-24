# **virtual assistant**
---

## **Overview**
---
This project is a set of all the projects of the Adakademy students, in this all the AI were integrated to make a more useful one that can cover more fields.
## **Description**
---
This project is an AI that facilitates several functions, such as creating a web page with Bootrap, downloading YouTube videos, making PowerPoint presentations, and creating Word documents.

```python
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
```

## **User Methods**

| Method                       | Arguments                                                    | Returns                                | Description                                                  |
| ---------------------------- | ------------------------------------------------------------ | -------------------------------------- | ------------------------------------------------------------ |
| **`anwer`**                  | `text`: str - User input text                                | str - Sanitized AI response            | Processes text through Gemini AI and returns cleaned response without special characters |
| **`talk`**                   | `talk`: str - Text to speak                                  | None                                   | Converts text to speech using gTTS, plays audio, then deletes temp file |
| **`trascrip`**               | None                                                         | str - Transcribed text or empty string | Listens for speech input until silence, returns transcription |
| **`key_board`**              | None                                                         | True                                   | Continuous speech recognition mode showing real-time partial results |
| **`crear_un_proyecto_wed`**  | `caracteristicas_pagina`: str - Website description `nombre`: str - Project name `ruta_proyecto`: str - Base directory | None                                   | Generates Bootstrap/CSS HTML project, creates folder structure, opens in browser/editor |
| **`escribir_un_documento`**  | `tema`: str - Document topic                                 | None                                   | Creates Python script that generates a document about the topic |
| **`crear_una_presentacion`** | `tema`: str - Presentation topic                             | None                                   | Generates and executes Python code to create PowerPoint presentation |
| **`escribe_una_nota`**       | `directorio_principal`: str - Base path `carpeta`: str - Folder name `tema`: str - Note content | None                                   | Creates and opens text file with content about specified topic |
| **`buscar_un_video`**        | `busqueda`: str - Search query                               | None                                   | Finds first YouTube result and opens in default browser      |

## **Dependencies**

- **Voice commands** (speech-to-text via VOSK & text-to-speech via gTTS)

- **AI-powered content generation** (Gemini AI for text, HTML, and scripts)

- **Document automation** (Word, PowerPoint, notes)

- **Web development** (Bootstrap-based projects)

- **YouTube integration** (search & download video

  

  ## **Getting Started**

  1. **Initialize the assistant**:

  ```python
  asistente = Asistente(
      model_name="gemini-pro",
      audio_path="response.mp3",
      vosk_path="./models/vosk-model-small-es-0.42",
      API="your_gemini_api_key"
  )
  ```

  1. **Basic voice interaction**:

  ```python
  user_input = asistente.transcrip()  # Speak your command  
  response = asistente.answer(user_input)  # Get AI response  
  asistente.talk(response)  # Hear the answer  
  ```

  1. **Create a project**:

  ```python
  asistente.crear_un_proyecto_wed(
      "Portfolio website", 
      "my_portfolio", 
      "~/projects"
  )
  ```

  ## **Donation**

  Support this project:

  - pago movil
  - zelle 
  - divisa 

