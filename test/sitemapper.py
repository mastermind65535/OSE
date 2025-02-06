import requests
from tkinter import *
from tkinter.ttk import Treeview
from threading import Thread
import tldextract
import re

start_url = "https://google.com"
extracted = tldextract.extract(start_url)
root_domain = "{}.{}".format(extracted.domain, extracted.suffix)

def getLinks(url, node):
    try:
        r = requests.get(url)
        pattern = r'(https?://[^\s"\'>]+)'
        links = re.findall(pattern, r.text)
        for link in links:
            found_domain = tldextract.extract(link)
            domain = "{}.{}".format(found_domain.domain, found_domain.suffix)
            if domain != root_domain: continue
            print(f"[{url}]\t[{domain}]\t[{link}]")
            child = treeview.insert(node, "end", text=link, open=True)
            Thread(target=getLinks, daemon=True, args=(link, child,)).start()
    except:
        pass

app = Tk()

treeview = Treeview(app, columns=("URL",))
treeview.pack(fill=BOTH, expand=True)

root_node = treeview.insert("", "end", text="Root", open=True)

Thread(target=getLinks, daemon=True, args=(start_url, root_node,)).start()

app.mainloop()