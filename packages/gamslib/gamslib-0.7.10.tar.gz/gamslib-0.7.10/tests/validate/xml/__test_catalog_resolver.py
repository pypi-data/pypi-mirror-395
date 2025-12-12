"Tests for the XML catalog resolver."
import os
from gamslib.validate.xml.catalog_resolver import CatalogResolver
from lxml import etree
import pytest
from unittest import mock
#from gamslib.validate.xml.catalog_resolver import CatalogResolver


def test_get_local_schema_path_returns_posix_path():
    "Check if loading the local schema returns a valid posix path."
    schema_file = CatalogResolver.get_local_schema_path("http://www.w3c.org/1999/xlink")
    assert schema_file.endswith("resources/schemas/xlink.xsd")
    assert os.path.isfile(schema_file)
    assert schema_file.startswith("/") # absolute posix path


def test_get_local_schema_path_unknown_returns_none():
    "Check if an unknown schema URL returns None."
    assert CatalogResolver.get_local_schema_path("http://example.invalid/unknown.xsd") is None


def test_resolver_resolves_local_schema():
    "Check if the resolver resolves a known schema URL."
    catalog_resolver = CatalogResolver()
    resolved_doc = catalog_resolver.resolve(
        "http://www.w3.org/2001/XMLSchema", None, None
    )
    assert resolved_doc is not None


def test_resolve_downloads_allowed_url(monkeypatch):
    """Test resolve downloads and returns schema for allowed URLs."""
    resolver_ = CatalogResolver()
    allowed_url = "http://gams.uni-graz.at/schema.xsd"
    fake_content = b"<schema/>"
    # Patch _get_local_schema_path to return None (not found locally)
    #monkeypatch.setattr(resolver_, "_get_local_schema_path", lambda url: None)
    # Patch _is_allowed_schema_url to True
    #monkeypatch.setattr(resolver_, "_is_allowed_schema_url", lambda url: True)
    # Patch requests.get to return a mock response
    mock_response = mock.Mock()
    mock_response.content = fake_content
    mock_response.raise_for_status = mock.Mock()
    with mock.patch("requests.get", return_value=mock_response):# as mock_get: #, \
            #mock.patch.object(resolver_, "resolve_string", return_value="remote_schema_doc") as mock_resolve_string:
        parser = etree.XMLParser() 
        parser.resolvers.add(CatalogResolver())
        schema_doc = etree.parse(BytesIO(fake_content), parser)
        assert etree.tostring(schema_doc) == fake_content
        #
        # XML-Schema und XML-Dokument laden und validieren  
        #schema_path = '/pfad/zum/ihrem/schema.xsd'  
        #xml_path = '/pfad/zum/ihrem/xml.xml'  
        #with open(schema_path, 'rb') as f:  
        #    schema_doc = etree.parse(f, parser) 




        #result = resolver_.resolve(allowed_url, None, None)
        #result_document = lxml.etree.parse(result)
        #lxml.etree.tostring(result_document) ==  fake_content.decode("utf-8")
        
        #mock_get.assert_called_once_with(allowed_url, timeout=10)
        #mock_resolve_string.assert_called_once_with(fake_content, None)
        #print(result)
        #assert lxml.etree.compare_xml(result.getroot(), lxml.etree.fromstring(fake_content))    
        #assert lxml.etree.tostring(result.getroot()) == fake_content.decode("utf-8") #result == "remote_schema_doc"


# Same problem as above: we need a way to test referenced external resources (and not the resource itself)
def test_resolve_handles_download_error(monkeypatch):
    """Test resolve returns None and prints error if download fails."""
    resolver = CatalogResolver()
    allowed_url = "http://gams.uni-graz.at/schema.xsd"
    monkeypatch.setattr(resolver, "get_local_schema_path", lambda url: None)
    monkeypatch.setattr(resolver, "is_allowed_schema_url", lambda url: True)
    with mock.patch("requests.get", side_effect=Exception("network error")), \
            mock.patch("builtins.print") as mock_print:
        result = resolver.resolve(allowed_url, None, None)
        assert result is None
        assert mock_print.called

def test_resolve_returns_none_for_disallowed_url(monkeypatch):
    """Test resolve returns None for URLs not allowed and not mapped."""
    resolver = CatalogResolver()
    disallowed_url = "http://not-allowed.com/schema.xsd"
    monkeypatch.setattr(resolver, "get_local_schema_path", lambda url: None)
    monkeypatch.setattr(resolver, "is_allowed_schema_url", lambda url: False)
    result = resolver.resolve(disallowed_url, None, None)
    assert result is None
