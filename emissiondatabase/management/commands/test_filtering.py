from django.core.management.base import BaseCommand
from emissiondatabase.models import Contributor
from emissiondatabase.filters import ContributorFilter

class Command(BaseCommand):
    help = 'Test filtering on Contributor model'

    def handle(self, *args, **kwargs):
        # Define the filter parameters
        filter_params = {'name': 'Ram'}

        # Apply the filter
        contributor_filter = ContributorFilter(filter_params, queryset=Contributor.objects.all())
        filtered_contributors = contributor_filter.qs

        # Print the filtered query
        self.stdout.write(f'Filtered Query: {filtered_contributors.query}')

        # Print the results
        for contributor in filtered_contributors:
            self.stdout.write(f'{contributor.name} - {contributor.organization}')
