from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandParser


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('static_dir', type=Path)
        parser.add_argument('media_dir', type=Path, nargs='?', default=None)

    def handle(self, *args, **options) -> None:
        static_path: Path = options['static_dir']
        static_url = settings.STATIC_URL.strip('/')
        media_path: Path | None = options['media_dir']
        media_url = getattr(settings, 'MEDIA_URL', '').strip('/')
        nginx_config = list[str]()
        for p in settings.STATIC_ROOT.glob('*'):
            if p.name.startswith('.'):
                continue
            if not (p.is_file() or p.is_dir()):
                continue
            nginx_config.append(f'location /{p.name} {{\n  root {static_path};\n}}')
        nginx_config.append(f'location /{static_url}/ {{\n  root {static_path}/;\n}}')
        if media_path and media_url:
            nginx_config.append(f'location /{media_url}/ {{\n  root {media_path}/;\n}}')
        print('\n'.join(nginx_config))
