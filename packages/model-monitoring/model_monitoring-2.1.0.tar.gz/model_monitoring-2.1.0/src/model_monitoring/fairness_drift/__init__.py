"""Classe utilizzata per monitorare e rilevare il drift nelle metriche di fairness di un modello.

Questa classe offre strumenti per confrontare le metriche di fairness correnti con le metriche storiche e generare un report di allarmi se si osservano drift significativi nelle performance in relazione a soglie predefinite.
"""

import pandas as pd
import warnings
from typing import Dict

from model_monitoring.utils import check_metrics_sets
from model_monitoring.config import read_config

from model_monitoring.fairness_drift.fairness_drift import (
    check_fairness_groups,
)

params = read_config(config_dir="config", name_params="params.yml")
standard_threshold = params["fairness_treshold"]


class FairnessDrift:
    """Classe utilizzata per monitorare e rilevare il Drift nelle metriche di fairness di un modello.

    La classe supporta due tipi di input:

    * **"curr_metrics"**: le metriche correnti di fairness vengono fornite come dizionario contenente le performance per ogni metrica e gruppo.

    * **"historic_metrics"**: le metriche storiche di fairness vengono fornite come dizionario contenente le performance storiche per ogni metrica e gruppo.

    La classe verifica che le metriche correnti e storiche siano compatibili e abbiano gli stessi gruppi di fairness.

    Permette una configurazione flessibile dove è possibile definire le metriche da monitorare, le soglie di allarme e le logiche di analisi specifiche per ciascuna metrica, oppure una configurazione di default tramite un file interno `params.yml`.

    **Descrizione dei parametri di configurazione per metrica:**

            - `logic`: Specifica come interpretare il cambiamento della metrica ai fini del drift (vedi 'Logiche di Drift Configurabili' sotto).
            - `axial_point`: Il punto di riferimento numerico usato solo quando `logic` è impostato su 'axial'.
            - `relative`: Contiene le soglie per il drift delle metriche di fairness.

                - `red`/`yellow`: Soglie di variazione percentuale rispetto al valore storico.
                - `absolute_tol`: Valore di tolleranza assoluta utilizzato per prevenire che valori molto piccoli possano causare drift apparentemente grandi nelle metriche.
            - `absolute`: Contiene le soglie assolute per le performance delle metriche di fairness dei valori correnti.

                - `red`/`yellow`: Valori numerici o intervalli (liste di due float `[min, max]`) che definiscono le soglie assolute per il valore corrente della metrica.

    **Funzionalità Principali:**

        *   Monitoraggio Assoluto: Confronta le performance correnti delle metriche con le soglie `absolute` impostate. Genera avvisi di tipo "red alert" o "yellow alert" se queste soglie vengono superate.
        *   Monitoraggio Relativo: Valuta l'evoluzione delle metriche confrontando le performance correnti con quelle storiche. Genera avvisi basati sulle soglie `relative` impostate.
        *   Logiche di Drift Configurabili (`logic`): Permette di definire come interpretare una variazione di performance ai fini del drift, in base alla natura della metrica:

            *   `"increase"`: Un *peggioramento* si verifica se la metrica *aumenta*
                (es. per metriche come il tasso di errore, dove un valore più basso è migliore).
            *   `"decrease"`: Un *peggioramento* si verifica se la metrica *diminuisce*
                (es. per metriche come l'accuratezza, dove un valore più alto è migliore).
            *   `"axial"`: Il drift viene valutato in base alla *deviazione* (in
                entrambe le direzioni) dal valore `axial_point` definito.
        *   Reporting Dettagliato: Riassume tutte le analisi in un report `pd.DataFrame` completo che include le performance correnti per metrica e gruppo, gli allarmi assoluti e relativi scattati, e i valori di drift delle metriche calcolati (con differenze percentuali).
    """

    def __init__(self, fair_metrics_curr, config_threshold=None):
        """Inizializza la classe `FairnessDrift`, configurando le metriche di fairness correnti e le soglie di monitoraggio per le metriche di fairness.

        La classe valida i dati di input, gestisce la configurazione delle soglie, identifica le metriche di fairness comuni tra quelle fornite e quelle configurate, e inizializza un `DataFrame` assegnandolo all'attributo `report_reduced` contenente le informazioni strutturali (variabili, gruppi) e i valori delle performance correnti per le metriche di fairness.

        Args:
            fair_metrics_curr (`dict`): Dizionario contenente le metriche correnti di fairness. Ogni chiave rappresenta una metrica e ogni valore è un altro dizionario che contiene le performance per ciascun gruppo di fairness.

            config_threshold (`dict`, opzionale): Dizionario contenente le soglie per ciascuna metrica di fairness. Se non fornito, vengono usate le soglie predefinite presenti all'interno del file `params.yml`, così strutturato:

                * `logic`: Specifica come interpretare il cambiamento della metrica ai fini del drift (vedi 'Logiche di Drift Configurabili' in :class:`.FairnessDrift`).
                * `axial_point`: Il punto di riferimento numerico usato solo quando `logic` è impostato su 'axial'.
                * `relative`: Contiene le soglie per il drift delle metriche di fairness.

                    * `red`/`yellow`: Soglie di variazione percentuale rispetto al valore storico.
                    * `absolute_tol`: Valore di tolleranza assoluta utilizzato per prevenire che valori molto piccoli possano causare drift apparentemente grandi nelle metriche.
                * `absolute`: Contiene le soglie assolute per le performance delle metriche di fairness dei valori correnti.

                    * `red`/`yellow`: Valori numerici o intervalli (liste di due float `[min, max]`) che definiscono le soglie assolute per il valore corrente della metrica.
                Default: `None`.
        """
        if not isinstance(fair_metrics_curr, Dict):
            raise ValueError(
                "Fairness metrics in input has not a valid format. It should be a dictionary containing functions as keys and values as values."
            )
        if config_threshold is None:
            config_threshold = standard_threshold

        check_metrics = [
            i for i in fair_metrics_curr.keys() if (i not in config_threshold.keys()) and (i != "proportion_1")
        ]
        if len(check_metrics) > 0:
            warnings.warn(f"{check_metrics} do not have threshold settings in config_threshold")

        list_com_metrics = list(set(fair_metrics_curr.keys()).intersection(set(config_threshold.keys())))
        fair_metrics_curr_com = {x: fair_metrics_curr[x] for x in list_com_metrics}

        # initialize reduced report with variables and groups
        self.report_reduced = pd.DataFrame(
            [
                {"vars": key, "groups": group, "curr_perc_label": values[1]}
                if len(values) == 2
                else {"vars": key, "groups": group, "curr_perc_label": values[1], "proportion_1_curr": values[2]}
                for key, groups in fair_metrics_curr_com[list(fair_metrics_curr_com.keys())[0]].items()
                for group, values in groups.items()
            ]
        )
        for x in fair_metrics_curr_com.keys():
            self.report_reduced[x + "_curr_perf"] = [
                values[0] for key, groups in fair_metrics_curr_com[x].items() for group, values in groups.items()
            ]
        # for output report columns ordering according to current percentage label
        self.report_reduced = self.report_reduced.sort_values(by=["vars", "curr_perc_label"], ascending=[True, False])

        self.fair_metrics_curr = fair_metrics_curr
        self.config_threshold = config_threshold
        self.perf_metrics_stor = None
        self.relative_reduced = False

    def get_absolute_reduced(self):
        """Applica le soglie (predefinite o fornite) alle porformance delle metriche di fairness correnti.

        Questo metodo calcola lo stato di allarme ("red", "yellow") per ciascuna metrica di fairness configurata, basandosi sul confronto tra il valore di performance **corrente** e le soglie **assolute** definite.

        Per ogni metrica e per ogni gruppo di fairness viene generata una colonna di warning `absolute_warning` nell'attributo `report_reduced`. Questa colonna contiene eventuali `warning` basati sul superamento o meno delle soglie di performance delle metriche di fairness.

        Args:
            None (metodo basato sulle metriche correnti e le soglie già impostate durante l'inizializzazione).

        Note:
            Il report aggiornato con queste colonne di allarme sarà quello restituito da successive chiamate a `get_report_reduced()`.
        """
        # Generation Alert
        for x in self.report_reduced.groups.values:
            warning_red = ""
            warning_yellow = ""
            for a in [y[:-10] for y in self.report_reduced.columns if "curr_perf" in y]:
                absolute_red = self.config_threshold[a]["absolute"]["red"]
                absolute_yellow = self.config_threshold[a]["absolute"]["yellow"]

                if self.config_threshold[a]["logic"] == "decrease":
                    curr_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_curr_perf"].values[0]
                    if absolute_red != "None":
                        if curr_perf <= absolute_red:
                            if warning_red == "":
                                warning_red += f"Red Alert for {a}"
                            else:
                                warning_red += f", {a}"
                        else:
                            if absolute_yellow != "None":
                                if (curr_perf > absolute_red) and (curr_perf <= absolute_yellow):
                                    if warning_yellow == "":
                                        warning_yellow += f"Yellow Alert for {a}"
                                    else:
                                        warning_yellow += f", {a}"
                    else:
                        if absolute_yellow != "None":
                            if curr_perf <= absolute_yellow:
                                if warning_yellow == "":
                                    warning_yellow += f"Yellow Alert for {a}"
                                else:
                                    warning_yellow += f", {a}"

                elif self.config_threshold[a]["logic"] == "increase":
                    curr_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_curr_perf"].values[0]
                    if absolute_red != "None":
                        if curr_perf >= absolute_red:
                            if warning_red == "":
                                warning_red += f"Red Alert for {a}"
                            else:
                                warning_red += f", {a}"
                        else:
                            if absolute_yellow != "None":
                                if (curr_perf < absolute_red) and (curr_perf >= absolute_yellow):
                                    if warning_yellow == "":
                                        warning_yellow += f"Yellow Alert for {a}"
                                    else:
                                        warning_yellow += f", {a}"
                    else:
                        if absolute_yellow != "None":
                            if curr_perf >= absolute_yellow:
                                if warning_yellow == "":
                                    warning_yellow += f"Yellow Alert for {a}"
                                else:
                                    warning_yellow += f", {a}"

                elif self.config_threshold[a]["logic"] == "axial":
                    curr_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_curr_perf"].values[0]
                    if absolute_red != "None":
                        if (curr_perf >= max(absolute_red)) or (curr_perf <= min(absolute_red)):
                            if warning_red == "":
                                warning_red += f"Red Alert for {a}"
                            else:
                                warning_red += f", {a}"
                        else:
                            if absolute_yellow != "None":
                                if ((curr_perf < max(absolute_red)) and (curr_perf > min(absolute_red))) and (
                                    (curr_perf >= max(absolute_yellow)) or (curr_perf <= min(absolute_yellow))
                                ):
                                    if warning_yellow == "":
                                        warning_yellow += f"Yellow Alert for {a}"
                                    else:
                                        warning_yellow += f", {a}"
                    else:
                        if absolute_yellow != "None":
                            if (curr_perf >= max(absolute_yellow)) or (curr_perf <= min(absolute_yellow)):
                                if warning_yellow == "":
                                    warning_yellow += f"Yellow Alert for {a}"
                                else:
                                    warning_yellow += f", {a}"
                else:
                    raise ValueError(
                        f"{self.config_threshold[a]['logic']} is not a valid logic for {a} metric. Choose between ['increase','decrease','axial']."
                    )
            if (warning_red != "") and (warning_yellow != ""):
                warning = warning_red + ", " + warning_yellow
            else:
                warning = warning_red + warning_yellow
            self.report_reduced.loc[self.report_reduced.groups == x, "absolute_warning"] = warning

        # Locate Absolute_warning before Stor_Perc_label
        if self.relative_reduced:
            absolute_warning = self.report_reduced.pop("absolute_warning")

            self.report_reduced.insert(
                self.report_reduced.columns.get_loc("stor_perc_label"), "absolute_warning", absolute_warning
            )

    def get_relative_reduced(self, fair_metrics_stor):
        """Calcola il drift delle metriche di fairness correnti rispetto alle metriche storiche.

        Il drift delle metriche viene calcolato confrontando le performance correnti con quelle storiche per ciascuna metrica di fairness, calcolando la differenza percentuale tra i due valori. Se la differenza supera una certa soglia, viene generato un `warning`.

        Per ogni gruppo di fairness il metodo genera nell'attributo `report_reduced`:

            * Una colonna di warning `relative_warning` per le metriche di fairness.
            * Le colonne delle performance delle metriche di fairness relative ai dati storici.
            * Le colonne relative al drift percentuale tra le performance delle metriche di fairness correnti e quelle storiche.

        Args:
            fair_metrics_stor (dict): Dizionario contenente le metriche storiche di fairness per il confronto relativo. Ogni chiave rappresenta una metrica e ogni valore è un altro dizionario che contiene le performance storiche per ciascun gruppo di fairness.

        Note:
            Se le metriche correnti e storiche non sono compatibili, viene sollevato un `warning`.
        """
        # re-initialize report
        if self.relative_reduced:
            list_drop = [
                x
                for x in self.report_reduced.columns
                if (x in ["stor_perc_label", "drift_perc", "relative_warning", "proportion_1_stor"])
                or ("stor_perf" in x)
            ]
            self.report_reduced = self.report_reduced.drop(columns=list_drop)

        # Check if the metrics are the same
        check_metrics_sets(metrics_1=fair_metrics_stor, metrics_2=self.fair_metrics_curr)

        list_com_metrics = list(set(fair_metrics_stor.keys()).intersection(set(self.fair_metrics_curr.keys())))
        self.fair_metrics_stor = {x: fair_metrics_stor[x] for x in list_com_metrics}
        stor_report_reduced = pd.DataFrame(
            [
                {"vars": key, "groups": group, "stor_perc_label": values[1]}
                if len(values) == 2
                else {"vars": key, "groups": group, "stor_perc_label": values[1], "proportion_1_stor": values[2]}
                for key, groups in self.fair_metrics_stor[list(self.fair_metrics_stor.keys())[0]].items()
                for group, values in groups.items()
            ]
        )
        for x in self.fair_metrics_stor.keys():
            stor_report_reduced[x + "_stor_perf"] = [
                values[0] for key, groups in self.fair_metrics_stor[x].items() for group, values in groups.items()
            ]

        # Check if the fairness group are the same
        list_no_join = check_fairness_groups(self.report_reduced, stor_report_reduced, multiindex=False)

        # Add historical fairness performances to the reduced report and limit to common fairness groups
        self.report_reduced = self.report_reduced.merge(stor_report_reduced, how="inner", on=["vars", "groups"])

        # Generation Drift
        for a in [y[:-10] for y in self.report_reduced.columns if "stor_perf" in y]:
            if self.config_threshold[a]["logic"] in ["decrease", "increase"]:
                for x in self.report_reduced.groups.values:
                    stor_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_stor_perf"].values[0]
                    curr_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_curr_perf"].values[0]
                    if stor_perf > 0:
                        self.report_reduced.loc[self.report_reduced.groups == x, "drift_perc_" + a] = (
                            (curr_perf - stor_perf) / stor_perf * 100
                        )
                    else:
                        self.report_reduced.loc[self.report_reduced.groups == x, "drift_perc_" + a] = (
                            (stor_perf - curr_perf) / stor_perf * 100
                        )
                drift = self.report_reduced.pop("drift_perc_" + a)
                self.report_reduced.insert(
                    self.report_reduced.columns.get_loc(a + "_stor_perf") + 1, "drift_perc_" + a, drift
                )

            elif self.config_threshold[a]["logic"] == "axial":
                axial_point = self.config_threshold[a]["axial_point"]
                for x in self.report_reduced.groups.values:
                    stor_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_stor_perf"].values[0]
                    curr_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_curr_perf"].values[0]
                    self.report_reduced.loc[self.report_reduced.groups == x, "drift_perc_" + a] = (
                        (abs(curr_perf - axial_point) - abs(stor_perf - axial_point))
                        / abs(stor_perf - axial_point)
                        * 100
                    )
                drift = self.report_reduced.pop("drift_perc_" + a)
                self.report_reduced.insert(
                    self.report_reduced.columns.get_loc(a + "_stor_perf") + 1, "drift_perc_" + a, drift
                )

            else:
                raise ValueError(
                    f"{self.config_threshold[a]['logic']} is not a valid logic for {a} metric. Choose between ['increase','decrease','axial']."
                )

        # Generation Alert
        for x in self.report_reduced.groups.values:
            warning_red = ""
            warning_yellow = ""
            for a in [y[:-10] for y in self.report_reduced.columns if "curr_perf" in y]:
                relative_red = self.config_threshold[a]["relative"]["red"]
                relative_yellow = self.config_threshold[a]["relative"]["yellow"]
                absolute_tol = self.config_threshold[a]["relative"]["absolute_tol"]

                if self.config_threshold[a]["logic"] == "decrease":
                    curr_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_curr_perf"].values[0]
                    stor_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_stor_perf"].values[0]
                    if relative_red != "None":
                        # check absolute tollerance for relative alert
                        if abs(curr_perf - stor_perf) >= absolute_tol:
                            drift_perf = self.report_reduced.loc[
                                self.report_reduced.groups == x, "drift_perc_" + a
                            ].values[0]
                            if drift_perf <= relative_red * 100:
                                if warning_red == "":
                                    warning_red += f"Red Alert for {a}"
                                else:
                                    warning_red += f", {a}"
                            else:
                                if relative_yellow != "None":
                                    if (drift_perf > relative_red * 100) and (drift_perf <= relative_yellow * 100):
                                        if warning_yellow == "":
                                            warning_yellow += f"Yellow Alert for {a}"
                                        else:
                                            warning_yellow += f", {a}"
                    else:
                        if relative_yellow != "None":
                            # check absolute tollerance for relative alert
                            if abs(curr_perf - stor_perf) >= absolute_tol:
                                drift_perf = self.report_reduced.loc[
                                    self.report_reduced.groups == x, "drift_perc_" + a
                                ].values[0]
                                if drift_perf <= relative_yellow * 100:
                                    if warning_yellow == "":
                                        warning_yellow += f"Yellow Alert for {a}"
                                    else:
                                        warning_yellow += f", {a}"

                elif self.config_threshold[a]["logic"] in ["increase", "axial"]:
                    curr_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_curr_perf"].values[0]
                    stor_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_stor_perf"].values[0]
                    if relative_red != "None":
                        # check absolute tollerance for relative alert
                        if abs(curr_perf - stor_perf) >= absolute_tol:
                            drift_perf = self.report_reduced.loc[
                                self.report_reduced.groups == x, "drift_perc_" + a
                            ].values[0]
                            if drift_perf >= relative_red * 100:
                                if warning_red == "":
                                    warning_red += f"Red Alert for {a}"
                                else:
                                    warning_red += f", {a}"
                            else:
                                if relative_yellow != "None":
                                    if (drift_perf < relative_red * 100) and (drift_perf >= relative_yellow * 100):
                                        if warning_yellow == "":
                                            warning_yellow += f"Yellow Alert for {a}"
                                        else:
                                            warning_yellow += f", {a}"
                    else:
                        if relative_yellow != "None":
                            # check absolute tollerance for relative alert
                            if abs(curr_perf - stor_perf) >= absolute_tol:
                                drift_perf = self.report_reduced.loc[
                                    self.report_reduced.groups == x, "drift_perc_" + a
                                ].values[0]
                                if drift_perf >= relative_yellow * 100:
                                    if warning_yellow == "":
                                        warning_yellow += f"Yellow Alert for {a}"
                                    else:
                                        warning_yellow += f", {a}"

                else:
                    raise ValueError(
                        f"{self.config_threshold[a]['logic']} is not a valid logic for {a} metric. Choose between ['increase','decrease','axial']."
                    )
            if (warning_red != "") and (warning_yellow != ""):
                warning = warning_red + ", " + warning_yellow
            else:
                warning = warning_red + warning_yellow
            self.report_reduced.loc[self.report_reduced.groups == x, "relative_warning"] = warning

        self.relative_reduced = True

    def get_report_reduced(self):
        """Restituisce un report comprensivo dei risultati del drift delle metriche di fairness con warning assoluti e relativi.

        Args:
            None (metodo basato sulle metriche correnti e le soglie già impostate durante l'inizializzazione ed eventualmente le metriche storiche).

        Returns:
            `pd.DataFrame`: Restituisce il report con le metriche e i gruppi di fairness

        Note:
            * Se lanciato dopo `get_absolute_reduced()` conterrà anche i `warning` assoluti sulle performance delle metriche correnti.
            * Se lanciato dopo `get_relative_reduced()` conterrà anche i `warning` relativi al drift sulle performance delle metriche correnti rispetto a quelle storiche.
            * Il report contiene per ogni gruppo di fairness, oltre al valore della metrica, anche la percentuale di campioni appartenenti al gruppo rispetto al numero totale di campioni.
            * Se l'attributo `return_prop_true` dell'`__init__` della classe **FairnessMeasures** è `True` il dizionario delle metriche di fairness conterrà anche la percentuale di 1 (veri positivi) all'interno del gruppo in un contesto di classificazione binaria, e di conseguenza il report conterrà anche la colonna `proportion_1_curr`, e `proportion_1_stor` se chiamato dopo `get_relative_reduced()`.

        **Dati utilizzati per gli esempi**

        >>> df_esempio_corr

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature_num</th>      <th>feature_cat</th>      <th>target_clf</th>      <th>pred_clf</th>      <th>target_reg</th>      <th>pred_reg</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>2</td>      <td>B</td>      <td>0</td>      <td>0</td>      <td>7.652628</td>      <td>-1.427613</td>    </tr>    <tr>      <th>1</th>      <td>3</td>      <td>A</td>      <td>1</td>      <td>0</td>      <td>17.712800</td>      <td>3.589763</td>    </tr>    <tr>      <th>2</th>      <td>4</td>      <td>C</td>      <td>0</td>      <td>0</td>      <td>17.682912</td>      <td>32.339399</td>    </tr>    <tr>      <th>3</th>      <td>5</td>      <td>B</td>      <td>0</td>      <td>0</td>      <td>22.671351</td>      <td>20.413588</td>    </tr>    <tr>      <th>4</th>      <td>6</td>      <td>A</td>      <td>0</td>      <td>1</td>      <td>31.209811</td>      <td>31.885093</td>    </tr>    <tr>      <th>5</th>      <td>7</td>      <td>C</td>      <td>1</td>      <td>0</td>      <td>25.433599</td>      <td>11.186117</td>    </tr>    <tr>      <th>6</th>      <td>8</td>      <td>D</td>      <td>0</td>      <td>1</td>      <td>31.375411</td>      <td>25.931584</td>    </tr>    <tr>      <th>7</th>      <td>9</td>      <td>E</td>      <td>0</td>      <td>1</td>      <td>42.188562</td>      <td>43.297788</td>    </tr>    <tr>      <th>8</th>      <td>10</td>      <td>C</td>      <td>0</td>      <td>1</td>      <td>44.935844</td>      <td>33.425909</td>    </tr>    <tr>      <th>9</th>      <td>11</td>      <td>A</td>      <td>1</td>      <td>0</td>      <td>56.571237</td>      <td>60.328217</td>    </tr>  </tbody></table>

        >>> df_esempio_stor

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature_num</th>      <th>feature_cat</th>      <th>target_clf</th>      <th>pred_clf</th>      <th>target_reg</th>      <th>pred_reg</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>1</td>      <td>A</td>      <td>0</td>      <td>0</td>      <td>-1.131079</td>      <td>13.795709</td>    </tr>    <tr>      <th>1</th>      <td>2</td>      <td>B</td>      <td>1</td>      <td>1</td>      <td>5.259965</td>      <td>12.331217</td>    </tr>    <tr>      <th>2</th>      <td>3</td>      <td>A</td>      <td>0</td>      <td>0</td>      <td>12.151730</td>      <td>-6.433172</td>    </tr>    <tr>      <th>3</th>      <td>4</td>      <td>C</td>      <td>0</td>      <td>0</td>      <td>15.114249</td>      <td>1.408011</td>    </tr>    <tr>      <th>4</th>      <td>5</td>      <td>B</td>      <td>0</td>      <td>1</td>      <td>21.146841</td>      <td>17.845778</td>    </tr>    <tr>      <th>5</th>      <td>6</td>      <td>A</td>      <td>1</td>      <td>1</td>      <td>29.831444</td>      <td>14.678544</td>    </tr>    <tr>      <th>6</th>      <td>7</td>      <td>C</td>      <td>1</td>      <td>0</td>      <td>29.835704</td>      <td>41.836306</td>    </tr>    <tr>      <th>7</th>      <td>8</td>      <td>A</td>      <td>1</td>      <td>0</td>      <td>45.712137</td>      <td>27.485945</td>    </tr>    <tr>      <th>8</th>      <td>9</td>      <td>B</td>      <td>1</td>      <td>0</td>      <td>41.951110</td>      <td>44.644955</td>    </tr>    <tr>      <th>9</th>      <td>10</td>      <td>C</td>      <td>1</td>      <td>0</td>      <td>57.347082</td>      <td>52.882838</td>    </tr>  </tbody></table>

        **Esempio 1:**

        >>> FM = FairnessMeasures(approach_type="supervised", model_type="classification")
        >>> fair_dict_corr = FM.compute_metrics(
        ...     df_esempio_corr.pred_clf,
        ...     df_esempio_corr,
        ...     target=df_esempio_corr.target_clf,
        ...     fair_feat=['feature_cat']
        ... )
        >>> fair_dict_stor = FM.compute_metrics(
        ...     df_esempio_stor.pred_clf,
        ...     df_esempio_stor,
        ...     target=df_esempio_stor.target_clf,
        ...     fair_feat=['feature_cat']
        ... )
        >>> from model_monitoring.fairness_drift import FairnessDrift
        >>> FD = FairnessDrift(fair_dict_corr)
        >>> FD.get_report_reduced()

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
            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>vars</th>      <th>groups</th>      <th>curr_perc_label</th>      <th>proportion_1_curr</th>      <th>equal_opportunity_difference_curr_perf</th>      <th>average_odds_difference_curr_perf</th>      <th>statistical_parity_difference_curr_perf</th>      <th>disparate_impact_ratio_curr_perf</th>      <th>predictive_parity_difference_curr_perf</th>    </tr>  </thead>  <tbody>    <tr>      <th>1</th>      <td>feature_cat</td>      <td>A</td>      <td>0.3</td>      <td>0.666667</td>      <td>0.0</td>      <td>0.25</td>      <td>-0.095238</td>      <td>0.777778</td>      <td>0.0</td>    </tr>    <tr>      <th>2</th>      <td>feature_cat</td>      <td>C</td>      <td>0.3</td>      <td>0.333333</td>      <td>0.0</td>      <td>-0.05</td>      <td>-0.095238</td>      <td>0.777778</td>      <td>0.0</td>    </tr>    <tr>      <th>0</th>      <td>feature_cat</td>      <td>B</td>      <td>0.2</td>      <td>0.000000</td>      <td>0.0</td>      <td>-0.40</td>      <td>-0.500000</td>      <td>0.000000</td>      <td>0.0</td>    </tr>    <tr>      <th>3</th>      <td>feature_cat</td>      <td>D</td>      <td>0.1</td>      <td>0.000000</td>      <td>0.0</td>      <td>0.25</td>      <td>0.666667</td>      <td>3.000000</td>      <td>0.0</td>    </tr>    <tr>      <th>4</th>      <td>feature_cat</td>      <td>E</td>      <td>0.1</td>      <td>0.000000</td>      <td>0.0</td>      <td>0.25</td>      <td>0.666667</td>      <td>3.000000</td>      <td>0.0</td>    </tr>  </tbody></table>

        **Esempio 2: Uso con get_absolute_reduced**

        >>> FD.get_absolute_reduced()
        >>> FD.get_report_reduced()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>vars</th>      <th>groups</th>      <th>curr_perc_label</th>      <th>proportion_1_curr</th>      <th>equal_opportunity_difference_curr_perf</th>      <th>average_odds_difference_curr_perf</th>      <th>statistical_parity_difference_curr_perf</th>      <th>disparate_impact_ratio_curr_perf</th>      <th>predictive_parity_difference_curr_perf</th>      <th>absolute_warning</th>    </tr>  </thead>  <tbody>    <tr>      <th>1</th>      <td>feature_cat</td>      <td>A</td>      <td>0.3</td>      <td>0.666667</td>      <td>0.0</td>      <td>0.25</td>      <td>-0.095238</td>      <td>0.777778</td>      <td>0.0</td>      <td>Yellow Alert for average_odds_difference, disparate_impact_ratio</td>    </tr>    <tr>      <th>2</th>      <td>feature_cat</td>      <td>C</td>      <td>0.3</td>      <td>0.333333</td>      <td>0.0</td>      <td>-0.05</td>      <td>-0.095238</td>      <td>0.777778</td>      <td>0.0</td>      <td>Yellow Alert for disparate_impact_ratio</td>    </tr>    <tr>      <th>0</th>      <td>feature_cat</td>      <td>B</td>      <td>0.2</td>      <td>0.000000</td>      <td>0.0</td>      <td>-0.40</td>      <td>-0.500000</td>      <td>0.000000</td>      <td>0.0</td>      <td>Red Alert for statistical_parity_difference, disparate_impact_ratio</td>    </tr>    <tr>      <th>3</th>      <td>feature_cat</td>      <td>D</td>      <td>0.1</td>      <td>0.000000</td>      <td>0.0</td>      <td>0.25</td>      <td>0.666667</td>      <td>3.000000</td>      <td>0.0</td>      <td>Red Alert for statistical_parity_difference, disparate_impact_ratio, Yellow Alert for average_odds_difference</td>    </tr>    <tr>      <th>4</th>      <td>feature_cat</td>      <td>E</td>      <td>0.1</td>      <td>0.000000</td>      <td>0.0</td>      <td>0.25</td>      <td>0.666667</td>      <td>3.000000</td>      <td>0.0</td>      <td>Red Alert for statistical_parity_difference, disparate_impact_ratio, Yellow Alert for average_odds_difference</td>    </tr>  </tbody></table>

        **Esempio 3: Uso con get_relative_reduced**

        >>> FD.get_relative_reduced(fair_dict_stor)
        >>> FD.get_report_reduced()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>vars</th>      <th>groups</th>      <th>curr_perc_label</th>      <th>proportion_1_curr</th>      <th>equal_opportunity_difference_curr_perf</th>      <th>statistical_parity_difference_curr_perf</th>      <th>predictive_parity_difference_curr_perf</th>      <th>average_odds_difference_curr_perf</th>      <th>disparate_impact_ratio_curr_perf</th>      <th>absolute_warning</th>      <th>stor_perc_label</th>      <th>proportion_1_stor</th>      <th>equal_opportunity_difference_stor_perf</th>      <th>drift_perc_equal_opportunity_difference</th>      <th>statistical_parity_difference_stor_perf</th>      <th>drift_perc_statistical_parity_difference</th>      <th>predictive_parity_difference_stor_perf</th>      <th>drift_perc_predictive_parity_difference</th>      <th>average_odds_difference_stor_perf</th>      <th>drift_perc_average_odds_difference</th>      <th>disparate_impact_ratio_stor_perf</th>      <th>drift_perc_disparate_impact_ratio</th>      <th>relative_warning</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>feature_cat</td>      <td>A</td>      <td>0.3</td>      <td>0.666667</td>      <td>0.0</td>      <td>-0.095238</td>      <td>0.0</td>      <td>0.25</td>      <td>0.777778</td>      <td>Yellow Alert for average_odds_difference, disparate_impact_ratio</td>      <td>0.4</td>      <td>0.500000</td>      <td>0.25</td>      <td>-100.0</td>      <td>-0.083333</td>      <td>14.285714</td>      <td>0.500000</td>      <td>-100.0</td>      <td>-0.125000</td>      <td>100.0</td>      <td>0.750000</td>      <td>-11.111111</td>      <td>Red Alert for average_odds_difference</td>    </tr>    <tr>      <th>1</th>      <td>feature_cat</td>      <td>C</td>      <td>0.3</td>      <td>0.333333</td>      <td>0.0</td>      <td>-0.095238</td>      <td>0.0</td>      <td>-0.05</td>      <td>0.777778</td>      <td>Yellow Alert for disparate_impact_ratio</td>      <td>0.3</td>      <td>0.666667</td>      <td>-0.50</td>      <td>-100.0</td>      <td>-0.428571</td>      <td>-77.777778</td>      <td>-0.666667</td>      <td>-100.0</td>      <td>-0.416667</td>      <td>-88.0</td>      <td>0.000000</td>      <td>-77.777778</td>      <td></td>    </tr>    <tr>      <th>2</th>      <td>feature_cat</td>      <td>B</td>      <td>0.2</td>      <td>0.000000</td>      <td>0.0</td>      <td>-0.500000</td>      <td>0.0</td>      <td>-0.40</td>      <td>0.000000</td>      <td>Red Alert for statistical_parity_difference, average_odds_difference, disparate_impact_ratio</td>      <td>0.3</td>      <td>0.666667</td>      <td>0.25</td>      <td>-100.0</td>      <td>0.523810</td>      <td>-4.545455</td>      <td>-0.500000</td>      <td>-100.0</td>      <td>0.625000</td>      <td>-36.0</td>      <td>4.666667</td>      <td>-72.727273</td>      <td></td>    </tr>  </tbody></table>
        """
        return self.report_reduced
