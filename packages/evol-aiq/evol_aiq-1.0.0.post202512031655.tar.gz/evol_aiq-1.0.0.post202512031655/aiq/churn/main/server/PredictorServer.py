import os
import threading
from datetime import datetime
import time
import psutil
import json

from flask import Flask, request, jsonify
import logging
from aiq.churn.main.server.controllers.ControllerFactory import create_churn_bp
from aiq.churn.main.server.services.ChurnService import ChurnService



class PredictorServer:
    logger = logging.getLogger(__name__)
    churn_service: ChurnService = None
    app: Flask = None
    config: dict = None

    def monitor_resources(self):
        interval = 10
        process = psutil.Process(os.getpid())
        while True:
            process = psutil.Process(os.getpid())

            # Collect metrics
            metrics = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "cpu_percent": process.cpu_percent(interval=interval),
                "memory_mb": round(process.memory_info().rss / (1024 * 1024), 2),
                "memory_percent": round(process.memory_percent(), 2),
                "io": {
                    "read_count": process.io_counters().read_count,
                    "write_count": process.io_counters().write_count,
                    "read_bytes": process.io_counters().read_bytes,
                    "write_bytes": process.io_counters().write_bytes
                },
                "threads": process.num_threads(),
                "context_switches": {
                    "voluntary": process.num_ctx_switches().voluntary,
                    "involuntary": process.num_ctx_switches().involuntary
                },
                "open_files": len(process.open_files())
            }
            log_line = json.dumps(metrics, separators=(',', ':'))
            self.logger.error(log_line)
            time.sleep(1)

    def __init__(self, config: dict):
        self.app = Flask(__name__)
        self.config = config

        # Monitor perf matrix
        monitor_thread = threading.Thread(target=self.monitor_resources, )
        monitor_thread.start()

        churn_service = ChurnService(config)
        self.app.register_blueprint(create_churn_bp(churn_service, "1"))

        # --- Register Auth Filter ---
        self._register_auth_filter()

    def _register_auth_filter(self):
        """Global authentication filter using before_request"""

        @self.app.before_request
        def auth_filter():
            # Allow health or public routes without auth if needed
            if request.endpoint in ['health_check']:
                return None

            try:
                data = request.get_json(silent=False) or {}
            except Exception:
                return jsonify({"error": "Invalid JSON"}), 400

            username = data.get("username")
            password = data.get("password")
            

            # Basic authentication check (replace with your real logic)
            if username != self.config['aiq_core']["auth_username"] or password != self.config['aiq_core']["auth_password"]:
                return jsonify({"error": "Unauthorized"}), 401
            return None

    def run(self):
        self.app.run(port=self.config['port'], host=self.config['host'])

    def get_app(self) -> Flask:
        return self.app
