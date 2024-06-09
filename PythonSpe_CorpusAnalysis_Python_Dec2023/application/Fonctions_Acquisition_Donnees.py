import praw
import json
import xmltodict
import urllib.request as libreq
from urllib.parse import quote_plus
from datetime import datetime as dt
import os
import pandas as pd
from Classes_Data import *




def charger_config_json(chemin):
    """
    Charge une configuration depuis un fichier JSON.

    :param chemin: Le chemin vers le fichier JSON.
    :return: Un dictionnaire contenant la configuration chargée.
    """
    with open(chemin, 'r') as file:
        return json.load(file)


def initialiser_reddit(config):
    """
    Initialise une instance de l'API Reddit.

    :param config: Dictionnaire contenant les clés de configuration pour Reddit.
    :return: Une instance de l'API Reddit.
    """
    return praw.Reddit(client_id=config['REDDIT']['client_id'],
                       client_secret=config['REDDIT']['client_secret'],
                       user_agent=config['REDDIT']['user_agent'])


def recuperer_posts_reddit(reddit, mot_de_recherche, taille):
    """
    Récupère des posts de Reddit basés sur un mot-clé de recherche.

    :param reddit: L'instance de l'API Reddit.
    :param mot_de_recherche: Le mot-clé pour la recherche.
    :param taille: Le nombre maximum de posts à récupérer.
    :return: Une liste de posts Reddit.
    """
    return reddit.subreddit('all').search(query=mot_de_recherche, limit=taille)


def creer_dataframe_reddit(posts):
    """
    Crée un DataFrame à partir des posts Reddit.

    :param posts: Une liste de posts Reddit.
    :return: Un DataFrame contenant les données des posts.

    """
    data_reddit = [{
        'id_post_reddit': post.id,
        'titre': post.title,
        'auteur': post.author.name if post.author else 'N/A',
        'date': dt.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
        'texte': post.selftext,
        'url': post.url,
        'subreddit': post.subreddit.display_name,
        'upvotes': post.ups,
        'score': post.score,
        'nombre_commentaires': post.num_comments,
        'flairs': post.link_flair_text,
        'source': "reddit"
    } for post in posts]
    return pd.DataFrame(data_reddit)


def recuperer_articles_arxiv(sequence_de_recherche, taille):
    """
    Récupère des articles depuis arXiv.

    :param sequence_de_recherche: Le mot-clé pour la recherche.
    :param taille: Le nombre maximum d'articles à récupérer.
    :return: Un objet xmltodict contenant les articles récupérés.
    """
    contenu = quote_plus(sequence_de_recherche) # contrairement à praw, dans xreddit il faut formater la sequence afin qu'il n'y ait pas d'espaces
    cible = 'all'
    cible_exclusion = 'ti'
    contenu_exclusion = 'monkey' # exemple insignifiant, juste pour tester la variable exclusion
    requete_arxiv = f"http://export.arxiv.org/api/query?search_query={cible}:{contenu}+ANDNOT+%28{cible_exclusion}:{contenu_exclusion}%29&start=0&max_results={taille}"
    with libreq.urlopen(requete_arxiv) as url:
        return xmltodict.parse(url.read())


def creer_dataframe_arxiv(parsed_xml):
    """
    Crée un DataFrame à partir des données arXiv.

    :param parsed_xml: Les données arXiv sous forme de dictionnaire XML.
    :return: Un DataFrame contenant les données des articles arXiv.
    """
    entries = parsed_xml['feed'].get('entry', [])
    if not isinstance(entries, list):  # Si un seul article, il ne sera pas sous forme de liste
        entries = [entries]

    data_arxiv = [{
        'titre': entry['title'],
        'auteur': entry['author']['name'] if isinstance(entry['author'], dict) else entry['author'][0]['name'],
        'co_auteurs': ', '.join([author['name'] for author in entry['author'][1:]]) if isinstance(entry['author'],
                                                                                                  list) and len(
            entry['author']) > 1 else None,
        'date': dt.strptime(entry['published'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S'),
        'texte': entry['summary'],
        'url': entry['link'][0]['@href'] if isinstance(entry['link'], list) else entry['link']['@href'],
        'catégorie': 'cs',
        'source': 'arxiv'
    } for entry in entries]
    return pd.DataFrame(data_arxiv)


def appliquer_recherche(nom_corpus, mot_de_recherche, taille_par_source):
    """
    Applique une recherche et crée un corpus à partir des résultats.

    :param nom_corpus: Le nom à donner au corpus.
    :param mot_de_recherche: Le mot-clé pour la recherche.
    :param taille_par_source: Le nombre d'articles à récupérer par source.
    :return: Un objet Corpus contenant les articles récupérés.
    """
    config = charger_config_json('config.json')
    reddit = initialiser_reddit(config)

    posts_reddit = recuperer_posts_reddit(reddit, mot_de_recherche, taille_par_source)
    df_reddit = creer_dataframe_reddit(posts_reddit)

    parsed_xml = recuperer_articles_arxiv(mot_de_recherche, taille_par_source)
    df_arxiv = creer_dataframe_arxiv(parsed_xml)

    df_unified = pd.concat([df_arxiv, df_reddit], ignore_index=True, sort=False)
    if 'nombre_commentaires' not in df_unified.columns:
        df_unified['nombre_commentaires'] = 0
    else:
        df_unified['nombre_commentaires'] = df_unified['nombre_commentaires'].fillna(0)
    if 'co_auteurs' not in df_unified.columns:
        df_unified['co_auteurs'] = 'Aucun'
    else:
        df_unified['co_auteurs'] = df_unified['co_auteurs'].fillna('Aucun').replace('', 'Aucun')
    df_unified['texte'] = df_unified['texte'].str.replace('\n', ' ').str.strip()

    fichier_corpus = f"data/{nom_corpus}.csv"
    df_unified.to_csv(fichier_corpus, index=False, encoding='utf-8', sep='\t')

    corpus_articles = DocumentFactory.create_corpus(fichier_corpus, nom_corpus)
    corpus_articles.save(f"data/{nom_corpus}.pkl")

    return corpus_articles


# Exemple d'appel de la fonction
if __name__ == "__main__":
    nom_corpus = "python"
    mot_de_recherche = "python"
    taille_par_source = 100
    corpus_articles = appliquer_recherche(nom_corpus, mot_de_recherche, taille_par_source)


    ex = Corpus.load('data/python.pkl')


