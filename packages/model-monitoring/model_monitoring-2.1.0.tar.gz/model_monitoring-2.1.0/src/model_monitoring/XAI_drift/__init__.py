"""Classe per il monitoraggio del drift dello XAI (Explainable AI) di un modello.

Questa classe consente di rilevare il drift dell'importanza delle feature di un modello.
"""

import pandas as pd
import numpy as np
import warnings

from model_monitoring.utils import check_features_sets

from model_monitoring.config import read_config

params = read_config(config_dir="config", name_params="params.yml")
standard_threshold = params["xai_threshold"]
standard_psi_threshold = params["data_drift_threshold"]


class XAIDrift:
    """Classe per il monitoraggio del drift dello XAI (Explainable AI) di un modello.

    Confronta l'importanza delle feature di un modello corrente con quella di un modello storico. Supporta il calcolo del drift relativo ed eventualmente viene utilizzata la metrica PSI (Population Stability Index) per verificare le variazioni delle distribuzioni delle importanze delle feature.
    """

    def __init__(self, xai_curr, xai_stor, feat_to_check=None, config_threshold=None):
        """Inizializza la classe XAIDrift per il monitoraggio del drift dell'importanza delle feature.

        Questa funzione inizializza la classe XAIDrift, che è progettata per monitorare il drift dell'importanza delle feature tra il modello corrente e il modello storico. Vengono confrontate le importanze delle feature dei due modelli, con la possibilità di specificare quali feature controllare e definire le soglie di drift, oppure utilizzare delle soglie predefinite contenute all'interno del file `params.yml`. Soglie predefinite:

            * `relative_red`: 0.4
            * `relative_yellow`: 0.2
            * `absolute_tol`: 0.1 (Valore di tolleranza assoluta utilizzato per prevenire che valori molto piccoli possano causare drift apparentemente grandi nelle metriche).

        Args:
            xai_curr (`dict`): Dizionario contenente i valori di importanza delle feature del modello corrente.
            xai_stor (`dict`): Dizionario contenente i valori di importanza delle feature del modello storico.
            feat_to_check (`list`, opzionale): Lista delle feature da controllare. Se `None`, vengono confrontate tutte le feature. Default: `None`.
            config_threshold (`dict`, opzionale): Dizionario contenente le soglie relative per il monitoraggio del drift dell'importanza delle feature. Default: `None`.

        Note:
            * Se il parametro `config_threshold` è impostato a `None` il metodo utilizza i valori predefiniti specificati nel file `params.yml`.
            * Assicurarsi che i dizionari `xai_curr` e `xai_stor` abbiano la stessa struttura per evitare errori di compatibilità.

        """
        # Set configuration for relative and asbolute tolerance threshold for alerting
        if config_threshold is None:
            config_threshold = standard_threshold
        self.config_theshold = config_threshold

        # Check if the scores are assigned to the same set of features
        check_features_sets(
            features_1=list(xai_curr["feat_importance"].keys()), features_2=list(xai_stor["feat_importance"].keys())
        )

        if feat_to_check is not None:
            self.xai_curr = {
                "type": xai_curr["type"],
                "feat_importance": {x: xai_curr["feat_importance"][x] for x in feat_to_check},
            }
            self.xai_stor = {
                "type": xai_stor["type"],
                "feat_importance": {x: xai_stor["feat_importance"][x] for x in feat_to_check},
            }
        else:
            self.xai_curr = xai_curr
            self.xai_stor = xai_stor

        self.feat_to_check = feat_to_check

        # Check if the type of feature importance of historical and current xai model is the same
        if self.xai_curr["type"] != self.xai_stor["type"]:
            if (self.xai_curr["type"] == "coef") or (self.xai_stor["type"] == "coef"):
                raise ValueError(
                    f"'{self.xai_curr['type']}' type of feature importance in current xai model is not compatible with '{xai_stor['type']}' typ in historical xai model"
                )
            else:
                warnings.warn(
                    "the type of feature importance in current and historical xai model are not the same but they are compatible"
                )

        # Initialize the report
        xai_drift_report = (
            pd.DataFrame.from_dict(self.xai_curr["feat_importance"], "index", columns=["curr_score"])
            .reset_index()
            .rename(columns={"index": "feature"})
        )
        xai_stor_report = (
            pd.DataFrame.from_dict(self.xai_stor["feat_importance"], "index", columns=["stor_score"])
            .reset_index()
            .rename(columns={"index": "feature"})
        )
        # Save features not in common in both xai model dictionaries
        self.feat_only_cur = list(set(xai_drift_report.feature.unique()) - set(xai_stor_report.feature.unique()))
        self.feat_only_stor = list(set(xai_stor_report.feature.unique()) - set(xai_drift_report.feature.unique()))

        xai_drift_report = xai_drift_report.merge(xai_stor_report, how="outer", on="feature").fillna(0)

        self.xai_drift_report = xai_drift_report
        self.xai_psi = False

    def get_drift(self, xai_psi=True, psi_config_threshold=None):
        """Calcola e aggiorna il report sul drift dell'importanza delle feature, inclusi eventuali avvisi relativi.

        Questa funzione calcola il drift dell'importanza delle feature confrontando l'importanza delle feature nel modello corrente rispetto al modello storico.
        Viene anche calcolato il PSI (Population Stability Index) per le feature, se richiesto, per monitorare la stabilità delle distribuzioni dell'importanza delle feature nel tempo.

        Args:
            xai_psi (`bool`, opzionale): Se True, calcola il PSI per l'importanza delle feature. Default: `True`.
            psi_config_threshold (`dict`, opzionale): Dizionario contenente le soglie per il calcolo del PSI. Default: `None`.

        Note:
            * Se le soglie di PSI non vengono configurate, il metodo utilizza i valori predefiniti specificati nella classe :class:`.DataDrift` per determinare il drift.
        """
        self.relative_red = self.config_theshold["relative_red"]
        self.relative_yellow = self.config_theshold["relative_yellow"]
        self.absolute_tol = self.config_theshold["absolute_tol"]

        # Verify if 'control_type' column exist in report
        if "control_type" not in self.xai_drift_report.columns:
            # if control_type column doesn't exist, it is created in first position
            self.xai_drift_report.insert(0, "control_type", "feature drift perc")

        self.xai_psi = xai_psi
        if self.xai_psi:
            # Set thresholds for PSI
            if psi_config_threshold is None:
                psi_config_threshold = standard_psi_threshold
            self.psi_config_threshold = psi_config_threshold
            # Add 'xai_psi' feature if it doesn't exist yet
            if "xai_psi" not in self.xai_drift_report.feature.values:
                self.xai_drift_report = pd.concat(
                    [self.xai_drift_report, pd.DataFrame({"feature": ["xai_psi"]})], ignore_index=True
                )
                self.xai_drift_report.loc[lambda x: x.feature == "xai_psi", "control_type"] = "psi xai score"
        else:
            if "xai_psi" in self.xai_drift_report.feature.values:
                self.xai_drift_report = self.xai_drift_report.loc[lambda x: x.feature != "xai_psi"]

        # Generation Drift
        for a in self.xai_drift_report.feature.values:
            stor_score = self.xai_drift_report.loc[self.xai_drift_report.feature == a, "stor_score"].values[0]
            curr_score = self.xai_drift_report.loc[self.xai_drift_report.feature == a, "curr_score"].values[0]
            self.xai_drift_report.loc[self.xai_drift_report.feature == a, "value"] = (
                (curr_score - stor_score) / stor_score * 100 if stor_score != 0 else 0
            )
            if a == "xai_psi":
                psi_score = (
                    self.xai_drift_report.loc[lambda x: x.feature != "xai_psi", ["curr_score", "stor_score"]]
                    .clip(lower=0.000001)
                    .assign(psi=lambda x: (x.curr_score - x.stor_score) * (np.log(x.curr_score / x.stor_score)))
                    .loc[:, "psi"]
                    .sum()
                )
                self.xai_drift_report.loc[self.xai_drift_report.feature == a, "value"] = psi_score

        # Generation Alert
        for a in self.xai_drift_report.feature.values:
            stor_score = self.xai_drift_report.loc[self.xai_drift_report.feature == a, "stor_score"].values[0]
            curr_score = self.xai_drift_report.loc[self.xai_drift_report.feature == a, "curr_score"].values[0]
            if a in self.feat_only_cur:
                self.xai_drift_report.loc[
                    self.xai_drift_report.feature == a, "relative_warning"
                ] = "Feature not used in historical model"
            elif a in self.feat_only_stor:
                self.xai_drift_report.loc[
                    self.xai_drift_report.feature == a, "relative_warning"
                ] = "Feature not used in current model"
            else:
                if abs(curr_score - stor_score) >= self.absolute_tol:
                    drift_xai = self.xai_drift_report.loc[self.xai_drift_report.feature == a, "value"].values[0]
                    if abs(drift_xai) >= self.relative_red * 100:
                        self.xai_drift_report.loc[self.xai_drift_report.feature == a, "relative_warning"] = "Red Alert"
                    else:
                        if (abs(drift_xai) < self.relative_red * 100) and (
                            abs(drift_xai) >= self.relative_yellow * 100
                        ):
                            self.xai_drift_report.loc[
                                self.xai_drift_report.feature == a, "relative_warning"
                            ] = "Yellow Alert"
                        else:
                            self.xai_drift_report.loc[self.xai_drift_report.feature == a, "relative_warning"] = np.nan
                else:
                    self.xai_drift_report.loc[self.xai_drift_report.feature == a, "relative_warning"] = np.nan
            if a == "xai_psi":
                if psi_score >= self.psi_config_threshold["max_psi"]:
                    self.xai_drift_report.loc[self.xai_drift_report.feature == a, "relative_warning"] = "Red Alert"
                else:
                    if (psi_score < self.psi_config_threshold["max_psi"]) and (
                        psi_score >= self.psi_config_threshold["mid_psi"]
                    ):
                        self.xai_drift_report.loc[
                            self.xai_drift_report.feature == a, "relative_warning"
                        ] = "Yellow Alert"
                    else:
                        self.xai_drift_report.loc[self.xai_drift_report.feature == a, "relative_warning"] = np.nan

    def get_report(self):
        """Restituisce il report sul drift dell'importanza delle feature.

        Questa funzione restituisce un `DataFrame` che contiene il report sul drift dell'importanza delle feature, ordinato in ordine crescente in base all'importanza delle feature nel modello storico.
        Il report include le informazioni sull'importanza delle feature nel modello corrente e storico, nonché eventuali drift rilevati in base al confronto tra i due e warning relativi.

        Returns:
            `pd.DataFrame`: Report con l'importanza delle feature nel modello corrente e storico, e l'eventuale drift rilevato con i relativi warning.

        Note:
            * Se chiamato dopo il metodo `get_drift` il report presenterà anche informazioni sul drift tra il valore corrente e quello storico ed eventuli `warning` basati su di esso.

        **Dati utilizzati per gli esempi:**

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
            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature_num</th>      <th>feature_cat</th>      <th>pred_clf</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>1</td>      <td>A</td>      <td>0</td>    </tr>    <tr>      <th>1</th>      <td>3</td>      <td>B</td>      <td>1</td>    </tr>    <tr>      <th>2</th>      <td>1</td>      <td>A</td>      <td>0</td>    </tr>    <tr>      <th>3</th>      <td>1</td>      <td>B</td>      <td>0</td>    </tr>    <tr>      <th>4</th>      <td>1</td>      <td>B</td>      <td>0</td>    </tr>    <tr>      <th>5</th>      <td>3</td>      <td>A</td>      <td>1</td>    </tr>    <tr>      <th>6</th>      <td>1</td>      <td>B</td>      <td>0</td>    </tr>    <tr>      <th>7</th>      <td>1</td>      <td>B</td>      <td>0</td>    </tr>    <tr>      <th>8</th>      <td>1</td>      <td>B</td>      <td>0</td>    </tr>    <tr>      <th>9</th>      <td>3</td>      <td>A</td>      <td>1</td>    </tr>  </tbody></table>

        >>> df_esempio_stor

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature_num</th>      <th>feature_cat</th>      <th>pred_clf</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>1</td>      <td>A</td>      <td>0</td>    </tr>    <tr>      <th>1</th>      <td>2</td>      <td>B</td>      <td>1</td>    </tr>    <tr>      <th>2</th>      <td>3</td>      <td>A</td>      <td>0</td>    </tr>    <tr>      <th>3</th>      <td>4</td>      <td>C</td>      <td>0</td>    </tr>    <tr>      <th>4</th>      <td>5</td>      <td>B</td>      <td>0</td>    </tr>    <tr>      <th>5</th>      <td>6</td>      <td>A</td>      <td>0</td>    </tr>    <tr>      <th>6</th>      <td>7</td>      <td>C</td>      <td>0</td>    </tr>    <tr>      <th>7</th>      <td>8</td>      <td>A</td>      <td>1</td>    </tr>    <tr>      <th>8</th>      <td>9</td>      <td>B</td>      <td>1</td>    </tr>    <tr>      <th>9</th>      <td>10</td>      <td>C</td>      <td>0</td>    </tr>  </tbody></table>

        **Esempio:**

        >>> Xai = XAI(model_input='custom', model=modelLR)
        >>> Xai.fit(df_esempio_corr.drop(columns=['pred_clf']),df_esempio_corr['pred_clf'], standardize=True)
        >>> importance_corr=Xai.get_feature_importance(feat_imp_mode='coef')
        >>> importance_corr
        {'type': 'coef',
         'feat_importance': {'feature_num': 0.8989692717116683,
          'feature_cat': 0.1010307282883317}}
        >>> Xai.fit(df_esempio_stor.drop(columns=['pred_clf']),df_esempio_stor['pred_clf'], standardize=True)
        >>> importance_stor=Xai.get_feature_importance(feat_imp_mode='coef')
        >>> importance_stor
        {'type': 'coef',
         'feat_importance': {'feature_num': 0.5098198313687213,
          'feature_cat': 0.4901801686312786}}
        >>> from model_monitoring.XAI_drift import XAIDrift
        >>> XaiD = XAIDrift(importance_corr,importance_stor)
        >>> XaiD.get_report()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature</th>      <th>curr_score</th>      <th>stor_score</th>    </tr>  </thead>  <tbody>    <tr>      <th>1</th>      <td>feature_cat</td>      <td>0.101031</td>      <td>0.49018</td>    </tr>    <tr>      <th>0</th>      <td>feature_num</td>      <td>0.898969</td>      <td>0.50982</td>    </tr>  </tbody></table>

        >>> XaiD.get_drift()
        >>> XaiD.get_report()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>control_type</th>      <th>feature</th>      <th>curr_score</th>      <th>stor_score</th>      <th>value</th>      <th>relative_warning</th>    </tr>  </thead>  <tbody>    <tr>      <th>1</th>      <td>feature drift perc</td>      <td>feature_cat</td>      <td>0.101031</td>      <td>0.49018</td>      <td>-79.389062</td>      <td>Red Alert</td>    </tr>    <tr>      <th>0</th>      <td>feature drift perc</td>      <td>feature_num</td>      <td>0.898969</td>      <td>0.50982</td>      <td>76.330777</td>      <td>Red Alert</td>    </tr>    <tr>      <th>2</th>      <td>psi xai score</td>      <td>xai_psi</td>      <td>NaN</td>      <td>NaN</td>      <td>0.835325</td>      <td>Red Alert</td>    </tr>  </tbody></table>

        """
        return self.xai_drift_report.sort_values("stor_score", key=abs)

    def plot(self):
        """Genera e visualizza un grafico a barre orizzontali dell'importanza delle feature storiche e correnti.

        Utilizza il `DataFrame` salvato nell'attributo `xai_drift_report` (generato da `get_report`) per creare una visualizzazione immediata delle feature storiche e correnti più importanti secondo il modello e il metodo di interpretazione scelto. Le feature sono mostrate sull'asse y e la loro importanza sull'asse x.

        Args:
            `None`: (metodo basato sulle importanze delle feature generate nei metodi precedenti).

        Note:
            - Il grafico mostra le feature ordinate in base all'importanza storica, crescente dal basso verso l'alto.

        **Esempio:**

        >>> XaiD.plot()

        .. image:: ../../../build/images/xaid_plot.png

        """
        self.xai_drift_report.loc[lambda x: x.feature != "xai_psi"].sort_values("stor_score", key=abs).plot(
            x="feature", y=["curr_score", "stor_score"], kind="barh", title="Features Importance Drift"
        )
