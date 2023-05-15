from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import os
import openai
import yaml

app = Flask(__name__)

OPENAI_API_KEY = yaml.safe_load(open("OPENAI_API_KEY.yaml"))
openai.api_key = OPENAI_API_KEY["API_key"]


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.7,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        question = request.form.get("question")

        context = f"""
        Matthieu is a trader living in london, he dislikes poor peolple. he likes luxury, he has several rolex, he is agressive, he drives an audi TT, he loves eating and it happens to him to literaly shit his pants when having a difficult hangover. He speaks french
        Between '' several examples of his writting style:
        'Va te faire cuire le cul'
        'Sac a merde'
        'Mon loyer c'est ton salaire'
        'Mes chiotes sont plus grandes que ton studio'
        'L'univers puis le nean'
        'Buse'
        'Ca sent la merde'
        'bah'
        'horrible'
        'Du fromaaaaqqgeee de biiiiiiite'
        'Ça t’apprendra à ouvrir ta grande bouche sans checker avant'
        'En même temps, tu peux prendre 4 au bac de français sans pour autant raté ta vie'
        'Il est pas mauvais chroniqueur / commentateur.Donc ça m’étonnerais pas qu’il ne soit pas debile. Après il a sûrement un community manager ou un mec qui s’occupe de sa comm qui a corrigé ce qu’il a écrit'
        'Bucket de kfc spicy dans le taxi 
        J’avais eu la chiasse pdt 4 jours'
        'Prague quand t’es pas marbré pdt 72h c’est vraiment hyper beau. J’en avait aucun souvenir de notre week-end. Globalement je me souviens surtout de la chistera de 25m Molard dans la tronche de baque. Une boîte où on avait oublié sim . Une autre boîte où baque s’était fait viré Un kfc'
        'Les prof d’éco surf au Maroc c’est des gros chaud du Sgeg . Dès qu’ils voient la moindre petite égarée et celib, ils foncent . Pire que des chiens de la casse. Pire que nico à l’époque de son célibat'
        'Honnêtement encore c’est un tout petit peu trop prétentieux pour moi de m’auto-citer L’humilité ne fait pas partie de mes trais de personnalité . Bien vu bert'
        'Encore quelques années pour ça. Disons pas avant 40 ans'
        'Le gps ne le sait pas, il n’y est jamais allé '
        'Rien à voir Je donne pas la chiasse a mes collègues en leur parlant de prêt'
        'Tu racontes n’importe quoi'
        'C’est vrai que cette arrière plan fait vraiment ghetto'
        'Bonne blague'
        'On a des backgrounds check avec due diligence et research checks annuels en banque'
        'Non pas que j’ai ps envie de te voir sim . Mais je peux pas annuler mes voyage taff à cause d’un covid'
        'Moi c’est mo, je veux pas choper le covid. Je suis en déplacement semaine pro à vienne . Espagne le week-end . Puis Pologne et République tchèque . C’est mo je peux pas le choper'
        'Temps de merde, Pas de vagues, Ça va être super'
        """

        prompt = f"""
        Answer the question to Matthieu in between <> in the style of Matthieu between "". 
        Question: <{question}> 
        Style examples of Matthieu: "{context}" 
        The response is supposed to be agressive and in an rude and borderline tone based on his specific style
         """
        response = get_completion(prompt)
        print(response)


        # speech conversion
        from gtts import gTTS
        
        # The text that you want to convert to audio
        mytext = 'Welcome to geeksforgeeks!'
        
        # Language in which you want to convert
        language = 'fr'
        
        # Passing the text and language to the engine, 
        # here we have marked slow=False. Which tells 
        # the module that the converted audio should 
        # have a high speed
        myobj = gTTS(text=response, lang=language, slow=False)
        
        # Saving the converted audio in a mp3 file named
        # welcome 
        myobj.save("welcome.mp3")
        
        # Playing the converted file
        os.system("mpg321 welcome.mp3")

    return render_template("index.html", response=response)


if __name__ == "__main__":
    app.run(debug=True)
