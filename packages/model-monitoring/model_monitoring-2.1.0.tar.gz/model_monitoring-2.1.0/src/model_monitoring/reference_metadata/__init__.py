"""Classe per la gestione e la creazione di metadati di riferimento.

Questa classe consente di generare e confrontare metadati tra un dataset di riferimento e nuovi dataset.
"""
from tqdm import tqdm
import sys

from model_monitoring.utils import (
    get_categorical_features,
    get_numerical_features,
    check_features_sets,
    convert_Int_dataframe,
)
from model_monitoring.reference_metadata.reference_metadata import retrieve_bins_dict, map_bins_dict


class ReferenceMetaData:
    """Classe per la gestione e la creazione di metadati di riferimento.

    La classe è utile per analizzare e mappare le feature di un dataset, includendo informazioni sui tipi di variabili, valori minimi e massimi, distribuzioni a bin e valori mancanti.

    La classe offre i metodi necessari per:

    - Generare metadati di riferimento da un dataset di riferimento.

    - Mappare in metadati un nuovo dataset con i metadati di riferimento .

    Le distribuzioni a bin rappresentano il risultato del processo di campionamento dei dati in gruppi ben definiti. Ogni bin ritorna il valore di occorrenza dei valori contenuti al suo interno. Per le feature categoriche, se questo valore non dovesse rispettare il valore minimo di occorrenza (vedi Note) il bin viene accorpato con il bin che ha la percentuale di occorrenza più bassa. Questo processo viene fatto in maniera iterativa fino a quando tutti i bin non risultano maggiori o uguali del valore minimo di occorrenza. Per le feature numeriche l'accorpamento viene fatto seguendo l'ordine della partizione.

    Il processo di **campionamento** si traduce in:

        - Prendere le **feature numeriche** e campionarle in bin creati appositamente, seguendo dei valori di impostazione definiti dall'utente o predefiniti. Questi bin saranno definiti tra un valore minimo e uno massimo, quindi tutti i valori compresi in questo intervallo entreranno a far parte di un bin piuttosto che un altro. I bin estremi avranno come valore minimo o massimo dell'intervallo il valore infinito (positivo o negativo) per comprendere tutti i valori possibli.
        - Prendere le **feature categoriche** e campionarle in bin creati appositamente, seguendo dei valori di impostazione definiti dall'utente o predefiniti. Questi bin saranno definiti da una o più categorie, quindi tutti i valori appartenenti ad una delle categorie rappresentate da quel bin entreranno a far parte di esso. A differenza del caso delle feature numeriche in cui venivano considerati tutti i valori possibili qui vengono utilizzati solo i valori del dataset passato. Questo dettaglio comporta, per quanto riguarda la creazione dei metadati rispetto ad un altro dataset tramite il metodo `get_meta_new`, la creazione di un bin "fittizio" chiamato `_other_` in cui saranno presenti eventuali categorie non presenti nel dataset di riferimento.

    Le informazioni generate sono particolarmente utili in contesti di monitoraggio del modello, per verificare la coerenza tra i dati di addestramento e i nuovi dati in ingresso.

    Note:
        - I valori configurabili per la creazione dei bin sono il numero massimo di bin e la percentuale minima di occorrenza all'interno di ogni bin, rispettivamente i parametri `nbins` (default 1000) e `bin_min_pct` (default 0.04) nel metodo `get_meta_reference`.
    """

    def __init__(self, meta_ref_dict=None):
        """Inizializza la classe `ReferenceMetaData` con un dizionario di metadati di riferimento opzionale.

        Se non fornito, il dizionario sarà inizializzato come `None` e dovrà essere impostato successivamente.

        Args:
            meta_ref_dict (`dict`, opzionale): Dizionario di metadati di riferimento. Questo dizionario viene utilizzato per la mappatura dei nuovi dati con i metadati di riferimento generati in precedenza. Default: `None`.

        Note:
            * Se il dizionario di metadati di riferimento non viene fornito, dovrà essere configurato successivamente tramite il metodo `get_meta_reference`.
        """
        self.meta_ref_dict = meta_ref_dict

    def get_meta_reference(self, data_reference, feat_to_check=None, nbins=1000, bin_min_pct=0.04, missing_values=True):
        """Genera un dizionario di metadati di riferimento per un dataset originale.

        Questo dizionario include informazioni sui tipi di variabili (numeriche o categoriche), valori minimi e massimi, distribuzioni a bin/categorie, e informazioni sui valori mancanti.

        Args:
            data_reference (`pd.DataFrame`): Dataset originale su cui basare la creazione dei metadati di riferimento.
            feat_to_check (`list`, opzionale): Lista delle feature da analizzare. Se `None`, vengono analizzate tutte le colonne di `data_reference`. Default: `None`.
            nbins (`int`, opzionale): Numero massimo di bin in cui suddividere le feature numeriche. Default: 1000.
            bin_min_pct (`float`, opzionale): Percentuale minima di osservazioni per ciascun bin. Default: 0.04 (4%).
            missing_values (`bool`, opzionale): Se `True`, includerà informazioni sui valori mancanti per ogni variabile. Default: `True`.

        Returns:
            `dict`: Dizionario contenente i metadati di riferimento per ciascuna feature del dataset, inclusi tipo, valori minimi e massimi, distribuzioni a bin e percentuali di valori mancanti.

        **Esempio:**

        >>> from model_monitoring.reference_metadata import ReferenceMetaData
        >>> data_storico = pd.DataFrame({'feature_num': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],'feature_cat': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'A', 'B', 'C']})
        >>> RMD = ReferenceMetaData()
        >>> meta_storico = RMD.get_meta_reference(data_storico)
        >>> meta_storico
        {'feature_num': {'type': 'numerical',
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
        """
        if feat_to_check is None:
            feat_to_check = data_reference.columns

        self.feat_to_check = feat_to_check
        self.data_reference = convert_Int_dataframe(data_reference)

        self.nbins = nbins
        self.bin_min_pct = bin_min_pct
        self.missing_values = missing_values

        # Generation reference metadata dictionary
        meta_ref_dict = dict()
        numerical_feat = get_numerical_features(self.data_reference[self.feat_to_check])
        categorical_feat = get_categorical_features(self.data_reference[self.feat_to_check])

        features_pb = tqdm(self.feat_to_check, file=sys.stdout, desc="Performing bin mapping", ncols=100, leave=True)
        for ix, col in enumerate(features_pb):
            col_dict = dict()
            if col in numerical_feat:
                col_dict["type"] = "numerical"
                col_dict["min_val"] = self.data_reference[col].min()
                col_dict["max_val"] = self.data_reference[col].max()
                col_dict["not_missing_values"] = len(self.data_reference[col]) - self.data_reference[col].isnull().sum()
            if col in categorical_feat:
                col_dict["type"] = "categorical"
                col_dict["not_missing_values"] = len(self.data_reference[col]) - self.data_reference[col].isnull().sum()
            bins_dict = retrieve_bins_dict(self.data_reference, col, nbins=self.nbins, bin_min_pct=self.bin_min_pct)[
                col
            ]
            if bins_dict != dict():
                col_dict.update(bins_dict)
            if missing_values:
                col_dict["missing_values"] = self.data_reference[col].isnull().mean()
            meta_ref_dict[col] = col_dict

            if ix == len(self.feat_to_check) - 1:
                features_pb.set_description("Completed bin mapping", refresh=True)

        self.meta_ref_dict = meta_ref_dict

        return self.meta_ref_dict

    def get_meta_new(self, new_data, meta_dict=None):
        """Recupera i metadati per un nuovo dataset mappandolo con un dizionario di metadati di riferimento.

        Questa funzione genera le feature del nuovo dataset a partire da quelle del dizionario di metadati di riferimento, calcolando i valori minimi e massimi per le variabili numeriche, applicando la mappatura dei bin predefiniti e calcolando le percentuali di valori mancanti.

        Args:
            new_data (`pd.DataFrame`): Nuovo dataset da mappare con i metadati di riferimento.
            meta_dict (`dict`, opzionale): Dizionario di metadati di riferimento. Se `None`, verrà utilizzato l'attributo predefinito `meta_ref_dict`, ovvero il dizionario creato dal metodo `get_meta_reference`. Default: `None`.

        Returns:
            `dict`: Dizionario contenente i metadati per il nuovo dataset, inclusi tipo di variabile, min/max, bin e valori mancanti.

        Note:
            * Se non viene passato il dizionario di metadati `meta_dict` deve essere chiamato prima il metodo `get_meta_reference`.
            * In caso di mismatch tra le feature dei nuovi dati e il dizionario dei metadati viene sollevato un warning e vengono considerate solo le variabili comuni.

        **Esempio:**

        >>> from model_monitoring.reference_metadata import ReferenceMetaData
        >>> data_storico = pd.DataFrame({'feature_num': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],'feature_cat': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'A', 'B', 'C']})
        >>> data_corrente = pd.DataFrame({'feature_num': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],'feature_cat': ['B', 'A', 'C', 'B', 'A', 'C', 'D', 'E', 'C', 'A'] })
        >>> RMD = ReferenceMetaData()
        >>> meta_storico = RMD.get_meta_reference(data_storico)
        >>> RMD.get_meta_new(data_corrente,meta_storico)
        {'feature_num': {'type': 'numerical',
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
          'not_missing_values': 10},
         'feature_cat': {'type': 'categorical',
          'A': {'labels': ['A'], 'freq': 0.3},
          'B': {'labels': ['B'], 'freq': 0.2},
          'C': {'labels': ['C'], 'freq': 0.3},
          '_other_': {'labels': ['E', 'D'], 'freq': 0.2},
          'missing_values': 0.0,
          'not_missing_values': 10}}
        """
        if (meta_dict is None) and (self.meta_ref_dict is None):
            raise ValueError("no reference metadata dictionary provided")
        elif meta_dict is None:
            meta_dict = self.meta_ref_dict
        # Check if the features are the same
        check_features_sets(features_1=list(meta_dict.keys()), features_2=list(new_data.columns))

        list_com_metrics = list(set(meta_dict.keys()).intersection(set(new_data.columns)))
        self.new_data = convert_Int_dataframe(new_data[list_com_metrics])
        self.meta_dict = {k: meta_dict[k] for k in list_com_metrics}

        # Generation metadata dictionary for new data
        meta_new_dict = dict()
        for col in list_com_metrics:
            col_dict = dict()
            if self.meta_dict[col]["type"] not in ["categorical", "numerical"]:
                raise ValueError(
                    f"{self.meta_dict[col]['type']} is not a valid type for {col} feature. Choose between ['categorical','numerical']."
                )
            else:
                col_dict["type"] = self.meta_dict[col]["type"]
            if col_dict["type"] == "numerical":
                col_dict["min_val"] = self.new_data[col].min()
                col_dict["max_val"] = self.new_data[col].max()
            bins_dict = map_bins_dict(self.new_data, self.meta_dict, col)[col]
            if bins_dict != dict():
                col_dict.update(bins_dict)
            if "missing_values" in self.meta_dict[col]:
                col_dict["missing_values"] = self.new_data[col].isnull().mean()
                col_dict["not_missing_values"] = len(self.new_data[col]) - self.new_data[col].isnull().sum()
            meta_new_dict[col] = col_dict

        self.meta_new_dict = meta_new_dict

        return self.meta_new_dict
