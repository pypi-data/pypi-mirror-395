"""Classe che gestisce il calcolo delle metriche di performance per modelli supervisionati e non supervisionati.

La classe supporta diversi tipi di modelli (regressione, classificazione, clustering) e permette di configurare diverse metriche di performance a seconda del tipo di approccio e modello.
"""

# regression
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    explained_variance_score,
    median_absolute_error,
)

# classification
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    balanced_accuracy_score,
)

import warnings
import pandas as pd
import numpy as np
from typing import Dict
import inspect

from model_monitoring.imputer import cluster_imputing
from model_monitoring.utils import (
    check_size,
    convert_Int_series,
    convert_Int_dataframe,
    convert_date_columns_to_seconds,
    convert_cluster_labels,
)
from model_monitoring.performance_measures.performance_measures import (
    compute_metric,
    compute_unsupervised_metric,
)
from model_monitoring.additional_metrics import classification_clustering


class PerformancesMeasures:
    """Classe che gestisce il calcolo delle metriche di performance per modelli supervisionati e non supervisionati.

    Questa classe fornisce un metodo per valutare le prestazioni di diversi tipi di modelli di machine learning: regressione, classificazione (binaria e multiclasse) e clustering. Permette di utilizzare set di metriche standard predefinite o di specificare metriche personalizzate.

    Per i modelli supervisionati le metriche standard utilizzate sono:

      * **Regressione:**

            * MSE (Mean Squared Error)
            * R² (Coefficient of Determination)
            * MAE (Median Absolute Error)
            * Explained Variance Score
      * **Classificazione:**

            * Accuracy
            * Precision
            * Recall
            * F1-score
            * ROC AUC (Receiver Operating Characteristic Area Under Curve)
            * Balanced Accuracy
      * **Multiclasse:**

            * Accuracy
            * ROC AUC (Receiver Operating Characteristic Area Under Curve)
            * Balanced Accuracy

    Per i modelli non supervisionati (clustering), la qualità viene valutata principalmente tramite un compito ausiliario di classificazione. Si addestra un classificatore Gradient Boosting (`LGBMClassifier`) per prevedere le etichette di cluster (assegnate dall'algoritmo di clustering) utilizzando le feature originali dei dati. Questo addestramento viene ripetuto più volte (default 5) su diverse combinazioni di splitting dei dati  tramite l'utilizzo di una `StratifiedKFold`, in cui viene fatto il train su tutti i fold tranne uno e il test sul fold rimanente.

    La performance finale del classificatore è data dalla mediana dei risultati ottenuti in questi addestramenti (le performance fanno riferimento al test), misurata secondo una metrica configurabile (default `balanced_accuracy`). Un valore elevato di questa performance indica che i cluster identificati sono ben distinguibili nello spazio delle feature, suggerendo quindi un clustering di buona qualità.

    Oltre a questo approccio, è possibile valutare il clustering anche con metriche intrinseche (es. Silhouette Score), se vengono fornite come metriche personalizzate.

    La classe gestisce anche la conversione dei tipi di dati e l'imputazione opzionale
    dei valori mancanti (`NaN`) per i dati di clustering.

    **Imputazione NaN:**

        * Viene aggiunta la colonna relativa alle etichette di cluster assegnate ai dati dall'algoritmo di clustering e vengono raggruppati i dati in base all'etichetta di clustering.
        * Se in un raggruppamento sono presenti colonne completamente vuote (tutti `NaN`) vengono riempite con statistiche (moda per i valori categorici o mediana per i valori numerici) calcolate sull'intero dataset.
        * Per ogni gruppo di cluster vengono trasformate le colonne categoriche tramite la codifica One-Hot Encoding.
        * Se presenti dei valori `NaN` vengono calcolate delle distanze di similarità tra la riga contenente il valore `NaN` e tutte le altre del gruppo.
        * Vengono prese le prime k righe con similarità più alta e viene sostituito il valore `NaN` con il valore medio di queste righe. Se anche le k righe "vicine" presentano dei `NaN` viene utilizzato il valore medio del gruppo.
        * Le colonne precedentemente codificate con One-Hot Encoding vengono riconvertite in formato categorico. Per ogni riga, si identifica la colonna dummy (tra quelle associate alla stessa feature) con il valore massimo; il nome di questa colonna determina la categoria assegnata.

    """

    def __init__(
        self,
        approach_type="supervised",
        model_type="auto",
        set_metrics="standard",
        new_metrics=None,
        impute_nans=False,
        **kwargs,
    ):
        """Inizializza l'oggetto PerformancesMeasures per configurare il calcolo delle metriche.

        Questo costruttore imposta il tipo di approccio (supervisionato/non supervisionato), il tipo di modello, come selezionare le metriche (standard, aggiuntive, nuove), e opzioni specifiche come l'imputazione dei NaN per il clustering.

        Args:
            approach_type (`str`, optional): Specifica l'approccio di machine learning.
                Deve essere 'supervised' o 'unsupervised'.
                Default: 'supervised'.
            model_type (`str`, optional): Specifica il tipo di modello.

                - Per `approach_type='supervised'`: 'regression', 'classification', 'multiclass', o 'auto'. Se 'auto', il tipo verrà dedotto dai dati `target` durante `compute_metrics`.
                - Per `approach_type='unsupervised'`: Deve essere 'clustering'.
                Default: 'auto'.
            set_metrics (`str`, optional): Definisce come vengono impostate le metriche da calcolare.

                - 'standard': Usa le metriche predefinite per il `model_type` specificato.
                - 'add': Aggiunge le metriche in `new_metrics` a quelle standard.
                - 'new': Usa **solo** le metriche specificate in `new_metrics`.
                Default: 'standard'.
            new_metrics (`dict`/`list`/`None`, optional): Metriche personalizzate da aggiungere o usare.

                - Per `approach_type='supervised'`: Un dizionario dove le chiavi sono le funzioni delle metriche e i valori sono stringhe che indicano l'input richiesto dalla metrica: 'pred' per le predizioni, 'prob' per le probabilità.
                Esempio: `{matthews_corrcoef: 'pred', log_loss: 'prob'}`.

                - Per `approach_type='unsupervised'`: Una lista di funzioni di metriche.
                  Esempio: `[silhouette_score, davies_bouldin_score]`.

                Default: `None`.
            impute_nans (`bool`, optional): Se `True` e `approach_type='unsupervised'`, i valori NaN nella `data_matrix` verranno imputati usando una strategia basata sui cluster prima del calcolo delle metriche (vedi `Imputazione NaN` in :class:`.PerformancesMeasures`). Ignorato se `approach_type='supervised'`.
                Default: `False`.
            **kwargs: Parametri aggiuntivi che possono essere utilizzati da specifiche metriche o funzioni interne.

        Note:
            - Se `model_type` è 'auto' per l'approccio supervisionato, verrà determinato in `compute_metrics` in base al numero di valori unici nel `target`:

                * <=2 -> 'classification' (Classificazione Binaria)
                * <11 -> 'multiclass' (Classificazione Multiclasse)
                * >=11 -> 'regression' (Regressione)
        """
        if approach_type not in ["supervised", "unsupervised"]:
            raise ValueError(
                f"{approach_type} is not a valid approach, select one of the following:\n['supervised','unsupervised']"
            )
        else:
            self.approach_type = approach_type
        # Check approach_type and model_type

        if self.approach_type == "supervised":
            if model_type in ["clustering"]:
                raise ValueError(
                    f"{model_type} is not a supervised model, select one of the following:\n['auto', 'regression', 'classification', 'multiclass'], or select an unsupervised one between:\n['clustering']"
                )
            elif model_type not in ["auto", "regression", "classification", "multiclass"]:
                raise ValueError(
                    f"{model_type} is not a valid algo_type. It should be one of the following:\n['auto', 'regression', 'classification', 'multiclass','clustering']"
                )
            else:
                self.model_type = model_type
                self.impute_nans = False
        else:
            if model_type in ["auto", "regression", "classification", "multiclass"]:
                raise ValueError(
                    f"{model_type} is not an unsupervised model, select one of the following:\n['clustering'], or select a supervised one between:\n['auto', 'regression', 'classification', 'multiclass']"
                )
            elif model_type not in ["clustering"]:
                raise ValueError(
                    f"{model_type} is not a valid algo_type. It should be one of the following:\n['auto', 'regression', 'classification', 'multiclass','clustering']"
                )
            else:
                self.model_type = model_type
                self.impute_nans = impute_nans
        # Check the set_metrics

        if set_metrics not in ["standard", "add", "new"]:
            raise ValueError(
                f"{set_metrics} is not a valid set_metrics. It should be one of the following:\n ['standard', 'add', 'new']"
            )
        self.set_metrics = set_metrics

        # Check new_metrics
        if self.set_metrics in ["add", "new"]:
            if self.approach_type == "supervised":
                if new_metrics is None:
                    self.new_metrics = {}
                else:
                    if isinstance(new_metrics, Dict):
                        if set(new_metrics.values()).issubset(set(["pred", "prob"])):
                            self.new_metrics = new_metrics
                        else:
                            raise ValueError(
                                f"{list(set(new_metrics.values()))} contains invalid input. Valid inputs are ['pred', 'prob']"
                            )
                    else:
                        raise ValueError(
                            f"{new_metrics} has not a valid format. It should be a dictionary containing functions as keys and one of ['pred', 'prob'] as values."
                        )
            else:
                if new_metrics is None:
                    self.new_metrics = []
                else:
                    if isinstance(new_metrics, list):
                        self.new_metrics = new_metrics
                    else:
                        raise ValueError(
                            f"{new_metrics} has not a valid format. It should be a list containing functions"
                        )
        else:
            self.new_metrics = new_metrics
        # Set the metrics for each set_metric case
        if self.set_metrics == "new":
            self.metrics = self.new_metrics
        if self.set_metrics in ["standard", "add"]:
            if self.model_type == "regression":
                self.metrics = {
                    mean_squared_error: "pred",
                    r2_score: "pred",
                    median_absolute_error: "pred",
                    explained_variance_score: "pred",
                }
            elif self.model_type == "classification":
                self.metrics = {
                    balanced_accuracy_score: "pred",
                    accuracy_score: "pred",
                    precision_score: "pred",
                    recall_score: "pred",
                    f1_score: "pred",
                    roc_auc_score: "prob",
                }

            elif self.model_type == "clustering":
                self.metrics = [classification_clustering]
            else:
                self.metrics = {balanced_accuracy_score: "pred", accuracy_score: "pred", roc_auc_score: "prob"}
            if self.set_metrics == "add":
                if self.approach_type == "supervised":
                    self.metrics = {**self.metrics, **self.new_metrics}
                else:
                    self.metrics = self.metrics + self.new_metrics

        # Check model_params
        self.predictions = None
        self.prob = None
        self.target = None
        self.perf_metrics = None
        self.cluster_labels = None
        self.data_matrix = None
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def compute_metrics(
        self,
        target=None,
        predictions=None,
        prob=None,
        cluster_labels=None,
        data_matrix=None,
        return_prop_true=True,
        classification_threshold=0.5,
        **kwargs,
    ):
        """Calcola le metriche di performance configurate sui dati forniti.

        Questo metodo esegue il calcolo effettivo delle metriche definite durante l'inizializzazione della classe, utilizzando i dati di input appropriati per l'approccio (supervisionato o non supervisionato) e il tipo di modello.

        Args:
            target (`np.array`/`pd.Series`/`None`, optional): I valori reali o ground truth. Richiesto per `approach_type='supervised'`.
                Default: `None`.
            predictions (`np.array`/`pd.Series`/`None`, optional): Le predizioni del modello. Richiesto per `model_type='regression'`. Per 'classification'/'multiclass', può essere omesso se `prob` è fornito (verrà derivato usando `classification_threshold`).
                Default: `None`.
            prob (`np.array`/`pd.Series`/`None`, optional): Le probabilità predette dal modello. Utilizzato per metriche specifiche di classificazione (es. ROC AUC, LogLoss). Per 'classification', se `predictions` non è fornito, queste probabilità vengono usate per generare le predizioni binarie. Per 'multiclass', può contenere array di probabilità per classe.
                Default: `None`.
            cluster_labels (`np.array`/`pd.Series`/`None`, optional): Le etichette assegnate a ciascun cluster di dati. Richiesto per `approach_type='unsupervised'`.
                Default: `None`.
            data_matrix (`pd.DataFrame`/`np.array`/`None`, optional): La matrice di dati (features) utilizzata per il clustering. Richiesta per `approach_type='unsupervised'`.
                Default: `None`.
            return_prop_true (`bool`, optional): Se `True` e il modello è di classificazione binaria, aggiunge la proporzione di etichette positive nel `target` alla chiave 'proportion_1' del dizionario dei risultati.
                Default: `True`.
            classification_threshold (`float`, optional): La soglia utilizzata per convertire le probabilità (`prob`) in predizioni binarie (0 o 1) per i modelli di classificazione binaria, solo se `predictions` non viene fornito esplicitamente.
                Default: 0.5.
            **kwargs (`dict`, opzionale): Altri parametri opzionali da passare alla funzione, che possono includere le configurazioni personalizzate per il calcolo delle metriche.

        Returns:
            `dict`: Un dizionario contenente i nomi delle metriche calcolate come chiavi e i loro valori numerici come valori.

        Note:
            - Se `model_type` è 'auto' per l'approccio supervisionato, viene determinato qui basandosi sui valori unici nel `target`:

                * <=2 -> 'classification' (Classificazione Binaria)
                * <11 -> 'multiclass' (Classificazione Multiclasse)
                * >=11 -> 'regression' (Regressione)
            - Per quanto riguarda la gestione dei valori `NaN`:

                * Le righe con `NaN` in `cluster_labels` vengono rimosse sia da `cluster_labels` che da `data_matrix`.
                * Se `data_matrix` contiene `NaN` e in `__init__` il parametro `impute_nans` è `True`, i `NaN` vengono imputati attreverso una strategia basata sui cluster prima del calcolo delle metriche (vedi `Imputazione NaN` in :class:`.PerformancesMeasures`). Se è `False`, il calcolo di alcune metriche potrebbe fallire.
            - Per metriche come ROC AUC in contesti multiclasse, viene utilizzata la strategia One-vs-Rest (`multi_class='ovr'`).
            - Se il `target` ha un solo valore unico, alcune metriche (es. ROC AUC) non possono essere calcolate e verrà emesso un `warning`.
            - Per quanto riguarda il contesto di clustering i valori che posso settare nei `kwargs` per la metrica di clustering predefinita sono `n_splits` (default 5) e `classification_clustering_metric` (default 'balanced_accuracy_score'), rispettivamnete il numero di split e la metrica di validazione di classificazione. Inoltre posso controllare l'imputazione dei `NaN` tramite i parametri `k` (default 5) e `size` (default 500), rispettivamente il numero di neighbors e il numero di campioni in cui cercare i k-neighbors.

        **Dati utilizzati per gli esempi**

        >>> df_esempio

        .. raw:: html

            <style>
               /* Stile base per la tabella con la nostra classe specifica */
               .jupyter-style-table {
                   border-collapse: collapse; /* Bordi uniti */
                   margin: 1em 0; /* Margine sopra/sotto */
                   font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; /* Font simile a Jupyter */
                   font-size: 0.9em; /* Dimensione font leggermente ridotta */
                   border: 1px solid #d3d3d3; /* Bordo esterno leggero */
                   width: auto; /* Larghezza basata sul contenuto */
                   max-width: 100%; /* Non superare il contenitore */
                   overflow-x: auto; /* Abilita lo scroll orizzontale se necessario (meglio sul wrapper, ma ok qui) */
                   display: block; /* Necessario per far funzionare overflow-x su una tabella */
               }

               /* Stile per le celle dell'header (th) */
               .jupyter-style-table thead th {
                   background-color: #f5f5f5; /* Sfondo grigio chiaro per header */
                   font-weight: bold; /* Grassetto */
                   padding: 8px 10px; /* Padding interno */
                   text-align: right; /* Allineamento testo (spesso a destra per numeri/default) */
                   border-bottom: 1px solid #d3d3d3; /* Linea sotto l'header */
                   vertical-align: bottom; /* Allineamento verticale */
               }

               /* Stile per le celle dei dati (td) */
               .jupyter-style-table tbody td {
                   padding: 6px 10px; /* Padding interno */
                   text-align: right; /* Allineamento testo (aggiusta se hai testo a sinistra) */
                   border-right: 1px solid #d3d3d3; /* Linea verticale tra celle (opzionale) */
                   border-top: 1px solid #d3d3d3; /* Linea orizzontale tra righe */
                   vertical-align: middle; /* Allineamento verticale */
               }
               .jupyter-style-table tbody td:last-child {
                   border-right: none; /* Rimuovi bordo destro sull'ultima cella */
               }

               /* Stile per l'header dell'indice (se presente) */
               .jupyter-style-table thead th.blank { /* Header vuoto sopra l'indice */
                   background-color: white;
                   border: none;
               }
               .jupyter-style-table tbody th { /* Celle dell'indice nel body */
                   padding: 6px 10px;
                   text-align: right;
                   font-weight: normal;
                   border-right: 1px solid #d3d3d3;
                   border-top: 1px solid #d3d3d3;
                   background-color: #f5f5f5; /* Sfondo leggero per indice */
               }


               /* Striping delle righe (alternanza colori) */
               .jupyter-style-table tbody tr:nth-child(even) {
                   background-color: #f9f9f9; /* Sfondo molto leggero per righe pari */
               }

               /* Effetto Hover (cambio colore al passaggio del mouse) */
               .jupyter-style-table tbody tr:hover {
                   background-color: #f0f0f0; /* Sfondo leggermente più scuro su hover */
               }
            </style>

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature_num</th>      <th>feature_cat</th>      <th>target_clf</th>      <th>pred_clf</th>      <th>target_reg</th>      <th>pred_reg</th>      <th>prob_clf</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>2</td>      <td>B</td>      <td>0</td>      <td>0</td>      <td>7.652628</td>      <td>-1.427613</td>      <td>0.032526</td>    </tr>    <tr>      <th>1</th>      <td>3</td>      <td>A</td>      <td>1</td>      <td>0</td>      <td>17.712800</td>      <td>3.589763</td>      <td>0.474443</td>    </tr>    <tr>      <th>2</th>      <td>4</td>      <td>C</td>      <td>0</td>      <td>0</td>      <td>17.682912</td>      <td>32.339399</td>      <td>0.482816</td>    </tr>    <tr>      <th>3</th>      <td>5</td>      <td>B</td>      <td>0</td>      <td>0</td>      <td>22.671351</td>      <td>20.413588</td>      <td>0.404199</td>    </tr>    <tr>      <th>4</th>      <td>6</td>      <td>A</td>      <td>0</td>      <td>1</td>      <td>31.209811</td>      <td>31.885093</td>      <td>0.652307</td>    </tr>    <tr>      <th>5</th>      <td>7</td>      <td>C</td>      <td>1</td>      <td>0</td>      <td>25.433599</td>      <td>11.186117</td>      <td>0.048836</td>    </tr>    <tr>      <th>6</th>      <td>8</td>      <td>D</td>      <td>0</td>      <td>1</td>      <td>31.375411</td>      <td>25.931584</td>      <td>0.842117</td>    </tr>    <tr>      <th>7</th>      <td>9</td>      <td>E</td>      <td>0</td>      <td>1</td>      <td>42.188562</td>      <td>43.297788</td>      <td>0.720076</td>    </tr>    <tr>      <th>8</th>      <td>10</td>      <td>C</td>      <td>0</td>      <td>1</td>      <td>44.935844</td>      <td>33.425909</td>      <td>0.561019</td>    </tr>    <tr>      <th>9</th>      <td>11</td>      <td>A</td>      <td>1</td>      <td>0</td>      <td>56.571237</td>      <td>60.328217</td>      <td>0.247588</td>    </tr>  </tbody></table>

        **Esempio:**

        >>> from model_monitoring.performance_measures import PerformancesMeasures
        >>> from model_monitoring.additional_metrics import lift_score
        >>> Perf_Meas = PerformancesMeasures(model_type="classification", set_metrics="add",new_metrics={lift_score:"prob"})
        >>> dict_perf = Perf_Meas.compute_metrics(target=df_esempio['target_clf'], predictions=df_esempio['pred_clf'], prob=df_esempio['prob_clf'])
        >>> dict_perf
        {'balanced_accuracy_score': 0.21428571428571427,
         'accuracy_score': 0.3,
         'precision_score': 0.0,
         'recall_score': 0.0,
         'f1_score': 0.0,
         'roc_auc_score': 0.1904761904761905,
         'lift_score': 0.0,
         'proportion_1': 0.3}

        """
        # Create perf_metric dict
        for k, v in kwargs.items():
            self.__dict__[k] = v
        perf_metrics = dict()
        # Metric if supervised approach
        if self.approach_type == "supervised":
            # Check one among predictions and prob exists
            if target is None:
                raise ValueError("target must not be None")
            if (predictions is None) and (prob is None):
                raise ValueError("at least one among predictions and prob must be not None")

            # Check size of the predictions and target
            if predictions is not None:
                check_size(predictions, target)

            # Check size of the target and prob
            if prob is not None:
                check_size(target, prob)

            if isinstance(target, np.ndarray):
                target = pd.Series(target, name="target")
            vals = target.nunique()
            if vals == 1:
                warnings.warn("The target column selected is constant")
            elif self.model_type == "auto":
                if vals <= 2:
                    self.model_type = "classification"
                elif vals < 11:
                    self.model_type = "multiclass"
                else:
                    self.model_type = "regression"

            if self.model_type == "regression":
                if predictions is None:
                    raise ValueError("predictions not provided")

            self.target = convert_Int_series(target)
            if predictions is not None:
                self.predictions = convert_Int_series(predictions)
            else:
                self.predictions = predictions
            if prob is not None:
                self.prob = convert_Int_series(prob)
            else:
                self.prob = prob

            self.return_prop_true = return_prop_true
            self.classification_threshold = classification_threshold

            if self.model_type == "regression":
                for i, j in self.metrics.items():
                    dict_to_use = {
                        k: v for k, v in self.__dict__.items() if k in inspect.signature(i).parameters.keys()
                    }
                    if j == "pred":
                        perf_metrics[i.__name__] = compute_metric(
                            self.target, self.predictions, metric=i, **dict_to_use
                        )
                    else:
                        warnings.warn(
                            f"{j} is a wrong label for regression model type. Label {i.__name__} with 'pred'."
                        )
            elif self.model_type == "classification":
                if self.predictions is None:
                    try:
                        self.predictions = self.prob.apply(lambda x: 1 if x > self.classification_threshold else 0)
                    except Exception:
                        self.predictions = np.array([1 if i > self.classification_threshold else 0 for i in self.prob])
                for i, j in self.metrics.items():
                    dict_to_use = {
                        k: v for k, v in self.__dict__.items() if k in inspect.signature(i).parameters.keys()
                    }
                    # some metrics don't work well with 1 target value (e.g. roc_auc_score)
                    if vals == 1:
                        if i.__name__ in ["roc_auc_score", "lift_score", "gain_score"]:
                            warnings.warn(f"{i.__name__} cannot be used when target has a constant value.")
                            continue
                    if j == "prob":
                        if self.prob is None:
                            warnings.warn(f"{i.__name__} needs prob, but prob are not provided")
                        else:
                            perf_metrics[i.__name__] = compute_metric(self.target, self.prob, metric=i, **dict_to_use)
                    else:
                        perf_metrics[i.__name__] = compute_metric(
                            self.target, self.predictions, metric=i, **dict_to_use
                        )
                if self.return_prop_true:
                    perf_metrics["proportion_1"] = (self.target == 1).mean()  # Add proportion of 1 label
            elif self.model_type == "multiclass":
                if self.predictions is None:
                    self.predictions = pd.Series([np.argmax(x) for x in self.prob], name="prob")
                for i, j in self.metrics.items():
                    dict_to_use = {
                        k: v for k, v in self.__dict__.items() if k in inspect.signature(i).parameters.keys()
                    }
                    if i.__name__ in [
                        "precision_score",
                        "recall_score",
                        "f1_score",
                        "fbeta_score",
                        "brier_score_loss",
                        "class_likelihood_ratios",
                        "dcg_score",
                        "jaccard_score",
                        "log_loss",
                        "matthews_corrcoef",
                        "ndcg_score",
                    ]:
                        warnings.warn(f"{i.__name__} is used for binary classification")
                    elif j == "prob":
                        if self.prob is None:
                            warnings.warn(f"{i.__name__} needs prob, but prob are not provided")
                        else:
                            perf_metrics[i.__name__] = compute_metric(
                                self.target, self.prob, metric=i, multi_class="ovr"
                            )
                    else:
                        perf_metrics[i.__name__] = compute_metric(
                            self.target, self.predictions, metric=i, **dict_to_use
                        )
            else:
                raise ValueError("Invalid model type.")
        # Metric if unsupervised approach
        else:
            # data quality
            if (cluster_labels is None) or (data_matrix is None):
                raise ValueError("Both cluster_labels and data_matrix must be not None")
            else:
                check_size(data_matrix, cluster_labels)
                data_matrix = convert_date_columns_to_seconds(data_matrix)
            if not isinstance(cluster_labels, pd.Series):
                cluster_labels = pd.Series(cluster_labels, name="cluster_labels")
            cluster_labels = convert_Int_series(cluster_labels)

            if cluster_labels.isna().any():
                condition = ~cluster_labels.isna()
                cluster_labels = cluster_labels[condition].reset_index(drop=True)
                data_matrix = data_matrix[condition].reset_index(drop=True)

            vals = cluster_labels.nunique()
            # uniform cluster value and type
            cluster_labels = convert_cluster_labels(cluster_labels, vals)

            if not isinstance(data_matrix, pd.DataFrame):
                data_matrix = pd.DataFrame(data_matrix)
            data_matrix = convert_Int_dataframe(data_matrix)
            if data_matrix.isna().any().any():
                if self.impute_nans:
                    valid_params = inspect.signature(cluster_imputing).parameters.keys()
                    dict_to_use = {k: v for k, v in self.__dict__.items() if k in valid_params}

                    self.data_matrix, self.cluster_labels = cluster_imputing(data_matrix, cluster_labels, **dict_to_use)
                else:
                    self.data_matrix = data_matrix
                    self.cluster_labels = cluster_labels
            else:
                self.data_matrix = data_matrix
                self.cluster_labels = cluster_labels

            categorical_cols = self.data_matrix.select_dtypes(exclude=["number"]).columns
            if self.new_metrics:
                data_matrix_dummies = self.data_matrix.copy()
                data_matrix_dummies = pd.get_dummies(data_matrix_dummies, columns=categorical_cols)
            self.data_matrix[categorical_cols] = self.data_matrix[categorical_cols].astype("category")
            # warning for classification clustering
            # compute metrics
            if vals != 1:
                for i in self.metrics:
                    dict_to_use = {
                        k: v for k, v in self.__dict__.items() if k in inspect.signature(i).parameters.keys()
                    }
                    try:
                        if i.__name__ != "classification_clustering":
                            metric = compute_unsupervised_metric(
                                data_matrix_dummies, self.cluster_labels, i, **dict_to_use
                            )
                            perf_metrics[i.__name__] = metric
                        else:
                            metric = compute_unsupervised_metric(
                                self.data_matrix, self.cluster_labels, i, **dict_to_use
                            )
                            perf_metrics[i.__name__] = metric
                    except Exception:
                        if not self.impute_nans:
                            if self.data_matrix.isna().any().any():
                                raise ValueError(
                                    f"\n An error occured while computing {i.__name__}, the reason could be impute_nans is set to False, try set it as True while initializating the class"
                                )
                        else:
                            raise ValueError(
                                f"\n{i.__name__} is not a valid additional metric for clustering monitoring"
                            )
            # Many metrics don't work well with a single cluster
            else:
                for i in self.metrics:
                    try:
                        if i.__name__ != "classification_clustering":
                            metric = compute_unsupervised_metric(
                                data_matrix_dummies, self.cluster_labels, i, **dict_to_use
                            )
                            perf_metrics[i.__name__] = metric
                        else:
                            metric = compute_unsupervised_metric(
                                self.data_matrix, self.cluster_labels, i, **dict_to_use
                            )
                            perf_metrics[i.__name__] = metric
                    except Exception:
                        warnings.warn(
                            f"\n{i.__name__} is not a valid additional metric for clustering monitoring with a single cluster"
                        )
                        pass
        self.perf_metrics = perf_metrics
        return self.perf_metrics
