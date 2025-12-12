from __future__ import annotations

from typing import Optional, Any

from ckan.plugins import Interface


class ISelfinfo(Interface):
    """Implement custom Selfinfo response modification."""

    def selfinfo_after_prepared(
        self, data: dict[str, Optional[Any]]
    ) -> dict[str, Optional[Any]]:
        """Return selinfo data.
        This method is called after the data is prepared and before it is returned.
        Useful if you want to anonymize the data or extend.
        :returns: dictionary
        :rtype: dict

        """

        return data
