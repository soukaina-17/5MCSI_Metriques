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
# URL de l'API pour récupérer les commits
GITHUB_COMMITS_API = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"

# Route pour extraire les minutes de la date du commit
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

# Route pour récupérer les commits et créer le graphique
@app.route('/commits/')
def commits():
    # Récupérer les commits de l'API GitHub
    response = requests.get(GITHUB_COMMITS_API)
    commits_data = response.json()

    # Extraire les minutes des dates de commit
    minutes_list = []
    for commit in commits_data:
        commit_date = commit['commit']['author']['date']
        minutes = extract_minutes_from_date(commit_date)
        minutes_list.append(minutes)

    # Compter les commits par minute
    commit_counts = Counter(minutes_list)

    # Créer un graphique à partir des données
    fig, ax = plt.subplots()
    ax.bar(commit_counts.keys(), commit_counts.values())
    ax.set_xlabel('Minute')
    ax.set_ylabel('Nombre de commits')
    ax.set_title('Nombre de commits par minute')
  

if __name__ == "__main__":
  app.run(debug=True)

#com


