from flask import Blueprint, Flask

blueprint: Blueprint

def create_audit_logs_blueprint(app: Flask) -> Blueprint: ...
