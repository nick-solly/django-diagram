import unittest
from textwrap import dedent

from django_diagram.mermaid import (
    Attribute,
    Entity,
    FirstToSecondCardinality,
    Identity,
    MermaidERD,
    Relationship,
    SecondToFirstCardinality,
)


class TestMermaid(unittest.TestCase):
    def test_render(self):
        """A test to render a simple ERD"""
        erd = MermaidERD("Test Diagram")
        erd.add_entity(
            Entity("A", [Attribute("x", "string"), Attribute("y", "integer")])
        )
        erd.add_entity(Entity("B", [Attribute("z", "string")]))
        erd.add_relationship(
            Relationship(
                "A",
                FirstToSecondCardinality.ONE_OR_MORE,
                SecondToFirstCardinality.ZERO_OR_ONE,
                "B",
                Identity.IDENTIFYING,
                "label",
            )
        )
        expected = dedent(
            """\
            ---
            Test Diagram
            ---
            erDiagram
            A {
                string x
                integer y
            }
            B {
                string z
            }
            A }|--o| B : label"""
        )
        self.assertEqual(erd.render(), expected)


if __name__ == "__main__":
    unittest.main()
