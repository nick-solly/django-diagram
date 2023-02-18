import argparse
import os

from django_diagram.app import App

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a Mermaid Entity Relationship Diagram for Django Models",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-s",
        "--settings",
        type=str,
        required=False,
        default="",
        help="Override Django Settings Module",
    )
    parser.add_argument(
        "-t",
        "--title",
        type=str,
        required=False,
        default="",
        help="Diagram Title",
    )
    parser.add_argument(
        "-a",
        "--app",
        type=str,
        required=False,
        default="",
        help="Django app name",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=False,
        default="",
        help="Output file name",
    )

    args = parser.parse_args()

    django_settings_module = args.settings or os.environ.get("DJANGO_SETTINGS_MODULE")
    if not django_settings_module:
        raise Exception(
            "No Django Settings Module - either set the environment variable DJANGO_SETTINGS_MODULE or use the --settings argument."
        )

    app = App(
        django_settings_module=django_settings_module,
        title=args.title,
        app_name=args.app,
        output=args.output,
    )

    app.run()
