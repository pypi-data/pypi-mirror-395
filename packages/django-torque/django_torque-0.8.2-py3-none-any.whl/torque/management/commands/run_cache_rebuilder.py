from django.core.management.base import BaseCommand
from torque.cache_rebuilder import background


class Command(BaseCommand):
    help = "Starts the cache rebuilder"

    def handle(self, *args, **options):
        cache_rebuilder = background.CacheRebuilder()
        cache_rebuilder.run()
