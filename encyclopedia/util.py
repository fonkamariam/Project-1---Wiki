import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def Md_to_Html(text):
    list=[]
    for line in text.splitlines():
        if line: 
            if heading := re.search(r'^(\#+) (.+)',line):
                counter=heading.group(1)
                h=0
                for y in counter:
                    if y == '#':
                        h+=1
                x = (f"<h{h}>{heading.group(2)}</h{h}>")
                if bold := re.search(r'(.*)\*{2}(.+)\*{2}(.*)',x):
                    x= (f"{bold.group(1)}<strong>{bold.group(2)}</strong>{bold.group(3)}")
                if italic := re.search(r'(.*)\*{1}(.+)\*{1}(.*)',x):
                    x=((f"{italic.group(1)}<em>{italic.group(2)}</em>{italic.group(3)}"))
                if link := re.search(r'(.*)\[(.+)\]\((.+)\)(.*)',x):
                    x= (f"{link.group(1)}<a href='{link.group(3)}'>{link.group(2)}</a> {link.group(4)}")
                list.append(x)
            elif ul :=re.search(r'^\* (.*)',line):
                x= f"<ul>{ul.group(1)}</ul>"
                if bold := re.search(r'(.*)\*{2}(.+)\*{2}(.*)',x):
                    x= (f"{bold.group(1)}<strong>{bold.group(2)}</strong>{bold.group(3)}")
                if italic := re.search(r'(.*)\*{1}(.+)\*{1}(.*)',x):
                    x=((f"{italic.group(1)}<em>{italic.group(2)}</em>{italic.group(3)}"))
                if link := re.search(r'(.*)\[(.+)\]\((.+)\)(.*)',x):
                    x= (f"{link.group(1)}<a href='{link.group(3)}'>{link.group(2)}</a> {link.group(4)}")
                list.append(x)
            elif ol := re.search(r'^\d+\. (.+)$',line):
                x= f"<li>{ol.group(1)}</li>"
                if bold := re.search(r'(.*)\*{2}(.+)\*{2}(.*)',x):
                    x= (f"{bold.group(1)}<strong>{bold.group(2)}</strong>{bold.group(3)}")
                if italic := re.search(r'(.*)\*{1}(.+)\*{1}(.*)',x):
                    x=((f"{italic.group(1)}<em>{italic.group(2)}</em>{italic.group(3)}"))
                if link := re.search(r'(.*)\[(.+)\]\((.+)\)(.*)',x):
                    x= (f"{link.group(1)}<a href='{link.group(3)}'>{link.group(2)}</a> {link.group(4)}")
                list.append(x)
            else:
                x=f"<p>{line}</p>"
                if bold := re.search(r'(.*)\*{2}(.+)\*{2}(.*)',x):
                    x= (f"{bold.group(1)}<strong>{bold.group(2)}</strong>{bold.group(3)}")
                if italic := re.search(r'(.*)\*{1}(.+)\*{1}(.*)',x):
                    x=((f"{italic.group(1)}<em>{italic.group(2)}</em>{italic.group(3)}"))
                if link := re.search(r'(.*)\[(.+)\]\((.+)\)(.*)',x):
                    x= (f"{link.group(1)}<a href='{link.group(3)}'>{link.group(2)}</a> {link.group(4)}")
                list.append(x)
    return "\n".join(list)

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    content_in_html=Md_to_Html(content)
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))
    # Save in Html form
    file_html=f"encyclopedia/templates/encyclopedia/{title}.html"
    default_storage.save(file_html,ContentFile(content_in_html))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
