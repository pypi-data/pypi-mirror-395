"""Classe utilizzata per monitorare e rilevare il Data Drift tra due dataset.

Questa classe offre gli strumenti per confrontare le variazioni di distribuzione delle variabili di un dataset di riferimento rispetto ad un altro attraverso misure o test statistici standard, e generare un report di alerting su data drift critici.
"""

import pandas as pd
from typing import Dict

from model_monitoring.data_drift.data_drift import stat_report
from model_monitoring.utils import check_features_sets, convert_Int_dataframe, convert_Int_series

from model_monitoring.config import read_config

params = read_config(config_dir="config", name_params="params.yml")
standard_threshold_psi = params["data_drift_threshold"]


class DataDrift:
    """Classe utilizzata per monitorare e rilevare il Data Drift tra due dataset.

    Questa classe fornisce strumenti per:

    a)  Quantificare il cambiamento nelle distribuzioni utilizzando metriche statistiche come il Population Stability Index (PSI) o i p-value derivati da test statistici (Kolmogorov-Smirnov per numeriche, Chi-quadrato per categoriche).
    b)  Generare un report (in formato `DataFrame Pandas`) di alerting basato su threshold configurabili. Valori di default:

        * Max PSI: 0.2
        * Mid PSI: 0.1
        * p-value: 0.05
        Questo rileva i data drift critici (alerting rosso) e i data drift rilevanti (alerting giallo).

    c)  Implementare tecniche di ottimizzazione di binning delle variabili per la generazione dei metadati. (Per dettagli :class:`.ReferenceMetaData`)
    d)  Gestire diversi formati di input:

        * `DataFrame Pandas` (type_data=”data”).
        * Dizionari contenenti metadati pre-calcolati (type_data=”metadata”).
        * Rilevamento automatico del formato (type_data=”auto”).
    e)  Opzionalmente, calcolare e includere nel report il drift della percentuale di valori mancanti (`NaN`) per ciascuna variabile.
    """

    def __init__(self, data_stor, data_curr, type_data="auto", feat_to_check=None, config_threshold=None):
        """Inizializza la classe `DataDrift`, configurando i dati di riferimento e i dati correnti, il tipo di dati, e le feature da monitorare.

        A seconda del tipo di dati forniti, la classe prepara i dati per il calcolo del data drift, infatti possono essere inseriti come input sia i dati in formato `DataFrame` che in formato `dict` nel caso fossero metadati.

        Inoltre, la classe verifica se esistono feature in comune tra i due dataset e, se necessario, configura le soglie per il monitoraggio del data drift. Se non vengono fornite soglie specifiche, vengono usate quelle predefinite.

        Args:
            data_stor (`pd.DataFrame`/`dict`): Il dataset storico (di riferimento) con cui confrontare il dataset corrente. Questo dataset contiene le informazioni da utilizzare per il confronto delle feature con i dati correnti.

            data_curr (`pd.DataFrame`/`dict`): Il dataset corrente che rappresenta i nuovi dati da analizzare. Questo dataset contiene i dati attuali da confrontare con quelli storici per il rilevamento del data drift.

            type_data (`str`, opzionale): Indica il tipo di dati forniti:

                - "auto": La classe determina automaticamente se i dati sono `DataFrame` o metadati.
                - "data": I dati vengono forniti come `DataFrame` Pandas.
                - "metadata": I dati vengono forniti come metadati (dizionari).
                Default: "auto".

            feat_to_check (list, opzionale): Una lista delle feature da verificare. Se non specificato, verranno analizzate tutte le feature comuni tra i due dataset. Default: `None`
            config_threshold (dict, opzionale): Dizionario contenente le soglie PSI e p-value, che definiscono i limiti per il rilevamento del data drift. Se non fornito, vengono usate le soglie predefinite. Valori di default:

                * Max PSI: 0.2
                * Mid PSI: 0.1
                * p-value: 0.05
                Default: `None`
        """
        # Set psi threshold
        if config_threshold is None:
            config_threshold = standard_threshold_psi
        self.config_threshold = config_threshold

        if type_data not in ["auto", "data", "metadata"]:
            raise ValueError(
                f"{type_data} is not a valid type_data. It should be one of the following:\n ['auto','data','metadata']"
            )

        if type_data == "auto":
            if isinstance(data_stor, pd.DataFrame) and isinstance(data_curr, pd.DataFrame):
                type_data = "data"
            elif isinstance(data_stor, Dict) and isinstance(data_curr, Dict):
                type_data = "metadata"
            else:
                raise ValueError("format data inputs are not valid. Choose both pd.DataFrame or both dict")
        self.type_data = type_data

        if type_data == "data":
            check_features_sets(features_1=list(data_stor.columns), features_2=list(data_curr.columns))
            list_com_features = list(set(data_stor.columns).intersection(set(data_curr.columns)))
        else:
            check_features_sets(features_1=list(data_stor.keys()), features_2=list(data_curr.keys()))
            list_com_features = list(set(data_stor.keys()).intersection(set(data_curr.keys())))
        if len(list_com_features) == 0:
            raise ValueError("No features in common between the two sets")

        if feat_to_check is None:
            feat_to_check = list_com_features

        self.feat_to_check = feat_to_check

        if isinstance(self.feat_to_check, str):
            self.feat_to_check = [self.feat_to_check]

        self.data_stor_original = data_stor
        self.data_curr_original = data_curr
        if type_data == "data":
            if len(self.feat_to_check) == 1:
                self.data_stor = pd.DataFrame(convert_Int_series(data_stor[self.feat_to_check[0]]))
                self.data_curr = pd.DataFrame(convert_Int_series(data_curr[self.feat_to_check[0]]))
            else:
                self.data_stor = convert_Int_dataframe(data_stor[self.feat_to_check])
                self.data_curr = convert_Int_dataframe(data_curr[self.feat_to_check])
        else:
            self.data_stor = {x: data_stor[x] for x in self.feat_to_check}
            self.data_curr = {x: data_curr[x] for x in self.feat_to_check}

        # Check valid format for metadata
        if type_data == "metadata":
            for x in self.feat_to_check:
                if "type" not in self.data_stor[x].keys():
                    raise ValueError(f"not type provided for {x} feature in reference metadata")
                elif "type" not in self.data_curr[x].keys():
                    raise ValueError(f"not type provided for {x} feature in new metadata")
                else:
                    if self.data_stor[x]["type"] not in ["categorical", "numerical"]:
                        raise ValueError(
                            f"{self.data_stor[x]['type']} not valid type for {x} feature. Choose among ['categorical','numerical']"
                        )
                    if self.data_curr[x]["type"] not in ["categorical", "numerical"]:
                        raise ValueError(
                            f"{self.data_curr[x]['type']} not valid type for {x} feature. Choose among ['categorical','numerical']"
                        )
                    if self.data_stor[x]["type"] == "numerical":
                        if "min_val" not in self.data_stor[x].keys():
                            raise ValueError(f"not min_val provided for {x} numerical feature in reference metadata")
                        if "max_val" not in self.data_stor[x].keys():
                            raise ValueError(f"not max_val provided for {x} numerical feature in reference metadata")
                        for y in [
                            k
                            for k in self.data_stor[x].keys()
                            if k not in ["type", "min_val", "max_val", "missing_values", "not_missing_values"]
                        ]:
                            if "min" not in self.data_stor[x][y].keys():
                                raise ValueError(
                                    f"not min provided for {x} numerical feature for {y} bin in reference metadata"
                                )
                            if "max" not in self.data_stor[x][y].keys():
                                raise ValueError(
                                    f"not max provided for {x} numerical feature for {y} bin in reference metadata"
                                )
                            if "freq" not in self.data_stor[x][y].keys():
                                raise ValueError(
                                    f"not freq provided for {x} numerical feature for {y} bin in reference metadata"
                                )
                    if self.data_curr[x]["type"] == "numerical":
                        if "min_val" not in self.data_curr[x].keys():
                            raise ValueError(f"not min_val provided for {x} numerical feature in new metadata")
                        if "max_val" not in self.data_curr[x].keys():
                            raise ValueError(f"not max_val provided for {x} numerical feature in new metadata")
                        for y in [
                            k
                            for k in self.data_curr[x].keys()
                            if k not in ["type", "min_val", "max_val", "missing_values", "not_missing_values"]
                        ]:
                            if "min" not in self.data_curr[x][y].keys():
                                raise ValueError(
                                    f"not min provided for {x} numerical feature for {y} bin in new metadata"
                                )
                            if "max" not in self.data_curr[x][y].keys():
                                raise ValueError(
                                    f"not max provided for {x} numerical feature for {y} bin in new metadata"
                                )
                            if "freq" not in self.data_curr[x][y].keys():
                                raise ValueError(
                                    f"not freq provided for {x} numerical feature for {y} bin in new metadata"
                                )
                    if self.data_stor[x]["type"] == "categorical":
                        for y in [
                            k
                            for k in self.data_stor[x].keys()
                            if k not in ["type", "missing_values", "not_missing_values"]
                        ]:
                            if "labels" not in self.data_stor[x][y].keys():
                                raise ValueError(
                                    f"not labels provided for {x} categorical feature for {y} bin in reference metadata"
                                )
                            if "freq" not in self.data_stor[x][y].keys():
                                raise ValueError(
                                    f"not freq provided for {x} categorical feature for {y} bin in reference metadata"
                                )
                    if self.data_curr[x]["type"] == "categorical":
                        for y in [
                            k
                            for k in self.data_curr[x].keys()
                            if k not in ["type", "missing_values", "not_missing_values"]
                        ]:
                            if "labels" not in self.data_curr[x][y].keys():
                                raise ValueError(
                                    f"not labels provided for {x} categorical feature for {y} bin in new metadata"
                                )
                            if "freq" not in self.data_curr[x][y].keys():
                                raise ValueError(
                                    f"not freq provided for {x} categorical feature for {y} bin in new metadata"
                                )

        # Initialize the report
        self.data_drift_report = None
        self.meta_ref_dict = None

    def report_drift(
        self,
        psi_nbins=1000,
        psi_bin_min_pct=0.04,
        stat="psi",
        drift_missing=True,
        return_meta_ref=False,
        dim_threshold=5000,
    ):
        """Restituisce il report con PSI o p-value per ciascuna feature in entrambi i dataset (storico e corrente) e segnala avvisi (`Warning`) se i PSI superano le soglie predefinite o se i p-value non superano il livello di significatività (alpha).

        Questa funzione calcola il report del drift dei dati confrontando il dataset storico (di riferimento) con il dataset corrente. Il data drift viene calcolato utilizzando il Population Stability Index (PSI) o i p-value, a seconda del valore del parametro `stat`. Se il PSI supera la soglia predefinita o se il p-value non supera il livello di significatività (alpha), vengono generati degli avvisi.

        Args:

            psi_nbins (`int`, opzionale): Numero di intervalli (bins) in cui le feature verranno suddivise per il calcolo del PSI. Default: 1000.
            psi_bin_min_pct (`float`, opzionale): Percentuale minima di osservazioni per ciascun intervallo (bucket). Default: 0.04 (4%).
            stat (`str`, opzionale): Tipo di statistica da utilizzare. Può essere "psi" (Population Stability Index) o "pval" (p-value derivato dal test di Kolmogorov-Smirnov per feature numeriche o dal test del Chi-quadrato per feature categoriche). Default: "psi".
            drift_missing (`bool`, opzionale): Se True, include nel report anche il drift dei valori mancanti (missing values). Default: True.
            return_meta_ref (`bool`, opzionale): Se True, salva il dizionario dei metadati di riferimento come attributo della classe. Default: False.
            dim_threshold (`int`, opzionale): Dimensione massima del set di test significativo per il test del Chi-quadrato. Default: 5000.

        Returns:
            `pd.DataFrame`: Il report generato dalla classe che contiene le informazioni sul data drift delle feature. Il `DataFrame` include il valore del PSI o del p-value per ciascuna feature, eventuali avvisi e, se richiesto, anche le informazioni sul drift dei valori mancanti.

        Note:

            - Se il parametro `stat` è impostato su "psi", la funzione calcolerà il PSI per le feature numeriche e categoriche.
            - Se il parametro `stat` è impostato su "pval", la funzione eseguirà il test di Kolmogorov-Smirnov per le feature numeriche e il test del Chi-quadrato per quelle categoriche.
            - Gli avvisi sono generati se i PSI superano la soglia massima predefinita o se i p-value non superano il livello di significatività (alpha).

        **Esempio 1: Utilizzo con DataFrame Pandas**

        >>> import pandas as pd
        >>> from model_monitoring.data_drift import DataDrift
        >>> data_storico = pd.DataFrame({
        ...  'feature_num': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        ...  'feature_cat': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'A', 'B', 'C']
        ...  })
        >>> data_corrente = pd.DataFrame({
        ...  'feature_num': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11], # Leggero shift
        ...  'feature_cat': ['B', 'A', 'C', 'B', 'A', 'C', 'D', 'E', 'C', 'A'] # Distribuzione diversa
        ...  })
        >>> drift_detector = DataDrift(data_storico, data_corrente, type_data="data")
        >>> report = drift_detector.report_drift(stat="psi", drift_missing=True)
        >>> report

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

                <table class="jupyter-style-table" border="0">
                    <thead>
                        <tr style="text-align: right;">
                          <th>feature</th>
                          <th>common_psi</th>
                          <th>warning</th>
                          <th>total_psi</th>
                          <th>proportion_new_data</th>
                          <th>proportion_old-fashioned_data</th>
                          <th>validity_warning</th>
                          <th>drift_perc_missing</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr>
                          <td>feature_cat</td>
                          <td>0.069315</td>
                          <td>None</td>
                          <td>2.510517</td>
                          <td>0.2</td>
                          <td>0.0</td>
                          <td>Red Alert - new categorical data</td>
                          <td>0.0</td>
                        </tr>
                        <tr>
                          <td>feature_num</td>
                          <td>1.220596</td>
                          <td>Red Alert</td>
                          <td>1.220596</td>
                          <td>0.0</td>
                          <td>0.0</td>
                          <td>Information - values above the upper bound in the new data</td>
                          <td>0.0</td>
                        </tr>
                        </tbody>
                    </table>

        **Esempio 2: Utilizzo con Metadati (struttura semplificata)**

        >>> meta_storico = {
            'feature_num': {'type': 'numerical',
              'min_val': 1,
              'max_val': 10,
              'not_missing_values': 10,
              'bin_0': {'min': -inf, 'max': 1.0, 'freq': 0.1},
              'bin_1': {'min': 1.0, 'max': 2.0, 'freq': 0.1},
              'bin_2': {'min': 2.0, 'max': 3.0, 'freq': 0.1},
              'bin_3': {'min': 3.0, 'max': 4.0, 'freq': 0.1},
              'bin_4': {'min': 4.0, 'max': 5.0, 'freq': 0.1},
              'bin_5': {'min': 5.0, 'max': 6.0, 'freq': 0.1},
              'bin_6': {'min': 6.0, 'max': 7.0, 'freq': 0.1},
              'bin_7': {'min': 7.0, 'max': 8.0, 'freq': 0.1},
              'bin_8': {'min': 8.0, 'max': 9.0, 'freq': 0.1},
              'bin_9': {'min': 9.0, 'max': inf, 'freq': 0.1},
              'missing_values': 0.0},
            'feature_cat': {'type': 'categorical',
              'not_missing_values': 10,
              'A': {'labels': ['A'], 'freq': 0.4},
              'B': {'labels': ['B'], 'freq': 0.3},
              'C': {'labels': ['C'], 'freq': 0.3},
              'missing_values': 0.0}}
        >>> meta_corrente = {
            'feature_cat': {'type': 'categorical',
              'A': {'labels': ['A'], 'freq': 0.3},
              'B': {'labels': ['B'], 'freq': 0.2},
              'C': {'labels': ['C'], 'freq': 0.3},
              '_other_': {'labels': ['D', 'E'], 'freq': 0.2},
              'missing_values': 0.0,
              'not_missing_values': 10},
             'feature_num': {'type': 'numerical',
              'min_val': 2,
              'max_val': 11,
              'bin_0': {'min': -inf, 'max': 1.0, 'freq': 0.0},
              'bin_1': {'min': 1.0, 'max': 2.0, 'freq': 0.1},
              'bin_2': {'min': 2.0, 'max': 3.0, 'freq': 0.1},
              'bin_3': {'min': 3.0, 'max': 4.0, 'freq': 0.1},
              'bin_4': {'min': 4.0, 'max': 5.0, 'freq': 0.1},
              'bin_5': {'min': 5.0, 'max': 6.0, 'freq': 0.1},
              'bin_6': {'min': 6.0, 'max': 7.0, 'freq': 0.1},
              'bin_7': {'min': 7.0, 'max': 8.0, 'freq': 0.1},
              'bin_8': {'min': 8.0, 'max': 9.0, 'freq': 0.1},
              'bin_9': {'min': 9.0, 'max': inf, 'freq': 0.2},
              'missing_values': 0.0,
              'not_missing_values': 10}}
        >>> drift_detector_meta = DataDrift(meta_storico, meta_corrente, type_data="metadata")
        >>> report_meta = drift_detector_meta.report_drift(stat="psi", drift_missing=True)
        >>> report_meta

        .. raw:: html

            <table class="jupyter-style-table" border="0">
                    <thead>
                        <tr style="text-align: right;">
                          <th>feature</th>
                          <th>common_psi</th>
                          <th>warning</th>
                          <th>total_psi</th>
                          <th>proportion_new_data</th>
                          <th>proportion_old-fashioned_data</th>
                          <th>validity_warning</th>
                          <th>drift_perc_missing</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr>
                          <td>feature_cat</td>
                          <td>0.069315</td>
                          <td>None</td>
                          <td>2.510517</td>
                          <td>0.2</td>
                          <td>0.0</td>
                          <td>Red Alert - new categorical data</td>
                          <td>0.0</td>
                        </tr>
                        <tr>
                          <td>feature_num</td>
                          <td>1.220596</td>
                          <td>Red Alert</td>
                          <td>1.220596</td>
                          <td>0.0</td>
                          <td>0.0</td>
                          <td>Information - values above the upper bound in the new data</td>
                          <td>0.0</td>
                        </tr>
                        </tbody>
                    </table>
        """
        self.psi_nbins = psi_nbins
        self.psi_bin_min_pct = psi_bin_min_pct
        if stat not in ["psi", "pval"]:
            raise ValueError(f"{stat} is not a valid test. It should be one of the following:\n ['psi','pval']")
        self.stat = stat
        self.drift_missing = drift_missing
        self.return_meta_ref = return_meta_ref
        self.dim_threshold = dim_threshold

        if self.stat == "psi":
            # data drift psi report
            data_drift_report, meta_ref_dict = stat_report(
                base_df=self.data_stor,
                compare_df=self.data_curr,
                type_data=self.type_data,
                feat_to_check=self.feat_to_check,
                stat=self.stat,
                alpha=None,
                max_psi=self.config_threshold["max_psi"],
                mid_psi=self.config_threshold["mid_psi"],
                psi_nbins=self.psi_nbins,
                psi_bin_min_pct=self.psi_bin_min_pct,
                return_meta_ref=self.return_meta_ref,
                dim_threshold=self.dim_threshold,
            )

        else:
            # data drift p-value report
            data_drift_report, meta_ref_dict = stat_report(
                base_df=self.data_stor,
                compare_df=self.data_curr,
                type_data=self.type_data,
                feat_to_check=self.feat_to_check,
                stat=self.stat,
                alpha=self.config_threshold["alpha"],
                max_psi=None,
                mid_psi=None,
                psi_nbins=self.psi_nbins,
                psi_bin_min_pct=self.psi_bin_min_pct,
                return_meta_ref=self.return_meta_ref,
                dim_threshold=self.dim_threshold,
            )

        self.meta_ref_dict = meta_ref_dict

        # missing values drift
        if drift_missing:
            if self.type_data == "data":
                perc_drift_missing = pd.Series(
                    (
                        self.data_curr[self.feat_to_check].isnull().mean()
                        - self.data_stor[self.feat_to_check].isnull().mean()
                    )
                    * 100,
                    name="drift_perc_missing",
                )
                if self.return_meta_ref:
                    for col in self.meta_ref_dict:
                        self.meta_ref_dict[col]["missing_values"] = self.data_stor[col].isnull().mean()
            else:
                missing_dict = dict()
                for col in self.feat_to_check:
                    try:
                        missing_dict[col] = (
                            self.data_curr[col]["missing_values"] - self.data_stor[col]["missing_values"]
                        ) * 100
                    except Exception:
                        raise ValueError(f"no missing values provided for {col} feature")
                perc_drift_missing = pd.DataFrame.from_dict(
                    missing_dict, orient="index", columns=["drift_perc_missing"]
                )
            data_drift_report = data_drift_report.merge(perc_drift_missing, left_on="feature", right_index=True)
        self.data_drift_report = data_drift_report
        return self.data_drift_report

    def get_meta_ref(self):
        """Restituisce il dizionario dei metadati di riferimento.

        Questa funzione restituisce il dizionario che contiene i metadati relativi ai dataset storici (di riferimento) utilizzati per il monitoraggio del data drift. I metadati includono:

            * Il tipo di feature (categorica o numerica)
            * Informazioni sui bin, in particolare:

                - Feature numeriche: Si calcola la frequenza con cui ciascuna feature numerica compare all'interno di intervalli (bin) di valori continui, definiti automaticamente.
                - Feature categoriche: Si calcola la frequenza con cui ciascuna feature categorica compare all'interno di gruppi (bin) di categorie, creati automaticamente tramite accorpamento.
            * Informazioni sui missing values
            * Per le feature numeriche, informazioni aggiuntive sul dataset di riferimento:

                - Il valore minimo complessivo osservato.
                - Il valore massimo complessivo osservato.
                - Il numero totale di campioni del dataset.

        Returns:
            `dict`: Il dizionario contenente i metadati di riferimento, che descrivono le feature dei dataset di riferimento.

        Note:
            - Il dizionario restituito è stato creato durante l'esecuzione della funzione `report_drift` quando il parametro `return_meta_ref` è impostato su `True`.
            - Questo dizionario può essere utile per ottenere informazioni di dettaglio sui dati di riferimento e per eseguire un'analisi più rapida del data drift delle feature.

        Esempio di utilizzo:

        >>> data_storico = pd.DataFrame({'feature_num': [1, 2, 3], 'feature_cat': ['A', 'B', 'A']})
        >>> data_corrente = pd.DataFrame({'feature_num': [4, 5, 6], 'feature_cat': ['C', 'D', 'C']})
        >>> drift_detector = DataDrift(data_storico, data_corrente, type_data="data")
        >>> report = drift_detector.report_drift(stat="psi", return_meta_ref=True)
        >>> meta_ref = drift_detector.get_meta_ref()
        >>> meta_ref
        {'feature_num': {'type': 'numerical',
            'min_val': 1,
            'max_val': 3,
            'not_missing_values': 3,
            'bin_0': {'min': -inf, 'max': 1.0, 'freq': 0.3333333333333333},
            'bin_1': {'min': 1.0, 'max': 2.0, 'freq': 0.3333333333333333},
            'bin_2': {'min': 2.0, 'max': inf, 'freq': 0.3333333333333333},
            'missing_values': 0.0},
            'feature_cat': {'type': 'categorical',
            'A': {'labels': ['A'], 'freq': 0.6666666666666666},
            'B': {'labels': ['B'], 'freq': 0.3333333333333333},
            'missing_values': 0.0}}
        """
        return self.meta_ref_dict
