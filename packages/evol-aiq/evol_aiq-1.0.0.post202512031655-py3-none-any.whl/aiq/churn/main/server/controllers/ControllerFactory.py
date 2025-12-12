from flask import Blueprint

from aiq.churn.main.server.controllers.v1.ChurnController import create_churn_bp_v1

def create_churn_bp(churn_service, api_version: str) -> Blueprint | None:
    match api_version:
        case '1':
            return create_churn_bp_v1(churn_service)
    return None