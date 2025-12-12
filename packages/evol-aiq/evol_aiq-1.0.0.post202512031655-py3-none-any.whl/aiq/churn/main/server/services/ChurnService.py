import logging
import os
import shutil
import threading
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
import pandas as pd

from scipy.odr import Model

from aiq.churn.dao.db.ChurnTrainStatusDAO import ChurnTrainStatusDAO
from aiq.churn.dao.db.SupportedAlgorithmDao import SupportedAlgorithmDao
from aiq.churn.main.AIQCoreAPP import AIQCoreAPP
from aiq.churn.main.server.dto import PublishModelResult
from aiq.churn.main.server.dto.PublishModelResult import PublishModelResult
from aiq.churn.main.server.dto.StartTrainResult import StartTrainResult
from aiq.churn.utility import round_double
from aiq.churn.algo.model_registry import ModelRegistry
from aiq.churn.main.server.dto.LoadModelResult import LoadModelResult
from aiq.churn.main.server.dto.PredictionResult import PredictionResult
from aiq.churn.plugin.inputs.DataTransformer import DataTransformer
from aiq.churn.plugin.model.ModelDataGenerator import ModelDataGenerator
from aiq.churn.utility import load_class
from aiq.churn.utils.JSONUtils import JSONUtils


class ChurnService:
    logger = logging.getLogger(__name__)
    config: dict = None
    churn_train_status: ChurnTrainStatusDAO = None
    train_executor: ThreadPoolExecutor = None
    aiq_core_app: AIQCoreAPP = None
    supported_algorithms_dao: SupportedAlgorithmDao = None
    has_loaded_model: bool = False

    model_data_generator: ModelDataGenerator = None
    model: Model = None
    data_transformer: DataTransformer = None

    def __init__(self, config: dict):
        self.logger.info("starting ChurnService...")
        self.config = config
        self.churn_train_status = ChurnTrainStatusDAO(config)
        self.supported_algorithms_dao = SupportedAlgorithmDao(config)
        self.train_executor = ThreadPoolExecutor(max_workers=1)
        self.aiq_core_app = AIQCoreAPP(config)
        self.churn_train_status.fail_running_status(error_message="stopped during restart")
        self.load_plugins()
        trained_loaded_state = self.churn_train_status.get_loaded_and_published_state();
        if trained_loaded_state:
            self.logger.info("loading model from state {}".format(trained_loaded_state))
            published_dir: str = trained_loaded_state.get("model_artifact_path")
            self.has_loaded_model = self.load_model(trained_loaded_state, published_dir)
        else:
            self.logger.warning("no published model state found please publish before predict")
        self.logger.info("started ChurnService... with has_loaded_model {}".format(self.has_loaded_model))


    def load_plugins(self):
        self.model_data_generator = load_class(self.config['aiq_core']["model_data_gen_module"], self.config['aiq_core']["model_data_gen_class"], ModelDataGenerator)

    def start_train(self, data: dict) -> StartTrainResult:
        self.logger.debug("API start_train data {}".format(data))

        #
        # req data
        #

        service_name: str = JSONUtils.decode_str(data, "service_name", "")
        algorithm: str = JSONUtils.decode_str(data, "algorithm", "")
        overwrite_model: bool = JSONUtils.decode_bool(data, "overwrite_model", False)
        hyper_parameters = JSONUtils.decode_dict(data, "hyper_parameters")

        #validate Algo
        algo = self.supported_algorithms_dao.get_algo_by_id(algorithm)

        result: StartTrainResult = None
        if not algo:
            result = StartTrainResult(response_code=1, response_message="Algo not found")
        else:
            if overwrite_model:
                print(f"overwrite_model is set to {overwrite_model} algorithm {algorithm}")
                last_unpublished_state = self.churn_train_status.last_unpublished_state(algorithm)
                print(f"last_unpublished_state is set to {last_unpublished_state} ")
                if not last_unpublished_state:
                    result = StartTrainResult(response_code=1, response_message="no unpublished state found, overwrite model not possible")
                else:
                    result = self.train(algorithm, hyper_parameters, algo, service_name, overwrite_model)
            else:
                result = self.train(algorithm, hyper_parameters, algo, service_name, overwrite_model)

        self.logger.debug("API start_train result {}".format(result.to_dict(api_version="1.0")))
        return result

    def train(self, algorithm: str, hyper_parameters: dict, algo: dict, service_name: str, overwrite_model: bool) -> StartTrainResult:
        result: StartTrainResult = None
        # check if a train is running
        running_job = self.churn_train_status.is_a_job_running()
        if running_job:
            running_job_id = running_job.get("id")
            result = StartTrainResult(response_code=1, response_message="Already one training is in progress with run id =" + str(running_job_id) + ". Please try after some time")
        else:
            # insert the job in db
            run_id = self.churn_train_status.create(algorithm, "1", "RUNNING", hyperparams=hyper_parameters)

            # Submit training asynchronously
            train_input = {"algorithm": algo.get('algorithm'), "hyperparams": hyper_parameters, "service_name": service_name, "overwrite_model": overwrite_model}
            future_result = self.train_executor.submit(self.aiq_core_app.train, train_input)

            # Start monitoring in a separate thread
            monitor_thread = threading.Thread(target=self.monitor_future, args=(future_result, run_id),
                                              daemon=True)
            monitor_thread.start()

            # send a success
            response_message = "algorithm " + algo.get('algorithm') + " training is started with run id = " + str(run_id)
            result = StartTrainResult(response_code=0, response_message=response_message)

        return result


    def publish_model(self, data: dict) -> PublishModelResult:
        self.logger.debug("API publish_model data {}".format(data))

        #
        # req data
        #

        run_id: str = JSONUtils.decode_str(data, "run_id", "")

        # check this run was successful
        result: PublishModelResult = None
        trained_state = self.churn_train_status.get_to_publish_by_id(run_id);

        if not trained_state:
            result = PublishModelResult(response_code=1, response_message="This model is not publishable or already published", service_name="", model_name="", model_version="", model_published=False)

        else:
            model_input = trained_state.get('model_artifact_path');
            model_published = model_input + "/published"
            source_dir = os.path.join(model_input)
            target_dir = os.path.join(model_published)
            if not os.path.exists(source_dir):
                result = PublishModelResult(response_code=1, response_message="AIQ core is not able to take request at the moment. Please contact administrator to check details", service_name="", model_name="", model_version="", model_published=False)
                self.logger.error("source_dir {} does not exist".format(source_dir))
            else:
                try:
                    os.makedirs(target_dir, exist_ok=True)
                    shutil.rmtree(target_dir)
                    shutil.copytree(source_dir, target_dir)

                    model_name = trained_state.get('algorithm_id');
                    model_version = trained_state.get('model_version');

                    if self.load_model(trained_state, target_dir):
                        self.churn_train_status.publish_by_id(run_id)
                        result = PublishModelResult(response_code=0, response_message="Model version " + model_version + " is published successfully", service_name="NA", model_name=model_name, model_version=model_version, model_published=True)
                        self.has_loaded_model = True
                    else:
                        result = PublishModelResult(response_code=1, response_message="AIQ core is not able to take request at the moment. Please contact administrator to check details", service_name="NA", model_name=model_name, model_version=model_version, model_published=False)
                        self.has_loaded_model = False
                        self.logger.error("unable to load_model")

                except Exception as e:
                    self.logger.error("Exception {}".format(e))
                    result = PublishModelResult(response_code=1, response_message="AIQ core is not able to take request at the moment. Please contact administrator to check details", service_name="", model_name="", model_version="", model_published=False)
                    self.logger.error("system error {}".format(e))
        self.logger.debug("API publish_model result {}".format(result.to_dict(api_version="1.0")))
        return result

    def predict(self, data: dict) -> PredictionResult:
        self.logger.debug("API predict data {}".format(data))
        prediction_result: PredictionResult = None
        results = []
        if not self.has_loaded_model:
            prediction_result = PredictionResult(1, "model not loaded", results)
        else:
            records = JSONUtils.decode_array(data, "records")

            with ThreadPoolExecutor(max_workers=15) as executor:
                results = list(executor.map(self.predict_record, records))

            # for record in records:
            #     result = self.predict_record(record)
            #     results.append(result)
            prediction_result = PredictionResult(0, "success", results)
        self.logger.debug("API predict prediction_result {}".format(prediction_result.to_dict(api_version="1.0")))
        return prediction_result


    def predict_record(self, record: dict) -> dict:
        identifier: str = JSONUtils.decode_str(record, "identifier")
        feature_data: dict = JSONUtils.decode_json(record, "feature_data")
        debug_mode: bool = JSONUtils.decode_bool(record, "debug", default=False)

        prediction: float = -1.0
        try:
            df_features = pd.DataFrame([feature_data])

            # 1. Data pre-processor
            cleaner = self.aiq_core_app.data_cleaner
            cleaner._load_data(df_features)
            cleaned_df = cleaner.process(
                cols_to_drop=self.config.get('columns_to_drop', []),
                required_cols=list(self.config.get('required_columns', {}).keys()),
                exclude_check=['CustomerID']
            )

            # 2. EDA (Standardization)
            eda = self.aiq_core_app.eda
            #eda.load_data(cleaned_df)
            standardized_df = eda.standardize_categories(cleaned_df.copy())

            # 3. Data Transformation
            X_transformed = self.data_transformer.transform(standardized_df)

            # 4. Feature Alignment
            if hasattr(self.model, "feature_names_in_"):
                model_features = self.model.feature_names_in_
                X_final = X_transformed[model_features]
            elif hasattr(self.model, "feature_name_"):
                model_features = self.model.feature_name_
                X_final = X_transformed[model_features]
            else:
                self.logger.warning("Model feature names not found, passing transformed data directly.")
                X_final = X_transformed

            # 5. Prediction
            if hasattr(self.model, "predict_proba"):
                prediction = float(self.model.predict_proba(X_final)[:, 1][0])
            else:
                prediction = float(self.model.predict(X_final)[0])

            model_details = self.churn_train_status.get_loaded_and_published_state()
            model_version = model_details.get("model_version", "v1")
            algorithm_id = model_details.get("algorithm_id")
            if algorithm_id and self.supported_algorithms_dao:
                try:
                    algo_name = self.supported_algorithms_dao.get_algo_by_id(algorithm_id).get('algorithm', 'unknown_algo')
                except Exception:
                    self.logger.warning(f"Could not retrieve algorithm name for ID: {algorithm_id}")
                    algo_name = algorithm_id
            else:
                algo_name = "unknown_algo"

            full_result = {
                "identifier": identifier,
                "prediction": prediction,
                "churn_probability": round(prediction * 100, 2),  # Converted to %
                "algorithm_name": algo_name,
                "model_version": self.churn_train_status.get_loaded_and_published_state().get("model_version", "v1"),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error predicting record {identifier}: {str(e)}")
            import traceback
            self.logger.error(traceback.format_exc())

            full_result = {
                "identifier": identifier,
                "prediction": -1.0,
                "error": str(e)
            }

        if debug_mode:
            return full_result
        else:
            return {
                "identifier": identifier,
                "churn_probability": round(prediction * 100, 2)
            }

    def load_model(self, trained_state: dict, model_published_dir: str) -> bool:
        loaded_model: bool = False
        algo = self.supported_algorithms_dao.get_algo_by_id(trained_state.get("algorithm_id"))
        model_name = algo.get('algorithm')

        model_dir = os.path.join(model_published_dir)
        file_name = "model.joblib"
        model_file_path = os.path.join(model_dir, file_name)
        transformer_file = os.path.join(model_dir, "transformer.joblib")
        self.logger.debug("published dir is {} and model_path path is {}".format(model_dir, model_file_path))
        if not os.path.exists(model_file_path):
            self.logger.error("Model file {} not found in published directory {}".format(file_name, file_name))
            loaded_model = False
        else:
            try:
                registry = ModelRegistry(model_dir)
                self.model = registry.load_model(Path(model_published_dir))
                self.data_transformer = DataTransformer().load_saved_state(transformer_file)
                self.logger.info("model loaded from model_dir {}".format(model_dir))
                loaded_model = True

            except Exception as e:
                self.logger.error("error while loading model {} error is {}".format(model_name, e))
                loaded_model = False

        return loaded_model

    # Function to monitor the future in a separate thread
    def monitor_future(self, future_result, run_id):
        self.logger.info("monitoring thread looking for train result with run_id {}".format(run_id))
        result = future_result.result()  # Blocks until training completes
        model_version = result.get("model_version")
        records_trained = result.get("records_trained")
        self.logger.debug("monitoring thread got train result {} for run_id {}".format(result, run_id))

        accuracy = result.get("accuracy")
        precision = result.get("precision")
        recall = result.get("recall")
        f1_score = result.get("f1_score")

        #normalize
        accuracy = round_double(accuracy, 3)
        precision = round_double(precision, 3)
        recall = round_double(recall, 3)
        f1_score = round_double(f1_score, 3)


        model_artifact_path = result.get("model_artifact_path")
        error_message = result.get("error_message")
        self.churn_train_status.complete(run_id, model_version, records_trained, accuracy, precision, recall, f1_score, model_artifact_path, error_message)
        self.logger.info("monitoring thread got train result and completed train for run_id {}".format(run_id))