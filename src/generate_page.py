from markdown_to_html import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    with open(dest_path, "w") as f:
        f.write(page)
