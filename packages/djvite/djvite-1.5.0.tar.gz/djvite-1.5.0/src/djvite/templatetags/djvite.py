from collections.abc import Iterable
from dataclasses import dataclass
from functools import cache
from json import load
from pathlib import Path
from typing import Literal
from typing import NotRequired
from typing import Protocol
from typing import Self
from typing import TypedDict
from typing import cast

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe


class Config(TypedDict):
    DEV_MODE: bool
    MODULE_EXTS: Iterable[str]
    VITE_MANIFEST_PATH: Path | str


default_config = Config(
    DEV_MODE=True,
    MODULE_EXTS=['.js'],
    VITE_MANIFEST_PATH=Path('vite.manifest.json'),
)


@cache
def config() -> Config:
    cfg = getattr(settings, 'DJVITE', {})
    if not isinstance(cfg, dict):
        raise ValueError("DJVITE config setting should be a dictionary")
    for key, value in default_config.items():
        if cfg.get(key) is None:
            cfg[key] = value
    return cast(Config, cfg)


@cache
def is_dev_mode() -> bool:
    return bool(config()['DEV_MODE'])


@cache
def get_module_exts() -> list[str]:
    return list(config()['MODULE_EXTS'])


@cache
def get_vite_manifest_path() -> Path:
    path = config()['VITE_MANIFEST_PATH']
    match path:
        case Path():
            return path
        case str():
            return Path(path)


# Manifest definition and usage: https://vite.dev/guide/backend-integration.html
type Filename = str
type FileId = str
type ScriptType = Literal['module', 'modulepreload']
type StrOrVar = str | template.Variable
type Attrs = dict[str, StrOrVar]
type Assets = list[str]


class ChunkManifest(TypedDict):
    file: Filename
    isEntry: NotRequired[bool]
    isDynamicEntry: NotRequired[bool]
    name: NotRequired[str]
    src: NotRequired[Filename]
    imports: NotRequired[list[FileId]]
    dynamicImports: NotRequired[list[FileId]]
    css: NotRequired[list[Filename]]
    assets: NotRequired[list[Filename]]


type Manifest = dict[str, ChunkManifest]


@dataclass
class HtmlTag:
    name: str
    auto_close: bool
    attrs: Attrs

    def to_html(self, context: template.Context) -> str:
        attr_lst = list[str]()
        for key, value in sorted(self.attrs.items()):
            value_resolved = value.resolve(context) if isinstance(value, template.Variable) else value
            if value_resolved is True or str(value_resolved).lower() in ('true', '1', 'on'):
                attr_lst.append(key)
            else:
                attr_lst.append(f'{key}="{value_resolved}"')
        attributes = ' '.join(attr_lst)
        end_tag = '/>' if self.auto_close else f'></{self.name}>'
        return f'<{" ".join((self.name, attributes))}{end_tag}'

    def __hash__(self) -> int:
        parts = [self.name, self.auto_close]
        for k, v in self.attrs.items():
            parts.append(k)
            parts.append(v)
        return hash(tuple(parts))

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)


class AssetRenderer(Protocol):
    def get_tags(self, attrs: Attrs, assets: Assets) -> list[HtmlTag]: ...

    @staticmethod
    def get_ext(name: str) -> str:
        return Path(name).suffix


class DevAssetRenderer(AssetRenderer):
    def get_tags(self, attrs: Attrs, assets: Assets) -> list[HtmlTag]:
        tags = list[HtmlTag]()
        module_exts = get_module_exts()
        for asset in assets:
            tag: HtmlTag | None
            if asset == 'hotreload':
                tag = HtmlTag(
                    'script',
                    False,
                    {
                        'src': '/@vite/client',
                        'type': 'module',
                    },
                )
            elif self.get_ext(asset) in module_exts:
                tag = HtmlTag(
                    'script',
                    False,
                    attrs
                    | {
                        'src': asset,
                        'type': 'module',
                    },
                )
            elif self.get_ext(asset) == '.css':
                tag = HtmlTag(
                    'link',
                    True,
                    attrs
                    | {
                        'href': asset,
                        'rel': 'stylesheet',
                    },
                )
            if tag and tag not in tags:
                tags.append(tag)
        return tags


class ProdAssetRenderer(AssetRenderer):
    def __init__(self, vite_manifest_path: Path) -> None:
        with vite_manifest_path.open() as f:
            self.manifest = cast(Manifest, load(f))

    def get_tags(self, attrs: Attrs, assets: Assets) -> list[HtmlTag]:
        assets = [asset.lstrip('/') for asset in assets]  # assets do not start with a '/' in manifest
        stylesheets = [stylesheet for asset in assets for stylesheet in self.get_stylesheets(self.manifest.get(asset))]
        scripts = [script for asset in assets for script in self.get_scripts(self.manifest.get(asset))]
        tags = list[HtmlTag]()
        for tag in self.stylesheet_tags(stylesheets, attrs):
            if tag not in tags:
                tags.append(tag)
        for tag in self.script_tags(scripts, attrs):
            if tag not in tags:
                tags.append(tag)
        for tag in self.preload_tags(scripts):
            if tag not in tags:
                tags.append(tag)
        return tags

    def get_stylesheets(self, chunk: ChunkManifest | None, read_ids: set[FileId] | None = None) -> list[Filename]:
        res = list[Filename]()
        if chunk:
            if read_ids is None:
                read_ids = set()
            res.extend(chunk.get('css', []))
            for import_id in chunk.get('imports', []):
                if import_id not in read_ids:
                    read_ids.add(import_id)
                    res.extend(self.get_stylesheets(self.manifest.get(import_id), read_ids))
            if chunk.get('isEntry') is True and self.get_ext(css := chunk['file']) == '.css':
                res.append(css)
        return res

    def get_scripts(self, chunk: ChunkManifest | None, read_ids: set[FileId] | None = None) -> list[tuple[ScriptType, Filename]]:
        res = list[tuple[ScriptType, Filename]]()
        if chunk:
            if read_ids is None:
                read_ids = set()
            if self.get_ext(script := chunk['file']) == '.js':
                res.append(('module' if chunk.get('isEntry') else 'modulepreload', script))
            for import_id in chunk.get('imports', []):
                if import_id not in read_ids:
                    read_ids.add(import_id)
                    res.extend(self.get_scripts(self.manifest.get(import_id), read_ids))
        return res

    def stylesheet_tags(self, stylesheets: list[Filename], attrs: Attrs) -> list[HtmlTag]:
        return [
            HtmlTag(
                'link',
                True,
                attrs
                | {
                    'rel': 'stylesheet',
                    'href': f'/{css_file}',
                },
            )
            for css_file in stylesheets
        ]

    def script_tags(self, scripts: list[tuple[ScriptType, Filename]], attrs: Attrs) -> list[HtmlTag]:
        return [
            HtmlTag(
                'script',
                False,
                attrs
                | {
                    'type': 'module',
                    'src': f'/{script_file}',
                },
            )
            for (script_type, script_file) in scripts
            if script_type == 'module'
        ]

    def preload_tags(self, scripts: list[tuple[ScriptType, Filename]]) -> list[HtmlTag]:
        return [
            HtmlTag(
                'link',
                True,
                {
                    'rel': 'modulepreload',
                    'href': f'/{script_file}',
                },
            )
            for (script_type, script_file) in scripts
            if script_type == 'modulepreload'
        ]


class ViteNode(template.Node):
    def __init__(self, tags: list[HtmlTag]) -> None:
        self.tags = tags

    def render(self, context: template.Context) -> str:
        return mark_safe('\n'.join(tag.to_html(context) for tag in self.tags))

    @classmethod
    def parse_tag(cls, parser: template.base.Parser, token: template.base.Token) -> Self:
        tag_name, params = token.contents.split()[0], token.split_contents()[1:]
        assets, attrs = cls.read_params(params)
        if not assets:
            raise template.TemplateSyntaxError(f"{tag_name} tag requires at least one asset, hotreload keyword or a script/link")
        asset_renderer = DevAssetRenderer() if is_dev_mode() else ProdAssetRenderer(get_vite_manifest_path())
        tags = asset_renderer.get_tags(attrs, assets)
        return cls(tags)

    @classmethod
    def is_quoted(cls, value: str) -> bool:
        return len(value) >= 2 and (f'{value[0]}{value[-1]}' == '""' or f'{value[0]}{value[-1]}' == "''")

    @classmethod
    def unquote(cls, value: str) -> str:
        return value[1:-1] if cls.is_quoted(value) else value

    @classmethod
    def parse_value(cls, value: str) -> StrOrVar:
        return value[1:-1] if cls.is_quoted(value) else template.Variable(value)

    @classmethod
    def read_params(cls, params: list[str]) -> tuple[Assets, Attrs]:
        assets: Assets = list()
        attrs: Attrs = dict()
        for param in params:
            if '=' in param:
                key, value = param.split('=', 1)
                attrs[key] = cls.parse_value(value)
            else:
                assets.append(cls.unquote(param))
        return assets, attrs


register = template.Library()
register.tag(name='vite')(ViteNode.parse_tag)
