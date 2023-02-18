# django-diagram
Generate an Entity Relationship Diagram for a Django project in Mermaid format

![logo.png](logo.png)

## Installation

You can install via pip:

```bash
pip install django-diagram
```

## Usage

Navigate to the directory containing your Django project (the folder containing manage.py) and run:

```bash
python -m django_diagram
```

The following options are available:

`--settings=project.settings.local` - The dotted path to the settings module
(either this option must be provided or the `DJANGO_SETTINGS_MODULE` environment
variable must be set)

`--title="My Title"` - The title to use for the diagram

`--app=app_name` - Restrict to only a particular Django app

`--output=diagram.txt` - The output file to write the diagram, if this option
is not provided the output will be written to stdout
