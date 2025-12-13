from django.core.cache import cache
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Purges the entire cache."

    def handle(self, *args, **options):
        self.stdout.write("Purging cache...")

        try:
            cache.clear()
            self.stdout.write(self.style.SUCCESS("Successfully purged cache."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to purge cache: {e}"))
