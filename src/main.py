import os, shutil

from generate_page import copy_content_recursive, generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
from_path = "./content"
template_path = "template.html"



def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_content_recursive(dir_path_static, dir_path_public)

    generate_pages_recursive(from_path,template_path,dir_path_public)

if __name__ == "__main__":
    main()