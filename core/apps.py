from django.apps import AppConfig
import os

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Run migrations only once in production
        if os.environ.get('RUN_MAIN') != 'true':  # prevent double run in dev
            return

        from django.db import connections
        from django.db.utils import OperationalError
        from django.core.management import call_command

        try:
            db_conn = connections['default']
            db_conn.ensure_connection()
        except OperationalError:
            print("⛔ DB not ready. Skipping migrations.")
            return

        print("🔄 Running migrate from apps.py...")
        try:
            call_command('migrate', interactive=False)
            print("✅ Migrations done!")
        except Exception as e:
            print(f"⚠️ Error running migrations: {e}")
