from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("name")  # 第1引数
        parser.add_argument("age")  # 第2引数
        parser.add_argument("--birthday")

    def handle(self, *args, **options):
        name = options["name"]
        age = options["age"]
        birthday = options["birthday"]
        print(f"name = {name}, age = {age}, birthday = {birthday}")
