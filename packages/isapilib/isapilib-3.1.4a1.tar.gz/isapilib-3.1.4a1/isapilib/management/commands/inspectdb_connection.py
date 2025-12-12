from django.core.management.commands.inspectdb import Command as InspectDBCommand

from isapilib.api.models import ConnectionAPI


class Command(InspectDBCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "connection",
            help="Nominates a ConnectionAPI primary key to introspect",
            type=int,
        )
        parser.add_argument(
            "table",
            nargs="*",
            type=str,
            help="Selects what tables or views should be introspected.",
        )
        parser.add_argument(
            "--include-partitions",
            action="store_true",
            help="Also output models for partition tables.",
        )
        parser.add_argument(
            "--include-views",
            action="store_true",
            help="Also output models for database views.",
        )

    def handle_inspection(self, options):
        connection_pk = options.pop("connection")
        connection = ConnectionAPI.objects.get(pk=connection_pk)
        options['database'] = connection.create_connection()
        return super().handle_inspection(options)

    def normalize_col_name(self, col_name, used_column_names, is_relation):
        new_name, field_params, field_notes = super().normalize_col_name(col_name, used_column_names, is_relation)
        return new_name, field_params, []
