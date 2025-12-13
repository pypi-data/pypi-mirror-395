from django.apps import AppConfig


JOB_STATUS_PK_MAP = {}


class JobTemplateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'job_template'

    def ready(self):
        # Load data on startup if tables already exist (e.g., when deploying after local migrations)
        load_data_if_tables_exist()


def tables_exist(table_names):
    """Helper function to check if the tables exist in the database."""
    from django.db import connection
    with connection.cursor():
        existing_tables = connection.introspection.table_names()
        return all(table in existing_tables for table in table_names)


def load_data_if_tables_exist():
    required_tables = ['job_status_constant']
    if tables_exist(required_tables):
        load_data()


def load_data():
    global JOB_STATUS_PK_MAP
    from .models import JobStatusConstant

    JOB_STATUS_PK_MAP = {
        obj['code']: obj['id']
        for obj in JobStatusConstant.objects.values('id', 'code')
    }
