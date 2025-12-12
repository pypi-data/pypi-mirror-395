import os

HOME = os.path.expanduser("~")

CONFIG_PATH = os.path.join(HOME, ".config/odoo_deets.toml")

DECIMAL_PLACES = 6

TABLE_LIMIT = 25

OUTPUT_FOLDER = os.path.join(HOME, "deets_profiles/")

IMPORT_TXT = "from odoo_deets import deets_profile\n"

CSS_URL = "https://odoo-deets-d15440.gitlab.io/styles.css"

DECORATOR_TXT = "    @deets_profile\n"

INJECT_PATHS = {
    "16.0": {
        "file": "odoo/odoo/api.py",
        "decorator_line": 1282,
        "import_line": 25,
        "checks": [(1281, "def clear(self):")],
    },
    "17.0": {
        "file": "odoo/odoo/api.py",
        "decorator_line": 1322,
        "import_line": 25,
        "checks": [(1321, "def clear(self):")],
    },
    "18.0": {
        "file": "odoo/odoo/api.py",
        "decorator_line": 1481,
        "import_line": 9,
        "checks": [(1480, "def clear(self):")],
    },
}
