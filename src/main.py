from blocks import *
from textnode import TextNode, TextType
import os
import shutil
import sys

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"

def static_to_public(static, public):
    if os.path.exists(static):
        for file in os.listdir(static):
            if os.path.isfile(os.path.join(static, file)):
                shutil.copy(os.path.join(static, file), os.path.join(public, file))
                print(f"file copy - {os.path.join(static, file), os.path.join(public, file)}")
            elif os.path.isdir(os.path.join(static, file)):
                if not os.path.exists(os.path.join(public, file)):
                    os.mkdir(os.path.join(public, file))
                    print(f"directory created - {os.path.join(public, file)}")
                    static_to_public(os.path.join(static, file), os.path.join(public, file))

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        file_from_path = f.read()
    with open(template_path, "r") as f:
        file_template_path = f.read()

    html_string = markdown_to_html_node(file_from_path)
    html_string_two = html_string.to_html()
    title = extract_title(file_from_path)
    final_html = file_template_path.replace("{{ Title }}", title)
    final_html_two = final_html.replace("{{ Content }}", html_string_two)
    final_html_three = final_html_two.replace("href='/", f"href='{basepath}")
    final_html_four = final_html_three.replace("src='/", f"src='{basepath}")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path,"w") as f:
        print(f"file created {final_html_four}")
        new_file = f.write(final_html_four)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, root=None, basepath="/"):
    if root is None:
        root = dir_path_content
    for file in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, file)
        print(f"this is full path {full_path}")
        if os.path.isfile(full_path) and file.endswith(".md"):
            relative_path = os.path.relpath(full_path, root)
            print(f"this is relative path {relative_path}")
            new_path = os.path.join(dest_dir_path, relative_path).replace(".md", ".html")
            print(f"this is new path {new_path}")
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            print(f"this is template path {template_path}")
            generate_page(full_path, template_path, new_path, basepath)
        elif os.path.isdir(full_path):
            generate_pages_recursive(full_path, template_path, dest_dir_path, root, basepath)

    

def main():
    static_directory = "/home/vinic/workspace/portfolio2/static"
    public_directory = "/home/vinic/workspace/portfolio2/docs"

    if os.path.exists(public_directory):
        shutil.rmtree(public_directory)
    os.makedirs(public_directory, exist_ok=True)
    static_to_public(static_directory, public_directory)
    generate_pages_recursive("/home/vinic/workspace/portfolio2/content", "/home/vinic/workspace/portfolio2/template.html",
                             "/home/vinic/workspace/portfolio2/docs", basepath="/")


if __name__ == "__main__":
    main()