import cProfile
import io
import logging
import pstats
from sys import api_version
from flask import Blueprint, request, jsonify, Response
import orjson

from aiq.churn.main.server.services.ChurnService import ChurnService

api_version = "1"

logger = logging.getLogger(__name__)

def create_churn_bp_v1(churn_service: ChurnService):
    churn_bp = Blueprint('churn_bp', __name__, url_prefix='/churn/v1/')

    # POST /churn/v1/startTrain - JSON: {username, password}
    @churn_bp.route('/startTrain', methods=['POST'])
    def start_train():
        data = request.get_json()
        start_train_result = churn_service.start_train(data)
        return jsonify(start_train_result.to_dict(api_version)), 200

    # POST /churn/v1/publishModel - JSON: {model_name, service_name, model_version, username, password}
    @churn_bp.route('/publishModel', methods=['POST'])
    def publish_model():
        data = request.get_json()
        publish_model_result = churn_service.publish_model(data)
        return jsonify(publish_model_result.to_dict(api_version)), 200

    # POST /churn/v1/predict - JSON: {model_name, service_name, model_version, username, password}
    @churn_bp.route('/predict', methods=['POST'])
    def predict():
        #profiler = cProfile.Profile()
        #profiler.enable()

        data = request.get_json()
        prediction_result = churn_service.predict(data)
        result = prediction_result.to_dict(api_version)
        #profiler.disable()

        #stream = io.StringIO()
        #stats = pstats.Stats(profiler, stream=stream).sort_stats('cumtime')
        #stats.print_stats(20)  # Top 20 slowest functions

        # Log or return profiling results
        #print(stream.getvalue())  # Or write to a log
        #logger.info(stream.getvalue())

        return Response(orjson.dumps(result), content_type="application/json", status=200)
        #return jsonify(prediction_result.to_dict(api_version)), 200

    return churn_bp