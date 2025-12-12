"""
This module implements a catalog resolver for XML schema validation.

libxml2 version 2.14.0 started to enforce the use of XML catalogs for
resolving external entities. This class provides a resolver that uses
a specified catalog file to resolve schema locations.
"""

from importlib import resources as impresources
import logging
import re
from typing import Any
from lxml import etree
import requests
from io import BytesIO


logger = logging.getLogger(__name__)

# Map schema urls to local schema files
# The paths are relative to the gamslib.validate.xml package
SCHEMA_MAP = {
    "http://www.w3.org/2001/XMLSchema": "resources/schemas/XMLSchema.xsd",
    "http://www.w3c.org/1999/xlink": "resources/schemas/xlink.xsd",
    "http://www.loc.gov/mets/mets.xsd": "resources/schemas/mets.xsd",   
    "https://www.loc.gov/standards/xlink/xlink.xsd": "resources/schemas/xlink.xsd",
}

# It is ok to load a schema from the internet if matching one of these urls
ALLOWD_SCHEMA_URLS = [
    r"^https?://gams.uni-graz.at/.*",
    r"^https?://gams-staging.uni-graz.at/.*",
    r"^https?://localhost/.*",
]


class CatalogResolver(etree.Resolver):
    """A dynamic XML catalog resolver for lxml to resolve external entities.

    This class extends `etree.Resolver` to provide custom resolution of external XML entities
    using a local catalog. It intercepts requests for external resources (such as DTDs or schemas)
    and attempts to resolve them to local files, improving performance and reliability.

    The local schema files are mapped in the `SCHEMA_MAP` dictionary defined in this module.

    """

    def resolve(self, system_url: str, public_id: str | None, context: Any) -> str | None:
        """Resolve the system ID using the catalog.

        Args:
            url (str): The system ID (URL) to resolve.
            public_id (str | None): The public ID (not used, kept for compatibility).
            context (Any): The parser context (not used, kept for compatibility).

        Returns:
            str | None: The resolved local filename, or None if not found.
            url: The system ID (url) to resolve.
            public_id: The public ID (not used - kept for compatibility).
            context: The parser context (not used - kept for compatibility).
        """
        # load from file
        schema_path = self.get_local_schema_path(system_url)
        if schema_path is not None:
            return self.resolve_filename(schema_path, context)
        
        # locally not found, check if loading from internet is allowed
        if self.is_allowed_schema_url(system_url): 
            try:
                response = requests.get(system_url, timeout=10)
                response.raise_for_status()
                return self.resolve_string(response.content, context)
            except requests.RequestException as e:
                    logger.warning("Fehler beim Herunterladen der Ressource %s: %s", system_url, e)    
                    return None
        return None

    def resolve_string(self, data: bytes, context: Any) -> Any:  # etree._InputDocument:
        """Resolve the data from a byte string.

        :param data: The byte string containing the XML data.
        :param context: The parser context.
        :return: An _InputDocument containing the XML data.
        """
        return self.resolve_file(BytesIO(data), context)

    @classmethod
    def is_allowed_schema_url(cls, schema_url: str) -> bool:
        """Check if the schema URL is allowed to be loaded directly from the internet.

        :param schema_url: The URL of the schema.
        :return: True if the URL is allowed, False otherwise.
        """
        return any(re.match(pattern, schema_url) for pattern in ALLOWD_SCHEMA_URLS)

    @classmethod
    def get_local_schema_path(cls, schema_url: str) -> str | None:
        """Get the local schema file path for a given schema URL.

        :param schema_url: The URL of the schema.
        :return: The local file path of the schema, or None if not found.
        """
        if schema_url in SCHEMA_MAP:
            with impresources.path(
                "gamslib.validate.xml", SCHEMA_MAP[schema_url]
            ) as schema_path:
                return schema_path.as_posix()   
        return None