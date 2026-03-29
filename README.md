# CV-Tracker

CV-Tracker est une application web moderne qui facilite la gestion, l’indexation et la recherche intelligente de CV (PDF, Word, Excel) grâce à la puissance d’Apache Solr et de Flask.

## Fonctionnalités principales

- **Upload de CV** : Ajoutez facilement vos fichiers via un formulaire simple et sécurisé.
- **Indexation automatique** : Les documents sont analysés (titre, auteur, contenu, format) grâce à Solr Cell (Tika).
- **Recherche intelligente** : Une barre de recherche unique interroge tous les champs importants (titre, auteur, contenu) avec une pertinence optimisée.
- **Filtres dynamiques** : Affinez vos résultats par format de fichier, auteur ou même ciblez un fichier précis.
- **Classement par pertinence** : Les résultats sont triés du plus pertinent au moins pertinent, avec affichage du score Solr.
- **Interface moderne** : Design responsive et professionnel basé sur Bootstrap 5.

## Prérequis
- Python 3.8+
- Apache Solr (avec Solr Cell/Tika activé)
- Les dépendances Python listées dans `requirements.txt`

## Installation rapide
1. **Clonez le projet**
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Lancez Solr et créez un core nommé `cvtracker` :
   ```bash
   bin/solr start
   bin/solr create -c cvtracker
   ```
4. Démarrez l’application Flask :
   ```bash
   python app.py
   ```
5. Accédez à l’interface sur [http://localhost:5000](http://localhost:5000)

## À propos
CV-Tracker a été conçu pour simplifier la gestion de vos CV et accélérer la recherche de profils. L’interface est intuitive, la recherche puissante, et l’indexation automatique vous fait gagner un temps précieux.

N’hésitez pas à contribuer ou à adapter le projet à vos besoins !
