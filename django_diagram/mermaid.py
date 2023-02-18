from enum import Enum


class FirstToSecondCardinality(Enum):
    ZERO_OR_ONE = "|o"
    EXACTLY_ONE = "||"
    ZERO_OR_MORE = "}o"
    ONE_OR_MORE = "}|"


class SecondToFirstCardinality(Enum):
    ZERO_OR_ONE = "o|"
    EXACTLY_ONE = "||"
    ZERO_OR_MORE = "o{"
    ONE_OR_MORE = "|{"


class Identity(Enum):
    IDENTIFYING = "--"
    NON_IDENTIFYING = ".."


class Relationship:
    def __init__(
        self,
        first_entity: str,
        first_to_second_cardinality: FirstToSecondCardinality,
        second_to_first_cardinality: SecondToFirstCardinality,
        second_entity: str,
        identity: Identity = None,
        label: str = "",
    ):
        self.first_entity = first_entity
        self.first_to_second_cardinality = first_to_second_cardinality
        self.second_to_first_cardinality = second_to_first_cardinality
        self.second_entity = second_entity
        self.identity = identity or Identity.IDENTIFYING
        self.label = label or '""'

    @property
    def link(self) -> str:
        return f"{self.first_to_second_cardinality.value}{self.identity.value}{self.second_to_first_cardinality.value}"

    def render(self) -> str:
        return f"{self.first_entity} {self.link} {self.second_entity} : {self.label}"


class Attribute:
    def __init__(self, attribute_name: str, attribute_type: str):
        self.attribute_name = attribute_name
        self.attribute_type = attribute_type

    def render(self) -> str:
        return f"{self.attribute_type} {self.attribute_name}"


class Entity:
    def __init__(self, name: str, attributes: list[Attribute] = None):
        self.name = name
        self.attributes = attributes or []

    def render(self) -> str:
        return "\n".join(
            [
                f"{self.name} {{",
            ]
            + [f"    {attribute.render()}" for attribute in self.attributes]
            + [
                "}",
            ]
        )


class MermaidERD:
    def __init__(self, title: str):
        self.title = title
        self.entities = []
        self.relationships = []

    def add_relationship(self, relationship: Relationship):
        self.relationships.append(relationship)

    def add_entity(self, entity: Entity):
        self.entities.append(entity)

    def render(self) -> str:
        return "\n".join(
            [
                f"---\n{self.title}\n---",
                "erDiagram",
            ]
            + [entity.render() for entity in self.entities]
            + [relationship.render() for relationship in self.relationships]
        )
