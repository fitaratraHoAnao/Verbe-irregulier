from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_verbs():
    url = "https://www.e-anglais.com/ressources/verbes_irreguliers.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find('table')
    rows = table.find_all('tr')[1:]  # Ignorer la premiÃ¨re ligne (en-tÃªtes)
    
    verbs = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 5:
            verb = {
                "infinitif": cols[1].text.strip(),
                "preterit": cols[2].text.strip(),
                "participe_passe": cols[3].text.strip(),
                "traduction": cols[4].text.strip()
            }
            verbs.append(verb)
    
    return verbs

@app.route('/verbe_irregulier')
def get_irregular_verbs():
    verbs = scrape_verbs()
    return jsonify(verbs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
