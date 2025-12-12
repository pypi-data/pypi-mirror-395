import logging

from aiq.churn.plugin.model.ModelDataGenerator import ModelDataGenerator


class TestModelDataGen(ModelDataGenerator):
    logger = logging.getLogger(__name__)
    def __init__(self):
        super().__init__()

    def generate_model_readable_data(self, data: dict) -> dict | None:
        return data