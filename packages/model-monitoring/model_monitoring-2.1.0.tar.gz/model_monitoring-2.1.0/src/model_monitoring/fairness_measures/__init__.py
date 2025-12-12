"""Classe utilizzata per calcolare e monitorare le metriche di fairness nei modelli di machine learning.

La classe supporta sia modelli supervisionati (classificazione e regressione) che non supervisionati (clustering). Il calcolo delle metriche di fairness è cruciale per monitorare se i modelli di machine learning discriminano rispetto a diversi gruppi di fairness.
"""

import pandas as pd
import numpy as np
import warnings
from typing import Callable, List
import inspect

# classification
from model_monitoring.fairness_measures.fairness_measures import (
    statistical_parity_difference,
    disparate_impact_ratio,
    predictive_parity_difference,
    equal_opportunity_difference,
    average_odds_difference,
)

# regression
from model_monitoring.fairness_measures.fairness_measures import ddre_independence, ddre_separation, ddre_sufficiency

from model_monitoring.utils import (
    check_size,
    convert_Int_dataframe,
    convert_Int_series,
    convert_date_columns_to_seconds,
    convert_cluster_labels,
)
from model_monitoring.fairness_measures.fairness_measures import compute_metric_fairness


class FairnessMeasures:
    r"""Classe utilizzata per calcolare e monitorare le metriche di fairness nei modelli di machine learning.

    La classe offre la possibilità di:

    - Scegliere tra diversi approcci di fairness: "supervised" e "unsupervised".

    - Calcolare delle metriche di fairness standard predefinite, che variano in base al tipo di modello (quando `set_metrics` è "standard" o "add"). Metriche di Fairness Predefinite:

        *   **Per model_type="classification":**

            *   ``statistical_parity_difference``: Monitora la differenza nel **Positive Rate** (tasso di predizioni positive, calcolato come ``(TP+FP)/(TP+FP+TN+FN)``) tra i gruppi di fairness. Un valore vicino a 0 indica che le distribuzioni delle predizioni positive (gli "1") sono simili nei gruppi di fainess. Se i gruppi di fairness sono più di due, si applica una logica “One-vs-all”, ovvero che ogni gruppo di fairness viene confrontato con tutti gli altri. Formula:

            .. math::

               Pr(\hat{Y}={pos\_label}|D={unprivileged}) - Pr(\hat{Y}={pos\_label}|D={privileged})

            *   ``disparate_impact_ratio``: Monitora il **rapporto** del **Positive Rate** tra i gruppi di fairness. Un valore vicino a 1 indica che le distribuzioni delle predizioni positive (gli "1") sono simili nei gruppi di fainess.  Se i gruppi di fairness sono più di due, si applica una logica “One-vs-all”, ovvero che ogni gruppo di fairness viene confrontato con tutti gli altri. Formula:

                .. math::

                   \frac{Pr(\hat{Y}={pos\_label}|D={unprivileged})}{Pr(\hat{Y}={pos\_label}|D={privileged})}
            *   ``predictive_parity_difference``: Monitora la differenza nella **Precision** (Accuratezza delle predizioni positive, ``TP / (TP + FP)``) tra i gruppi di fairness.  Un valore vicino a 0 indica che l'accuratezza delle predizioni positive (gli "1") è simile nei gruppi di fainess. Se i gruppi di fairness sono più di due, si applica una logica “One-vs-all”, ovvero che ogni gruppo di fairness viene confrontato con tutti gli altri. Formula:

            .. math::

               prec_{D={unprivileged}} - prec_{D={privileged}}

            *   ``equal_opportunity_difference``: Monitora la differenza nella **Recall** (Tasso di Veri Positivi, ``TP / (TP + FN)``) tra i gruppi di fairness. Un valore vicino a 0 indica che il modello identifica correttamente i casi positivi reali con la stessa accuratezza per entrambi i gruppi. Se i gruppi di fairness sono più di due, si applica una logica “One-vs-all”, ovvero che ogni gruppo di fairness viene confrontato con tutti gli altri. Formula:

            .. math::

               TPR_{D={unprivileged}} - TPR_{D={privileged}}

            *   ``average_odds_difference``: Monitora la media aritmetica della differenza nel **False Positive Rate** (Tasso di Falsi Positivi, ``FP / (FP + TN)``) e della differenza nella **Recall** (Tasso di Veri Positivi) tra i gruppi di fairness. Un valore vicino a 0 indica un simile bilanciamento tra i tassi di veri positivi e falsi positivi per entrambi i gruppi. Se i gruppi di fairness sono più di due, si applica una logica “One-vs-all”, ovvero che ogni gruppo di fairness viene confrontato con tutti gli altri. Formula:

            .. math::

               \frac{(FPR_{D={unprivileged}} - FPR_{D={privileged}}) + (TPR_{D={unprivileged}} - TPR_{D={privileged}})}{2}

        *   **Per model_type="regression" (basate su Direct Density Ratio Estimation - DDRE):**

            *   ``ddre_independence``: Dato `S` l’insieme delle predizioni e `A` l’insieme dei gruppi di fairness, la metrica monitora l’indipendenza delle predizioni di un modello di regressione dai gruppi di fairness (``S⟂A``). Un valore vicino a 1 indica che le predizioni seguono la stessa distribuzione rispetto ai gruppi di fairness. Se i gruppi di fairness sono più di due, si applica una logica “One-vs-all”, ovvero che ogni gruppo di fairness viene confrontato con tutti gli altri. Formula:

            .. math::

               \hat{r}_{{ind}} = \frac{n_0}{n_1 n} \sum_{i=1}^{n} \frac{\rho(1|s_i)}{1 - \rho(1|s_i)}
            Nella formula si denota con :math:`n_0`, :math:`n_1` e :math:`n` rispettivamente il numero delle righe relative al gruppo di Fairness di riferimento, a quello composto da tutti gli altri e al numero totale delle righe. Con `⍴` si denota un classificatore binario (Logistic Regression) per approssimare la densità di probabilità condizionata di un gruppo di fairness data la previsione.

            *   ``ddre_separation``: Dato `S` l’insieme delle predizioni, `Y` l’insieme dei valori del target vero e `A` l’insieme dei gruppi di fairness, la metrica monitora l’indipendenza delle predizioni di un modello di regressione dai gruppi di fairness, dato il target (``S⟂A | Y``). Un valore vicino a 1 indica che le predizioni rispetto al target seguono la stessa distribuzione rispetto ai gruppi di fairness. Se i gruppi di fairness sono più di due, si applica una logica “One-vs-all”, ovvero che ogni gruppo di fairness viene confrontato con tutti gli altri. Formula:

            .. math::

               \hat{r}_{{sep}} = \frac{1}{n} \sum_{i=1}^{n} \frac{\rho(1|y_i, s_i)}{1 - \rho(1|y_i, s_i)} \cdot \frac{1 - \rho(1|y_i)}{\rho(1|y_i)}
            Nella formula si denota con :math:`n` rispettivamente il numero totale delle righe. Con `⍴` si denota un classificatore binario (Logistic Regression) per approssimare le densità di probabilità condizionate di un gruppo di fairness dato il target vero e data la previsione ed il target vero.

            *   ``ddre_sufficiency``: Dato `S` l’insieme delle predizioni, `Y` l’insieme dei valori del target vero e `A` l’insieme dei gruppi di fairness, la metrica monitora l’indipendenza del target vero dai gruppi di fairness, date le predizioni di un modello di regressione (``Y⟂A | S``). Un valore vicino a 1 indica che il target vero rispetto alle predizioni segue la stessa distribuzione trasversalmente ai gruppi di fairness. Se i gruppi di fairness sono più di due, si applica una logica “One-vs-all”, ovvero che ogni gruppo di fairness viene confrontato con tutti gli altri. Formula:

            .. math::

               \hat{r}_{{suf}} = \frac{1}{n} \sum_{i=1}^{n} \frac{\rho(1|y_i, s_i)}{1 - \rho(1|y_i, s_i)} \cdot \frac{1 - \rho(1|s_i)}{\rho(1|s_i)}
            Nella formula si denota con :math:`n` rispettivamente il numero totale delle righe. Con `⍴` si denota un classificatore binario (Logistic Regression) per approssimare le densità di probabilità condizionate di un gruppo di fairness date le predizioni e data la previsione ed il target vero.

        *   **Per model_type="clustering" ( richiede approach_type = "unsupervised" ):**

            *   ``ddre_independence``: Dato `S` l’insieme delle etichette di clustering e `A` l’insieme dei gruppi di fairness, la metrica monitora l’indipendenza delle etichette di clustering dai gruppi di fairness (``S⟂A``). Un valore vicino a 1 indica che le etichette di clustering seguono la stessa distribuzione rispetto ai gruppi di fairness. Se i gruppi di fairness sono più di due, si applica una logica “One-vs-all”, ovvero che ogni gruppo di fairness viene confrontato con tutti gli altri.

        *   **Per model_type="multiclass":**

            *   ``statistical_parity_difference``: Come per la classificazione, ma calcolata per ogni classe contro tutte le altre e andando poi ad aggregare le singole metriche per classe al valore massimo in valore assoluto (default) o sommandone i valori in valore assoluto.
            *   ``predictive_parity_difference``: Come per la classificazione, ma calcolata per ogni classe contro tutte le altre e andando poi ad aggregare le singole metriche per classe al valore massimo in valore assoluto (default) o sommandone i valori in valore assoluto.
            *   ``equal_opportunity_difference``: Come per la classificazione, ma calcolata per ogni classe contro tutte le altre e andando poi ad aggregare le singole metriche per classe al valore massimo in valore assoluto (default) o sommandone i valori in valore assoluto.
            *   ``average_odds_difference``: Come per la classificazione, ma calcolata per ogni classe contro tutte le altre e andando poi ad aggregare le singole metriche per classe al valore massimo in valore assoluto (default) o sommandone i valori in valore assoluto.

    - Aggiungere (`set_metrics="add"`) o sostituire completamente (`set_metrics="new"`) queste metriche di fairness con funzioni personalizzate fornite tramite il parametro `new_metrics`.
    """

    def __init__(
        self, approach_type="supervised", model_type="auto", set_metrics="standard", new_metrics=None, **kwargs
    ):
        """Inizializza la classe `FairnessMeasures`, configurando le impostazioni necessarie per calcolare le metriche di fairness.

        La funzione gestisce la scelta dell'approccio, del tipo di modello e delle metriche da calcolare, configurando l'analisi in base ai parametri forniti.

        A seconda dei parametri specificati, il costruttore imposta le metriche di fairness standard per il tipo di modello scelto oppure imposta, aggiunge o inizializza nuove metriche personalizzate. La classe supporta modelli supervisionati e non supervisionati.

        Args:
            approach_type (`str`, opzionale): Tipo di approccio per l'analisi della fairness. Può essere:

                - **"supervised"**: Approccio supervisionato.
                - **"unsupervised"**: Approccio non supervisionato, generalmente utilizzato per il clustering.
                Default: "supervised".

            model_type (`str`): Tipo di modello da analizzare. Può essere:

                - **"auto"**: La classe determinerà automaticamente il tipo di modello.
                - **"regression"**: Modello di regressione.
                - **"classification"**: Modello di classificazione binaria.
                - **"multiclass"**: Modello di classificazione multiclasse.
                - **"clustering"**: Modello di clustering (per approccio "unsupervised").
                Default: "auto".

            set_metrics (`str`, opzionale): Impostazioni per le metriche di fairness. Può essere:

                - **"standard"**: Vengono utilizzate le metriche di fairness predefinite per il tipo di modello.
                - **"add"**: Aggiunge nuove metriche a quelle standard.
                - **"new"**: Utilizza un nuovo insieme di metriche fornite dall'utente.
                Default: "standard".

            new_metrics (`list`, opzionale): Lista di nuove metriche da utilizzare quando `set_metrics` è impostato su "new" o "add". Le metriche devono essere fornite come funzioni. Default: `None`.

            **kwargs (`dict`, opzionale): Parametri aggiuntivi che possono essere utilizzati per configurare ulteriormente la classe.
        """
        # Check the approach_type
        if approach_type not in ["supervised", "unsupervised"]:
            raise ValueError(
                f"{approach_type} is not a valid approach_type. It should be one of the following:\n['supervised', 'unsupervised']"
            )
        else:
            self.approach_type = approach_type

        # Check the model_type
        if approach_type == "supervised":
            if model_type in ["clustering"]:
                raise ValueError(
                    f"{model_type} is not a valid algo_type for supervised approach. Select 'unsupervised' as approach_type or one of the following model_type:\n['auto', 'regression', 'classification', 'multiclass']"
                )
            elif model_type not in ["auto", "regression", "classification", "multiclass"]:
                raise ValueError(
                    f"{model_type} is not a valid algo_type. It should be one of the following:\n['auto', 'regression', 'classification', 'multiclass']"
                )
            else:
                self.model_type = model_type

        else:
            if model_type in ["auto", "regression", "classification", "multiclass"]:
                raise ValueError(
                    f"{model_type} is not a valid algo_type for unsupervised approach. Select 'supervised' as approach_type or one of the following model_type:\n['clustering']"
                )
            elif model_type not in ["clustering"]:
                raise ValueError(
                    f"{model_type} is not a valid algo_type. It should be one of the following:\n['clustering']"
                )
            else:
                self.model_type = model_type

        # Check the set_metrics
        if set_metrics not in ["standard", "add", "new"]:
            raise ValueError(
                f"{set_metrics} is not a valid set_metrics. It should be one of the following:\n ['standard', 'add', 'new']"
            )
        self.set_metrics = set_metrics

        # Check new_metrics
        if self.set_metrics in ["add", "new"]:
            if new_metrics is None:
                self.new_metrics = []
            else:
                if isinstance(new_metrics, List):
                    self.new_metrics = new_metrics
                elif isinstance(new_metrics, Callable):
                    self.new_metrics = [new_metrics]
                else:
                    raise ValueError(f"{new_metrics} has not a valid format. It should be a list containing functions")

        # Set the metrics for each set_metric case
        if self.set_metrics == "new":
            self.metrics = self.new_metrics
        if self.set_metrics in ["standard", "add"]:
            if self.model_type == "regression":
                self.metrics = [ddre_independence, ddre_separation, ddre_sufficiency]
            elif self.model_type == "classification":
                self.metrics = [
                    statistical_parity_difference,
                    disparate_impact_ratio,
                    predictive_parity_difference,
                    equal_opportunity_difference,
                    average_odds_difference,
                ]
            elif self.model_type == "clustering":
                self.metrics = [ddre_independence]
            else:
                self.metrics = [
                    statistical_parity_difference,
                    predictive_parity_difference,
                    equal_opportunity_difference,
                    average_odds_difference,
                ]
            if self.set_metrics == "add":
                self.metrics = self.metrics + self.new_metrics

        self.target = None
        self.predictions = None
        self.X_fair = None
        self.fair_feat = None
        self.perf_metrics = None

        for k, v in kwargs.items():
            self.__dict__[k] = v

    def compute_metrics(self, predictions, X_fair, target=None, fair_feat=None, return_prop_true=True, **kwargs):
        """Calcola le metriche di fairness basandosi sulle metriche di fairness impostate sui gruppi di fairness specificati.

        Questo metodo supporta sia modelli supervisionati che non supervisionati.

        Il metodo esegue il calcolo delle metriche di fairness per ciascun gruppo di fairness specificato e può restituire le proporzioni di 1 nel contesto di classificazione binaria.

        Args:
            predictions (`np.array`/`pd.Series`): Le previsioni (o le etichette di cluster) generate dal modello.
            X_fair (`pd.DataFrame`/`pd.Series`): Il dataset da analizzare per le metriche di fairness, contenente le feature che determinano i gruppi di fairness.
            target (`np.array`/`pd.Series`, opzionale): La colonna target per il modello supervisionato. Necessaria solo se `approach_type` è "supervised". Default: `None`.
            fair_feat (`str`/`list`, opzionale): Le feature da analizzare per il calcolo delle metriche di fairness. Se fornita una lista di liste di feature vengono analizzate tutte le combinazioni possibili dei valori di quelle feature per il calcolo delle metriche. Se non fornito, tutte le feature di `X_fair` vengono analizzate. Default: `None`.
            return_prop_true (`bool`, opzionale): Se True, la funzione restituirà anche la proporzione di etichette di target che sono uguali a 1 in ciascun gruppo di fairness in un contesto di classificazione binaria. Default: `True`.
            **kwargs (`dict`, opzionale): Altri parametri opzionali da passare alla funzione, che possono includere le configurazioni personalizzate per il calcolo delle metriche.

        Returns:
            `dict`: Un dizionario contenente le metriche di fairness calcolate per ciascun gruppo di fairness. Ogni chiave è una metrica, e ogni valore è un altro dizionario che contiene le performance per ciascun gruppo.

        Note:
            - Il dizionario ritornato dal metodo contiene per ogni gruppo di fairness, oltre al valore della metrica, anche la percentuale di campioni appartenenti al gruppo rispetto al numero totale di campioni.
            - Se `return_prop_true` è `True` il dizionario ritornato conterrà anche la percentuale di 1 (veri positivi) all'interno del gruppo in un contesto di classificazione binaria.

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

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature_num</th>      <th>feature_cat</th>      <th>target_clf</th>      <th>pred_clf</th>      <th>target_reg</th>      <th>pred_reg</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>2</td>      <td>B</td>      <td>0</td>      <td>0</td>      <td>7.652628</td>      <td>-1.427613</td>    </tr>    <tr>      <th>1</th>      <td>3</td>      <td>A</td>      <td>1</td>      <td>0</td>      <td>17.712800</td>      <td>3.589763</td>    </tr>    <tr>      <th>2</th>      <td>4</td>      <td>C</td>      <td>0</td>      <td>0</td>      <td>17.682912</td>      <td>32.339399</td>    </tr>    <tr>      <th>3</th>      <td>5</td>      <td>B</td>      <td>0</td>      <td>0</td>      <td>22.671351</td>      <td>20.413588</td>    </tr>    <tr>      <th>4</th>      <td>6</td>      <td>A</td>      <td>0</td>      <td>1</td>      <td>31.209811</td>      <td>31.885093</td>    </tr>    <tr>      <th>5</th>      <td>7</td>      <td>C</td>      <td>1</td>      <td>0</td>      <td>25.433599</td>      <td>11.186117</td>    </tr>    <tr>      <th>6</th>      <td>8</td>      <td>D</td>      <td>0</td>      <td>1</td>      <td>31.375411</td>      <td>25.931584</td>    </tr>    <tr>      <th>7</th>      <td>9</td>      <td>E</td>      <td>0</td>      <td>1</td>      <td>42.188562</td>      <td>43.297788</td>    </tr>    <tr>      <th>8</th>      <td>10</td>      <td>C</td>      <td>0</td>      <td>1</td>      <td>44.935844</td>      <td>33.425909</td>    </tr>    <tr>      <th>9</th>      <td>11</td>      <td>A</td>      <td>1</td>      <td>0</td>      <td>56.571237</td>      <td>60.328217</td>    </tr>  </tbody></table>

        **Esempio 1: Utilizzo con Classificazione**

        >>> from model_monitoring.fairness_measures import FairnessMeasures
        >>> prova_clf = FairnessMeasures(approach_type="supervised", model_type="classification")
        >>> fair_dict_clf = prova_clf.compute_metrics(
        ...     df_esempio.pred_clf,
        ...     df_esempio,
        ...     target=df_esempio.target_clf,
        ...     fair_feat=['feature_cat']
        ... )
        >>> fair_dict_clf
        {'statistical_parity_difference': {'feature_cat': {'B': [-0.5, 0.2, 0.0],
           'A': [-0.09523809523809523, 0.3, 0.6666666666666666],
           'C': [-0.09523809523809523, 0.3, 0.3333333333333333],
           'D': [0.6666666666666667, 0.1, 0.0],
           'E': [0.6666666666666667, 0.1, 0.0]}},
         'disparate_impact_ratio': {'feature_cat': {'B': [0.0, 0.2, 0.0],
           'A': [0.7777777777777778, 0.3, 0.6666666666666666],
           'C': [0.7777777777777778, 0.3, 0.3333333333333333],
           'D': [3.0, 0.1, 0.0],
           'E': [3.0, 0.1, 0.0]}},
         'predictive_parity_difference': {'feature_cat': {'B': [0.0, 0.2, 0.0],
           'A': [0.0, 0.3, 0.6666666666666666],
           'C': [0.0, 0.3, 0.3333333333333333],
           'D': [0.0, 0.1, 0.0],
           'E': [0.0, 0.1, 0.0]}},
         'equal_opportunity_difference': {'feature_cat': {'B': [0.0, 0.2, 0.0],
           'A': [0.0, 0.3, 0.6666666666666666],
           'C': [0.0, 0.3, 0.3333333333333333],
           'D': [0.0, 0.1, 0.0],
           'E': [0.0, 0.1, 0.0]}},
         'average_odds_difference': {'feature_cat': {'B': [-0.4, 0.2, 0.0],
           'A': [0.25, 0.3, 0.6666666666666666],
           'C': [-0.04999999999999999, 0.3, 0.3333333333333333],
           'D': [0.25, 0.1, 0.0],
           'E': [0.25, 0.1, 0.0]}}}


        **Esempio 2: Utilizzo con Regressione**

        >>> from model_monitoring.fairness_measures import FairnessMeasures
        >>> prova_reg = FairnessMeasures(approach_type="supervised", model_type="regression")
        >>> fair_dict_reg = prova_reg.compute_metrics(
        ...    df_esempio.pred_reg,
        ...    df_esempio,
        ...    target=df_esempio.target_reg,
        ...    fair_feat=['feature_cat']
        ... )
        >>> fair_dict_reg
        {'ddre_independence': {'feature_cat': {'B': [1.105141780859906, 0.2],
           'A': [1.0305683337638512, 0.3],
           'C': [1.0001623180326842, 0.3],
           'D': [0.9999460741465931, 0.1],
           'E': [1.0262780528726796, 0.1]}},
         'ddre_separation': {'feature_cat': {'B': [0.9314966649516162, 0.2],
           'A': [0.9962910535987769, 0.3],
           'C': [0.9999808022130929, 0.3],
           'D': [1.0007959938045, 0.1],
           'E': [0.9474475048436408, 0.1]}},
         'ddre_sufficiency': {'feature_cat': {'B': [0.9319339519285806, 0.2],
           'A': [0.998310923429683, 0.3],
           'C': [0.9999865564552243, 0.3],
           'D': [1.0004274343644692, 0.1],
           'E': [0.9516507505311746, 0.1]}}}
        """
        for k, v in kwargs.items():
            self.__dict__[k] = v
        if isinstance(predictions, np.ndarray):
            predictions = pd.Series(predictions, name="predictions")
        if isinstance(X_fair, pd.Series):
            X_fair = pd.DataFrame(X_fair, index=X_fair.index, columns=[X_fair.name])
        if isinstance(fair_feat, str):
            fair_feat = [fair_feat]
        self.predictions = convert_Int_series(predictions)
        if fair_feat is None:
            fair_feat = X_fair.columns

        X_fair = convert_Int_dataframe(X_fair)
        self.X_fair = convert_date_columns_to_seconds(X_fair)
        self.fair_feat = fair_feat
        perf_metrics = dict()

        # Check size of the target and the features to be analyzed
        check_size(predictions, X_fair)
        if self.approach_type == "supervised":
            if target is None:
                raise ValueError('Target must not be None if approach_type is "supervised"')
            # Check size of the predictions and target
            check_size(predictions, target)
            check_size(target, X_fair)
            if isinstance(target, np.ndarray):
                target = pd.Series(target, name="target")
            self.target = convert_Int_series(target)
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
            self.return_prop_true = return_prop_true

            if self.model_type in ["regression", "classification", "multiclass"]:
                for i in self.metrics:
                    dict_feat = dict()
                    for z in self.fair_feat:
                        dict_to_use = {
                            k: v for k, v in self.__dict__.items() if k in inspect.signature(i).parameters.keys()
                        }
                        dict_labels = dict()
                        for j in self.X_fair[z].dropna().drop_duplicates().values:
                            if isinstance(j, List) or isinstance(j, np.ndarray):
                                j_str = ", ".join(map(str, j))
                                perc_label = (
                                    self.X_fair[z][(self.X_fair[z] == j).all(axis=1)].shape[0] / self.X_fair[z].shape[0]
                                )
                            else:
                                j_str = j
                                perc_label = self.X_fair[z][self.X_fair[z] == j].shape[0] / self.X_fair[z].shape[0]
                            dict_labels[j_str] = [
                                compute_metric_fairness(
                                    self.target,
                                    self.predictions,
                                    metric=i,
                                    fair_attr=self.X_fair[z],
                                    unpriv_group=j,
                                    **dict_to_use,
                                ),
                                perc_label,
                            ]
                            if self.model_type == "classification":
                                if self.return_prop_true:
                                    try:  # One Fairness Attribute
                                        dict_labels[j_str].append(
                                            (self.target[self.X_fair[z] == j] == 1).mean()
                                        )  # Add proportion of 1 label
                                    except Exception:  # More Fairness Attributes
                                        dict_labels[j_str].append(
                                            (self.target[(self.X_fair[z] == j).all(axis=1)] == 1).mean()
                                        )  # Add proportion of 1 label
                        if isinstance(z, List):
                            z_str = ", ".join(map(str, z))
                        else:
                            z_str = z
                        dict_feat[z_str] = dict_labels
                    perf_metrics[i.__name__] = dict_feat
            else:
                raise ValueError("Invalid model type.")
        # Unsupervised approach
        elif self.approach_type == "unsupervised":
            if self.target is not None:
                self.target = None
            if self.model_type == "clustering":
                vals = predictions.nunique()
                predictions = convert_cluster_labels(predictions, vals)
                if vals == 1:
                    warnings.warn("There is a single cluster")
                for i in self.metrics:
                    dict_feat = dict()
                    for z in self.fair_feat:
                        dict_to_use = {
                            k: v for k, v in self.__dict__.items() if k in inspect.signature(i).parameters.keys()
                        }

                        dict_labels = dict()
                        for j in self.X_fair[z].dropna().drop_duplicates().values:
                            if isinstance(j, List) or isinstance(j, np.ndarray):
                                j_str = ", ".join(map(str, j))
                                perc_label = (
                                    self.X_fair[z][(self.X_fair[z] == j).all(axis=1)].shape[0] / self.X_fair[z].shape[0]
                                )
                            else:
                                j_str = j
                                perc_label = self.X_fair[z][self.X_fair[z] == j].shape[0] / self.X_fair[z].shape[0]
                            dict_labels[j_str] = [
                                compute_metric_fairness(
                                    self.target,
                                    self.predictions,
                                    metric=i,
                                    fair_attr=self.X_fair[z],
                                    unpriv_group=j,
                                    **dict_to_use,
                                ),
                                perc_label,
                            ]
                        if isinstance(z, List):
                            z_str = ", ".join(map(str, z))
                        else:
                            z_str = z
                        dict_feat[z_str] = dict_labels
                    perf_metrics[i.__name__] = dict_feat
            else:
                raise ValueError("Invalid model type.")
        self.perf_metrics = perf_metrics
        return self.perf_metrics
