from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)     

#Exercice 2 : Création d'une nouvelle route
@app.route('/contact/')
def MaPremiereAPI():
    return render_template("contact.html")
  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')
  
#Exercice 3 : Les données d'une API
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)


#Exercice 3 Bis : Les fichiers HTML
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
  

#Exercice 4 : Créer son histogramme
@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

#Exercice5
 #Fonction pour extraire la minute à partir de la date
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    return date_object.minute

# Route pour récupérer et traiter les commits
@app.route('/commits/')
def commits():
    # Récupérer les commits depuis l'API GitHub
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    commits_data = response.json()

    # Extraire les minutes de chaque commit
    minutes = [extract_minutes(commit['commit']['author']['date']) for commit in commits_data]

    # Compter le nombre de commits par minute
    commit_counts = Counter(minutes)

    # Créer un graphique
    plt.bar(commit_counts.keys(), commit_counts.values())
    plt.xlabel('Minute')
    plt.ylabel('Nombre de commits')
    plt.title('Nombre de commits par minute')

    # Convertir le graphique en image pour l'affichage sur la page web
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    # Retourner le graphique sous forme d'image Base64 à afficher dans le HTML
    return render_template('commits.html', img_base64=img_base64)






if __name__ == "__main__":
  app.run(debug=True)

#com


