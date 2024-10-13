from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_verbs():
    url = "https://www.e-anglais.com/ressources/verbes_irreguliers.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find('table')
    rows = table.find_all('tr')[1:]  # Ignorer la première ligne (en-têtes)
    
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

@app.route('/recherche')
def search_verbs():
    category = request.args.get('categorie', default='infinitif', type=str)
    verbs = scrape_verbs()
    
    if category in ['infinitif', 'preterit', 'participe_passe', 'traduction']:
        results = [verb[category] for verb in verbs]
        return jsonify({category: results})
    else:
        return jsonify({"error": "Catégorie non valide. Utilisez 'infinitif', 'preterit', 'participe_passe', ou 'traduction'."}), 400

@app.route('/dynamique')
def dynamic_search():
    query = request.args.get('q', default='', type=str).lower()
    verbs = scrape_verbs()

    if not query:
        return jsonify({"error": "Veuillez fournir une requête valide."}), 400

    parts = query.split()
    if len(parts) != 2:
        return jsonify({"error": "Format de requête invalide. Utilisez 'catégorie verbe'."}), 400

    category, verb = parts
    
    if category not in ['infinitif', 'preterit', 'participe_passe', 'traduction']:
        return jsonify({"error": "Catégorie non valide. Utilisez 'infinitif', 'preterit', 'participe_passe', ou 'traduction'."}), 400

    for v in verbs:
        if v['infinitif'].lower() == verb or v['traduction'].lower().startswith(verb):
            return jsonify({category: v[category]})

    return jsonify({"error": "Verbe non trouvé."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
