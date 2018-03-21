import json
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "This command is used to teach students how to write Django commands. This is known as the help text."

    def add_arguments(self, parser):
        #parser.add_argument('data_input', type=str)
        parser.add_argument('json_file', type=str)

    def handle(self, *args, **options):
        #data = options['data_input']
        #self.stdout.write(data)
        data = json.load(open(options['json_file']))
        self.stdout.write("Found {} rows". format(len(data)))
