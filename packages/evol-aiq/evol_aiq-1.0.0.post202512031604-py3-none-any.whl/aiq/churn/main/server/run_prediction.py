from flask import Flask
# waitress import serve

from aiq.churn.main.server.PredictorServer import PredictorServer
import os

config = {
    "aiq_core": {
        "port": 5000,
        "auth_username": "admin",
        "auth_password": "admin",
        "model_data_gen_module": "aiq.churn.plugin.model.TestModelDataGen",
        "model_data_gen_class": "TestModelDataGen",
        "mysql": {
            "host": "localhost",
            "user": "root",
            "password": "root",
            "database": "aiqdb",
            "charset": "utf8",
            "pool_name": "AIQPool",
            "pool_size": 15
        }
    },
    "random_state": 42,
    "target_column": "Churn",
    "input_data_type": "file",
    "paths": {
        "model_registry": "artifacts/model_registry",
        "evaluation_report": "artifacts/reports/evaluation_metrics.json",
        "evaluation_plot": "artifacts/reports"
    },
    "plugins": {
        "cleaner_package": "qa.plugins.cleaner.QACleaner",
        "cleaner_class": "QACleaner",
        "explorer_package": "qa.plugins.explorer.QADataExplorer",
        "explorer_class": "QADataExplorer",
        "eda_package": "qa.plugins.eda.QAEDA",
        "eda_class": "QAEDA"
    },
    "required_columns": {
        "CustomerID": "Int64",
        "Churn": "Int8",
        "Tenure": "Int16",
        "PreferredLoginDevice": "category",
        "CityTier": "Int8",
        "WarehouseToHome": "Int16",
        "PreferredPaymentMode": "category",
        "Gender": "category",
        "HourSpendOnApp": "Int8",
        "NumberOfDeviceRegistered": "Int8",
        "PreferedOrderCat": "category",
        "SatisfactionScore": "Int8",
        "MaritalStatus": "category",
        "NumberOfAddress": "Int8",
        "Complain": "Int8",
        "OrderAmountHikeFromlastYear": "Int8",
        "CouponUsed": "Int8",
        "OrderCount": "Int8",
        "DaySinceLastOrder": "Int16",
        "CashbackAmount": "float64"
    },
    "columns_to_drop": ["CustomerID"],
    "data_split": {
        "test_size": 0.2
    },
    "feature_selection": {
        "active": True,
        "method": "permutation",
        "scoring": "roc_auc",
        "cv_folds": 5,
        "step": 1,
        "min_features": 10
    },
    "model": {
        "service_name": "churn",
        "active": "lightgbm",
        "lightgbm": {
            "boosting_type": "gbdt",
            "objective": "binary",
            "num_leaves": 63,
            "min_data_in_leaf": 20,
            "max_depth": 7,
            "learning_rate": 0.05,
            "n_estimators": 185,
            "subsample": 0.8,
            "reg_lambda": 0.1,
            "random_state": 42,
            "verbose": -1
        },
        "xgboost": {
            "booster": "gbtree",
            "max_depth": 5,
            "learning_rate": 0.08,
            "n_estimators": 150,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "random_state": 42
        }
    },
    "hyperparameter_tuning": {
        "active": False,
        "search_method": "random",
        "scoring": "roc_auc",
        "cv_folds": 5,
        "n_iter": 50,
        "lightgbm": {
            "param_grid": {
                "num_leaves": [31, 63, 127, 255],
                "max_depth": [5, 6, 7, 8],
                "min_data_in_leaf": [20, 50, 100, 200],
                "learning_rate": [0.01, 0.05, 0.1],
                "n_estimators": [200, 400, 600],
                "boosting_type": ["gbdt", "dart"],
                "subsample": [0.8, 1.0],
                "colsample_bytree": [0.8, 1.0],
                "reg_alpha": [0.0, 0.1, 0.5],
                "reg_lambda": [0.0, 0.1, 0.5]
            }
        },
        "xgboost": {
            "param_grid": {
                "max_depth": [3, 4, 5, 6, 7],
                "learning_rate": [0.01, 0.05, 0.1, 0.2],
                "min_child_weight": [1, 3, 5, 7],
                "n_estimators": [100, 120, 150],
                "gamma": [0, 0.1, 0.2, 0.5, 1],
                "subsample": [0.6, 0.7, 0.8, 0.9, 1.0],
                "colsample_bytree": [0.6, 0.7, 0.8, 0.9, 1.0],
                "reg_lambda": [0.1, 0.5, 1],
                "reg_alpha": [0, 0.1, 0.5, 1]
            }
        }
    },
    "learning_task": {
        "type": "classification"
    },
    "data_source": {
        "type": "directory",
        "file": {
            "type": "csv",
            "path": "data/churn_raw_data.csv",
            "archive_path": "data/archive"
        },
        "directory": {
            "path": "data/raw_data",
            "archive_path": "data/archive",
            "max_workers": 4
        },
        "hive": {
            "host": "10.150.1.33",
            "port": 10000,
            "auth": "NONE",
            "database": "data_db",
            "query": "SELECT * FROM churnTblA",
            "chunk_size": 5000,
            "output_file": "output.csv",
            "output_format": "csv",
            "max_retries": 3,
            "connect_timeout": 30
        }
    },
    "logging": {
        "trainer_app": {
            "log_file": "logs/trainer_app.log",
            "log_level": "INFO",
            "max_bytes": 10485760,
            "backup_count": 5
        }
    }
}



def load_app() -> Flask:
    predictor_server = PredictorServer(config)
    app = predictor_server.get_app()
    return app

dev_deploy = os.environ.get("dev_deploy", "true")
app: Flask = load_app()

if dev_deploy == "true":
    app.run(port=config['app_sever']["port"])
#else:
    #serve(app, host='127.0.0.1', port=5000, threads=8)

