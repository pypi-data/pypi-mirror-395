import logging
import time
import traceback
from copy import deepcopy
from pathlib import Path
from typing import Mapping, Any, Dict, Tuple

from pandas import DataFrame

from aiq.churn.algo.evaluators.EvaluatorFactory import EvaluatorFactory
from aiq.churn.plugin.inputs.DataExplorer import DataExplorer
from aiq.churn.plugin.inputs.DataCleaner import DataCleaner
from aiq.churn.plugin.inputs.DataTransformer import DataTransformer
from aiq.churn.plugin.inputs.EDA import EDA
from aiq.churn.plugin.inputs.directory.DirectoryInputDataReader import DirectoryInputDataReader
from aiq.churn.plugin.inputs.file.FileInputDataReader import FileInputDataReader
from aiq.churn.plugin.inputs.hive.HiveInputDataReader import HiveInputDataReader
from aiq.churn.plugin.inputs.InputDataReader import InputDataReader

from aiq.churn.algo.feature_selectors.FeatureSelectorFactory import FeatureSelectorFactory
from aiq.churn.algo.model_registry import ModelRegistry
from aiq.churn.algo.trainers.TrainerFactory import TrainerFactory
from aiq.churn.utility import load_class
from aiq.churn.utils.logging_config import setup_logging

# force-load trainers so they register

class AIQCoreAPP:
    logger = logging.getLogger(__name__)
    input_data_reader: InputDataReader = None
    data_cleaner: DataCleaner = None
    data_explorer: DataExplorer = None
    eda: EDA = None
    config: dict = None
    data_transformer: DataTransformer = None

    def __init__(self, config: dict):

        # 1. Load Configuration
        self.config = config

        log_config = self.config['logging']['aiq_core']
        setup_logging(
            log_file=log_config.get('log_file'),
            log_level=log_config.get('log_level'),
            max_bytes=log_config.get('max_bytes'),
            backup_count=log_config.get('backup_count')
        )

        self.logger.info("logging config: %s",format(log_config))
        
        #input_type = self.config["input_data_type"]
        input_type = self.config["data_source"]["type"]
        
        if input_type == 'hive':
            self.config = self.lowercase_config_columns(self.config, ['target_column', 'required_columns', 'columns_to_drop'])     # for ADM columns
            self.input_data_reader = load_class('aiq.churn.plugin.inputs.hive.HiveInputDataReader', 'HiveInputDataReader', HiveInputDataReader);
        elif input_type == 'file':
            self.input_data_reader = load_class('aiq.churn.plugin.inputs.file.FileInputDataReader', 'FileInputDataReader', FileInputDataReader);
        elif input_type == 'directory':
            self.input_data_reader = load_class('aiq.churn.plugin.inputs.directory.DirectoryInputDataReader', 'DirectoryInputDataReader', DirectoryInputDataReader);
        else:
            self.input_data_reader = load_class('aiq.churn.plugin.inputs.file.FileInputDataReader', 'FileInputDataReader', FileInputDataReader);

        #self.input_data_reader.load_configs(config) # This is now handled dynamically in the 'run' method.
        self.data_transformer = DataTransformer()

        self.load_plugins()
        self.logger.info("plugins loaded")

    def load_plugins(self):
        self.data_cleaner = load_class(self.config['plugins']["cleaner_package"], self.config['plugins']["cleaner_class"], DataCleaner)
        self.data_explorer = load_class(self.config['plugins']["explorer_package"], self.config['plugins']["explorer_class"], DataExplorer)
        self.eda = load_class(self.config['plugins']["eda_package"], self.config['plugins']["eda_class"], EDA)


    def explore_data(self, dataframe: DataFrame) -> DataFrame:
        return self.data_explorer.explore_data(dataframe)



    def validate_data(self, dataframe: DataFrame) -> DataFrame:
        self.logger.info("validating data - final dataframe")
        self.logger.info(dataframe)
        return dataframe

    def run(self):

        # 1. Model setup
        registry = ModelRegistry(registry_path=self.config['paths']['model_registry'])
        service_name = self.config['model']['service_name']
        algo_name = self.config['model']['active']

        final_archive_path = registry.get_model_archive_path(
            service_name=service_name,
            algo_name=algo_name,
            version="v1"
        )
        self.logger.info(f"Calculated final data archive path: {final_archive_path}")

        # 2. Data Ingestion
        self.input_data_reader.load_configs(self.config, final_archive_path=final_archive_path)
        self.input_data_reader.read_data()
        data_frame = self.input_data_reader.get_data()

        # 3. Data Preprocessing
        self.data_cleaner._load_data(data_frame)
        cleaned_df = self.data_cleaner.process(
            cols_to_drop=self.config['columns_to_drop'],
            required_cols=list(self.config['required_columns'].keys())
        )

        # 4. EDA
        self.logger.info("\n" + "=" * 20 + " EDA " + "=" * 20)
        #self.eda.load_data(cleaned_df)
        cleaned_eda_df = self.eda.standardize_categories(cleaned_df)

        # 5. Data Transformation
        self.logger.info("\n" + "=" * 20 + " Data Transformation " + "=" * 20)
        self.data_transformer.prepare(df=cleaned_eda_df, target_column=self.config['target_column'])
        X_train, X_test, y_train, y_test = self.data_transformer.prepare_datasets(
            test_size=self.config['data_split']['test_size'],
            random_state=self.config['random_state']
        )
        self.logger.info("\nraw encoded features: %s", self.data_transformer.final_feature_names_)
        # save transformer state
        # self.data_transformer.save_state("artifacts/features/transformer.joblib")

        # 6. Feature Transformation
        self.logger.info("\n" + "=" * 20 + " Feature Transformation " + "=" * 20)
        trainer = TrainerFactory.create(self.config)
        fs_config = self.config.get('feature_selection', {})
        selector = None
        if fs_config.get('active', False):
            self.logger.info("Explicit Feature selection is ACTIVE.")
            selector = FeatureSelectorFactory.create(self.config, trainer.get_model())
            selector.fit(X_train, y_train)
            selector.plot(save_path=Path(self.config['paths']['evaluation_plot']) / "feature_selection_plot.png")

            X_train_selected = selector.transform(X_train)
            X_test_selected = selector.transform(X_test)
        else:
            self.logger.info("Explicit Feature selection is INACTIVE. Using all features.")
            X_train_selected = X_train
            X_test_selected = X_test

        # 7. model training & tuning
        self.logger.info("\n" + "=" * 20 + " model trainers & tuning " + "=" * 20)

        final_model = trainer.train(X_train_selected, y_train, X_valid=X_test_selected, y_valid=y_test, save_path=Path(self.config['paths']['evaluation_plot']) / "feature_importance_plot.png")
        self.logger.info(f"\nFinal model object: %s",final_model)
        self.logger.info("\nModel trained with features: %s", trainer.best_model_.feature_names_in_)
        trainer.plot_learning_curve(save_path=Path(self.config['paths']['evaluation_plot']) / "learning_curve_plot.png")
        trainer.plot_importance(save_path=Path(self.config['paths']['evaluation_plot']) / "feature_importance_plot.png")

        # 8. Evaluation
        self.logger.info("\n" + "=" * 20 + " model Evaluation " + "=" * 20)
        evaluator = EvaluatorFactory.create(final_model, self.config["learning_task"]["type"])
        #evaluator.run(
        #    X_test_selected,
        #    y_test,
        #    results_path=self.config['paths']['evaluation_report'],
        #    plot_path=Path(self.config['paths']['evaluation_plot']) / "confusion_matrix.png"
        #)



        # 9. Model Registration
        self.logger.info("\n" + "=" * 20 + " model Registration " + "=" * 20)
        #registry = ModelRegistry(registry_path=self.config['paths']['model_registry'])
        registry.register_model(
            model=final_model,
            service_name=self.config['model']['service_name'],
            algo_name=self.config['model']['active'],
            metrics=evaluator.metrics_,
            params=trainer.best_params_,
            train_data=X_train_selected,
            test_data=X_test_selected,
            transformer=self.data_transformer,
            featureSelector=selector
        )

        self.logger.info("all done")
        pass

    def lowercase_config_columns(config, keys):
        """
        Lowercases the column names in config for the provided keys. (for ADM)
        Example: lowercase_config_columns(config, ['required_columns', 'columns_to_drop'])
        """
        for key in keys:
            value = config.get(key)

            if value is None:
                # Skip if the key doesn't exist at the top level
                print(f"Warning: Configuration key '{key}' not found. Skipping.")
                continue

            if isinstance(value, list):
                config[key] = [col.lower() for col in value]
            elif isinstance(value, str):
                config[key] = value.lower()
            elif isinstance(value, dict):
                config[key] = {k.lower(): v for k, v in value.items()}
            else:
                print(f"Warning: Configuration key '{key}' has unhandled type {type(value)}. Skipping.")
        return config


# my_config = {
#     'input_type':'file',
#     'file_path':'C:\\Users\\rmitra.INDIA\\PycharmProjects\\nglm-ai\\support\\input-data.json',
#     'cleaner_package':'qa.plugins.cleaner.QACleaner',
#     'cleaner_class':'QACleaner1',
#     'explorer_package':'qa.plugins.explorer.QADataExplorer',
#     'explorer_class':'QADataExplorer',
#     'output_path':'C:\\Users\\rmitra.INDIA\\PycharmProjects\\nglm-ai\\support\\'
# }
# ai_trainer_app = AITrainerApp(my_config)
# ai_trainer_app.run()



    #
    # start_train api impl
    #

    def train(self, train_input: Mapping[str, Any]) -> Dict[str, Any]:

        start_time = time.time()

        # result
        result: Dict[str, Any] = {
            "model_version": None,
            "records_trained": 0,
            "accuracy": None,
            "precision": None,
            "recall": None,
            "f1_score": None,
            "model_artifact_path": None,
            "error_message": "",
            "training_duration_sec": None,
        }

        try:
            # 1. Validate & extract input
            self.logger.info("Starting training with input: %s", train_input)
            algorithm, hyperparams, service_name, overwrite_model = self.validate_and_extract(train_input)

            # Work on a copy of config so we don't mutate global self.config
            cfg = deepcopy(self.config)
            # Override dynamic fields from API input
            cfg["model"]["service_name"] = service_name
            cfg["model"]["active"] = algorithm
            self.apply_runtime_hyperparams(cfg, algorithm, hyperparams)

            self.logger.info("Resolved training config | service=%s algorithm=%s overwrite_model=%s",service_name, algorithm, overwrite_model )

            # 2. Model setup / registry
            registry = ModelRegistry(registry_path=cfg["paths"]["model_registry"])
            if overwrite_model:
                version = registry.get_latest_version(service_name, algorithm)
            else:
                version = registry.get_next_version(service_name, algorithm)

            final_archive_path = registry.get_model_archive_path(
                service_name=service_name,
                algo_name=algorithm,
                version=version,
                create=True,  # create the directory tree
            )

            self.logger.info("Calculated final data archive path: %s", final_archive_path)

            # OVERRIDE CONFIG PATHS TO BE VERSION-SPECIFIC
            original_report_filename = Path(cfg['paths']['evaluation_report']).name
            version_base_path = final_archive_path.parent
            self.logger.info(f"Setting version-specific base path for all outputs: {version_base_path}")

            # Override generic config paths with version-specific paths
            report_dir = version_base_path / "reports"
            plot_dir = version_base_path / "plots"
            report_dir.mkdir(parents=True, exist_ok=True)
            plot_dir.mkdir(parents=True, exist_ok=True)

            cfg['paths']['evaluation_report'] = report_dir / original_report_filename
            cfg['paths']['evaluation_plot'] = plot_dir

            plot_path = cfg['paths']['evaluation_plot']
            report_path = cfg['paths']['evaluation_report']

            # 3. Data Ingestion
            self.input_data_reader.load_configs(cfg, final_archive_path=final_archive_path)
            self.input_data_reader.read_data()
            data_frame = self.input_data_reader.get_data()

            # 4. Data Preprocessing
            self.data_cleaner._load_data(data_frame)
            cleaned_df = self.data_cleaner.process(
                cols_to_drop=cfg["columns_to_drop"],
                required_cols=list(cfg["required_columns"].keys()),
            )

            # 5. EDA
            self.logger.info("\n" + "=" * 20 + " EDA " + "=" * 20)
            #self.eda.load_data(cleaned_df)
            cleaned_eda_df = self.eda.standardize_categories(cleaned_df)
            #self.eda.plot_class_distribution(cleaned_df, target=cfg['target_column'], figsize=(6, 4), save_path=plot_path / "class_distribution_plot.png")
            #self.eda.plot_correlation_heatmap(cleaned_df, features=None, method='spearman', save_path=plot_path / "correlation_heatmap_plot.png")
            #self.eda.plot_feature_distributions_fixed(cleaned_df, max_features=30, max_plots_per_page=9, save_path_template=plot_path / "feature_dists_page_{page}.png")
            # eda.plot_feature_distributions(cleaned_df, features=['age','salary','gender','city'], sample=5000, save_path=Path(paths['evaluation_plot']) / "feature_dists_page_{page}.png")

            # 6. Data Transformation
            self.logger.info("\n" + "=" * 20 + " Data Transformation " + "=" * 20)
            self.data_transformer.prepare(
                df=cleaned_eda_df,
                target_column=cfg["target_column"],
            )
            X_train, X_test, y_train, y_test = self.data_transformer.prepare_datasets(
                test_size=cfg["data_split"]["test_size"],
                random_state=cfg["random_state"],
            )
            self.logger.info("\nraw encoded features: %s",self.data_transformer.final_feature_names_)

            # 7. Feature Transformation / Selection
            self.logger.info("\n" + "=" * 20 + " Feature Transformation " + "=" * 20)
            trainer = TrainerFactory.create(cfg)

            fs_config = cfg.get("feature_selection", {})
            selector = None

            if fs_config.get("active", False):
                self.logger.info("Explicit Feature selection is ACTIVE.")
                selector = FeatureSelectorFactory.create(cfg, trainer.get_model())
                selector.fit(X_train, y_train)
                #selector.plot( save_path=plot_path / "feature_selection_plot.png")

                X_train_selected = selector.transform(X_train)
                X_test_selected = selector.transform(X_test)
            else:
                self.logger.info("Explicit Feature selection is INACTIVE. Using all features.")
                X_train_selected = X_train
                X_test_selected = X_test

            # records_trained for result
            try:
                result["records_trained"] = (
                    X_train_selected.shape[0]
                    if hasattr(X_train_selected, "shape")
                    else len(X_train_selected)
                )
            except Exception:
                self.logger.warning("Could not determine records_trained from X_train_selected")

            # 8. Model training & tuning
            self.logger.info("\n" + "=" * 20 + " model trainers & tuning " + "=" * 20)

            final_model = trainer.train(
                X_train_selected,
                y_train,
                X_valid=X_test_selected,
                y_valid=y_test,
                save_path=plot_path / "feature_importance_plot.png",
            )

            self.logger.info("Final model object: %s", final_model)
            if hasattr(trainer, "best_model_") and hasattr(trainer.best_model_, "feature_names_in_"):
                self.logger.info("\nModel trained with features: %s",trainer.best_model_.feature_names_in_)

            # Optional plots
            try:
                trainer.plot_learning_curve(save_path=plot_path / "learning_curve_plot.png")
                trainer.plot_importance(save_path=plot_path / "feature_importance_plot.png")
                trainer.plot_training_loss(save_path=plot_path / "training_loss.png")
            except Exception as plot_exc:
                self.logger.warning("Plotting failed: %s", plot_exc)

            # 9. Evaluation
            self.logger.info("\n" + "=" * 20 + " model Evaluation " + "=" * 20)
            evaluator = EvaluatorFactory.create(final_model, cfg["learning_task"]["type"])
            evaluator.run(
                X_test_selected,
                y_test,
                results_path=report_path,
                plot_path=plot_path / "confusion_matrix.png",
            )
            #evaluator.plot_roc_curve(save_path=plot_path / "roc_curve.png")
            #evaluator.plot_precision_recall_curve(save_path=plot_path / "pr_curve.png")
            #evaluator.plot_calibration_dashboard(save_path=plot_path / "calibration_plot.png")

            # Propagate metrics into result if available
            metrics = getattr(evaluator, "metrics_", {}) or {}
            for k in ("accuracy", "precision", "recall", "f1_score"):
                if k in metrics:
                    try:
                        result[k] = float(metrics[k])
                    except Exception:
                        result[k] = metrics[k]

            # 10. Model Registration
            self.logger.info("\n" + "=" * 20 + " model Registration " + "=" * 20)

            registry.register_model(
                model=final_model,
                service_name=service_name,
                algo_name=algorithm,
                metrics=metrics,
                params=getattr(trainer, "best_params_", {}),
                train_data=X_train_selected,
                test_data=X_test_selected,
                transformer=self.data_transformer,
                featureSelector=selector,
                version=version,  # always use the same decided version
            )

            try:
                model_dir = final_archive_path.parent.resolve()
                result["model_artifact_path"] = str(model_dir)
                result["model_version"] = version
            except Exception as ver_exc:
                self.logger.warning("Could not derive model artifact path/version from registry: %s",ver_exc,)

            result["error_message"] = "all ok"
            self.logger.info("Training completed | service=%s algorithm=%s version=%s metrics=%s",
                service_name,
                algorithm,
                result["model_version"],
                {k: result[k] for k in ("accuracy", "precision", "recall", "f1_score")},
            )

        except Exception as exc:
            tb = traceback.format_exc()
            self.logger.error("Training failed: %s\n%s", exc, tb)
            result["error_message"] = f"{type(exc).__name__}: {exc}"

        finally:
            result["training_duration_sec"] = round(time.time() - start_time, 3)

        return result

    def validate_and_extract(self, train_input: Mapping[str, Any]) -> Tuple[str, Dict[str, Any], str, bool]:
        required_keys = ["algorithm", "hyperparams", "service_name", "overwrite_model"]
        missing = [k for k in required_keys if k not in train_input]
        if missing:
            raise ValueError(f"Missing required train_input keys: {missing}")

        algorithm = str(train_input["algorithm"])
        hyperparams = dict(train_input["hyperparams"] or {})
        service_name = str(train_input["service_name"])
        overwrite_model = bool(train_input["overwrite_model"])

        if not algorithm:
            raise ValueError("algorithm must be non-empty")
        if not service_name:
            raise ValueError("service_name must be non-empty")

        return algorithm, hyperparams, service_name, overwrite_model

    def apply_runtime_hyperparams(self, cfg: dict, algorithm: str, hyperparams: dict) -> None:
        if not hyperparams:
            self.logger.info(
                "No hyperparams provided in request; using config-defined tuning settings."
            )
            return

        if not isinstance(hyperparams, dict):
            raise TypeError(f"hyperparams must be a dict (from JSON), got {type(hyperparams)}")

        ht_cfg = cfg.setdefault("hyperparameter_tuning", {})
        ht_cfg["active"] = True
        model_ht_cfg = ht_cfg.setdefault(algorithm, {})
        model_ht_cfg["param_grid"] = hyperparams

        self.logger.info(
            "Overriding hyperparameter_tuning for model '%s' with param_grid: %s",
            algorithm,
            hyperparams,
        )
