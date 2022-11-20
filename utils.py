import re
import unidecode


def clearFrame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def slugify(text):
    text = unidecode.unidecode(text).lower()
    return re.sub(r'[\W_]+', '-', text)
