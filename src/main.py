import os, shutil, sys
from generate_page import copy_content_recursive, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
from_path = "./content"
template_path = "template.html"



def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] is not None else "/"
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_content_recursive(dir_path_static, dir_path_public)

    generate_pages_recursive(from_path,template_path,dir_path_public,basepath)

if __name__ == "__main__":
    main()