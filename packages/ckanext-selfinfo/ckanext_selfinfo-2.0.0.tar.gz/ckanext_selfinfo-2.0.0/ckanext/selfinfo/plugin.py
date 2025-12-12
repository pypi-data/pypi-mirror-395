import ckan.plugins as plugins
import ckan.plugins.toolkit as tk
from ckan.common import CKANConfig

from .logic import action
from . import cli


@tk.blanket.config_declarations
@tk.blanket.cli(cli.get_commands)
@tk.blanket.actions(action.get_actions)
@tk.blanket.blueprints
@tk.blanket.helpers
class SelfinfoPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    # IConfigurer

    def update_config(self, config_: CKANConfig):
        tk.add_template_directory(config_, "templates")
        tk.add_public_directory(config_, "public")
        tk.add_resource("assets", "selfinfo")
