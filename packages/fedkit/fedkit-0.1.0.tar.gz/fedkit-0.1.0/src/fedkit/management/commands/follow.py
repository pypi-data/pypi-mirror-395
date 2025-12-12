from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "follow somebody on the fediverse"

    def add_arguments(self, parser):
        """
        add arguments to the command

        args:
            ID to follow.

        use like this:
            parser.add_argument('feeds', nargs='+', type=int)
        """
        parser.add_argument("fediverseid", nargs="+", type=str)

    def handle(self, *args, **options):
        """
        handle the command

        args:
            args: arguments
            options: options
        """
        for fediverseid in options["fediverseid"]:
            self.stdout.write(f"Following {fediverseid}...")
            # follow somebody
            from fedkit.tasks import requestFollow

            requestFollow("https://pramari.de/@andreas", fediverseid)
            self.stdout.write(self.style.SUCCESS("Successfully followed!"))
