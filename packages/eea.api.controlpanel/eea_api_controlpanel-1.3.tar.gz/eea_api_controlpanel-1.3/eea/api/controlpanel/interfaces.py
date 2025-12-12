"""Module where all interfaces, events and exceptions live."""

from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from eea.api.controlpanel import EEAMessageFactory as _


class IEeaApiControlpanelLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IEEAVersionsBackend(Interface):
    """Registry record for the backend versions"""

    date = schema.Datetime(
        title=_("Date of last version update"),
        description=("The date when the version was last updated"),
        required=True,
    )

    version = schema.Text(
        title=_("Current version"),
        description=("The latest version that exists"),
        required=True,
    )

    old_version = schema.Text(
        title=_("Previous version"),
        description=("The version that was previously"),
        required=False,
    )


class IEEAVersionsFrontend(Interface):
    """Registry record for the frontend versions"""

    date = schema.Datetime(
        title=_("Date of last version update"),
        description=("The date when the version was last updated"),
        required=True,
    )

    version = schema.Text(
        title=_("Current version"),
        description=("The latest version that exists"),
        required=True,
    )

    old_version = schema.Text(
        title=_("Previous version"),
        description=("The version that was previously"),
        required=False,
    )
