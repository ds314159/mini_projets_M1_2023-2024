import unittest
from Classes_Data import *
import Fonctions_Acquisition_Donnees
from unittest.mock import mock_open, patch, MagicMock
import pandas as pd
from datetime import datetime
import xmltodict




class TestCorpus(unittest.TestCase):
    """
    Cette classe met en place un Test Unitaire à chaque méthode de la classe Corpus

    """

    def setUp(self):
        # Chargement du corpus archétype
        self.corpus = Corpus.load('data/corpus_1.pkl')

    def test_load_corpus(self):
        # Test si le corpus est chargé
        self.assertIsNotNone(self.corpus)

    def test_corpus_attributes(self):
        # Test les attributs du corpus
        self.assertTrue(hasattr(self.corpus, 'nom'))  # Vérifie si l'attribut nom existe
        self.assertTrue( hasattr(self.corpus, 'authors'))  # Vérifie si l'attribut authors (dictionnaire des auteurs) existe
        self.assertTrue( hasattr(self.corpus, 'id2doc'))  # Vérifie si l'attribut id2doc (dictionnaire des documents) existe
        self.assertTrue(hasattr(self.corpus, 'ndoc'))  # Vérifie si l'attribut ndoc (comptage des documents) existe
        self.assertTrue(hasattr(self.corpus, 'naut'))  # Vérifie si l'attribut naut (comptage des auteurs) existe

        # Vérifier les types des attributs
        self.assertIsInstance(self.corpus.authors, dict)
        self.assertIsInstance(self.corpus.id2doc, dict)
        self.assertIsInstance(self.corpus.ndoc, int)
        self.assertIsInstance(self.corpus.naut, int)

    def test_add_document(self):
        ndoc_avant = self.corpus.ndoc
        naut_avant = self.corpus.naut


        # Ajout d'un nouveau document
        self.corpus.add_document("arxiv", "Titre", "Auteur", "2020-03-03 02:29:11", "http://example.com",
                                 "Texte du document", "Co-auteurs")

        # Test si le document est ajouté à id2doc
        self.assertIn("Titre", self.corpus.id2doc)

        # Test si le compteur de documents est incrémenté
        self.assertEqual(self.corpus.ndoc, ndoc_avant + 1)

        # Test si l'auteur est ajouté au dictionnaire des auteurs
        self.assertIn("Auteur", self.corpus.authors)

        # Test si le compteur d'auteurs est correct
        self.assertEqual(self.corpus.naut, naut_avant + 1)

    def test_corpus_repr(self):
        # Initialisation de valeurs d'attributs
        self.corpus.nom = "Test Corpus"
        self.corpus.ndoc = 10
        self.corpus.naut = 5

        # Appel de __repr__ et vérification du résultat
        repr_str = repr(self.corpus)
        expected_repr = "Corpus 'Test Corpus' contenant 10 documents et 5 auteurs."

        self.assertEqual(repr_str, expected_repr)


    @patch('builtins.print')
    def test_documents_par_date(self, mock_print):
        # Initialisation d'un objet Corpus pour le test ( avec le corpus archétype c'est bcp plus compliqué)
        self.corpus_test_tri = Corpus("Test Tri Corpus")
        # Ajout de documents de test
        self.corpus_test_tri.add_document("arxiv", "Titre1", "Auteur1", "2020-03-04 02:29:11", "http://example1.com", "Texte1",
                                 "Co-auteurs1")
        self.corpus_test_tri.add_document("arxiv", "Titre2", "Auteur2", "2020-03-03 02:29:11", "http://example2.com", "Texte2",
                                 "Co-auteurs2")

        # Appel de la méthode documents_par_date
        self.corpus_test_tri.documents_par_date(2)

        # Vérification que print a été appelé avec les bonnes informations
        expected_calls = [
            unittest.mock.call("Titre: Titre1, Date: 2020-03-04, Auteur: Auteur1"),
            unittest.mock.call("Titre: Titre2, Date: 2020-03-03, Auteur: Auteur2")
        ]
        mock_print.assert_has_calls(expected_calls, any_order=False)

    @patch('builtins.print')
    def test_documents_par_titre(self, mock_print):
        # Initialisation d'un objet Corpus pour le test
        self.corpus_test_tri = Corpus("Test Tri Corpus")
        # Ajout de documents de test
        self.corpus_test_tri.add_document("arxiv", "B Titre", "Auteur2", "2020-03-04 02:29:11", "http://example2.com",
                                          "Texte2", "Co-auteurs2")
        self.corpus_test_tri.add_document("arxiv", "A Titre", "Auteur1", "2020-03-03 02:29:11", "http://example1.com",
                                          "Texte1", "Co-auteurs1")

        # Appel de la méthode documents_par_titre
        self.corpus_test_tri.documents_par_titre(2)

        # Vérification que print a été appelé avec les bonnes informations
        expected_calls = [
            unittest.mock.call("Titre: A Titre, Date: 2020-03-03, Auteur: Auteur1"),
            unittest.mock.call("Titre: B Titre, Date: 2020-03-04, Auteur: Auteur2")
        ]
        mock_print.assert_has_calls(expected_calls, any_order=False)

    @patch('builtins.print')
    def test_documents_par_date_et_titre(self, mock_print):
        # Initialisation d'un objet Corpus pour le test
        self.corpus_test_tri = Corpus("Test Tri Corpus")
        # Ajout de documents de test avec des dates et titres différents
        self.corpus_test_tri.add_document("arxiv", "B Titre", "Auteur2", "2020-03-04 02:29:11", "http://example2.com", "Texte2",
                                          "Co-auteurs2")
        self.corpus_test_tri.add_document("arxiv", "A Titre", "Auteur1", "2020-03-03 02:29:11", "http://example1.com", "Texte1",
                                          "Co-auteurs1")
        self.corpus_test_tri.add_document("arxiv", "C Titre", "Auteur3", "2020-03-04 02:29:11", "http://example3.com", "Texte3",
                                          "Co-auteurs3")

        # Appel de la méthode documents_par_date_et_titre
        self.corpus_test_tri.documents_par_date_et_titre(3)

        # Vérification que print a été appelé avec les bonnes informations
        expected_calls = [
            unittest.mock.call("Titre: A Titre, Date: 2020-03-03, Auteur: Auteur1"),
            unittest.mock.call("Titre: B Titre, Date: 2020-03-04, Auteur: Auteur2"),
            unittest.mock.call("Titre: C Titre, Date: 2020-03-04, Auteur: Auteur3")
        ]
        mock_print.assert_has_calls(expected_calls, any_order=False)

    def test_newest_doc_date(self):
        # Test avec un corpus contenant des documents
        self.corpus_test_dates = Corpus("Test Dates Corpus")
        self.corpus_test_dates.add_document("arxiv", "Titre1", "Auteur1", "2020-03-03 02:29:11", "http://example1.com", "Texte1",
                                            "Co-auteurs1")
        self.corpus_test_dates.add_document("arxiv", "Titre2", "Auteur2", "2020-03-04 02:29:11", "http://example2.com", "Texte2",
                                            "Co-auteurs2")

        newest_date = self.corpus_test_dates.newest_doc_date()
        self.assertEqual(str(newest_date), "2020-03-04")

        # Test avec un corpus vide
        self.corpus_vide = Corpus("Test Empty Corpus")
        newest_date_empty = self.corpus_vide.newest_doc_date()
        self.assertIsNone(newest_date_empty)

    def test_oldest_doc_date(self):
        # Test avec un corpus contenant des documents
        self.corpus_test_dates = Corpus("Test Dates Corpus")
        self.corpus_test_dates.add_document("arxiv", "Titre1", "Auteur1", "2020-03-03 02:29:11", "http://example1.com", "Texte1",
                                            "Co-auteurs1")
        self.corpus_test_dates.add_document("arxiv", "Titre2", "Auteur2", "2020-03-04 02:29:11", "http://example2.com", "Texte2",
                                            "Co-auteurs2")

        oldest_date = self.corpus_test_dates.oldest_doc_date()
        self.assertEqual(str(oldest_date), "2020-03-03")

        # Test avec un corpus vide
        self.corpus_vide = Corpus("Test Empty Corpus")
        oldest_date_empty = self.corpus_vide.oldest_doc_date()
        self.assertIsNone(oldest_date_empty)

    def test_concatener_textes(self):
        # Création d'un corpus de test et ajout de documents
        self.corpus_concat = Corpus("Test Concat Corpus")
        self.corpus_concat.add_document("arxiv", "Titre1", "Auteur1", "2020-03-03 02:29:11", "http://example1.com", "Texte1",
                                        "Co-auteurs1")
        self.corpus_concat.add_document("arxiv", "Titre2", "Auteur2", "2020-03-04 02:29:11", "http://example2.com", None,
                                        "Co-auteurs2")  # Document sans texte

        # Appel de la méthode concatener_textes
        self.corpus_concat.concatener_textes()

        # Vérification de la concaténation
        expected_concatenation = "Texte1 "
        self.assertEqual(self.corpus_concat.texte_concatene, expected_concatenation)

        # Réinitialisation de texte_concatene avant de concaténer à nouveau
        self.corpus_concat.texte_concatene = None

        # Ajout d'un autre document et re-vérification
        self.corpus_concat.add_document("arxiv", "Titre3", "Auteur3", "2020-03-05 02:29:11", "http://example3.com", "Texte3",
                                        "Co-auteurs3")
        self.corpus_concat.concatener_textes()
        updated_expected_concatenation = "Texte1  Texte3" # ne pas oublier de mettre un double espace
        self.assertEqual(self.corpus_concat.texte_concatene.strip(), updated_expected_concatenation)

    def test_search(self):
        # Initialisation d'un corpus de test et ajout de documents
        self.corpus_search = Corpus("Test Search Corpus")
        self.corpus_search.add_document("arxiv", "Titre1", "Auteur1", "2020-03-03 02:29:11", "http://example1.com",
                                        "Lorem ipsum dolor sit amet", "Co-auteurs1")
        self.corpus_search.add_document("arxiv", "Titre2", "Auteur2", "2020-03-04 02:29:11", "http://example2.com",
                                        "Ipsum lorem", "Co-auteurs2")

        # Recherche d'un mot-clé présent
        results = self.corpus_search.search("Lorem")
        self.assertEqual(len(results), 1) # 1 car sensible à la casse
        self.assertTrue(all(word == "Lorem" for word in results))

        # Recherche d'un mot-clé absent
        results_absent = self.corpus_search.search("NonExistant")
        self.assertEqual(len(results_absent), 0)

    def test_concorde(self):
        # Initialisation d'un corpus de test et ajout de documents
        self.corpus_concorde = Corpus("Test Concorde Corpus")
        self.corpus_concorde.add_document("arxiv", "Titre1", "Auteur1", "2020-03-03 02:29:11", "http://example1.com",
                                          "Texte autour de Lorem ipsum autour", "Co-auteurs1")
        self.corpus_concorde.add_document("arxiv", "Titre2", "Auteur2", "2020-03-04 02:29:11", "http://example2.com",
                                          "Ipsum lorem", "Co-auteurs2")

        # Recherche d'une expression avec un contexte de taille 6
        concordances = self.corpus_concorde.concorde("Lorem", 10)
        self.assertIsInstance(concordances, pd.DataFrame)
        self.assertEqual(len(concordances), 1)
        self.assertEqual(concordances.iloc[0]['motif trouvé'], "Lorem")
        self.assertIn("autour de ", concordances.iloc[0]['contexte gauche'])
        self.assertIn(" ipsum aut", concordances.iloc[0]['contexte droit'])

        # Test avec une expression absente
        concordances_absent = self.corpus_concorde.concorde("NonExistant", 6)
        self.assertEqual(len(concordances_absent), 0)

    def test_nettoyer_texte(self):
        # Nettoyage d'un texte normal
        texte = "Test 123! Lorem ipsum, dolor sit 2 amet."
        texte_nettoye = self.corpus.nettoyer_texte(texte)
        expected_texte = "test lorem ipsum dolor sit amet"  # Exemple attendu après nettoyage
        self.assertEqual(texte_nettoye, expected_texte)

        # Test avec une entrée non-textuelle (par exemple, None)
        texte_none = self.corpus.nettoyer_texte(None)
        self.assertEqual(texte_none, "")

        # Test avec une chaîne 'nan'
        texte_nan = self.corpus.nettoyer_texte('nan')
        self.assertEqual(texte_nan, "")

        # Test supplémentaire pour la suppression des stopwords
        texte_stopwords = "This is a test of the stopwords removal"
        texte_nettoye_stopwords = self.corpus.nettoyer_texte(texte_stopwords)

        # Vérifier que les stopwords courants sont supprimés
        for stopword in ['this', 'is', 'of', 'the']:
            self.assertNotIn(stopword, texte_nettoye_stopwords)

        # Vérifier que les mots non-stopwords restent
        for word in ['test', 'stopwords', 'removal']:
            self.assertIn(word, texte_nettoye_stopwords)

    def test_construire_vocabulaire(self):
        # Initialisation d'un corpus de test et ajout de documents
        self.corpus_vocab = Corpus("Test Vocab Corpus")
        self.corpus_vocab.add_document("arxiv", "Titre1", "Auteur1", "2020-03-03 02:29:11", "http://example1.com",
                                       "Lorem ipsum dolor sit amet", "Co-auteurs1")
        self.corpus_vocab.add_document("arxiv", "Titre2", "Auteur2", "2020-03-04 02:29:11", "http://example2.com", "Ipsum lorem",
                                       "Co-auteurs2")

        # Construction du vocabulaire
        vocabulaire = self.corpus_vocab.construire_vocabulaire()

        # Vérification de la construction du vocabulaire
        self.assertIsInstance(vocabulaire, dict)
        self.assertIn("lorem", vocabulaire.values())
        self.assertIn("ipsum", vocabulaire.values())
        self.assertIn("dolor", vocabulaire.values())

        # Test avec un corpus vide
        self.corpus_vide = Corpus("Test Empty Corpus")
        vocabulaire_vide = self.corpus_vide.construire_vocabulaire()
        self.assertEqual(vocabulaire_vide, {})

    def test_nombre_mots_uniques(self):
        # Initialisation d'un corpus de test et ajout de documents
        self.corpus_unique_words = Corpus("Test Unique Words Corpus")
        self.corpus_unique_words.add_document("arxiv", "Titre1", "Auteur1", "2020-03-03 02:29:11", "http://example1.com",
                                              "Lorem ipsum dolor sit amet", "Co-auteurs1")
        self.corpus_unique_words.add_document("arxiv", "Titre2", "Auteur2", "2020-03-04 02:29:11", "http://example2.com",
                                              "Ipsum lorem", "Co-auteurs2")

        # Calcul du nombre de mots uniques
        nb_mots_uniques = self.corpus_unique_words.nombre_mots_uniques()
        self.assertEqual(nb_mots_uniques,
                         5)

        # Test avec un corpus vide
        self.corpus_vide = Corpus("Test Empty Corpus")
        nb_mots_uniques_vide = self.corpus_vide.nombre_mots_uniques()
        self.assertEqual(nb_mots_uniques_vide, 0)

    def test_calculer_frequences(self):
        # Initialisation d'un corpus de test et ajout de documents
        self.corpus_freq = Corpus("Test Frequencies Corpus")
        self.corpus_freq.add_document("arxiv", "Titre1", "Auteur1", "2020-03-03 02:29:11", "http://example1.com",
                                      "Lorem ipsum dolor sit amet", "Co-auteurs1")
        self.corpus_freq.add_document("arxiv", "Titre2", "Auteur2", "2020-03-04 02:29:11", "http://example2.com", "Ipsum lorem",
                                      "Co-auteurs2")

        # Construction du vocabulaire et calcul des fréquences
        vocabulaire_dict = self.corpus_freq.construire_vocabulaire()
        freq_df = self.corpus_freq.calculer_frequences(vocabulaire_dict)

        # Vérification de la structure du DataFrame
        self.assertIsInstance(freq_df, pd.DataFrame)
        self.assertIn("lorem", freq_df.columns)
        self.assertIn("ipsum", freq_df.columns)

        # Vérification des fréquences pour un terme spécifique
        self.assertEqual(freq_df.loc["Titre1", "lorem"], 1)
        self.assertEqual(freq_df.loc["Titre2", "lorem"], 1)

        # Test avec un corpus vide
        self.corpus_vide = Corpus("Test Empty Corpus")
        freq_df_vide = self.corpus_vide.calculer_frequences({})
        self.assertTrue(freq_df_vide.empty)

    def test_vectoriser_documents(self):
        # Initialisation d'un corpus de test et ajout de documents
        self.corpus_vectorisation = Corpus("Test Vectorisation Corpus")
        self.corpus_vectorisation.add_document("arxiv", "Titre1", "Auteur1", "2020-03-03 02:29:11", "http://example1.com",
                                               "machine machine learning", "Co-auteurs1")
        self.corpus_vectorisation.add_document("arxiv", "Titre2", "Auteur2", "2020-03-04 02:29:11", "http://example2.com",
                                               "data science", "Co-auteurs2")

        # Vectorisation des documents
        self.corpus_vectorisation.vectoriser_documents()

        # Vérification de la structure de la matrice TF-IDF
        self.assertIsNotNone(self.corpus_vectorisation.tfidf_matrix)
        self.assertEqual(self.corpus_vectorisation.tfidf_matrix.shape[0], 2)  # Nombre de documents
        self.assertTrue(self.corpus_vectorisation.tfidf_matrix.shape[1] == 4)  # Nombre de termes uniques

        # S'assurer qu'une erreur est levée si le corpus est vide
        self.corpus_vide = Corpus("Test Empty Corpus Vectorisation")
        with self.assertRaises(ValueError):
            self.corpus_vide.vectoriser_documents()

    def test_rechercher_documents(self):
        # Initialisation d'un corpus de test et ajout de documents
        self.corpus_recherche = Corpus("Test Recherche Corpus")
        self.corpus_recherche.add_document("arxiv", "Titre1", "Auteur1", "2020-03-03 02:29:11", "http://example1.com",
                                           "Lorem ipsum dolor sit amet", "Co-auteurs1")
        self.corpus_recherche.add_document("arxiv", "Titre2", "Auteur2", "2020-03-04 02:29:11", "http://example2.com",
                                           "Ipsum lorem", "Co-auteurs2")

        # Recherche avec une requête
        requete = "Lorem"
        resultats = self.corpus_recherche.rechercher_documents(requete)

        # Vérification de la structure du DataFrame
        self.assertIsInstance(resultats, pd.DataFrame)
        self.assertTrue(all(col in resultats.columns for col in ['Document', 'Score']))

        # Vérification des résultats (les scores doivent être positifs)
        self.assertTrue(all(resultats['Score'] >= 0))

        # Test avec un corpus vide
        self.corpus_vide = Corpus("Test Empty Corpus Recherche")
        with self.assertRaises(ValueError):
            self.corpus_vide.rechercher_documents("mot")




    def test_copier_et_filtrer_avant_date(self):
        # Initialisation d'un corpus de test et ajout de documents
        self.corpus_filtrage = Corpus("Test Filtrage Corpus")
        self.corpus_filtrage.add_document("arxiv", "Titre1", "Auteur1", "2020-03-03 02:29:11", "http://example1.com", "Texte1", "Co-auteurs1")
        self.corpus_filtrage.add_document("arxiv", "Titre2", "Auteur2", "2021-04-04 02:29:11", "http://example2.com", "Texte2", "Co-auteurs2")

        # Définir une date limite et créer une copie filtrée
        date_limite = datetime.strptime("2021-01-01", "%Y-%m-%d").date()
        copie_corpus = self.corpus_filtrage.copier_et_filtrer_avant_date(date_limite)

        # Vérification que seul le document avant la date limite est conservé
        self.assertEqual(len(copie_corpus.id2doc), 1)
        self.assertIn("Titre1", copie_corpus.id2doc)
        self.assertNotIn("Titre2", copie_corpus.id2doc)

        # Vérification des attributs du corpus copié
        self.assertEqual(copie_corpus.ndoc, 1)
        self.assertEqual(copie_corpus.naut, 1)

        # Vérification de l'indépendance de la copie
        self.corpus_filtrage.add_document("arxiv", "Titre3", "Auteur3", "2022-05-05 02:29:11", "http://example3.com", "Texte3", "Co-auteurs3")
        self.assertNotEqual(self.corpus_filtrage.ndoc, copie_corpus.ndoc)

    def test_copier_et_filtrer_apres_date(self):
        # Initialisation d'un corpus de test et ajout de documents
        self.corpus_filtrage_apres = Corpus("Test Filtrage Apres Corpus")
        self.corpus_filtrage_apres.add_document("arxiv", "Titre1", "Auteur1", "2020-03-03 02:29:11", "http://example1.com",
                                                "Texte1", "Co-auteurs1")
        self.corpus_filtrage_apres.add_document("arxiv", "Titre2", "Auteur2", "2021-04-04 02:29:11", "http://example2.com",
                                                "Texte2", "Co-auteurs2")

        # Définir une date limite et créer une copie filtrée
        date_limite = datetime.strptime("2021-01-01", "%Y-%m-%d").date()
        copie_corpus_apres = self.corpus_filtrage_apres.copier_et_filtrer_apres_date(date_limite)

        # Vérification que seul le document après la date limite est conservé
        self.assertEqual(len(copie_corpus_apres.id2doc), 1)
        self.assertIn("Titre2", copie_corpus_apres.id2doc)
        self.assertNotIn("Titre1", copie_corpus_apres.id2doc)

        # Vérification des attributs du corpus copié
        self.assertEqual(copie_corpus_apres.ndoc, 1)
        self.assertEqual(copie_corpus_apres.naut, 1)

        # Vérification de l'indépendance de la copie
        self.corpus_filtrage_apres.add_document("arxiv", "Titre3", "Auteur3", "2022-05-05 02:29:11", "http://example3.com",
                                                "Texte3", "Co-auteurs3")
        self.assertNotEqual(self.corpus_filtrage_apres.ndoc, copie_corpus_apres.ndoc)

"""

# Si vous décommentez  ce test, veillez à fermer la fenêtre du nuage qui s'ouvre, pour que les tests se poursuivent

    def test_vision_d_ensemble(self):
        # Initialisation d'un corpus de test et ajout de documents
        self.corpus_vision = Corpus("Test Vision Corpus")
        self.corpus_vision.add_document("arxiv", "Titre1", "Auteur1", "2020-03-03 02:29:11", "http://example1.com",
                                        "Lorem ipsum dolor sit amet", "Co-auteurs1")
        self.corpus_vision.add_document("arxiv", "Titre2", "Auteur2", "2020-03-04 02:29:11", "http://example2.com",
                                        "Ipsum lorem", "Co-auteurs2")



        # Intercepter les appels à print
        with patch('builtins.print') as mock_print:
            self.corpus_vision.vision_d_ensemble()

            # Vérification des appels à print
            expected_calls = [
                unittest.mock.call(f"Ce Corpus est composé de : {self.corpus_vision.ndoc} document(s)."),
                unittest.mock.call(f"Ces documents ont été rédigés par : {self.corpus_vision.naut} auteur(s)"),
                unittest.mock.call(f"Le document le plus ancien a été rédigé le : {self.corpus_vision.oldest_doc_date()}."),
                unittest.mock.call(f"Le document le plus récent a été rédigé le : {self.corpus_vision.newest_doc_date()}."),
                unittest.mock.call(f"Le Corpus totalise  {self.corpus_vision.nombre_mots_uniques()} mots uniques."),
                unittest.mock.call( "Voici un nuage représentant Les mots par leur fréquence d'apparition dans le corpus")
            ]
            mock_print.assert_has_calls(expected_calls, any_order=False)

"""

class TestDocument(unittest.TestCase):

    def setUp(self):
        self.document = Document("Titre Test", "Auteur Test", "2021-01-01 12:00:00", "http://example.com",
                                 "Texte de test")

    def test_constructeur_document(self):

        # Assertions pour vérifier l'initialisation correcte
        self.assertEqual(self.document.titre, 'Titre Test')
        self.assertEqual(self.document.auteur, 'Auteur Test')
        self.assertEqual(self.document.date, datetime.strptime("2021-01-01 12:00:00", "%Y-%m-%d %H:%M:%S").date())
        self.assertEqual(self.document.url, "http://example.com")
        self.assertEqual(self.document.texte, "Texte de test")
        self.assertEqual(self.document.annotations, {})


    @patch('builtins.print')
    def test_afficher_infos_Document(self, mock_print):

        # Appel de la méthode afficher_infos
        self.document.afficher_infos()

        # Vérification que print a été appelé avec le texte attendu
        expected_output = "Titre: Titre Test\nAuteur: Auteur Test\nDate: 2021-01-01\nURL: http://example.com\nTexte: Texte de test"
        mock_print.assert_called_with(expected_output)

    def test_ajouter_annotation(self):
        # Données de test pour l'annotation
        id_annotation_test = "annotation1"
        texte_annotation_test = "Ceci est une annotation de test"
        position_test = (10, 20)
        auteur_test = "Annotateur Test"
        date_test = datetime.now()

        # Ajout de l'annotation
        self.document.ajouter_annotation(id_annotation_test, texte_annotation_test, position_test, auteur_test,
                                         date_test)

        # Vérifications
        self.assertIn(id_annotation_test, self.document.annotations)  # Vérifier que l'annotation est ajoutée
        annotation = self.document.annotations[id_annotation_test]
        self.assertEqual(annotation['texte'], texte_annotation_test)
        self.assertEqual(annotation['position'], position_test)
        self.assertEqual(annotation['auteur'], auteur_test)
        self.assertEqual(annotation['date'], date_test)

    @patch('builtins.print')
    def test_afficher_annotations(self, mock_print):
        # Ajout d'annotations de test
        self.document.ajouter_annotation("annotation1", "Annotation Test 1", None, "Annotateur1", datetime.now())
        self.document.ajouter_annotation("annotation2", "Annotation Test 2", None, "Annotateur2", datetime.now())

        # Appel de la méthode afficher_annotations
        self.document.afficher_annotations()

        # Vérifier que print a été appelé correctement
        self.assertEqual(mock_print.call_count, 2)
        calls = mock_print.call_args_list
        self.assertIn("Annotation Test 1", calls[0][0][0])
        self.assertIn("Annotation Test 2", calls[1][0][0])


class TestRedditDocument(unittest.TestCase):
    """
    Classe de test pour RedditDocument
    titres des tests explicites

    """

    def setUp(self):
        self.reddit_document = RedditDocument("reddit", "Titre Test", "Auteur Test", "2021-01-01 12:00:00", "http://example.com", "Texte de test", 15)

    def test_constructeur(self):
        self.assertEqual(self.reddit_document.titre, "Titre Test")
        self.assertEqual(self.reddit_document.nb_commentaires, 15)
        self.assertEqual(self.reddit_document.type, "reddit")

    def test_get_et_set_nb_commentaires(self):
        self.reddit_document.set_nb_commentaires(20)
        self.assertEqual(self.reddit_document.get_nb_commentaires(), 20)

    def test_get_type(self):
        self.assertEqual(self.reddit_document.get_type(), "reddit")

    @patch('builtins.print')
    def test_afficher_infos(self, mock_print):
        self.reddit_document.afficher_infos()
        mock_print.assert_called_with("Nombre de commentaires: 15")


class TestArxivDocument(unittest.TestCase):
    """
        Classe de test pour ArxivDocument
        titres des tests explicites

        """

    def setUp(self):
        self.arxiv_document = ArxivDocument("arxiv", "Titre Test", "Auteur Test", "2021-01-01 12:00:00", "http://example.com", "Texte de test", "Co-auteur1, Co-auteur2")

    def test_constructeur(self):
        self.assertEqual(self.arxiv_document.titre, "Titre Test")
        self.assertEqual(self.arxiv_document.co_auteurs, "Co-auteur1, Co-auteur2")
        self.assertEqual(self.arxiv_document.type, "arxiv")

    def test_get_et_set_co_auteurs(self):
        self.arxiv_document.set_co_auteurs("Co-auteur3")
        self.assertEqual(self.arxiv_document.get_co_auteurs(), "Co-auteur3")

    def test_get_type(self):
        self.assertEqual(self.arxiv_document.get_type(), "arxiv")

    @patch('builtins.print')
    def test_afficher_infos(self, mock_print):
        self.arxiv_document.afficher_infos()
        expected_calls = [
            unittest.mock.call("Source: arxiv"),
            unittest.mock.call(f"Titre: {self.arxiv_document.titre}\nAuteur: {self.arxiv_document.auteur}\nDate: {self.arxiv_document.date}\nURL: {self.arxiv_document.url}\nTexte: {self.arxiv_document.texte}"),
            unittest.mock.call("Co-auteurs: Co-auteur1, Co-auteur2")
        ]
        mock_print.assert_has_calls(expected_calls, any_order=False)


class TestFonctionsAcquisitionDonnees(unittest.TestCase):
    """
    Classe pour les tests unitaires des fonctions d'acquisition des données

    """

    @patch('Fonctions_Acquisition_Donnees.praw.Reddit')
    def test_initialiser_reddit(self, mock_reddit):
        # Configuration de test fictive
        config_fictive = {
            'REDDIT': {
                'client_id': 'test_client_id',
                'client_secret': 'test_client_secret',
                'user_agent': 'test_user_agent'
            }
        }

        # Appel de la fonction initialiser_reddit
        resultat = Fonctions_Acquisition_Donnees.initialiser_reddit(config_fictive)

        # Vérifier que praw.Reddit a été appelé avec les bons arguments
        mock_reddit.assert_called_with(client_id='test_client_id',
                                       client_secret='test_client_secret',
                                       user_agent='test_user_agent')

        # Vérifier que le résultat est bien un mock
        self.assertTrue(mock_reddit.called)


    def test_creer_dataframe_reddit(self):
        # Création de données de posts Reddit simulées
        posts_simules = [
            MagicMock(
                id="123",
                title="Post 1",
                author=MagicMock(name="Auteur1"),
                created_utc=datetime(2021, 1, 1).timestamp(),
                selftext="Contenu du post 1",
                url="http://exemple1.com",
                subreddit=MagicMock(display_name="Subreddit1"),
                ups=100,
                score=150,
                num_comments=10,
                link_flair_text="Flair1"
            )
        ]

        # Appel de la fonction creer_dataframe_reddit
        dataframe_resultat = Fonctions_Acquisition_Donnees.creer_dataframe_reddit(posts_simules)

        # Vérifications
        self.assertIsInstance(dataframe_resultat, pd.DataFrame)
        self.assertEqual(len(dataframe_resultat), len(posts_simules))
        self.assertTrue(all(col in dataframe_resultat.columns for col in
                            ['id_post_reddit', 'titre', 'auteur', 'date', 'texte', 'url', 'subreddit', 'upvotes',
                             'score', 'nombre_commentaires', 'flairs', 'source']))

    @patch('Fonctions_Acquisition_Donnees.libreq.urlopen')
    def test_recuperer_articles_arxiv(self, mock_urlopen):
        # Données simulées pour une réponse de test
        reponse_xml_simulee = '<xml>Contenu simule</xml>'
        mock_urlopen.return_value.__enter__.return_value.read.return_value = reponse_xml_simulee.encode()

        # Appel de la fonction recuperer_articles_arxiv
        sequence_de_recherche = "test"
        taille = 5
        resultat = Fonctions_Acquisition_Donnees.recuperer_articles_arxiv(sequence_de_recherche, taille)

        # Vérification que libreq.urlopen a été appelé correctement
        mock_urlopen.assert_called()

        # Vérification des résultats
        self.assertEqual(resultat, xmltodict.parse(reponse_xml_simulee))

    def test_creer_dataframe_arxiv(self):
        # Création de données arXiv simulées
        parsed_xml_simule = {
            'feed': {
                'entry': [
                    {
                        'title': 'Titre1',
                        'author': [{'name': 'Auteur1'}, {'name': 'CoAuteur1'}],
                        'published': '2021-01-01T10:00:00Z',
                        'summary': 'Résumé1',
                        'link': [{'@href': 'http://exemple1.com'}]
                    },
                    # Ajoutez ici plus d'entrées si nécessaire
                ]
            }
        }

        # Appel de la fonction creer_dataframe_arxiv
        dataframe_resultat = Fonctions_Acquisition_Donnees.creer_dataframe_arxiv(parsed_xml_simule)

        # Vérifications
        self.assertIsInstance(dataframe_resultat, pd.DataFrame)
        self.assertEqual(len(dataframe_resultat), len(parsed_xml_simule['feed']['entry']))
        self.assertTrue(all(col in dataframe_resultat.columns for col in
                            ['titre', 'auteur', 'co_auteurs', 'date', 'texte', 'url', 'catégorie', 'source']))





    @patch('Fonctions_Acquisition_Donnees.charger_config_json')
    @patch('Fonctions_Acquisition_Donnees.initialiser_reddit')
    @patch('Fonctions_Acquisition_Donnees.recuperer_posts_reddit')
    @patch('Fonctions_Acquisition_Donnees.creer_dataframe_reddit')
    @patch('Fonctions_Acquisition_Donnees.recuperer_articles_arxiv')
    @patch('Fonctions_Acquisition_Donnees.creer_dataframe_arxiv')
    @patch('pandas.DataFrame.to_csv')
    @patch('Classes_Data.DocumentFactory.create_corpus')
    def test_appliquer_recherche(self, mock_create_corpus, mock_to_csv, mock_creer_dataframe_arxiv,
                                 mock_recuperer_articles_arxiv, mock_creer_dataframe_reddit,
                                 mock_recuperer_posts_reddit, mock_initialiser_reddit, mock_charger_config_json):
        # Création d'une instance factice de Corpus
        fake_corpus = Corpus("TestCorpus")
        mock_create_corpus.return_value = fake_corpus

        # Configuration des mocks pour retourner des DataFrames avec une colonne 'texte'
        mock_creer_dataframe_reddit.return_value = pd.DataFrame({'texte': ['Texte Reddit']})
        mock_creer_dataframe_arxiv.return_value = pd.DataFrame({'texte': ['Texte Arxiv']})

        # Configuration des autres mocks
        mock_charger_config_json.return_value = {}
        mock_initialiser_reddit.return_value = MagicMock()
        mock_recuperer_posts_reddit.return_value = [MagicMock()]
        mock_recuperer_articles_arxiv.return_value = {'feed': {'entry': [{}]}}
        mock_to_csv.return_value = None

        # Appel de la fonction appliquer_recherche
        resultat = Fonctions_Acquisition_Donnees.appliquer_recherche("TestCorpus", "test", 10)

        # Vérifications
        mock_charger_config_json.assert_called_once()
        mock_initialiser_reddit.assert_called_once()
        mock_recuperer_posts_reddit.assert_called_once()
        mock_creer_dataframe_reddit.assert_called_once()
        mock_recuperer_articles_arxiv.assert_called_once()
        mock_creer_dataframe_arxiv.assert_called_once()
        mock_to_csv.assert_called_once()
        mock_create_corpus.assert_called_once()
        self.assertIsInstance(resultat, Corpus)




if __name__ == '__main__':
    unittest.main()