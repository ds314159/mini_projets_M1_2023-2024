import ipywidgets as widgets
from IPython.display import display, clear_output
from Fonctions_Acquisition_Donnees import *
import os
from collections import Counter
import itertools
import seaborn as sns

class Interface:
    def __init__(self):
        # Lors du choix d'un corpus de travail, ce choix est affecté à l'attribut corpus_courant de la classe interface
        self.corpus_courant = None
        # Nom dans le repertoire données du corpus courant
        self.nom_corpus_courant = None
        # Sous corpus si choix de selection par date
        self.sous_corpus_courant_predate = None
        # Sous corpus si choix de selection par date
        self.sous_corpus_courant_postdate = None
        # Lors d'une recherche par séquence, le résultat de la recherche est affecté à l'attribut recherche_courante
        self.recherche_courante = None
        # sortie moteur recherche
        self.output_mr = widgets.Output()

        self.concordances = None
        self.current_page_concordancier = 1
        self.output_concordances = widgets.Output()
        self.bouton_page_suivante_concordances = widgets.Button(description='Page Suivante', button_style='success')
        self.bouton_page_precedente_concordances = widgets.Button(description='Page Précédente', button_style='warning')

        self.output_analyse = widgets.Output()

    def charger_corpus(self, fichier):
        """
        Charge un corpus depuis un fichier.
        :param fichier: Chemin du fichier contenant le corpus.
        :return: Un objet Corpus chargé.
        """
        return Corpus.load(fichier)

    @property
    def corpus_courant(self):
        """
        Accesseur (getter) pour l'attribut corpus_courant.
        :return: L'objet Corpus actuellement chargé.
        """
        return self._corpus_courant

    @corpus_courant.setter
    def corpus_courant(self, value):
        """
        Modificateur (setter) pour l'attribut corpus_courant.
        :param value: Le nouveau corpus à définir comme corpus courant.
        """
        self._corpus_courant = value

    def lister_noms_corpus(self, directory="data"):
        """
        Liste les noms des corpus disponibles dans un répertoire.
        :param directory: Chemin du répertoire contenant les corpus, par défaut 'data'.
        :return: Une liste de noms de corpus.
        """
        return [f for f in os.listdir(directory) if f.endswith('.pkl')]





    def rechercher_documents_creer_corpus(self):
        """
        Crée une interface utilisateur pour construire un corpus à partir d'une séquence de recherche.
        """
        style = {'description_width': 'initial'}
        layout = widgets.Layout(width='500px')

        def on_bouton_executer_clicked(b):
            with output:
                clear_output(wait=True)
                try:
                    if mot_cle_widget.value.strip() == '' or nom_corpus_widget.value.strip() == '':
                        print("Veuillez entrer un mot-clé de recherche et attribuer un nom au résultat de la recherche.")
                        return
                    print(f"Recherche avec le mot-clé: '{mot_cle_widget.value}' pour {nombre_articles_widget.value} articles par api, veuillez patienter svp ...")
                    resultat = appliquer_recherche(nom_corpus_widget.value, mot_cle_widget.value, nombre_articles_widget.value)
                    display(resultat)
                except Exception as e:
                    print(f"Une erreur s'est produite: {e}")

        nom_corpus_widget = widgets.Text(description='Nom de la recherche:', style=style, layout=layout)
        mot_cle_widget = widgets.Text(description='Séquence de recherche:', style=style, layout=layout)
        nombre_articles_widget = widgets.IntSlider(description='Volume extraction:', min=0, max=200, value=100, step=10, style=style, layout=layout)
        bouton_executer = widgets.Button(description='Exécuter', button_style='info', tooltip='Cliquer ici pour lancer la recherche', icon='search')
        output = widgets.Output()

        bouton_executer.on_click(on_bouton_executer_clicked)

        return widgets.VBox([nom_corpus_widget, mot_cle_widget, nombre_articles_widget, bouton_executer, output])




    def choisir_charger_corpus_de_travail(self):
        """
        Crée une interface utilisateur pour charger un corpus existant.
        """
        def on_bouton_charger_clicked(b):
            with output:
                clear_output(wait=True)
                try:
                    nom_corpus = liste_corpus_widget.value
                    self.nom_corpus_courant = nom_corpus[:-4]
                    chemin_complet = os.path.join("data", nom_corpus)
                    self.corpus_courant = self.charger_corpus(chemin_complet)
                    print(f"Corpus '{nom_corpus}' chargé avec succès.")
                except Exception as e:
                    print(f"Une erreur s'est produite lors du chargement: {e}")

        liste_corpus_widget = widgets.Select(options=self.lister_noms_corpus(), description='Choisir :', disabled=False)
        bouton_charger = widgets.Button(description='Charger le Corpus', disabled=False)
        output = widgets.Output()

        bouton_charger.on_click(on_bouton_charger_clicked)

        return widgets.VBox([liste_corpus_widget, bouton_charger, output])

    def vision_d_ensemble_du_Corpus(self):
        """
        Crée une interface utilisateur pour configurer et afficher une vision d'ensemble du corpus.
        """
        style = {'description_width': 'initial'}
        layout = widgets.Layout(width='400px')

        max_words_widget = widgets.IntSlider(value=200, min=10, max=500, step=10, description='Nombre de mots à intègrer:', style=style,
                                             layout=layout)
        min_word_length_widget = widgets.IntSlider(value=0, min=0, max=10, step=1, description="Taille min d'un mot:",
                                                   style=style, layout=layout)
        background_color_widget = widgets.ColorPicker(value='pink', description='Couleur de fond de votre nuage', style=style,
                                                      layout=layout)
        bouton_vision_ensemble = widgets.Button(description='Afficher :', button_style='info',
                                                tooltip='Cliquer pour visualiser', icon='eye')
        output = widgets.Output()

        def on_bouton_vision_ensemble_clicked(b):
            with output:
                clear_output(wait=True)
                try:
                    if self.corpus_courant:
                        self.corpus_courant.vision_d_ensemble(max_words=max_words_widget.value,
                                                              min_word_length=min_word_length_widget.value,
                                                              background_color=background_color_widget.value)
                    else:
                        print("Aucun corpus n'est chargé actuellement.")
                except Exception as e:
                    print(f"Une erreur s'est produite: {e}")

        bouton_vision_ensemble.on_click(on_bouton_vision_ensemble_clicked)

        return widgets.VBox(
            [max_words_widget, min_word_length_widget, background_color_widget, bouton_vision_ensemble, output])


    def afficher_resultats_recherche(self):
        """Affiche les résultats de la recherche courante."""
        with self.output_mr:
            clear_output(wait=True)
            if self.recherche_courante is not None:
                # Affichage du texte de présentation
                nombre_resultats = len(self.recherche_courante)
                texte_explicatif = f"Les résultats ayant les meilleurs scores par ordre décroissant de pertinence :"
                print(texte_explicatif)
                for index, row in self.recherche_courante.iterrows():
                    label = widgets.Label(value=f"\nArticle d'index {index} et intitulé:")
                    bouton_doc = widgets.Button(description=row['Document'], layout=widgets.Layout(width='auto'))
                    bouton_doc.on_click(lambda b, idx=index: self.afficher_texte_document(idx))
                    display(label, bouton_doc)
            else:
                print("Aucun résultat de recherche à afficher.")

    def afficher_texte_document(self, index):
        """Affiche le texte du document à l'index spécifié et un bouton de retour."""
        with self.output_mr:
            clear_output(wait=True)
            try:
                doc = list(self.corpus_courant.id2doc.values())[index]
                print(f"Texte du document: {doc.texte}")
                bouton_retour = widgets.Button(description='Retour aux résultats', layout=widgets.Layout(width='auto'))
                bouton_retour.on_click(lambda b: self.afficher_resultats_recherche())
                display(bouton_retour)
            except Exception as e:
                print(f"Erreur lors de l'affichage du document: {e}")

    def moteur_de_recherche(self):
        """Crée une interface utilisateur pour effectuer une recherche dans le corpus courant."""
        style = {'description_width': 'initial'}
        layout = widgets.Layout(width='500px')

        sequence_recherche_widget = widgets.Text(description='Séquence de recherche:', style=style, layout=layout)
        nombre_resultats_widget = widgets.IntSlider(value=5, min=1, max=20, step=1, description='Nombre de résultats:',
                                                    style=style, layout=layout)
        bouton_rechercher = widgets.Button(description='Rechercher', button_style='info',
                                           tooltip='Cliquer pour rechercher', icon='search')

        def on_bouton_rechercher_clicked(b):
            with self.output_mr:
                clear_output(wait=True)
                try:
                    if self.corpus_courant:
                        resultats = self.corpus_courant.rechercher_documents(sequence_recherche_widget.value)
                        self.recherche_courante = resultats.head(nombre_resultats_widget.value)
                        self.afficher_resultats_recherche()
                    else:
                        print("Aucun corpus n'est chargé actuellement.")
                except Exception as e:
                    print(f"Une erreur s'est produite: {e}")

        bouton_rechercher.on_click(on_bouton_rechercher_clicked)

        return widgets.VBox([sequence_recherche_widget, nombre_resultats_widget, bouton_rechercher, self.output_mr])



    def afficher_page_concordances(self, concordances, page_num, results_per_page):
        with self.output_concordances:
            clear_output(wait=True)
            start = (page_num - 1) * results_per_page
            end = start + results_per_page
            page_concordances = concordances.iloc[start:end]
            display(page_concordances)

            # Gérer l'affichage des boutons de pagination
            self.bouton_page_precedente_concordances.disabled = page_num <= 1
            self.bouton_page_suivante_concordances.disabled = end >= len(concordances)

            if page_num > 1:
                display(self.bouton_page_precedente_concordances)

            if end < len(concordances):
                display(self.bouton_page_suivante_concordances)

    def concordancier(self):
        style = {'description_width': 'initial'}
        layout = widgets.Layout(width='500px')

        expression_widget = widgets.Text(description='Expression:', style=style, layout=layout)
        contexte_widget = widgets.IntSlider(value=30, min=20, max=100, step=1, description='Taille du contexte:', style=style, layout=layout)
        results_per_page_widget = widgets.IntSlider(value=10, min=1, max=100, step=1, description='Résultats par page:', style=style, layout=layout)
        bouton_concorde = widgets.Button(description='Concorde', button_style='info', icon='search')

        def update_page(concordances, change):
            new_page = self.current_page_concordancier + change
            max_page = (len(concordances) - 1) // results_per_page_widget.value + 1
            if 1 <= new_page <= max_page:
                self.current_page_concordancier = new_page
                self.afficher_page_concordances(concordances, self.current_page_concordancier, results_per_page_widget.value)

        self.bouton_page_suivante_concordances.on_click(lambda b: update_page(self.concordances, 1))
        self.bouton_page_precedente_concordances.on_click(lambda b: update_page(self.concordances, -1))

        def on_bouton_concorde_clicked(b):
            with self.output_concordances:
                clear_output(wait=True)
                if self.corpus_courant:
                    self.concordances = self.corpus_courant.concorde(expression_widget.value, contexte_widget.value)
                    self.current_page_concordancier = 1
                    self.afficher_page_concordances(self.concordances, self.current_page_concordancier, results_per_page_widget.value)
                else:
                    print("Aucun corpus n'est chargé actuellement.")

        bouton_concorde.on_click(on_bouton_concorde_clicked)

        return widgets.VBox([expression_widget, contexte_widget, results_per_page_widget, bouton_concorde, self.output_concordances])

    def diviser_et_presenter_selon_date(self):
        style = {'description_width': 'initial'}
        layout = widgets.Layout(width='500px')

        date_widget = widgets.DatePicker(description='Choisir une date:', style=style, layout=layout)
        bouton_diviser = widgets.Button(description='Diviser Corpus', button_style='info', icon='cut')
        output_division = widgets.Output()

        def on_bouton_diviser_clicked(b):
            with output_division:
                clear_output(wait=True)
                if self.corpus_courant:
                    date_limite = date_widget.value
                    self.sous_corpus_courant_predate = self.corpus_courant.copier_et_filtrer_avant_date(date_limite)
                    self.sous_corpus_courant_postdate = self.corpus_courant.copier_et_filtrer_apres_date(date_limite)

                    # Afficher les deux sous-corpus
                    print("\033[1m" + "Sous-corpus avant la date limite: \n" + "\033[0m")

                    self.sous_corpus_courant_predate.vision_d_ensemble(background_color = 'blue')

                    print("\033[1m" + "Sous-corpus après la date limite: \n" + "\033[0m")
                    self.sous_corpus_courant_postdate.vision_d_ensemble(background_color = 'green')
                else:
                    print("Aucun corpus n'est chargé actuellement.")

        bouton_diviser.on_click(on_bouton_diviser_clicked)

        return widgets.VBox([date_widget, bouton_diviser, output_division])



    def comparer_occurences_mots_frequents(self):
        style = {'description_width': 'initial'}
        layout = widgets.Layout(width='400px')

        nombre_mots_widget = widgets.IntSlider(value=10, min=5, max=50, step=1,
                                               description='Nombre de mots à comparer:', style=style, layout=layout)
        bouton_comparer = widgets.Button(description='Comparer', button_style='info', icon='bar-chart')
        output_comparaison = widgets.Output()

        def comparer_frequences_mots(corpus1, corpus2):
            vocabulaire1 = corpus1.construire_vocabulaire()
            vocabulaire2 = corpus2.construire_vocabulaire()

            frequences1 = corpus1.calculer_frequences(vocabulaire1)
            frequences2 = corpus2.calculer_frequences(vocabulaire2)

            # Comparer les fréquences des mots les plus courants dans chaque corpus
            mots_les_plus_frequents1 = frequences1.sum().sort_values(ascending=False).head(20)
            mots_les_plus_frequents2 = frequences2.sum().sort_values(ascending=False).head(20)

            # Retourne les mots les plus fréquents avec leurs fréquences pour chaque corpus
            return mots_les_plus_frequents1, mots_les_plus_frequents2

        def on_bouton_comparer_clicked(b):
            with output_comparaison:
                clear_output(wait=True)
                if self.sous_corpus_courant_predate and self.sous_corpus_courant_postdate:
                    nb_mots = nombre_mots_widget.value
                    frequences1, frequences2 = comparer_frequences_mots(self.sous_corpus_courant_predate,
                                                                        self.sous_corpus_courant_postdate)

                    # Préparation des données pour le graphique
                    mots = list(set(frequences1.index[:nb_mots]) | set(frequences2.index[:nb_mots]))
                    valeurs1 = [frequences1.get(mot, 0) for mot in mots]
                    valeurs2 = [frequences2.get(mot, 0) for mot in mots]

                    # Création du graphique
                    x = range(len(mots))
                    plt.bar(x, valeurs1, width=0.4, label='Corpus Pré-Date', align='center')
                    plt.bar(x, valeurs2, width=0.4, label='Corpus Post-Date', align='edge')
                    plt.xlabel('Mots')
                    plt.ylabel('Fréquence')
                    plt.title('Comparaison des Fréquences des Mots')
                    plt.xticks(x, mots, rotation='vertical')
                    plt.legend()
                    plt.show()
                else:
                    print("Les sous-corpus ne sont pas définis.")

        bouton_comparer.on_click(on_bouton_comparer_clicked)

        return widgets.VBox([nombre_mots_widget, bouton_comparer, output_comparaison])

    def comparer_occurences_liste_de_mots(self):
        style = {'description_width': 'initial'}
        layout = widgets.Layout(width='400px')

        mots_a_comparer_widget = widgets.Text(description='Mots à comparer (séparés par des virgules):', style=style,
                                              layout=layout)
        bouton_comparer = widgets.Button(description='Comparer', button_style='info', icon='bar-chart')
        output_comparaison = widgets.Output()

        def comparer_frequences_mots_specifiques(corpus1, corpus2, mots):
            vocabulaire1 = corpus1.construire_vocabulaire()
            vocabulaire2 = corpus2.construire_vocabulaire()

            frequences1 = corpus1.calculer_frequences(vocabulaire1)
            frequences2 = corpus2.calculer_frequences(vocabulaire2)

            frequences_mots1 = {mot: frequences1.sum().get(mot, 0) for mot in mots}
            frequences_mots2 = {mot: frequences2.sum().get(mot, 0) for mot in mots}

            return frequences_mots1, frequences_mots2

        def on_bouton_comparer_clicked(b):
            with output_comparaison:
                clear_output(wait=True)
                mots = [mot.strip() for mot in mots_a_comparer_widget.value.split(',') if mot.strip()]

                if len(mots) == 0 or len(mots) > 8:
                    print("Veuillez entrer entre 1 et 8 mots.")
                    return

                if self.sous_corpus_courant_predate and self.sous_corpus_courant_postdate:
                    frequences1, frequences2 = comparer_frequences_mots_specifiques(self.sous_corpus_courant_predate,
                                                                                    self.sous_corpus_courant_postdate,
                                                                                    mots)

                    mots = list(set(frequences1.keys()) | set(frequences2.keys()))
                    valeurs1 = [float(frequences1.get(mot, 0)) for mot in mots]
                    valeurs2 = [float(frequences2.get(mot, 0)) for mot in mots]

                    x = range(len(mots))
                    plt.bar(x, valeurs1, width=0.4, label='Corpus Pré-Date', align='center')
                    plt.bar(x, valeurs2, width=0.4, label='Corpus Post-Date', align='edge')
                    plt.xlabel('Mots')
                    plt.ylabel('Fréquence')
                    plt.title('Comparaison des Fréquences des Mots Spécifiques')
                    plt.xticks(x, mots, rotation='vertical')
                    plt.legend()
                    plt.show()
                else:
                    print("Les sous-corpus ne sont pas définis.")

        bouton_comparer.on_click(on_bouton_comparer_clicked)

        return widgets.VBox([mots_a_comparer_widget, bouton_comparer, output_comparaison])





    def calculer_et_afficher_cooccurrences(self):
        # Créer un widget pour la saisie des mots
        mots_input = widgets.Text(description="Mots :")
        bouton_calculer = widgets.Button(description="Calculer")
        output = widgets.Output()

        def on_calculer_clicked(b):
            with output:
                clear_output(wait=True)
                mots = [mot.strip() for mot in mots_input.value.split(',')]
                heatmap_data_predate = self.calculer_cooccurrences(self.sous_corpus_courant_predate, mots)
                heatmap_data_postdate = self.calculer_cooccurrences(self.sous_corpus_courant_postdate, mots)

                # Afficher les heatmaps
                fig, axes = plt.subplots(1, 2, figsize=(15, 7))
                sns.heatmap(heatmap_data_predate, annot=True, fmt="d", ax=axes[0])
                axes[0].set_title("Co-Occurrences Pré-Date")
                sns.heatmap(heatmap_data_postdate, annot=True, fmt="d", ax=axes[1])
                axes[1].set_title("Co-Occurrences Post-Date")
                plt.show()

        bouton_calculer.on_click(on_calculer_clicked)
        display(mots_input, bouton_calculer, output)

    def calculer_cooccurrences(self, corpus, mots):
        # Compter les co-occurrences dans le corpus
        cooccurrences = Counter()
        for doc in corpus.id2doc.values():
            doc.texte = str(doc.texte) if str(doc.texte) != 'nan' else ''
            texte = doc.texte.split()
            for combinaison in itertools.combinations(mots, 2):
                if all(mot in texte for mot in combinaison):
                    cooccurrences[combinaison] += 1

        # Créer un DataFrame pour la heatmap
        df = pd.DataFrame(index=mots, columns=mots).fillna(0)
        for (mot1, mot2), count in cooccurrences.items():
            df.at[mot1, mot2] = count
            df.at[mot2, mot1] = count
        return df







    def affichage_et_annotation(self):
        style = {'description_width': 'initial'}
        layout = widgets.Layout(width='500px')

        # Sélection de l'index du document
        index_document_widget = widgets.IntText(value=0, description='Index du Document:', style=style, layout=layout)
        bouton_afficher = widgets.Button(description='Afficher le Document', style=style)
        output_document = widgets.Output()

        def on_afficher_clicked(b):
            with output_document:
                clear_output(wait=True)
                index = index_document_widget.value
                if index < len(self.corpus_courant.id2doc):
                    doc = list(self.corpus_courant.id2doc.values())[index]
                    print(f"Texte du document: {doc.texte}")
                    self.interface_annotation(doc)
                else:
                    print("Index invalide.")

        bouton_afficher.on_click(on_afficher_clicked)

        return widgets.VBox([index_document_widget, bouton_afficher, output_document])

    def interface_annotation(self, document):
        # Définition du style et du layout pour les widgets
        style = {'description_width': 'initial'}
        layout = widgets.Layout(width='500px')

        # Widgets pour entrer les détails de l'annotation
        id_annotation_widget = widgets.IntText(description='ID de l\'annotation:', style=style, layout=layout)
        texte_annotation_widget = widgets.Textarea(description='Texte de l\'annotation:', style=style, layout=layout)
        position_annotation_widget = widgets.IntText(description='Position de l\'annotation:', style=style,
                                                     layout=layout)
        bouton_ajouter = widgets.Button(description='Ajouter Annotation', style=style)
        bouton_afficher_annotations = widgets.Button(description='Afficher les Anciennes Annotations', style=style)
        output_annotations = widgets.Output()

        # Fonction pour gérer le clic sur le bouton d'ajout
        def on_ajouter_clicked(b):
            id_annotation = id_annotation_widget.value
            texte = texte_annotation_widget.value
            position = position_annotation_widget.value
            document.ajouter_annotation(id_annotation, texte, position)
            id_annotation_widget.value = len(document.annotations) + 1
            texte_annotation_widget.value = ''
            position_annotation_widget.value = 0
            print("Annotation ajoutée.")

        # Fonction pour gérer le clic sur le bouton d'affichage
        def on_afficher_annotations_clicked(b):
            with output_annotations:
                clear_output(wait=True)
                if document.annotations:
                    document.afficher_annotations()
                else:
                    print("Pas d'anciennes annotations.")

        bouton_ajouter.on_click(on_ajouter_clicked)
        bouton_afficher_annotations.on_click(on_afficher_annotations_clicked)

        # Afficher les widgets
        display(id_annotation_widget, texte_annotation_widget, position_annotation_widget, bouton_ajouter,
                bouton_afficher_annotations, output_annotations)








    def sauvegarde_corpus(self):
        bouton_sauvegarder = widgets.Button(description='Sauvegarder',
                                            style={'description_width': 'initial'})
        output_sauvegarde = widgets.Output()

        def on_sauvegarder_clicked(b):
            with output_sauvegarde:
                clear_output(wait=True)
                try:
                    nom_fichier = f"data/{self.nom_corpus_courant}.pkl"
                    self.corpus_courant.save(nom_fichier)
                    print("Corpus sauvegardé avec succès.")
                except Exception as e:
                    print(f"Erreur lors de la sauvegarde : {e}")

        bouton_sauvegarder.on_click(on_sauvegarder_clicked)

        return widgets.VBox([bouton_sauvegarder, output_sauvegarde])


