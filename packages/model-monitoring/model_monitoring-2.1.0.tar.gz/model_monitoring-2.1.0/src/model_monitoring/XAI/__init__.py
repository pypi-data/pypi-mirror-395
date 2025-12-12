"""Classe per l'interpretabilità dei modelli di Machine Learning.

Questa classe offre gli strumenti per analizzare l'influenza delle diverse feature sulle previsioni di un modello di machine learning, utilizzando tecniche di interpretabilità standard (come SHAP o Permutation Importance), e generare un report sull'importanza relativa delle feature.
"""

import warnings
import re
import pandas as pd
import numpy as np
import shap
from functools import reduce

from sklearn.metrics import r2_score, roc_auc_score, balanced_accuracy_score
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold, KFold, GroupKFold
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.inspection import permutation_importance
from lightgbm import LGBMClassifier, LGBMRegressor
from model_monitoring.utils import (
    check_size,
    get_categorical_features,
    convert_Int_series,
    convert_Int_dataframe,
    absmax,
    convert_cluster_labels,
    convert_date_columns_to_seconds,
)

from model_monitoring.config import read_config

params = read_config(config_dir="config", name_params="params.yml")
default_grid = params["grid_xai"]


class XAI:
    """Classe per l'interpretabilità dei modelli di Machine Learning.

    Questa classe facilita la comprensione del comportamento dei modelli di ML, principalmente attraverso il calcolo e l'analisi dell'importanza delle feature. Permette di addestrare un modello interno (LightGBM per default) o di utilizzare un modello custom. L'obbiettivo è quello di approssimare i risultati del modello originale con un altro modello addestrandolo (overfittando) sui dati originali come feature e le predizioni fatte dal modello originale come target.

    Supporta diversi metodi per calcolare l'importanza delle feature:

        - **Valori SHAP (SHapley Additive exPlanations)**:
        Attribuisce a ciascuna feature il cambiamento nel valore atteso della predizione del modello, basandosi su principi della teoria dei giochi (valori di Shapley) per garantire equità e consistenza. Possono essere calcolati per modelli ad albero, per modelli generici, o per reti neurali.

        - **Permutation Importance**:
        Misura l'importanza di una feature calcolando il calo di performance del modello (su un set di dati) quando i valori di quella specifica feature vengono mescolati casualmente (permutati), rompendo così la relazione tra la feature e il target.

        - **Gini Importance** (per modelli ad albero):
        Specifica per modelli basati su alberi decisionali, quantifica quanto mediamente una feature contribuisce a ridurre l'impurità (es. Gini impurity o entropia) nei nodi degli alberi in cui viene utilizzata per lo split.

        - **Coefficienti del modello** (per modelli lineari):
        Nei modelli lineari (come Regressione Lineare/Logistica), il coefficiente mostra l'impatto di una feature: indica di quanto varia la previsione del modello per ogni aumento di 1 unità della feature, se tutte le altre restano uguali. La grandezza del coefficiente (senza considerare il segno) misura quanto è forte questa influenza.

        La classe gestisce anche la preparazione dei dati, inclusa la codifica One-Hot delle variabili categoriche e l'ottimizzazione degli iperparametri tramite cross-validation.

    Note:
      - Il flusso tipico è: inizializzare `XAI`, chiamare `fit`, chiamare `get_feature_importance`, e poi `get_report`, `get_score`, o `plot`.
      - Per l'approccio 'unsupervised' (clustering), viene addestrato un modello classificatore ausiliario per predire le etichette di cluster fornite.
    """

    def __init__(
        self,
        approach_type="supervised",
        model_input="default",
        model=None,
        use_cv=False,
        grid=None,
        cv_funct=RandomizedSearchCV,
        cv_scoring="auto",
        n_iter=40,
        cv_type=StratifiedKFold(5, random_state=42, shuffle=True),
        algo_type="auto",
        dim_cat_threshold=None,
    ):
        """Inizializza l'oggetto XAI configurando il modello e le opzioni di addestramento/interpretazione.

        Imposta i parametri per definire l'approccio (supervisionato/non supervisionato), il tipo di modello da usare (default LGBM o custom), se usare la cross-validation per l'ottimizzazione degli iperparametri, e come gestire le feature categoriche.

        Args:
            approach_type (`str`): Tipo di approccio per l'analisi della spiegabilità del modello. Può essere:

                - **"supervised"** (default): Approccio supervisionato.
                - **"unsupervised"**: Approccio non supervisionato, generalmente utilizzato per il clustering.
                Default: 'supervised'
            model_input (`str`, optional): Specifica l'origine del modello:

                * 'default': Utilizza un modello LightGBM interno (LGBMClassifier o LGBMRegressor in base a `algo_type`).
                * 'custom': Utilizza il modello fornito nell'argomento `model`.
                Default: 'default'.
            model (`object`/`None`, optional): Un modello (classificatore o regressore). Utilizzato solo se `model_input='custom'`. Default: `None`.
            use_cv (`bool`, optional): Se `True`, esegue la cross-validation (usando `cv_funct`, `grid`, `cv_scoring`, `n_iter`, `cv_type`) durante il metodo `fit` per ottimizzare gli iperparametri del modello. Default: `False`.
            grid (`dict`/`None`, optional): Dizionario della griglia degli iperparametri per la ricerca CV (es. per `RandomizedSearchCV`). Se `None` e si usa CV con `model_input='default'`, viene usata una griglia predefinita per LGBM.
                Default: `None`.
            cv_funct (`class`, optional): La classe per la ricerca dei parametri tramite CV (es. `RandomizedSearchCV`, `GridSearchCV`). Default: `RandomizedSearchCV`.
            cv_scoring (`str`, optional): La metrica di scoring da ottimizzare durante la CV. Se 'auto', seleziona automaticamente:

                - 'roc_auc' per `algo_type='classification'` (o clustering binario).
                - 'r2' per `algo_type='regression'`.
                - 'balanced_accuracy' per `algo_type='multiclass'` (o clustering multiclasse).
                Default: 'auto'.
            n_iter (`int`, optional): Numero di combinazioni di iperparametri da provare nella ricerca di essi. Default: 40.
            cv_type (`object`, optional): Un oggetto splitter per definire le suddivisioni della CV (es. `StratifiedKFold`, `KFold`, `GroupKFold`). Default: `StratifiedKFold(5, random_state=42, shuffle=True)`.
            algo_type (`str`, optional): Il tipo di problema ML. Opzioni: 'classification', 'multiclass', 'regression', 'clustering', 'auto'.

                * Se 'auto' (per `approach_type='supervised'`), il tipo viene determinato
                  in `fit` in base al numero di valori unici in `output_model`.
                * Deve essere 'clustering' per `approach_type='unsupervised'`.
                Default: 'auto'.
            dim_cat_threshold (`int`/`None`, optional): Soglia di cardinalità per le feature categoriche quando `model_input='custom'`. Se una feature categorica ha più valori unici di questa soglia, solo le top `dim_cat_threshold` categorie più frequenti vengono codificate con One-Hot Encoding (le altre vengono ignorate). Se `None`, viene applicato One-Hot Encoding standard a tutte le categorie. Ignorato se `model_input='default'`. Default: `None`.

        Note:
            - Il modello 'default' è LightGBM, che gestisce internamente le feature categoriche.
            - Per `model_input='custom'`, le feature categoriche vengono gestite tramite One-Hot Encoding (standard o Top-N basato su `dim_cat_threshold`) nel metodo `fit`.
            - La configurazione della CV (Cross-Validation) viene utilizzata solo se `use_cv=True`.
        """
        if model_input not in ["default", "custom"]:
            raise ValueError("model_input argument must be one of ['default','custom']")
        # check approach_type
        if approach_type not in ["supervised", "unsupervised"]:
            raise ValueError(
                f"{approach_type} is not a valid approach_type. It should be one of the following:\n['supervised', 'unsupervised']"
            )
        else:
            self.approach_type = approach_type
        # check algo_type
        if approach_type == "supervised":
            if algo_type in ["clustering"]:
                raise ValueError(
                    f"{algo_type} is not a valid algo_type for supervised approach. Select 'unsupervised' as approach_type or one of the following model_type:\n['auto', 'regression', 'classification', 'multiclass']"
                )
            elif algo_type not in ["auto", "regression", "classification", "multiclass"]:
                raise ValueError(
                    f"{algo_type} is not a valid algo_type. It should be one of the following:\n['auto', 'regression', 'classification', 'multiclass']"
                )
            else:
                self.algo_type = algo_type

        else:
            if algo_type in ["auto", "regression", "classification", "multiclass"]:
                raise ValueError(
                    f"{algo_type} is not a valid algo_type for unsupervised approach. Select 'supervised' as approach_type or one of the following model_type:\n['clustering']"
                )
            elif algo_type not in ["clustering"]:
                raise ValueError(
                    f"{algo_type} is not a valid algo_type. It should be one of the following:\n['clustering']"
                )
            else:
                self.algo_type = algo_type
        # Attributes
        self.model_input = model_input
        self.model = model
        self.use_cv = use_cv
        self.grid = grid
        self.cv_funct = cv_funct
        self.cv_scoring = cv_scoring
        self.n_iter = n_iter
        self.cv_type = cv_type
        self.dim_cat_threshold = dim_cat_threshold
        self._fitted = False
        self.report_feat_imp = None
        self.dict_report_feat_imp = None

    def fit(self, db, output_model, manage_groups=False, groups=None, standardize=False):
        """Addestra il modello utilizzando i dati forniti e i parametri configurati nella classe.

        Questo metodo gestisce il processo di addestramento:

        1.  Convalida i dati di input (`db`, `output_model`).
        2.  Se `algo_type` è 'auto' per l'approccio supervisionato, verrà determinato in base al numero di valori unici di `output_model`:

                * <=2 -> 'classification' (Classificazione Binaria)
                * <11 -> 'multiclass' (Classificazione Multiclasse)
                * >=11 -> 'regression' (Regressione)
        3.  Seleziona il modello base (LGBM default o custom).
        4.  Se `use_cv=True`, imposta l'oggetto di ricerca degli iperparametri tramite CV (es. `RandomizedSearchCV`).
        5.  Se `standardize=True`, applica uno Standard Scaler ai dati di input.
        6.  Gestisce le feature categoriche:

            - Per `model_input='default'` (LGBM): Converte le colonne 'object' in 'category' (le colonne 'category' vengono gestite dalla libreria LGBM).
            - Per `model_input='custom'`: Applica One-Hot Encoding (standard o Top-N basato sull'attributo `dim_cat_threshold`). I dati trasformati vengono salvati nell'attributo `db_tsf`.
        7.  Configura lo splitter CV per gestire i gruppi, se `manage_groups=True`.
        8.  Addestra il modello (attributo `model` o l'oggetto CV) utilizzando gli attributi `db_tsf` (o `db` se non trasformato) e `output_model`.
        9.  Se è stata usata la CV, estrae i migliori parametri.
        10.  Salva il modello finale addestrato nell'attributo `model_fitted`.

        Args:
            db (`pd.DataFrame`): Il `DataFrame` contenente le feature di input per l'addestramento.
            output_model (`pd.Series`/`np.array`): La variabile target (per approccio supervisionato) o le etichette di cluster (per approccio non supervisionato). Deve avere la stessa lunghezza (numero di righe) di `db`.
            manage_groups (`bool`, optional): Se `True`, indica che la CV deve tenere conto dei gruppi specificati nell'argomento `groups` per evitare che campioni dello stesso gruppo finiscano in fold diversi. Richiede l'uso di splitter CV compatibili come `GroupKFold` o `StratifiedGroupKFold`. Default: `False`.
            groups (`pd.Series`/`None`, optional): Una Serie pandas con lo stesso indice di `db`, contenente l'identificativo del gruppo per ciascun campione. Richiesto e utilizzato solo se `manage_groups=True`. Default: `None`.
            standardize (`bool`, optional): Se `True`, applica un metodo di scaling (StandardScaler) ai dati di input. Default: `False`.

        Note:
            - Per `approach_type='unsupervised'`, `output_model` rappresenta le etichette di cluster. Il modello addestrato (`model_fitted`) sarà un classificatore (LGBM default o custom) che impara a predire queste etichette dalle feature in `db`.
            - La gestione delle feature categoriche avviene così: LGBM le gestisce nativamente se sono di tipo 'category', mentre per altri modelli è necessario il OHE (One-Hot Encoding).
            - Il `DataFrame` effettivamente utilizzato per l'addestramento (potenzialmente dopo OHE) è memorizzato in `db_tsf`.
        """
        # Check size of the output of the model and dataset in input
        check_size(db, output_model)

        db = convert_Int_dataframe(db)
        self.db = convert_date_columns_to_seconds(db)
        if self.approach_type == "supervised":
            # Set algo_type in 'auto' mode
            self.output_model = convert_Int_series(output_model)

            vals = len(np.unique(self.output_model))
            self.vals = vals

            if vals == 1:
                warnings.warn("The output model selected is constant")
            else:
                if self.algo_type == "auto":
                    if vals <= 2:
                        self.algo_type = "classification"
                    elif vals < 11:
                        self.algo_type = "multiclass"
                    else:
                        self.algo_type = "regression"
                elif self.algo_type not in ["classification", "regression", "multiclass"]:
                    raise ValueError(
                        "algo_type argument must be one of ['auto', 'classification', 'regression', 'multiclass']"
                    )

            # Set model in 'default' mode
            if self.model_input == "default":
                if self.algo_type == "regression":
                    self.model = LGBMRegressor()
                else:
                    self.model = LGBMClassifier()

            # If using a CV strategy, define the model as the SearchCV, otherwise initialize the model provided in input as attribute
            if self.use_cv:
                if self.model_input == "default":
                    if self.algo_type == "regression":
                        self.grid = default_grid[self.algo_type]["grid_model"]
                    else:
                        self.grid = default_grid["classification"]["grid_model"]
                if self.grid is None:
                    self.grid = {}
                if self.cv_scoring == "auto":
                    if self.algo_type == "classification":
                        self.cv_scoring = "roc_auc"
                    elif self.algo_type == "regression":
                        self.cv_scoring = "r2"
                    else:
                        self.cv_scoring = "balanced_accuracy"
                if (self.algo_type == "regression") and (
                    str(self.cv_type.__class__()).startswith(("StratifiedKFold", "StratifiedGroupKFold"))
                ):
                    self.cv_type = KFold(
                        n_splits=self.cv_type.n_splits,
                        random_state=self.cv_type.random_state,
                        shuffle=self.cv_type.shuffle,
                    )
                    warnings.warn("Fold Cross Validation uncorrect for regression algorithm, KFold is set")
                try:
                    CVSel_algo = self.cv_funct(
                        self.model, self.grid, n_iter=self.n_iter, cv=self.cv_type, scoring=self.cv_scoring
                    )
                except Exception:
                    CVSel_algo = self.cv_funct(
                        self.model, self.grid, cv=self.cv_type, scoring=self.cv_scoring
                    )  # for GridSearchCV
                self.model = CVSel_algo

        elif self.approach_type == "unsupervised":
            if self.algo_type == "clustering":

                output_model = convert_Int_series(output_model)

                vals = len(np.unique(output_model))
                self.vals = vals

                self.output_model = convert_cluster_labels(output_model, vals)
                if self.model_input == "default":
                    self.model = LGBMClassifier()
                if self.use_cv:
                    if self.model_input == "default":
                        self.grid = default_grid["classification"]["grid_model"]
                    if self.grid is None:
                        self.grid = {}
                    if vals == 1:
                        warnings.warn("There is a single cluster")
                    else:
                        if vals <= 2:
                            if self.cv_scoring == "auto":
                                self.cv_scoring = "roc_auc"
                        else:
                            if self.cv_scoring == "auto":
                                self.cv_scoring = "balanced_accuracy"
                    try:
                        CVSel_algo = self.cv_funct(
                            self.model, self.grid, n_iter=self.n_iter, cv=self.cv_type, scoring=self.cv_scoring
                        )
                    except Exception:
                        CVSel_algo = self.cv_funct(
                            self.model, self.grid, cv=self.cv_type, scoring=self.cv_scoring
                        )  # for GridSearchCV
                    self.model = CVSel_algo
        # Groups check
        if manage_groups:
            if groups is None:
                warnings.warn("no group defined")
                manage_groups = False
            else:
                if not groups.index.equals(self.db.index):
                    raise ValueError("Groups Series index do not match with DataFrame index in input!")
        else:
            groups = None

        self.manage_groups = manage_groups
        if groups is not None:
            self.groups = convert_Int_series(groups)
        else:
            self.groups = groups

        self.categorical_ohe = False
        db_tsf = self.db.copy()

        if self.model_input == "default":
            # Convert object type columns in category type columns for LGBM
            db_tsf[db_tsf.select_dtypes(["object"]).columns] = db_tsf.select_dtypes(["object"]).apply(
                lambda x: x.astype("category")
            )
        else:
            cats_feat = get_categorical_features(self.db)
            self.cats_feat = cats_feat

            # Fillna with Missing and 0
            db_tsf[db_tsf.select_dtypes(["category"]).columns] = db_tsf.select_dtypes(["category"]).apply(
                lambda x: x.astype("object")
            )
            db_tsf[cats_feat] = db_tsf[cats_feat].fillna("Missing")
            db_tsf[[x for x in list(set(db_tsf.columns) - set(cats_feat))]] = db_tsf[
                [x for x in list(set(db_tsf.columns) - set(cats_feat))]
            ].fillna(0)

            # One-Hot-Encoding Categorical features
            if len(cats_feat) > 0:
                cats_ohe_feat = list(self.cats_feat)
                if self.dim_cat_threshold is not None:  # for Top-OHE
                    for col in cats_ohe_feat:
                        if db_tsf[col].nunique() > self.dim_cat_threshold:
                            values_cat = list(
                                db_tsf.groupby(col, sort=False)[col].count().sort_values(ascending=False).index
                            )[: self.dim_cat_threshold]
                            for val in values_cat:
                                db_tsf[col + "_" + str(val)] = (db_tsf[col] == val).astype("int")
                            db_tsf = db_tsf.drop(columns=col)
                            cats_ohe_feat.remove(col)
                preprocessor = ColumnTransformer(
                    transformers=[
                        ("cat", OneHotEncoder(handle_unknown="ignore", sparse=False), cats_ohe_feat),
                    ],
                    remainder="passthrough",
                )
                preprocessor.fit(db_tsf.fillna(0))
                feat_names = preprocessor.get_feature_names_out()
                feat_names = [re.sub(r"((remainder)|(cat))__", "", x) for x in feat_names]
                db_tsf = pd.DataFrame(preprocessor.transform(db_tsf), columns=feat_names)
                self.categorical_ohe = True

        # Standardize if flag is True
        if standardize:
            scaler = StandardScaler()
            db_tsf_standard = scaler.fit_transform(db_tsf)
            db_tsf_standard = pd.DataFrame(db_tsf_standard, columns=db_tsf.columns, index=db_tsf.index)
            db_tsf = db_tsf_standard

        self.db_tsf = db_tsf

        if self.use_cv:
            # Redifine KFold strategy if there are groups to consider
            if self.manage_groups:
                if len(self.groups) != len(self.db_tsf):
                    raise ValueError(
                        "dataset to be performed shap and groups-Series don't have the same number of rows ({0},{1})".format(
                            len(self.db_tsf), len(self.groups)
                        )
                    )
                number_splits = self.cv_type.n_splits
                if not (str(self.cv_type.__class__()).startswith(("GroupKFold", "StratifiedGroupKFold"))):
                    warnings.warn("GroupKFold is set for K Fold Cross Validation strategy with managing groups")
                    self.model.cv = GroupKFold(number_splits).split(self.db_tsf, self.output_model, self.groups)

        # Fit
        self.model_fitted = self.model.fit(self.db_tsf, self.output_model)
        if self.use_cv:
            self.model_fitted = self.model_fitted.best_estimator_
        self._fitted = True

        # Initialize the xai report dictionary
        self.dict_report_feat_imp = {}

    def get_feature_importance(
        self,
        feat_imp_mode="shap",
        shap_type="tree",
        n_weighted_kmeans=10,
        n_samples_deep=1000,
        n_repeats_permutation=5,
        perm_crit="mean",
    ):
        """Calcola e restituisce l'importanza delle feature del modello addestrato.

        Questo metodo calcola l'importanza di ciascuna feature utilizzando la tecnica specificata in `feat_imp_mode`. Gestisce l'aggregazione dei punteggi nel caso di One-Hot Encoding e normalizza i risultati.

        Args:
            feat_imp_mode (`str`, optional): Metodo per calcolare l'importanza. Opzioni:

                - 'shap': Calcola i valori SHAP aggregando per somma l'impatto di ciascuna feature sulla singola previsione.
                - 'permutation': Misura l'importanza valutando quanto peggiora la performance del modello se i valori di una feature vengono mescolati casualmente.
                - 'gini': Usa l'importanza basata sulla riduzione media dell'impurità di Gini nei nodi degli alberi (specifica per modelli ad albero come RandomForest/GradientBoosting).
                - 'coef': Usa i coefficienti diretti del modello, che rappresentano il peso di ciascuna feature in modelli lineari.
                Default: 'shap'.
            shap_type (`str`, optional): Tipo di SHAP explainer da usare se `feat_imp_mode='shap'`:

                - 'tree': Ottimizzato per modelli ad albero (es. LightGBM, XGBoost, CatBoost, RandomForest).
                - 'kernel': Model-agnostic, può spiegare qualsiasi modello black-box.
                - 'deep': Per modelli di deep learning (TensorFlow/Keras, PyTorch).
                Default: 'tree'.
            n_weighted_kmeans (`int`, optional): Numero di centroidi usati nei raggruppamenti nei dati di background per `shap_type='kernel'`. Default: 10.
            n_samples_deep (`int`, optional): Numero di campioni usati nei raggruppamenti nei dati di background per `shap_type='deep'`. Default: 1000.
            n_repeats_permutation (`int`, optional): Numero di ripetizioni per calcolare la Permutation Importance per ciascuna feature. Usato solo se `feat_imp_mode='permutation'`. Default: 5.
            perm_crit (`str`, optional): Criterio per aggregare i punteggi delle ripetizioni di Permutation Importance. Opzioni:

                * 'mean'
                * 'max'
                * 'min'.
                Usato solo se `feat_imp_mode='permutation'`. Default: 'mean'.

        Returns:
            `dict`: Un dizionario contenente i risultati dell'analisi. Contiene:

                - Il tipo di importanza usata (shap, gini o coef)
                - Un dizionario contenente le feature con il loro score di importanza
                - Lo score del modello (se il metodo `get_score` è stato chiamato)

        Note:
            - È necessario aver eseguito il metodo `fit` con successo prima di chiamare questa funzione.
            - Se è stato applicato One-Hot Encoding (nel metodo `fit` con il parametro `categorical_ohe=True`), l'importanza delle feature OHE derivate viene sommata per creare un unico valore attribuito alla feature categorica originale.
            - I punteggi di importanza ('gini', 'permutation', 'shap', 'coef') vengono normalizzati per somma a 1.
            - La velocità del calcolo dei valori SHAP è veloce quando `shap_type=tree`. Per `shap_type=kernel` e `shap_type=deep` il calcolo è potenzialmente lento, specialmente con molti dati e richiedono un subset di dati di background.

        **Dati utilizzati per gli esempi:**

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
            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature_num</th>      <th>feature_cat</th>      <th>pred_clf</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>1</td>      <td>A</td>      <td>0</td>    </tr>    <tr>      <th>1</th>      <td>3</td>      <td>B</td>      <td>1</td>    </tr>    <tr>      <th>2</th>      <td>1</td>      <td>A</td>      <td>0</td>    </tr>    <tr>      <th>3</th>      <td>1</td>      <td>B</td>      <td>0</td>    </tr>    <tr>      <th>4</th>      <td>1</td>      <td>B</td>      <td>0</td>    </tr>    <tr>      <th>5</th>      <td>3</td>      <td>A</td>      <td>1</td>    </tr>    <tr>      <th>6</th>      <td>1</td>      <td>B</td>      <td>0</td>    </tr>    <tr>      <th>7</th>      <td>1</td>      <td>B</td>      <td>0</td>    </tr>    <tr>      <th>8</th>      <td>1</td>      <td>B</td>      <td>0</td>    </tr>    <tr>      <th>9</th>      <td>3</td>      <td>A</td>      <td>1</td>    </tr>  </tbody></table>

        **Esempio:**

        >>> from sklearn.linear_model import LogisticRegression
        >>> modelLR = LogisticRegression()
        >>> from model_monitoring.XAI import XAI
        >>> Xai = XAI(model_input='custom', model=modelLR)
        >>> Xai.fit(df_esempio.drop(columns=['pred_clf']),df_esempio['pred_clf'], standardize=True)
        >>> importance=Xai.get_feature_importance(feat_imp_mode='coef')
        >>> importance
        {'type': 'coef',
         'feat_importance': {'feature_num': 0.8989692717116683,
          'feature_cat': 0.1010307282883317}}

        """
        # Check the type fo retrieving features importance
        if feat_imp_mode not in ["coef", "shap", "permutation", "gini"]:
            raise ValueError("feat_imp_mode argument must be one of ['coef', 'shap', 'permutation','gini']")
        self.feat_imp_mode = feat_imp_mode

        if self._fitted:
            feature_names = self.db_tsf.columns
            # Gini algorithm
            if self.feat_imp_mode == "gini":
                try:
                    feature_importances = np.abs(self.model_fitted.feature_importances_)
                except Exception:
                    raise ValueError(
                        f"{self.feat_imp_mode} not valid logic for retrieve feature importances with the model of the class"
                    )
            # Permutation algorithm
            elif self.feat_imp_mode == "permutation":
                if perm_crit not in ["mean", "max", "min"]:
                    raise ValueError("perm_crit argument must be one of ['mean','max','min']")
                self.perm_crit = perm_crit
                try:
                    self.n_repeats_permutation = n_repeats_permutation
                    perm_importance = permutation_importance(
                        self.model_fitted, self.db_tsf, self.output_model, n_repeats=n_repeats_permutation
                    )
                    # Aggregating permutation importance scores by mean
                    if self.perm_crit == "mean":
                        feature_importances = np.abs(perm_importance.importances).mean(axis=1)
                    # Aggregating permutation importance scores by max
                    elif self.perm_crit == "max":
                        feature_importances = np.abs(perm_importance.importances).max(axis=1)
                    # Aggregating permutation importance scores by min
                    elif self.perm_crit == "min":
                        feature_importances = np.abs(perm_importance.importances).min(axis=1)
                except Exception:
                    raise ValueError(
                        f"{self.feat_imp_mode} not valid logic for retrieve feature importances with the model of the class"
                    )
            # For Linear Models, retrieves absolute values of coefficients
            elif self.feat_imp_mode == "coef":
                try:
                    if self.algo_type == "regression":
                        feature_importances = self.model_fitted.coef_
                    elif self.algo_type == "classification":
                        feature_importances = self.model_fitted.coef_[0]
                    elif self.algo_type == "clustering":
                        if self.vals <= 2:
                            feature_importances = self.model_fitted.coef_[0]
                        else:
                            feature_importances = absmax(
                                self.model_fitted.coef_,
                                axis=0,
                            )

                    else:
                        feature_importances = absmax(
                            self.model_fitted.coef_,
                            axis=0,
                        )

                except Exception:
                    raise ValueError(
                        f"{self.feat_imp_mode} not valid logic for retrieve feature importances with the model of the class"
                    )
            # Features' Shapley Values algorithm
            elif self.feat_imp_mode == "shap":
                if shap_type not in ["tree", "kernel", "deep"]:
                    raise ValueError("shap_type argument must be one of ['tree','kernel','deep']")
                self.shap_type = shap_type
                # For tree models
                if self.shap_type == "tree":
                    try:
                        feature_importances = shap.TreeExplainer(self.model_fitted).shap_values(self.db_tsf)
                    except Exception:
                        raise ValueError(
                            f"{self.shap_type}-{self.feat_imp_mode} not valid logic for retrieve feature importances with the model of the class"
                        )
                # For any models. ATTENTION: very slow, it depends on size of background dataset (second parameter of KernelExplainer)
                if self.shap_type == "kernel":
                    self.n_weighted_kmeans = n_weighted_kmeans
                    try:
                        feature_importances = shap.KernelExplainer(
                            self.model_fitted.predict, shap.kmeans(self.db_tsf, self.n_weighted_kmeans)
                        ).shap_values(self.db_tsf)
                    except Exception:
                        raise ValueError(
                            f"{self.shap_type}-{self.feat_imp_mode} not valid logic for retrieve feature importances with the model of the class"
                        )
                # For deep learning models. ATTENTION: speed depends on size of background dataset (second parameter of DeepExplainer)
                if self.shap_type == "deep":
                    self.n_samples_deep = n_samples_deep
                    try:
                        feature_importances = shap.DeepExplainer(
                            self.model_fitted, self.db_tsf.sample(n=self.n_samples_deep)
                        ).shap_values(self.db_tsf.values)[0]
                    # DeepExplainer is not compatible for tensorflow models with version upper than 2.4.0
                    except AttributeError:
                        raise ValueError(
                            "model type not currently supported! If used a tensorflow model try using the following code in importing packages phase\n\nimport tensorflow as tf\ntf.compat.v1.disable_v2_behavior()"
                        )
                    except Exception:
                        raise ValueError(
                            f"{self.shap_type}-{self.feat_imp_mode} not valid logic for retrieve feature importances with the model of the class"
                        )
                # For (multi) classification
                if isinstance(feature_importances, list):
                    db_list = list()
                    for i in range(len(feature_importances)):
                        db_list.append(
                            pd.DataFrame(
                                {
                                    "feature": feature_names,
                                    "shap_importance_" + str(i): np.abs(feature_importances[i]).mean(axis=0),
                                }
                            )
                        )
                    shap_importance = (
                        reduce(lambda left, right: pd.merge(left, right, how="outer", on="feature"), db_list)
                        .set_index("feature")
                        .assign(shap_importance=lambda x: x.sum(axis=1))
                        .loc[:, "shap_importance"]
                        .reset_index()
                    )
                    feature_importances = shap_importance.shap_importance.values
                # For regression and (some - depending on the classifier) binary classification
                elif isinstance(feature_importances, np.ndarray):
                    feature_importances = np.abs(feature_importances).mean(axis=0)
            # initialize the report of feature importances
            report_feat_imp = pd.DataFrame({"feature": feature_names, "feat_importance": abs(feature_importances)})
            # mean feature importance scores for variables auto-encoded
            if self.categorical_ohe:
                for i in self.cats_feat:
                    report_feat_imp.loc[report_feat_imp.feature.str.startswith(i)] = report_feat_imp.loc[
                        report_feat_imp.feature.str.startswith(i)
                    ].assign(
                        feature=i,
                        feat_importance=report_feat_imp.loc[
                            report_feat_imp.feature.str.startswith(i), "feat_importance"
                        ].mean(),
                    )
                report_feat_imp = report_feat_imp.drop_duplicates().dropna().reset_index(drop=True)

            # normalize with sum to 1 feature importance scores and order by feature importance

            report_feat_imp.feat_importance = report_feat_imp.feat_importance / report_feat_imp.feat_importance.sum()

            self.report_feat_imp = report_feat_imp.sort_values(by=["feat_importance"], ascending=False)
        else:
            raise ValueError("no model fitted yet. Run '.fit()' with appropriate arguments before using this method.")

        self.dict_report_feat_imp["type"] = self.feat_imp_mode
        self.dict_report_feat_imp["feat_importance"] = self.report_feat_imp.set_index("feature")[
            "feat_importance"
        ].to_dict()

        return self.dict_report_feat_imp

    def get_report(self):
        """Restituisce il report dell'importanza delle feature come `DataFrame pandas`.

        Questo metodo fornisce accesso ai risultati calcolati da `get_feature_importance` in un formato tabellare.

        Returns:
            `pd.DataFrame`: Un `DataFrame` con due colonne:

                - 'feature': Nome della feature originale.
                - 'feat_importance': Punteggio di importanza calcolato (normalizzato a somma 1).
                L'importanza delle feature sono ordinate per rilevanza in ordine decrescente.

        Note:
            - Assicurarsi di aver chiamato `get_feature_importance` prima di usare questo metodo, altrimenti restituisce un `DataFrame` vuoto.

        **Esempio:**

        >>> Xai.get_report()

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

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature</th>      <th>feat_importance</th>    </tr>  </thead>  <tbody>    <tr>      <th>1</th>      <td>feature_num</td>      <td>0.898969</td>    </tr>    <tr>      <th>0</th>      <td>feature_cat</td>      <td>0.101031</td>    </tr>  </tbody></table>

        """
        return self.report_feat_imp

    def get_score(self):
        """Calcola e restituisce uno score di performance del modello sui dati di addestramento.

        Valuta le prestazioni del modello `model_fitted` utilizzando i dati trasformati `db_tsf` e i target/label originali `output_model` ottenute durante il `fit`. La metrica utilizzata dipende da `algo_type`.

        Metriche utilizzate:

        - `algo_type='regression'`: R² Score.
        - `algo_type='classification'` (binaria): ROC AUC Score. Se le probabilità non sono disponibili, usa la Balanced Accuracy Score.
        - `algo_type='multiclass'` o `'clustering'`: ROC AUC Score con strategia One-vs-Rest (`multi_class='ovr'`). Se le probabilità non sono disponibili, usa la Balanced Accuracy Score.
        - `algo_type='clustering'`: Come per 'classification' o 'multiclass'.

        Returns:
            `float`: Lo score di performance calcolato.

        Note:
            - Lo score calcolato qui riflette la performance del modello sul **set di dati utilizzato per l'addestramento** in `fit`. Non è uno score su un set di test separato.
            - Lo score viene anche memorizzato nell'attributo `model_score` e aggiunto nel dizionario che è l'output del metodo `get_feature_importance`.

        **Esempio:**

        >>> Xai.get_score()
        1.0

        """
        if self._fitted:
            if self.algo_type == "regression":
                model_score = r2_score(self.output_model, self.model_fitted.predict(self.db_tsf))
            elif self.algo_type == "classification":
                try:
                    model_score = roc_auc_score(self.output_model, self.model_fitted.predict_proba(self.db_tsf)[:, 1])
                except Exception:
                    model_score = balanced_accuracy_score(self.output_model, self.model_fitted.predict(self.db_tsf))
            elif self.algo_type == "clustering":
                if self.vals <= 2:
                    try:
                        model_score = roc_auc_score(
                            self.output_model, self.model_fitted.predict_proba(self.db_tsf)[:, 1]
                        )
                    except Exception:
                        model_score = balanced_accuracy_score(self.output_model, self.model_fitted.predict(self.db_tsf))
                else:
                    try:
                        model_score = roc_auc_score(
                            self.output_model, self.model_fitted.predict_proba(self.db_tsf), multi_class="ovr"
                        )
                    except Exception:
                        model_score = balanced_accuracy_score(self.output_model, self.model_fitted.predict(self.db_tsf))
            else:
                try:
                    model_score = roc_auc_score(
                        self.output_model, self.model_fitted.predict_proba(self.db_tsf), multi_class="ovr"
                    )
                except Exception:
                    model_score = balanced_accuracy_score(self.output_model, self.model_fitted.predict(self.db_tsf))
            self.model_score = model_score
            self.dict_report_feat_imp["model_score"] = self.model_score
        else:
            raise ValueError("no model fitted yet. Run '.fit()' with appropriate arguments before using this method.")
        return self.model_score

    def plot(self):
        """Genera e visualizza un grafico a barre orizzontali dell'importanza delle feature.

        Utilizza il `DataFrame` salvato nell'attributo `report_feat_imp` (generato da `get_feature_importance`) per creare una visualizzazione immediata delle feature più importanti secondo il modello e il metodo di interpretazione scelto. Le feature sono mostrate sull'asse y e la loro importanza sull'asse x.

        Args:
            `None`: (metodo basato sulle importanze delle feature calcolate negli altri metodi della classe).

        Note:
            - Il grafico mostra le feature ordinate in base all'importanza, crescente dal basso verso l'alto.

        **Esempio:**

        >>> Xai.plot()

        .. image:: ../../../build/images/xai_plot.png

        """
        if self.report_feat_imp is not None:
            self.report_feat_imp.sort_values(by=["feat_importance"], ascending=True).plot(
                x="feature", y="feat_importance", kind="barh", title="Features Importance"
            )
        else:
            raise ValueError("Missing report, run '.get_feature_importance()' first")
