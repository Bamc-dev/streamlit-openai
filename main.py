# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer
# from nltk.stem import WordNetLemmatizer
from openai import OpenAI
from PIL.Image import open
import io
import requests
import base64
from pydub import AudioSegment
# nltk.download('punkt_tab')
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')

class Processing():
    def __init__(self, secrets):
        # self.stemmer = PorterStemmer()
        # self.lemmatizer = WordNetLemmatizer()
        self.secrets = secrets
        self.client = OpenAI(api_key=secrets)
    # def tokenization(self, doc:str, stem:bool=False, lem:bool=False):
    #     tokens = word_tokenize(doc)
    #     tokens = [x for x in tokens if x not in stopwords.words('english') and x.isalnum()]
    #     tokens = [x.lower() for x in tokens]
    #     if(stem):
    #         tokens = [self.stemmer.stem(x) for x in tokens]
    #     if(lem):
    #         tokens = [self.lemmatizer.lemmatize(x) for x in tokens] 
    #     return tokens
    
    def openai_translate(self, textToTranslate):
        response = self.client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "system",
                "content": "Tu es traducteur uniquement de l'anglais vers le français. "
                        "L'utilisateur entre des phrases ou des mots en anglais et tu réponds par la traduction française. "
                        "Si l'utilisateur fait des fautes d'orthographe ou utilise des diminutifs d'expressions anglaises, "
                        "tu dois interpréter cela comme étant de l'anglais et fournir la meilleure traduction possible en français. "
                        "Sois indulgent avec les erreurs courantes ou les tournures incorrectes. "
                        "Si tu ne reconnais pas la langue de départ après avoir tenté de corriger les erreurs, tu réponds : "
                        "'Je ne traduis que de l'anglais vers le français'."
            },
            {
                "role": "user",
                "content": f"{textToTranslate}"
            }
        ],
        temperature=1, 
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        return response.choices[0].message.content

    def openai_text_summary(self, text):
        response = self.client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "text": "Tu es rédacteur web. Tu synthétise ce qu'on te donne en environ 100 mots. Afin que cela soit un bon article, tu utilises les conjonctions de coordinations",
                "type": "text"
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text" : f"{text}"
                }
            ]
            }
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
        )
        return response.choices[0].message.content

    def openai_text_gen(self, prompt):
        response = self.client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "text": "Tu es écrivain. On te demande de créer des text. A chaque fois cela prendre la forme de \"Thématique : ..... Contenue : ....\"",
                "type": "text"
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f"{prompt}"
                }
            ]
            }
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
        )
        return response.choices[0].message.content

    def openai_codex(self, code):
        response = self.client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "text": "Tu es un développeur aguéri. Chaque question que l'on te pose sur le code, tu sais y répondre. En tant qu'expert, il t'arrive souvent d'avoir du code envoyé. Tu le corriges. Tu renvoies seulement ce code corrigé sans donné de commentaire ou autre",
                "type": "text"
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f"{code}"
                }
            ]
            }
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
        )
        return response.choices[0].message.content
    
    def openai_create_image(self, prompt):
        response = self.client.images.generate(
        model="dall-e-3",
        prompt=f"{self.generate_prompt_with_chatgpt(prompt)}",
        size="1024x1024",
        quality="standard",
        n=1,
        )

        return response.data[0].url
    
    def openai_create_image_variation(self, img):
        response = self.client.images.create_variation(
        model="dall-e-2",
        image=open(io.BytesIO(img), "rb"),
        n=1,
        size="1024x1024"
        )
        return response.data[0].url
    
    def generate_prompt_with_chatgpt(self, prompt):
        response = self.client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": "Tu va prendre en entrée un prompt. Celui-ci sera d'un utilisateur lambda, qui ne s'y connait pas en IA.\nToi, ton travail sera d'améliorer se prompt afin que Dall-E puisse généré une image avec plus de détails.\nAucune autre instruction n'est toléré, ton but, juste amélioré un prompt."
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f"{prompt}"
                }
            ]
            }
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
        )
        return response.choices[0].message.content
    def vision_analyze_image(self, img):
        base64_image = base64.b64encode(img).decode('utf-8')
        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {self.secrets}"
        }

        payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "What’s in this image?"
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": "high"
                }
                }
            ]
            }
        ],
        "max_tokens": 300
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
    def openai_transcribe(self, audioBytes):
        buffer = io.BytesIO(audioBytes)
        buffer.name = "segment.mp3"
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=buffer
        )
        return transcription.text
    
    def openai_translate_audio(self, audioBytes):
        buffer = io.BytesIO(audioBytes)
        buffer.name = "recorded.mp3"
        transcript = self.client.audio.translations.create(
            model="whisper-1",
            file=buffer
        )
        return transcript.text