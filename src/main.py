import os
import shutil
import sys

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive, generate_sitemap, load_config

dir_path_static = "./static"
dir_path_content = "./content"
template_path = "./template.html"
config_path = "./site.json"


def main():
    # Uporaba: python3 src/main.py [basepath] [izhodna_mapa]
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    dir_path_public = sys.argv[2] if len(sys.argv) > 2 else "./docs"

    print(f"Deleting {dir_path_public} directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print(f"Copying static files to {dir_path_public} directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating content...")
    config = load_config(config_path)
    generate_pages_recursive(
        dir_path_content, template_path, dir_path_public, basepath, config
    )

    print("Generating sitemap.xml and robots.txt...")
    generate_sitemap(dir_path_content, dir_path_public, config)


if __name__ == "__main__":
    main()