import os
import sys
import unittest
from textwrap import dedent

from django_diagram.app import App


class TestApp(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super(TestApp, cls).setUpClass()
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "example_site"))

    def test_example_site(self):
        app = App(
            django_settings_module="example_site.settings",
            title="Example Site",
        )
        self.assertEqual(
            app.create_diagram(),
            dedent(
                """\
                ---
                Example Site
                ---
                erDiagram
                ContentType {
                    AutoField id
                    CharField app_label
                    CharField model
                }
                Session {
                    CharField session_key
                    TextField session_data
                    DateTimeField expire_date
                }
                ItemType {
                    BigAutoField id
                    CharField name
                }
                Item {
                    BigAutoField id
                    CharField name
                    IntegerField weight
                    ManyToManyField item_types
                }
                Buyer {
                    BigAutoField id
                    CharField name
                }
                Purchase {
                    BigAutoField id
                    OneToOneField item
                    ForeignKey buyer
                    IntegerField price
                }
                Location {
                    BigAutoField id
                    OneToOneField item
                    CharField shelf
                }
                Item }|--|{ ItemType : item_types
                Purchase ||--|| Item : item
                Purchase }|--|| Buyer : buyer
                Location ||--|| Item : item"""
            ),
        )

    def test_single_app(self):
        app = App(
            django_settings_module="example_site.settings",
            title="Example Site",
            app_name="inventory",
        )
        self.assertEqual(
            app.create_diagram(),
            dedent(
                """\
                ---
                Example Site
                ---
                erDiagram
                Location {
                    BigAutoField id
                    OneToOneField item
                    CharField shelf
                }
                Location ||--|| Item : item"""
            ),
        )


if __name__ == "__main__":
    unittest.main()
