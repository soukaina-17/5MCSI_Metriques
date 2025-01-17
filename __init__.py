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

# URL de l'API GitHub pour récupérer les commits
GITHUB_COMMITS_API = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    """
    Cette route prend une chaîne de date au format "YYYY-MM-DDTHH:MM:SSZ" et en extrait les minutes.
    """
    try:
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use "YYYY-MM-DDTHH:MM:SSZ".'}), 400

@app.route('/extract-commit-author/<commit_sha>', methods=['GET'])
def extract_commit_author(commit_sha):
    """
    Cette route prend un commit SHA et retourne le message du commit et le nom de l'auteur.
    """
    response = requests.get(f"{GITHUB_COMMITS_API}/{commit_sha}")
    
    if response.status_code == 200:
        commit_data = response.json()
        commit_message = commit_data['commit']['message']
        author_name = commit_data['commit']['author']['name']
        return jsonify({
            'commit_message': commit_message,
            'author_name': author_name
        })
    else:
        return jsonify({'error': 'Commit not found or invalid SHA'}), 404




if __name__ == "__main__":
  app.run(debug=True)

#com


