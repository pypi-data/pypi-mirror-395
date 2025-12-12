import os
from django.core.management.base import BaseCommand
from django.conf import settings
from zipfile import ZIP_DEFLATED, ZipFile
from io import BytesIO

class Command(BaseCommand):
    help = "Download the latest Lucide icons and update the local zip file."

    def handle(self, *args, **options):
        # Find the root directory of the project
        root_dir = settings.BASE_DIR if hasattr(settings, "BASE_DIR") else os.getcwd()
        output_path = os.path.join(root_dir, "lucide-latest.zip")

        # Check if the output path is writable
        import requests
        api_url = "https://api.github.com/repos/lucide-icons/lucide/releases/latest"
        r = requests.get(api_url)
        r.raise_for_status()
        version = r.json()["tag_name"]

        self.stdout.write(self.style.SUCCESS(f"Loading Lucide icons version {version} …"))
        zip_url = f"https://github.com/lucide-icons/lucide/releases/download/{version}/lucide-icons-{version}.zip"
        r = requests.get(zip_url)
        r.raise_for_status()
        input_zip = ZipFile(BytesIO(r.content))
        input_prefix = "icons/"

        try:
            os.remove(output_path)
        except FileNotFoundError:
            pass

        with ZipFile(output_path, "w", compression=ZIP_DEFLATED, compresslevel=9) as output_zip:
            for name in sorted(input_zip.namelist()):
                if name.startswith(input_prefix) and name.endswith(".svg"):
                    info = input_zip.getinfo(name)
                    data = input_zip.read(name).replace(b' data-slot="icon"', b"")
                    new_name = name[len(input_prefix):]
                    info.filename = new_name
                    output_zip.writestr(info, data)
                    self.stdout.write(f"  ✓ {new_name}")

        self.stdout.write(self.style.SUCCESS(f"\n✅ Newest Lucide icons loaded: {output_path}"))
