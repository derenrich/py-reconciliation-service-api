from typing import List, Optional

from . import BaseSchema


class UrlView(BaseSchema):
    url: str


class ManifestType(BaseSchema):
    id: str
    name: str


class PreviewManifest(BaseSchema):
    url: str
    width: int
    height: int


class SuggestServiceManifestEntry(BaseSchema):
    service_url: Optional[str] = None
    service_path: Optional[str] = None
    flyout_service_url: Optional[str] = None
    flyout_service_path: Optional[str] = None


class SuggestServiceManifest(BaseSchema):
    entity: Optional[SuggestServiceManifestEntry] = None
    property: Optional[SuggestServiceManifestEntry] = None
    type: Optional[SuggestServiceManifestEntry] = None


class Manifest(BaseSchema):
    versions: List[str]
    name: str
    identifier_space: str
    schema_space: str
    documentation: Optional[str] = None
    service_version: Optional[str] = None
    logo: Optional[str] = None
    view: Optional[UrlView] = None
    feature_view: Optional[UrlView] = None
    default_types: Optional[List[ManifestType]] = None
    preview: Optional[PreviewManifest] = None
    suggest: Optional[SuggestServiceManifest] = None
    batch_size: Optional[int] = None
    # TODO:
    #  - extend is not yet supported
    #  - authentication is not yet supported
