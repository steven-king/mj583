import csv
import datetime
from decimal import Decimal
import json

from django.core.management.base import BaseCommand, CommandError
from nobel.winners.models import Country

class Command(BaseCommand):
    help = 'Load country data'

    def add_arguments(self, parser):
        parser.add_argument('country_data_json', type=str)
        parser.add_argument('country_id_csv', type=str)

    def handle(self, *args, **options):
        json_path = options['country_data_json']
        csv_path = options['country_id_csv']

        csvreader = csv.reader(open(csv_path, encoding="utf-8"))
        # Cut off the header the make a list of id / name pairs
        country_ids = list(csvreader)[1:]

        # Convert to dictionary by name
        country_ids = {x[1]: x[0] for x in country_ids}

        by_country = json.load(open(json_path, encoding="utf-8"))

        for c in Country.objects.all():
            data = by_country.get(c.name)
            cid = country_ids.get(c.name)
            if not data:
                self.stderr.write(self.style.ERROR("Could not find data for {}".format(c.name)))
                continue
            
            if not cid:
                self.stderr.write(self.style.ERROR("Could not find id for {}".format(c.name)))
                continue
            
            c.alpha_code = data["alpha3Code"]  # AFG
            c.numeric_code = '{:03d}'.format(int(cid))  # "4" -> "004"
            c.lat = str(Decimal(data["latlng"][0]))[:10]
            c.lng = str(Decimal(data["latlng"][1]))[:10]
            c.save()
            self.stdout.write(self.style.SUCCESS("Added data for {}".format(c.name)))


        