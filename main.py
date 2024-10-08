# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer
# from nltk.stem import WordNetLemmatizer
from openai import OpenAI

# nltk.download('punkt_tab')
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')

class Processing():
    def __init__(self, secrets):
        # self.stemmer = PorterStemmer()
        # self.lemmatizer = WordNetLemmatizer()
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
        print(response.choices[0].message.content)
        return response.choices[0].message.content

