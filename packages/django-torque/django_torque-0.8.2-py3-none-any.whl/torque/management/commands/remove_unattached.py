from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from torque.models import Field, Document, ValueEdit
import sys


class Command(BaseCommand):
    help = "Cleans out unattached fields and documents"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force running even if there are edits associated with affected fields/documents",
        )

    def handle(self, *args, **options):
        fields = Field.objects.filter(attached=False)
        documents = Document.objects.filter(attached=False)

        edits = ValueEdit.objects.filter(
            Q(value__field__attached=False) | Q(value__document__attached=False)
        )

        if edits.count() > 0:
            if not options["force"]:
                print("There are edits that will be deleted, use --force to continue")
                sys.exit(1)

        print("Removing %s fields" % fields.count())
        print("Removing %s documents" % documents.count())
        fields.delete()
        documents.delete()
