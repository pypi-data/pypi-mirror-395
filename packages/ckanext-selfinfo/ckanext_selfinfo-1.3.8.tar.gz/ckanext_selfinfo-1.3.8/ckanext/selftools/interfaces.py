from __future__ import annotations

from typing import Any

from ckan.plugins import Interface


class ISelftools(Interface):
    """Implement custom Selftools response modification."""

    def selftools_db_models(self, models_list: list[Any]) -> list[Any]:
        """Return DB models list.
        This method is called after the models list is prepared and before it is returned.
        Useful if you want to add additional models or custom models.
        :returns: list
        :rtype: list

        """

        return models_list
