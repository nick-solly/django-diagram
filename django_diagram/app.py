import os

import django
from django.apps import apps
from django.db.models import Model

from django_diagram.mermaid import (
    Attribute,
    Entity,
    FirstToSecondCardinality,
    Identity,
    MermaidERD,
    Relationship,
    SecondToFirstCardinality,
)


class App:

    RELATIONSHIP_MAP = {
        "ForeignKey": (
            FirstToSecondCardinality.ONE_OR_MORE,
            SecondToFirstCardinality.EXACTLY_ONE,
        ),
        "ManyToManyField": (
            FirstToSecondCardinality.ONE_OR_MORE,
            SecondToFirstCardinality.ONE_OR_MORE,
        ),
        "OneToOneField": (
            FirstToSecondCardinality.EXACTLY_ONE,
            SecondToFirstCardinality.EXACTLY_ONE,
        ),
    }

    DEFAULT_TITLE = "Django ER Diagram"

    def __init__(
        self,
        django_settings_module: str,
        title: str = "",
        app_name: str = "",
        output: str = "",
    ):
        os.environ["DJANGO_SETTINGS_MODULE"] = django_settings_module
        django.setup()
        self.mermaid = MermaidERD(title or self.DEFAULT_TITLE)
        self.app_name = app_name
        self.output = output

    def process_relationship(
        self, model: Model, field_name: str, field_type: str, field_related_model: Model
    ) -> None:
        (
            first_to_second_cardinality,
            second_to_first_cardinality,
        ) = self.RELATIONSHIP_MAP[field_type]
        self.mermaid.add_relationship(
            Relationship(
                first_entity=model.__name__,
                second_entity=field_related_model.__name__,
                first_to_second_cardinality=first_to_second_cardinality,
                second_to_first_cardinality=second_to_first_cardinality,
                identity=Identity.IDENTIFYING,
                label=field_name,
            )
        )

    def process_attributes(self, model: Model) -> list[Attribute]:
        attributes = []
        for field in model._meta.get_fields():
            if not field.concrete:
                continue
            field_name, field_type, field_related_model = (
                field.name,
                field.get_internal_type(),
                field.related_model,
            )
            attributes.append(
                Attribute(
                    attribute_name=field_name,
                    attribute_type=field_type,
                )
            )
            if field_related_model:
                self.process_relationship(
                    model,
                    field_name,
                    field_type,
                    field_related_model,
                )

        return attributes

    def process_models(self) -> None:
        for model in apps.get_models():
            if self.app_name and model._meta.app_label != self.app_name:
                continue
            attributes = self.process_attributes(model)
            self.mermaid.add_entity(
                Entity(
                    name=model.__name__,
                    attributes=attributes,
                )
            )

    def create_diagram(self) -> str:
        self.process_models()
        return self.mermaid.render()

    def run(self):
        diagram = self.create_diagram()
        if not self.output:
            print(diagram)
            return
        with open(self.output, "w") as f:
            f.write(diagram)
