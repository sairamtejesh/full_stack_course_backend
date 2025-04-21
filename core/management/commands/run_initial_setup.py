from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Run initial setup like migrations'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("🔄 Running initial migrations..."))
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS("✅ Migrations complete!"))
