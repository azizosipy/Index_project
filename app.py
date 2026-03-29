import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pysolr
from werkzeug.utils import secure_filename

# Configuration Flask
app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'xlsx', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuration Solr
SOLR_URL = 'http://localhost:8983/solr/cvtracker'
solr = pysolr.Solr(SOLR_URL, always_commit=True, timeout=10)

# Vérifie l'extension du fichier
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Page d'accueil et recherche
@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.args.get('q', '')
    selected_format = request.args.get('format', '')
    selected_author = request.args.get('author', '')
    results = []
    facets = {'format': [], 'author': []}
    selected_file = request.args.get('file_id', '')
    file_ids = []
    if query:
        # Construction de la requête eDisMax avec boosts
        params = {
            'defType': 'edismax',
            'qf': 'titre^3 auteur^2 contenu^1',
            'fl': '*,score',
            'facet': 'true',
            'facet.field': ['format', 'auteur'],
            'facet.mincount': 1
        }
        fq = []
        if selected_format:
            fq.append(f'format:"{selected_format}"')
        if selected_author:
            fq.append(f'auteur:"{selected_author}"')
        if selected_file:
            fq.append(f'id:"{selected_file}"')
        if fq:
            params['fq'] = fq
        solr_results = solr.search(query, **params)
        results = solr_results.docs
        # Récupération des facettes
        if 'facet_counts' in solr_results.raw_response:
            facets = {
                'format': solr_results.raw_response['facet_counts']['facet_fields']['format'],
                'author': solr_results.raw_response['facet_counts']['facet_fields']['auteur']
            }
        # Ajout du score à chaque résultat
        for doc in results:
            doc['score'] = doc.get('score', 0)
        # Tri par score décroissant
        results = sorted(results, key=lambda x: x['score'], reverse=True)
    # Récupérer la liste des fichiers indexés pour le filtre
    try:
        all_files = solr.search('*:*', **{'fl': 'id,titre', 'rows': 1000})
        file_ids = [{'id': doc.get('id'), 'titre': doc.get('titre', doc.get('id'))} for doc in all_files.docs]
    except Exception:
        file_ids = []
    return render_template('index.html', results=results, query=query, facets=facets, selected_format=selected_format, selected_author=selected_author, file_ids=file_ids, selected_file=selected_file)

# Upload et indexation de fichier
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('Aucun fichier sélectionné', 'danger')
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash('Aucun fichier sélectionné', 'danger')
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)
        # Indexation via Solr Cell (Tika)
        try:
            with open(filepath, 'rb') as f:
                solr_response = solr.extract(f, params={
                    'literal.id': filename,
                    'resource.name': filename,
                    'commit': 'true',
                    'extractOnly': 'false',
                    'uprefix': 'attr_',
                    'fmap.content': 'contenu',
                    'fmap.title': 'titre',
                    'fmap.author': 'auteur',
                    'literal.format': filename.rsplit('.', 1)[1].upper()
                })
            flash('Fichier indexé avec succès', 'success')
        except Exception as e:
            flash(f'Erreur lors de l\'indexation : {e}', 'danger')
        return redirect(url_for('index'))
    else:
        flash('Format de fichier non supporté', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
