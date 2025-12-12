"""Classe utilizzata per monitorare e rilevare il drift nelle metriche di performance di un modello.

Questa classe offre strumenti per confrontare le metriche di performance correnti con le metriche storiche e generare un report di allarmi se si osservano drift significativi nelle performance in relazione a soglie predefinite.
"""

import pandas as pd
import numpy as np
from typing import Dict
import warnings

from model_monitoring.utils import check_metrics_sets

from model_monitoring.config import read_config

params = read_config(config_dir="config", name_params="params.yml")
standard_threshold = params["performance_threshold"]


class PerformancesDrift:
    """Classe utilizzata per monitorare e rilevare il Drift nelle metriche di performance di un modello.

    La classe supporta due tipi di input:

    * **"perf_metrics_curr"**: le metriche correnti di performance vengono fornite come dizionario contenente le performance per ogni metrica.

    * **"perf_metrics_historic"**: le metriche storiche di performance vengono fornite come dizionario contenente le performance storiche per ogni metrica.

    La classe verifica che le metriche correnti e storiche siano compatibili.

    Permette una configurazione flessibile dove è possibile definire le metriche da monitorare, le soglie di allarme e le logiche di analisi specifiche per ciascuna metrica, oppure una configurazione di default tramite un file interno `params.yml`.

    **Descrizione dei parametri di configurazione per metrica:**

            - `logic`: Specifica come interpretare il cambiamento della metrica ai fini del drift (vedi 'Logiche di Drift Configurabili' sotto).
            - `relative`: Contiene le soglie per il drift delle metriche di performance.

                - `red`/`yellow`: Soglie di variazione percentuale rispetto al valore storico.
            - `absolute`: Contiene le soglie assolute per le metriche di performance dei valori correnti.

                - `red`/`yellow`: Valori numerici che definiscono le soglie assolute per il valore corrente della metrica.

    **Funzionalità Principali:**

        *   Monitoraggio Assoluto: Confronta le performance correnti delle metriche con le soglie `absolute` impostate. Genera avvisi di tipo "red alert" o "yellow alert" se queste soglie vengono superate.
        *   Monitoraggio Relativo: Valuta l'evoluzione delle metriche confrontando le performance correnti con quelle storiche. Genera avvisi basati sulle soglie `relative` impostate.
        *   Logiche di Drift Configurabili (`logic`): Permette di definire come interpretare una variazione di performance ai fini del drift, in base alla natura della metrica:

            *   `"increase"`: Un *peggioramento* si verifica se la metrica *aumenta*
                (es. per metriche come il tasso di errore, dove un valore più basso è migliore).
            *   `"decrease"`: Un *peggioramento* si verifica se la metrica *diminuisce*
                (es. per metriche come l'accuratezza, dove un valore più alto è migliore).
        *   Reporting Dettagliato: Riassume tutte le analisi in un report `pd.DataFrame` completo che include le performance correnti per metrica, gli allarmi assoluti e relativi scattati, e i valori di drift delle metriche calcolati (con differenze percentuali).
    """

    def __init__(self, perf_metrics_curr, config_threshold=None):
        """Inizializza la classe `PerformancesDrift`, configurando le metriche di performance correnti e le soglie di monitoraggio per le metriche di performance.

        La classe valida i dati di input, gestisce la configurazione delle soglie, identifica le metriche di performance comuni tra quelle fornite e quelle configurate, e inizializza un `DataFrame` assegnandolo all'attributo `report` contenente le informazioni strutturali e i valori delle performance delle metriche correnti.

        Args:
            perf_metrics_curr (`dict`): Dizionario contenente le metriche correnti di performance. Ogni chiave rappresenta una metrica e ogni valore è un altro dizionario che contiene le performance.

            config_threshold (`dict`, opzionale): Dizionario contenente le soglie per ciascuna metrica di performance. Se non fornito, vengono usate le soglie predefinite presenti all'interno del file `params.yml`, così strutturato:

                * `logic`: Specifica come interpretare il cambiamento della metrica ai fini del drift (vedi 'Logiche di Drift Configurabili' in :class:`.PerformancesDrift`).
                * `relative`: Contiene le soglie per il drift delle metriche di performance.

                    * `red`/`yellow`: Soglie di variazione percentuale rispetto al valore storico.
                * `absolute`: Contiene le soglie assolute per le metriche di performance dei valori correnti.

                    * `red`/`yellow`: Valori numerici che definiscono le soglie assolute per il valore corrente della metrica.
                Default: `None`.
        """
        if not isinstance(perf_metrics_curr, Dict):
            raise ValueError(
                "Performance metrics in input has not a valid format. It should be a dictionary containing functions as keys and values as values."
            )
        if config_threshold is None:
            config_threshold = standard_threshold

        check_metrics = [
            i for i in perf_metrics_curr.keys() if (i not in config_threshold.keys()) and (i != "proportion_1")
        ]
        if len(check_metrics) > 0:
            warnings.warn(f"{check_metrics} do not have threshold settings in config_threshold")

        list_com_metrics = list(set(perf_metrics_curr.keys()).intersection(set(config_threshold.keys())))

        # initialize report
        report_df = (
            pd.DataFrame.from_dict({x: perf_metrics_curr[x] for x in list_com_metrics}, "index", columns=["curr_perf"])
            .reset_index()
            .rename(columns={"index": "metric"})
        )
        self.report = report_df
        # For binary classification we put proportion of 1 in report
        if "proportion_1" in perf_metrics_curr.keys():
            self.report.insert(1, "proportion_1_curr", perf_metrics_curr["proportion_1"])

        self.perf_metrics_curr = perf_metrics_curr
        self.config_threshold = config_threshold
        self.perf_metrics_stor = None

    def get_absolute(self):
        """Applica le soglie (predefinite o fornite) alle porformance delle metriche correnti.

        Questo metodo calcola lo stato di allarme ("red", "yellow") per ciascuna metrica di performance configurata, basandosi sul confronto tra il valore di performance **corrente** e le soglie **assolute** definite.

        Per ogni metrica di performance viene generata una colonna di warning `absolute_warning` nell'attributo `report`. Questa colonna contiene eventuali `warning` basati sul superamento o meno delle soglie di performance delle metriche.

        Args:
            None (metodo basato sulle metriche correnti e le soglie già impostate durante l'inizializzazione).

        Note:
            Il report aggiornato con queste colonne di allarme sarà quello restituito da successive chiamate a `get_report()`.
        """
        # Generation Alert
        for a in self.report.metric.values:
            absolute_red = self.config_threshold[a]["absolute"]["red"]
            absolute_yellow = self.config_threshold[a]["absolute"]["yellow"]
            curr_perf = self.report.loc[self.report.metric == a, "curr_perf"].values[0]
            if self.config_threshold[a]["logic"] == "decrease":
                if absolute_red != "None":
                    if curr_perf <= absolute_red:
                        self.report.loc[self.report.metric == a, "absolute_warning"] = "Red Alert"
                    else:
                        if absolute_yellow != "None":
                            if (curr_perf > absolute_red) and (curr_perf <= absolute_yellow):
                                self.report.loc[self.report.metric == a, "absolute_warning"] = "Yellow Alert"
                            else:
                                self.report.loc[self.report.metric == a, "absolute_warning"] = np.nan
                        else:
                            self.report.loc[self.report.metric == a, "absolute_warning"] = np.nan
                else:
                    if absolute_yellow != "None":
                        if curr_perf <= absolute_yellow:
                            self.report.loc[self.report.metric == a, "absolute_warning"] = "Yellow Alert"
                        else:
                            self.report.loc[self.report.metric == a, "absolute_warning"] = np.nan
                    else:
                        self.report.loc[self.report.metric == a, "absolute_warning"] = np.nan
            elif self.config_threshold[a]["logic"] == "increase":
                if absolute_red != "None":
                    if curr_perf >= absolute_red:
                        self.report.loc[self.report.metric == a, "absolute_warning"] = "Red Alert"
                    else:
                        if absolute_yellow != "None":
                            if (curr_perf < absolute_red) and (curr_perf >= absolute_yellow):
                                self.report.loc[self.report.metric == a, "absolute_warning"] = "Yellow Alert"
                            else:
                                self.report.loc[self.report.metric == a, "absolute_warning"] = np.nan
                        else:
                            self.report.loc[self.report.metric == a, "absolute_warning"] = np.nan
                else:
                    if absolute_yellow != "None":
                        if curr_perf >= absolute_yellow:
                            self.report.loc[self.report.metric == a, "absolute_warning"] = "Yellow Alert"
                        else:
                            self.report.loc[self.report.metric == a, "absolute_warning"] = np.nan
                    else:
                        self.report.loc[self.report.metric == a, "absolute_warning"] = np.nan
            else:
                raise ValueError(
                    f"{self.config_threshold[a]['logic']} is not a valid logic for {a} metric. Choose between ['increase','decrease']."
                )
        # Locate Absolute_warning after Curr_perf
        absolute_warning = self.report.pop("absolute_warning")
        self.report.insert(self.report.columns.get_loc("curr_perf") + 1, "absolute_warning", absolute_warning)

    def get_relative(self, perf_metrics_stor):
        """Calcola il drift delle metriche di performance correnti rispetto alle metriche storiche.

        Il drift delle metriche viene calcolato confrontando le performance correnti con quelle storiche per ciascuna metrica, calcolando la differenza percentuale tra i due valori. Se la differenza supera una certa soglia, viene generato un `warning`.

        Il metodo genera nell'attributo `report`:

            * La colonna di warning `relative_warning` per le metriche di performance.
            * La colonna delle performance delle metriche relative ai dati storici.
            * La colonna relative al drift percentuale tra le performance delle metriche correnti e quelle storiche.

        Args:
            perf_metrics_stor (dict): Dizionario contenente le metriche storiche di performance per il confronto relativo. Ogni chiave rappresenta una metrica e ogni valore è un altro dizionario che contiene le performance storiche.

        Note:
            Se le metriche correnti e storiche non sono compatibili, viene sollevato un `warning`.
        """
        # Check if the metrics are the same
        check_metrics_sets(metrics_1=perf_metrics_stor, metrics_2=self.perf_metrics_curr)

        list_com_metrics = [
            x
            for x in list(set(perf_metrics_stor.keys()).intersection(set(self.perf_metrics_curr.keys())))
            if x != "proportion_1"
        ]
        self.perf_metrics_stor = {x: perf_metrics_stor[x] for x in list_com_metrics}
        stor_perf_df = (
            pd.DataFrame.from_dict(self.perf_metrics_stor, "index", columns=["stor_perf"])
            .reset_index()
            .rename(columns={"index": "metric"})
        )
        # For binary classification we put proportion of 1 in report
        if "proportion_1" in perf_metrics_stor.keys():
            stor_perf_df.insert(1, "proportion_1_stor", perf_metrics_stor["proportion_1"])

        if "stor_perf" in self.report.columns:
            self.report.loc[:, "stor_perf"] = stor_perf_df.stor_perf
            if "proportion_1_stor" in stor_perf_df:
                self.report.loc[:, "proportion_1_stor"] = stor_perf_df.proportion_1_stor
        else:
            self.report = self.report.merge(stor_perf_df, how="outer", on="metric")

        # Generation Drift
        for a in self.report.metric.values:
            stor_perf = self.report.loc[self.report.metric == a, "stor_perf"].values[0]
            curr_perf = self.report.loc[self.report.metric == a, "curr_perf"].values[0]
            if self.config_threshold[a]["logic"] in ["decrease", "increase"]:
                if stor_perf > 0:
                    self.report.loc[self.report.metric == a, "drift_perc"] = (curr_perf - stor_perf) / stor_perf * 100
                else:
                    self.report.loc[self.report.metric == a, "drift_perc"] = (stor_perf - curr_perf) / stor_perf * 100
            else:
                raise ValueError(
                    f"{self.config_threshold[a]['logic']} is not a valid logic for {a} metric. Choose between ['increase','decrease']."
                )

        # Generation Alert
        for a in self.report.metric.values:
            relative_red = self.config_threshold[a]["relative"]["red"]
            relative_yellow = self.config_threshold[a]["relative"]["yellow"]
            drift_perf = self.report.loc[self.report.metric == a, "drift_perc"].values[0]
            if self.config_threshold[a]["logic"] == "decrease":
                if relative_red != "None":
                    if drift_perf <= relative_red * 100:
                        self.report.loc[self.report.metric == a, "relative_warning"] = "Red Alert"
                    else:
                        if relative_yellow != "None":
                            if (drift_perf > relative_red * 100) and (drift_perf <= relative_yellow * 100):
                                self.report.loc[self.report.metric == a, "relative_warning"] = "Yellow Alert"
                            else:
                                self.report.loc[self.report.metric == a, "relative_warning"] = np.nan
                        else:
                            self.report.loc[self.report.metric == a, "relative_warning"] = np.nan
                else:
                    if relative_yellow != "None":
                        if drift_perf <= relative_yellow * 100:
                            self.report.loc[self.report.metric == a, "relative_warning"] = "Yellow Alert"
                        else:
                            self.report.loc[self.report.metric == a, "relative_warning"] = np.nan
                    else:
                        self.report.loc[self.report.metric == a, "relative_warning"] = np.nan
            elif self.config_threshold[a]["logic"] == "increase":
                if relative_red != "None":
                    if drift_perf >= relative_red * 100:
                        self.report.loc[self.report.metric == a, "relative_warning"] = "Red Alert"
                    else:
                        if relative_yellow != "None":
                            if (drift_perf < relative_red * 100) and (drift_perf >= relative_yellow * 100):
                                self.report.loc[self.report.metric == a, "relative_warning"] = "Yellow Alert"
                            else:
                                self.report.loc[self.report.metric == a, "relative_warning"] = np.nan
                        else:
                            self.report.loc[self.report.metric == a, "relative_warning"] = np.nan
                else:
                    if relative_yellow != "None":
                        if drift_perf >= relative_yellow * 100:
                            self.report.loc[self.report.metric == a, "relative_warning"] = "Yellow Alert"
                        else:
                            self.report.loc[self.report.metric == a, "relative_warning"] = np.nan
                    else:
                        self.report.loc[self.report.metric == a, "relative_warning"] = np.nan
            else:
                raise ValueError(
                    f"{self.config_threshold[a]['logic']} is not a valid logic for {a} metric. Choose between ['increase','decrease']."
                )

    def get_report(self):
        """Restituisce un report comprensivo dei risultati del drift delle metriche di performance con warning assoluti e relativi.

        Args:
            None (metodo basato sulle metriche correnti e le soglie già impostate durante l'inizializzazione ed eventualmente le metriche storiche).

        Returns:
            `pd.DataFrame`: Restituisce il report con le metriche di performance

        Note:
            * Se lanciato dopo `get_absolute()` conterrà anche i `warning` assoluti sulle performance delle metriche correnti.
            * Se lanciato dopo `get_relative()` conterrà anche i `warning` relativi al drift sulle performance delle metriche correnti rispetto a quelle storiche.
            * Se l'attributo `return_prop_true` dell'`__init__` della classe **PerformancesMeasures** è `True` il dizionario delle metriche di performance conterrà anche la percentuale di 1 (veri positivi) in un contesto di classificazione binaria, e di conseguenza il report conterrà anche la colonna `proportion_1_curr`, e `proportion_1_stor` se chiamato dopo `get_relative()`.

        **Dati utilizzati per gli esempi**

        >>> df_esempio_corr

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

        >>> df_esempio_stor

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature_num</th>      <th>feature_cat</th>      <th>target_clf</th>      <th>pred_clf</th>      <th>target_reg</th>      <th>pred_reg</th>      <th>prob_clf</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>1</td>      <td>A</td>      <td>0</td>      <td>0</td>      <td>-1.131079</td>      <td>13.795709</td>      <td>0.041599</td>    </tr>    <tr>      <th>1</th>      <td>2</td>      <td>B</td>      <td>1</td>      <td>1</td>      <td>5.259965</td>      <td>12.331217</td>      <td>0.063112</td>    </tr>    <tr>      <th>2</th>      <td>3</td>      <td>A</td>      <td>0</td>      <td>0</td>      <td>12.151730</td>      <td>-6.433172</td>      <td>0.161446</td>    </tr>    <tr>      <th>3</th>      <td>4</td>      <td>C</td>      <td>0</td>      <td>0</td>      <td>15.114249</td>      <td>1.408011</td>      <td>0.321464</td>    </tr>    <tr>      <th>4</th>      <td>5</td>      <td>B</td>      <td>0</td>      <td>1</td>      <td>21.146841</td>      <td>17.845778</td>      <td>0.999736</td>    </tr>    <tr>      <th>5</th>      <td>6</td>      <td>A</td>      <td>1</td>      <td>1</td>      <td>29.831444</td>      <td>14.678544</td>      <td>0.140501</td>    </tr>    <tr>      <th>6</th>      <td>7</td>      <td>C</td>      <td>1</td>      <td>0</td>      <td>29.835704</td>      <td>41.836306</td>      <td>0.791112</td>    </tr>    <tr>      <th>7</th>      <td>8</td>      <td>A</td>      <td>1</td>      <td>0</td>      <td>45.712137</td>      <td>27.485945</td>      <td>0.936301</td>    </tr>    <tr>      <th>8</th>      <td>9</td>      <td>B</td>      <td>1</td>      <td>0</td>      <td>41.951110</td>      <td>44.644955</td>      <td>0.894670</td>    </tr>    <tr>      <th>9</th>      <td>10</td>      <td>C</td>      <td>1</td>      <td>0</td>      <td>57.347082</td>      <td>52.882838</td>      <td>0.109044</td>    </tr>  </tbody></table>

        **Esempio 1:**

        >>> Perf_Meas = PerformancesMeasures(model_type="classification", set_metrics="add",new_metrics={lift_score:"prob"})
        >>> new_perf = Perf_Meas.compute_metrics(target=df_esempio_corr['target_clf'], predictions=df_esempio_corr['pred_clf'], prob=df_esempio_corr['prob_clf'])
        >>> new_perf
        {'balanced_accuracy_score': 0.21428571428571427,
         'accuracy_score': 0.3,
         'precision_score': 0.0,
         'recall_score': 0.0,
         'f1_score': 0.0,
         'roc_auc_score': 0.1904761904761905,
         'lift_score': 0.0,
         'proportion_1': 0.3}
        >>> old_perf = Perf_Meas.compute_metrics(target=df_esempio_stor['target_clf'], predictions=df_esempio_stor['pred_clf'], prob=df_esempio_stor['prob_clf'])
        >>> old_perf
        {'balanced_accuracy_score': 0.5416666666666666,
         'accuracy_score': 0.5,
         'precision_score': 0.6666666666666666,
         'recall_score': 0.3333333333333333,
         'f1_score': 0.4444444444444444,
         'roc_auc_score': 0.5,
         'lift_score': 0.8333333333333334,
         'proportion_1': 0.6}
        >>> from model_monitoring.model_performance import PerformancesDrift
        >>> Perf_Drift = PerformancesDrift(new_perf)
        >>> Perf_Drift.get_report()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>metric</th>      <th>proportion_1_curr</th>      <th>curr_perf</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>f1_score</td>      <td>0.3</td>      <td>0.000000</td>    </tr>    <tr>      <th>1</th>      <td>recall_score</td>      <td>0.3</td>      <td>0.000000</td>    </tr>    <tr>      <th>2</th>      <td>accuracy_score</td>      <td>0.3</td>      <td>0.300000</td>    </tr>    <tr>      <th>3</th>      <td>lift_score</td>      <td>0.3</td>      <td>0.000000</td>    </tr>    <tr>      <th>4</th>      <td>precision_score</td>      <td>0.3</td>      <td>0.000000</td>    </tr>    <tr>      <th>5</th>      <td>roc_auc_score</td>      <td>0.3</td>      <td>0.190476</td>    </tr>    <tr>      <th>6</th>      <td>balanced_accuracy_score</td>      <td>0.3</td>      <td>0.214286</td>    </tr>  </tbody></table>

        **Esempio 2: Uso con get_absolute**

        >>> Perf__Drift.get_absolute()
        >>> Perf__Drift.get_report()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>metric</th>      <th>proportion_1_curr</th>      <th>curr_perf</th>      <th>absolute_warning</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>f1_score</td>      <td>0.3</td>      <td>0.000000</td>      <td>NaN</td>    </tr>    <tr>      <th>1</th>      <td>recall_score</td>      <td>0.3</td>      <td>0.000000</td>      <td>NaN</td>    </tr>    <tr>      <th>2</th>      <td>accuracy_score</td>      <td>0.3</td>      <td>0.300000</td>      <td>NaN</td>    </tr>    <tr>      <th>3</th>      <td>lift_score</td>      <td>0.3</td>      <td>0.000000</td>      <td>Red Alert</td>    </tr>    <tr>      <th>4</th>      <td>precision_score</td>      <td>0.3</td>      <td>0.000000</td>      <td>NaN</td>    </tr>    <tr>      <th>5</th>      <td>roc_auc_score</td>      <td>0.3</td>      <td>0.190476</td>      <td>Red Alert</td>    </tr>    <tr>      <th>6</th>      <td>balanced_accuracy_score</td>      <td>0.3</td>      <td>0.214286</td>      <td>Red Alert</td>    </tr>  </tbody></table>

        **Esempio 3: Uso con get_relative**

        >>> Perf__Drift.get_relative()
        >>> Perf__Drift.get_report()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>metric</th>      <th>proportion_1_curr</th>      <th>curr_perf</th>      <th>absolute_warning</th>      <th>proportion_1_stor</th>      <th>stor_perf</th>      <th>drift_perc</th>      <th>relative_warning</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>f1_score</td>      <td>0.3</td>      <td>0.000000</td>      <td>NaN</td>      <td>0.6</td>      <td>0.444444</td>      <td>-100.000000</td>      <td>Red Alert</td>    </tr>    <tr>      <th>1</th>      <td>recall_score</td>      <td>0.3</td>      <td>0.000000</td>      <td>NaN</td>      <td>0.6</td>      <td>0.333333</td>      <td>-100.000000</td>      <td>Red Alert</td>    </tr>    <tr>      <th>2</th>      <td>accuracy_score</td>      <td>0.3</td>      <td>0.300000</td>      <td>NaN</td>      <td>0.6</td>      <td>0.500000</td>      <td>-40.000000</td>      <td>Yellow Alert</td>    </tr>    <tr>      <th>3</th>      <td>lift_score</td>      <td>0.3</td>      <td>0.000000</td>      <td>Red Alert</td>      <td>0.6</td>      <td>0.833333</td>      <td>-100.000000</td>      <td>Red Alert</td>    </tr>    <tr>      <th>4</th>      <td>precision_score</td>      <td>0.3</td>      <td>0.000000</td>      <td>NaN</td>      <td>0.6</td>      <td>0.666667</td>      <td>-100.000000</td>      <td>Red Alert</td>    </tr>    <tr>      <th>5</th>      <td>roc_auc_score</td>      <td>0.3</td>      <td>0.190476</td>      <td>Red Alert</td>      <td>0.6</td>      <td>0.500000</td>      <td>-61.904762</td>      <td>Red Alert</td>    </tr>    <tr>      <th>6</th>      <td>balanced_accuracy_score</td>      <td>0.3</td>      <td>0.214286</td>      <td>Red Alert</td>      <td>0.6</td>      <td>0.541667</td>      <td>-60.439560</td>      <td>Red Alert</td>    </tr>  </tbody></table>

        """
        return self.report
