import os, shutil
from functions import markdown_to_html_node, extract_title

def copy_content_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_content_recursive(from_path, dest_path)

def generate_page(from_path, template_path, dest_path,basepath):
    destfile_path = os.path.join(dest_path,"index.html")
    print(f"Generating page from {from_path} to {destfile_path} using {template_path}.")

    mf = open(from_path)
    md_content = mf.read()

    tf = open(template_path)
    tp_content = tf.read()

    html_nodes = markdown_to_html_node(md_content)
    html_content = html_nodes.to_html()
    site_title = extract_title(md_content)

    html_site = tp_content.replace("{{ Title }}",site_title)
    html_site = html_site.replace("{{ Content }}",f"{html_content}")
    html_site = html_site.replace('href="/', f'href="{basepath}')
    html_site = html_site.replace('src="/', f'src="{basepath}')

    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    with open(destfile_path, "w") as f:
        f.write(html_site)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,basepath):
    dir_entries = os.listdir(dir_path_content)
    print(f"dir entries are:{dir_entries}")
    for entry in dir_entries:
        entry_path = os.path.join(dir_path_content,entry)
        print(f"Entry path is: {entry_path}")
        if os.path.isfile(entry_path):
            contentfile_path = os.path.join(dir_path_content, entry)
            destfile_path = os.path.join(dest_dir_path, "index.html")
            print(f"Generating page from {dir_path_content} to {destfile_path} using {template_path}.")

            mf = open(contentfile_path)
            md_content = mf.read()

            tf = open(template_path)
            tp_content = tf.read()

            html_nodes = markdown_to_html_node(md_content)
            html_content = html_nodes.to_html()
            site_title = extract_title(md_content)

            html_site = tp_content.replace("{{ Title }}", site_title)
            html_site = html_site.replace("{{ Content }}", f"{html_content}")
            html_site = html_site.replace('href="/', f'href="{basepath}')
            html_site = html_site.replace('src="/', f'src="{basepath}')

            if not os.path.exists(dest_dir_path):
                os.mkdir(dest_dir_path)

            with open(destfile_path, "w") as f:
                f.write(html_site)
        else:
            new_dest_dir_path = os.path.join(dest_dir_path,entry)
            if not os.path.exists(new_dest_dir_path):
                os.mkdir(new_dest_dir_path)
            generate_pages_recursive(entry_path, template_path, new_dest_dir_path,basepath)




