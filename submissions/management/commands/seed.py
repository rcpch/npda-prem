from django.core.management.base import BaseCommand

from submissions.models import SubmissionPeriod
from django.utils import timezone

class Command(BaseCommand):
    help = "Seed database with open submission period for current year."

    def handle(self, *args, **options):
        now = timezone.now()
        current_year = now.year

        # Check if there's already an open submission period for the current year
        if SubmissionPeriod.objects.filter(year=current_year, is_open=True).exists():
            self.stdout.write(self.style.WARNING(f"An open submission period for {current_year} already exists."))
            return

        # Create a new submission period for the current year
        SubmissionPeriod.objects.create(year=current_year, is_open=True)
        self.stdout.write(self.style.SUCCESS(f"Created an open submission period for {current_year}."))