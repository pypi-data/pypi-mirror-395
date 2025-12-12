import os
import re
import urllib.request
import shutil
import setuptools
import zipfile


PACKAGE_DIR = os.path.dirname(__file__)
BINDINGS_DIR = os.path.join(PACKAGE_DIR, "zaber_motion_bindings")


def get_version():
    with open(os.path.join(PACKAGE_DIR, "pyproject.toml"), "r", encoding="utf-8") as fh:
        pyproject = fh.read()

    return re.search(r'version = "(.*?)"', pyproject).group(1)


def download_bindings(version):
    url = f"https://api.zaber.io/downloads/software-downloads?product=zml_cpp_src&version={version}"
    archive_file = f"ZaberMotionCppSource-{version}.zip"
    bindings_prefix = "ZaberMotionCppSource/build/zaber-motion-core"

    with urllib.request.urlopen(url) as response, open(archive_file, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

    with zipfile.ZipFile(archive_file, 'r') as archive:
        files = archive.namelist()
        bindings = [f for f in files if f.startswith(bindings_prefix)]
        archive.extractall(".", bindings)

    shutil.rmtree(BINDINGS_DIR, ignore_errors=True)
    shutil.move("ZaberMotionCppSource/build", BINDINGS_DIR)
    shutil.rmtree("ZaberMotionCppSource", ignore_errors=True)
    os.remove(archive_file)


def setup():
    if not os.environ.get("SETUP_SKIP_ZML_BINDINGS"):
        version = get_version()
        download_bindings(version)

    setuptools.setup()


setup()
