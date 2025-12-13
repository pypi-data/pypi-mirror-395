from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from job_template.constants import JobStatusEnum
from job_template.models import JobStatusConstant


class Command(BaseCommand):
    help = 'Populate JobStatusConstant table with status and corresponding code'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing status constants before populating',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating',
        )

    def handle(self, *args, **options):
        status_mappings = JobStatusEnum.to_dict()

        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING('DRY RUN - No changes will be made')
            )
            self.stdout.write('Would create/update the following status constants:')
            for status, code in status_mappings.items():
                self.stdout.write(f'{code} -> {status}')
            return

        try:
            with transaction.atomic():
                if options['clear']:
                    deleted_count, _ = JobStatusConstant.objects.all().delete()
                    self.stdout.write(
                        self.style.WARNING(f'Cleared {deleted_count} existing status constants')
                    )

                created_count = 0
                updated_count = 0

                for status, code in status_mappings.items():
                    obj, created = JobStatusConstant.objects.update_or_create(
                        status=status,
                        defaults={'code': code}
                    )
                    
                    if created:
                        created_count += 1
                        self.stdout.write(f'Created: {code} -> {status}')
                    else:
                        updated_count += 1
                        self.stdout.write(f'Updated: {code} -> {status}')

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully processed {len(status_mappings)} status constants '
                        f'({created_count} created, {updated_count} updated)'
                    )
                )

        except Exception as e:
            raise CommandError(f'Error populating status constants: {str(e)}')
