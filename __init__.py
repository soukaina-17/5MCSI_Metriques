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
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    # Convertir la date au format souhaité
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

@app.route('/get-commits')
def get_commits():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)
    commits = response.json()  # Convertir la réponse JSON en objet Python

    # Extraire les informations de chaque commit
    commit_data = []
    for commit in commits:
        commit_info = {
            "commit": commit['sha'],
            "author": commit['commit']['author']['name'],
            "date": commit['commit']['author']['date']
        }
        commit_data.append(commit_info)

    return jsonify(commit_data)



if __name__ == "__main__":
  app.run(debug=True)

#com


