from datetime import datetime
import pandas as pd
import pickle
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import copy
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


########################################################################################################################
class Author:
    """
    Classe représentant un auteur.

    Cette classe stocke le nom de l'auteur, le nombre de documents qu'il a publiés,
    et un dictionnaire des documents écrits par l'auteur.
    """

    def __init__(self, name):
        self.name = name
        self.ndoc = 0  # Nombre de documents publiés par l'auteur
        self.production = {}  # Dictionnaire des documents écrits par l'auteur

    def add(self, doc):
        """
        Ajoute un document à la production de l'auteur
        """
        self.ndoc += 1
        self.production[doc.titre] = doc

    def __str__(self):
        return f"{self.name} - {self.ndoc} document(s) publié(s)"

########################################################################################################################

class Document:
    """
    Classe représentant un document.

    Cette classe stocke les informations d'un document, y compris son titre, auteur,
    date, URL, et le contenu textuel.
    """

    def __init__(self, titre, auteur, date, url, texte):
        self.titre = titre
        self.auteur = auteur
        self.date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
        self.url = url
        self.texte = texte

        self.annotations = {}  # attribut pour stocker des annotations éventuelles du document


    def afficher_infos(self):
        return print(f"Titre: {self.titre}\nAuteur: {self.auteur}\nDate: {self.date}\nURL: {self.url}\nTexte: {self.texte}")

    def __str__(self):
        return self.titre

    def ajouter_annotation(self, id_annotation, texte, position = None, auteur=None, date=None):
        """
        Fonction pour rajouter des annotations à un document lors de la phase d'analyse
        :param id_annotation:
        :param texte:
        :param position:
        :param auteur:
        :param date:

        """
        self.annotations[id_annotation] = {
            'texte': texte,
            'position': position,
            'auteur': auteur,
            'date': date
        }

    def afficher_annotations(self):
        """
        Fonction pour afficher les annotations d'un document
        :return:
        """
        for id_annotation, info in self.annotations.items():
            print(
                f"ID: {id_annotation}, Texte: {info['texte']}, Position: {info['position']}, Auteur: {info['auteur']}, Date: {info['date']}")


########################################################################################################################
class RedditDocument(Document):
    """
    Classe représentant un document Reddit.

    Hérite de la classe mère Document

    Cette classe stocke les informations d'un document Reddit, y compris son titre, auteur,
    date, URL, et le contenu textuel. Mais aussi le nombre de commentaires ..
    """

    def __init__(self, source, titre, auteur, date, url, texte, nb_commentaires):
        super().__init__(titre, auteur, date, url, texte)
        self.nb_commentaires = nb_commentaires
        self.type = source

    def get_nb_commentaires(self):
        return self.nb_commentaires

    def set_nb_commentaires(self, nb_commentaires):
        self.nb_commentaires = nb_commentaires

    def get_type(self):
        return self.type

    def afficher_infos(self):
        print(f"Source: {self.type}")
        super().afficher_infos()
        print(f"Nombre de commentaires: {self.nb_commentaires}")

########################################################################################################################
class ArxivDocument(Document):
    """
      Classe représentant un document Arxiv.

      Hérite de la classe mère Document

      Cette classe stocke les informations d'un document Arxiv, y compris son titre, auteur,
      date, URL, et le contenu textuel. Mais aussi les co-auteurs..
      """

    def __init__(self, source, titre, auteur, date, url, texte, co_auteurs):
        super().__init__(titre, auteur, date, url, texte)
        self.co_auteurs = co_auteurs
        self.type = source

    def get_co_auteurs(self):
        return self.co_auteurs

    def set_co_auteurs(self, co_auteurs):
        self.co_auteurs = co_auteurs

    def get_type(self):
        return self.type

    def afficher_infos(self):
        print(f"Source: {self.type}")
        super().afficher_infos()
        print(f"Co-auteurs: {self.co_auteurs}" if self.co_auteurs else "Co_auteurs: aucun")


########################################################################################################################
class DocumentFactory:
    """
    Classe DocumentFactory utilisée pour la création d'instances de documents.

    Cette classe suit le motif de conception 'Factory', permettant de créer des instances de différentes
    classes de documents en fonction du type de source spécifié.
    """

    @staticmethod
    def create_document(source, titre, auteur, date, url, texte, co_auteurs, nb_commentaires):
        """
        Crée une instance de document basée sur la source spécifiée.

        :param source: La source du document (par exemple, 'reddit' ou 'arxiv').
        :param titre: Le titre du document.
        :param auteur: L'auteur du document.
        :param date: La date de publication du document.
        :param url: L'URL du document.
        :param texte: Le contenu textuel du document.
        :param co_auteurs: Les co-auteurs du document (utilisé uniquement pour les documents arXiv).
        :param nb_commentaires: Le nombre de commentaires (utilisé uniquement pour les documents Reddit).
        :return: Une instance de RedditDocument, ArxivDocument, ou lève une exception si la source est inconnue.
        """
        if source == "reddit":
            return RedditDocument(source, titre, auteur, date, url, texte, nb_commentaires)
        elif source == "arxiv":
            return ArxivDocument(source, titre, auteur, date, url, texte, co_auteurs)
        else:
            raise ValueError(f"Type de document {source} non reconnu")


    def create_corpus(chemin_donnees_acquises, nom_corpus):
        """
        Crée un corpus à partir de données acquises.

        :param chemin_donnees_acquises: Le chemin d'accès au fichier contenant les données acquises.
        :param nom_corpus: Le nom à attribuer au corpus créé.
        :return: Un objet Corpus contenant les documents acquis.
        """
        # récupérer notre enregistrement corpus (l'ensemble de nos docs)
        docs = pd.read_csv(chemin_donnees_acquises, sep='\t')

        # instancier un objet Corpus pour y stocker sous forme d'instances d'autres objets les articles acquis
        corpus_articles = Corpus(nom_corpus)

        for _, doc in docs.iterrows():
            corpus_articles.add_document(doc['source'],
                                         doc['titre'],
                                         doc['auteur'],
                                         doc['date'],
                                         doc['url'],
                                         doc['texte'],
                                         doc['co_auteurs'],
                                         doc['nombre_commentaires'])
        return corpus_articles

########################################################################################################################

class Corpus:
    """
    Classe représentant L'ensemble de documents récoltés suite à une recherche.

    Le corpus est doté :
                      - d'un dictionnaire des documents le composant
                      - des auteurs les ayant écrits
                      - d'un compteur du nombre de documents
                      - d'un compteur du nombre d'auteurs
                      - et aussi d'un sac de mots, qui sera l'ensemble des textes concaténés

    """

    def __init__(self, nom):
        self.nom = nom
        self.authors = {}  # Dictionnaire des auteurs
        self.id2doc = {}  # Dictionnaire des documents
        self.ndoc = 0  # Comptage des documents
        self.naut = 0  # Comptage des auteurs
        self.texte_concatene = None # sera acquis au premier appel de la fonction search

    def add_document(self,source ,titre, auteur, date, url, texte, co_auteurs, nb_commentaires=0):
        # Créer une nouvelle instance de Document

        doc = DocumentFactory.create_document(source ,titre, auteur, date, url, texte, co_auteurs, nb_commentaires)

        # Ajouter le document à id2doc
        self.id2doc[titre] = doc

        # Incrémenter le comptage des documents
        self.ndoc += 1

        # Vérifier si l'auteur existe déjà dans authors
        if auteur not in self.authors:
            # Si l'auteur n'existe pas, créer une nouvelle instance et l'ajouter au dictionnaire
            current_auteur = Author(auteur)
            self.authors[auteur] = current_auteur
            self.naut += 1
        else:
            # Si l'auteur existe déjà, récupérer l'instance existante
            current_auteur = self.authors[auteur]

        # Utiliser la méthode "add" de l'instance pour ajouter le document à sa production
        current_auteur.add(doc)

    def __repr__(self):
        return f"Corpus '{self.nom}' contenant {self.ndoc} documents et {self.naut} auteurs."

    def __repr__html(self):
        # Commencer par une chaîne de caractères contenant le début de la table HTML
        html = f"<h3>Corpus: {self.nom}</h3>"
        html += "<table border='1'>"
        html += "<tr><th>Titre</th><th>Auteur</th><th>Date</th><th>URL</th><th>Extrait</th></tr>"

        # Pour chaque document, ajouter une ligne au tableau HTML
        for doc in self.id2doc.values():
            html += f"<tr><td>{doc.titre}</td><td>{doc.auteur}</td><td>{doc.date}</td><td><a href='{doc.url}'>Lien</a></td><td>{doc.texte[:100]}...</td></tr>"

        # Terminer la table HTML
        html += "</table>"

        # Retourner la chaîne de caractères HTML
        return html

    def documents_par_date(self, n):
        # Trier les documents par date puis par titre
        sorted_docs = sorted(self.id2doc.values(), key=lambda x: (x.date), reverse = True)

        # Afficher les n premiers documents triés
        for doc in sorted_docs[:n]:
            print(f"Titre: {doc.titre}, Date: {doc.date}, Auteur: {doc.auteur}")

    def documents_par_titre(self, n):
        # Trier les documents par date puis par titre
        sorted_docs = sorted(self.id2doc.values(), key=lambda x: (x.titre))

        # Afficher les n premiers documents triés
        for doc in sorted_docs[:n]:
            print(f"Titre: {doc.titre}, Date: {doc.date}, Auteur: {doc.auteur}")

    def documents_par_date_et_titre(self, n):
        # Trier les documents par date puis par titre
        sorted_docs = sorted(self.id2doc.values(), key=lambda x: (x.date, x.titre))

        # Afficher les n premiers documents triés
        for doc in sorted_docs[:n]:
            print(f"Titre: {doc.titre}, Date: {doc.date}, Auteur: {doc.auteur}")

    def newest_doc_date(self):
        """
        Retourne la date du document le plus récent du corpus.
        """
        if not self.id2doc:
            return None

        return max(doc.date for doc in self.id2doc.values())

    def oldest_doc_date(self):
        """
        Retourne la date du document le plus ancien du corpus.
        """
        if not self.id2doc:
            return None

        return min(doc.date for doc in self.id2doc.values())
    def save(self, filename):
        """
        Sauvegarde l'objet Corpus dans un fichier.

        Args:
            filename (str): Le nom du fichier où sauvegarder l'objet.
        """
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, filename):
        """
        Charge un objet Corpus à partir d'un fichier.

        Args:
            filename (str): Le nom du fichier depuis lequel charger l'objet.

        Returns:
            Corpus: L'objet Corpus chargé.
        """
        with open(filename, 'rb') as file:
            return pickle.load(file)

    def concatener_textes(self):
        if self.texte_concatene is None:
            self.texte_concatene = ' '.join([str(doc.texte) if doc.texte is not None else '' for doc in self.id2doc.values()])

    def search(self, mot_clef):

        self.concatener_textes()

        # Utilisez re.findall pour trouver toutes les occurrences du mot-clé
        return re.findall(mot_clef, self.texte_concatene)

    def concorde(self, expression, taille_contexte):
        """
        Recherche les occurrences de l'expression dans le corpus, en fournissant un contexte autour de chaque occurrence.

        Args:
            expression (str): L'expression à rechercher dans le corpus.
            taille_contexte (int): La taille du contexte autour de l'expression trouvée.

        Returns:
            DataFrame: Un DataFrame contenant les contextes gauche et droit de chaque occurrence de l'expression.
        """
        # concatener les textes
        self.concatener_textes()

        # Trouver toutes les occurrences de l'expression
        pattern = re.compile(
            r'(.{{0,{}}})({})(.{{0,{}}})'.format(taille_contexte, re.escape(expression), taille_contexte))
        matches = pattern.finditer(self.texte_concatene)

        # Créer une liste pour stocker les résultats
        concordances_list = []

        # Remplir la liste avec les résultats
        for match in matches:
            concordance = {
                'contexte gauche': match.group(1),
                'motif trouvé': match.group(2),
                'contexte droit': match.group(3)
            }
            concordances_list.append(concordance)

        # Convertir la liste en DataFrame
        concordances = pd.DataFrame(concordances_list, columns=['contexte gauche', 'motif trouvé', 'contexte droit'])

        return concordances

    def nettoyer_texte(self, texte):
        """
        Nettoie le texte en appliquant plusieurs traitements.
        """
        # s'assurer de bien transmettre une chaine de texte

        if texte is None or str(texte).lower() == 'nan':
            return ''

        # suppression des nombres et conversion en minuscules
        texte = re.sub(r'\d+', '', texte).lower()

        # Suppression de la ponctuation
        texte = re.sub(r'[^\w\s]', '', texte)

        # Supprimer les stopwords
        stop_words = set(stopwords.words('english'))  # ne pas oublier de le spécifier
        mots = texte.split()
        mots_filtrés = [mot for mot in mots if mot not in stop_words]
        texte_nettoye = ' '.join(mots_filtrés)

        return texte_nettoye

    def construire_vocabulaire(self):
        """
        Construit le vocabulaire à partir des textes de tous les documents du corpus.

        Returns:
            dict: Un dictionnaire avec chaque mot unique et son nombre d'occurrences.
        """
        vocabulaire = set()

        # Boucler sur chaque document et extraire les mots
        for doc in self.id2doc.values():
            # Nettoyer le texte (en utilisant la fonction nettoyer_texte si elle est définie)
            texte_nettoye = self.nettoyer_texte(doc.texte)

            # Séparer les mots en utilisant l'espace, la tabulation, et la ponctuation comme délimiteurs
            mots = re.findall(r'\b\w+\b', texte_nettoye)

            # Ajouter les mots au set vocabulaire
            vocabulaire.update(mots)

        # Convertir le set en dictionnaire avec le compte des occurrences
        vocabulaire_dict = {index: mot for index, mot in enumerate(vocabulaire)}


        return vocabulaire_dict

    def nombre_mots_uniques(self):
        """
        Détermine le nombre total de mots uniques dans le corpus.
        Soit la taille du dictionnaire

        Returns:
            int: Le nombre de mots uniques dans le corpus.
        """
        vocabulaire_dict = self.construire_vocabulaire()
        return len(vocabulaire_dict)

    def calculer_frequences(self, vocabulaire_dict):
        # Créer un dictionnaire pour stocker les fréquences des termes dans chaque document
        freq_par_doc = {doc.titre: {mot: 0 for mot in vocabulaire_dict.values()} for doc in self.id2doc.values()}

        for doc in self.id2doc.values():
            # Nettoyage et extraction des mots
            texte_nettoye = self.nettoyer_texte(doc.texte)
            mots = re.findall(r'\b\w+\b', texte_nettoye)

            # Compter les fréquences des mots pour ce document
            for mot in mots:
                if mot in freq_par_doc[doc.titre]:
                    freq_par_doc[doc.titre][mot] += 1

        # Transformer le dictionnaire en DataFrame pour une meilleure lisibilité
        freq_df = pd.DataFrame.from_dict(freq_par_doc, orient='index')

        return freq_df

    def calculer_frequences_2(self, vocabulaire_dict):
        # Créer un dictionnaire pour stocker les fréquences des termes dans chaque document
        freq_par_doc = {index: {mot: 0 for mot in vocabulaire_dict.values()} for index, doc in
                        enumerate(self.id2doc.values())}

        for index, doc in enumerate(self.id2doc.values()):
            # Nettoyage et extraction des mots
            texte_nettoye = self.nettoyer_texte(doc.texte)
            mots = re.findall(r'\b\w+\b', texte_nettoye)

            # Compter les fréquences des mots pour ce document spécifique
            for mot in mots:
                if mot in vocabulaire_dict.values():  # Assurez-vous que le mot est dans le vocabulaire
                    freq_par_doc[index][mot] += 1

        # Transformer le dictionnaire en DataFrame pour une meilleure lisibilité
        freq_df = pd.DataFrame.from_dict(freq_par_doc, orient='index')

        return freq_df

    def vectoriser_documents(self):
        """
        Vectorise les documents du corpus en utilisant TF-IDF.
        """
        # Assurez-vous que les textes sont concaténés
        self.concatener_textes()

        # Initialiser le vectoriseur TF-IDF
        self.vectorizer = TfidfVectorizer()

        # Créer une liste de tous les textes des documents
        documents = [str(doc.texte) if doc.texte is not None else '' for doc in self.id2doc.values()]

        # Vectoriser les documents
        self.tfidf_matrix = self.vectorizer.fit_transform(documents)

    def rechercher_documents(self, requete):
        """
        Recherche les documents pertinents basés sur une requête multi-mots.

        Args:
            requete (str): La requête de recherche entrée par l'utilisateur.

        Returns:
            DataFrame: Un DataFrame contenant les documents triés par pertinence.
        """
        # Vérifiez si les documents ont été vectorisés
        if not hasattr(self, 'tfidf_matrix'):
            self.vectoriser_documents()

        # Nettoyer et vectoriser la requête
        requete_vectorisee = self.vectorizer.transform([requete])

        # Calculer la similarité cosinus
        cos_similarities = cosine_similarity(requete_vectorisee, self.tfidf_matrix)

        # Récupérer les scores de similarité pour chaque document
        scores = cos_similarities[0]

        # Créer un DataFrame pour les résultats
        resultats = pd.DataFrame({
            'Document': [doc.titre for doc in self.id2doc.values()],
            'Score': scores
        })

        # Trier les résultats par score de similarité
        resultats_ordonnes = resultats.sort_values(by='Score', ascending=False)

        return resultats_ordonnes

    def vision_d_ensemble(self, max_words = 200, min_word_length = 0, background_color = 'pink' ):
        """
        Présentation générale du corpus
        Génère et affiche un nuage de mots pour le texte du corpus.
        """
        print(f"Ce Corpus est composé de : {self.ndoc} document(s).")
        print(f"Ces documents ont été rédigés par : {self.naut} auteur(s)")
        print(f"Le document le plus ancien a été rédigé le : {self.oldest_doc_date()}.")
        print(f"Le document le plus récent a été rédigé le : {self.newest_doc_date()}.")
        print(f"Le Corpus totalise  {self.nombre_mots_uniques()} mots uniques.")
        print("Voici un nuage représentant Les mots par leur fréquence d'apparition dans le corpus")
        # Concaténer tous les textes du corpus
        full_text = ' '.join(str(doc.texte) for doc in self.id2doc.values() if str(doc.texte) != 'nan')

        # Générer le nuage de mots
        wordcloud = WordCloud(width=800, height=400, background_color= background_color, max_words=max_words, min_word_length = min_word_length).generate(full_text)

        # Afficher le nuage de mots à l'aide de matplotlib
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

    def copier_et_filtrer_avant_date(self, date_limite):
        # Créer une copie profonde du corpus
        copie_corpus = copy.deepcopy(self)

        # Filtrer les documents pour ne garder que ceux avant la date limite
        documents_filtrés = {titre: doc for titre, doc in copie_corpus.id2doc.items() if doc.date < date_limite}
        copie_corpus.id2doc = documents_filtrés

        # Ajuster les attributs de la copie
        copie_corpus.ndoc = len(documents_filtrés)
        copie_corpus.naut = len({doc.auteur for doc in documents_filtrés.values()})
        copie_corpus.texte_concatene = None  # Reset et sera recalculé si nécessaire

        return copie_corpus

    def copier_et_filtrer_apres_date(self, date_limite):
        # Créer une copie profonde du corpus
        copie_corpus = copy.deepcopy(self)

        # Filtrer les documents pour ne garder que ceux après la date limite
        documents_filtrés = {titre: doc for titre, doc in copie_corpus.id2doc.items() if doc.date >= date_limite}
        copie_corpus.id2doc = documents_filtrés

        # Ajuster les attributs de la copie
        copie_corpus.ndoc = len(documents_filtrés)
        copie_corpus.naut = len({doc.auteur for doc in documents_filtrés.values()})
        copie_corpus.texte_concatene = None  # Reset et sera recalculé si nécessaire

        return copie_corpus

