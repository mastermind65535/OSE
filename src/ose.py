from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Scrollbar
from tkinter.ttk import Progressbar
from tkinter.ttk import Treeview
from tkinter.ttk import Style

from customtkinter import *
from customtkinter import CTkTabview
from customtkinter import CTkButton
from customtkinter import ThemeManager
from CTkMenuBar import CustomDropdownMenu
from CTkMenuBar import CTkMenuBar
from CTkMenuBar import CTkTitleMenu
from CTkListbox import CTkListbox
from tkintermapview import TkinterMapView

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from PIL import *
from PIL import Image
from PIL import ImageTk

from io import BytesIO

from urllib.parse import urlparse
from urllib.parse import urljoin

from threading import Thread

import socket
import platform
import psutil
import tldextract
import time
import re
import pathlib
import requests
import os
import sys

EXECUTE_PATH = pathlib.Path(__file__).parent.resolve()
ASSETS_PATH = os.path.join(EXECUTE_PATH, "assets")
BIN_PATH = os.path.join(EXECUTE_PATH, "bin")

# Images
ICON_PATH = os.path.join(ASSETS_PATH, "icon.ico")
ICON_PHOTO_PATH = os.path.join(ASSETS_PATH, "icon.png")

# Binaries
CHROME_DRIVER = os.path.join(BIN_PATH, "chromedriver.exe")
DRIVER = None

# Networks
GLOBAL_USERAGENT = "OSE /3.2.0 (mastermind65535@gmail.com)"

class Version:
    def __init__(self):
        self.root = CTkToplevel()
        self.root.title("O.S.E. - Version")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.after(201, lambda :self.root.iconbitmap(ICON_PATH))

        ImagePath = ICON_PATH
        centerImg = CTkImage(
            light_image=Image.open(ImagePath),
            dark_image=Image.open(ImagePath),
            size=(200, 200),
        )
        self.Imagebox = CTkLabel(self.root, image=centerImg, text='')
        self.Imagebox.pack_configure(anchor="n", pady=30)
        self.Imagebox.pack()

        self.versionText = CTkLabel(
            self.root,
            text="""
O.S.E. (OSINT Search Engine) v3.2.0

Present by @mastermind65535
https://github.com/mastermind65535


(c) 2025 mastermind65535, All Rights Reserved.
""",
            font=CTkFont("Arial", 15),
            justify="left",
            anchor="w"
        )
        self.versionText.pack_configure(fill='both', expand=True, padx=30)
        self.versionText.pack()

        self.root.mainloop()

class License():
    def __init__(self):
        self.root = CTkToplevel()
        self.root.title("O.S.E. - License")
        self.root.geometry("700x400")
        self.root.resizable(False, False)
        self.root.wm_iconbitmap()
        self.root.after(201, lambda :self.root.iconbitmap(ICON_PATH))

        self.licenseText = CTkLabel(
            self.root,
            text="""
MIT License

Copyright (c) 2023 Tom Schimansky

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",
            font=CTkFont("Arial", 15),
            justify="left",
            anchor="nw"
        )
        self.licenseText.pack_configure(fill='both', expand=True, anchor="n", padx=10)
        self.licenseText.pack()

        self.root.mainloop()

class LocationViewer(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.marker_list = []
        self.cross = None
        self.cross_loc = [0, 0]

        self.cross_image = PhotoImage(file=os.path.join(ASSETS_PATH, "cross.png"))

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = CTkFrame(self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = CTkFrame(self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        self.frame_left.grid_rowconfigure(2, weight=1)

        self.button_1 = CTkButton(self.frame_left, text="Set Marker", command=self.set_marker_event)
        self.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.button_2 = CTkButton(self.frame_left, text="Clear Markers", command=self.clear_marker_event)
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        self.map_label = CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))

        self.map_option_menu = CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite"],
                                             command=self.change_map)
        self.map_option_menu.grid(row=4, column=0, padx=(20, 20), pady=(10, 0))

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=10)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        self.entry = CTkEntry(self.frame_right, placeholder_text="Type address")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)

        self.button_5 = CTkButton(self.frame_right, text="Search", width=90, command=self.search_event)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        self.update_cross_pointer()

    def search_event(self, event=None):
        address = self.entry.get()

        try:
            data = self.getAddress(address)
            if data:
                lat, lon = data["lat"], data["lon"]
                self.map_widget.set_position(float(lat), float(lon))
                print(f"[DEBUG] Address Found: {address} -> lat {lat}, lon {lon}")
            else:
                print("[DEBUG] Address Not Found")
                messagebox.showerror("Error", "Address Not Found")
        except requests.RequestException as e:
            print(f"[DEBUG] Request Error: {e}")

    def getAddress(self, address:str):
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": address,
            "format": "jsonv2",
            "addressdetails": 1,
            "limit": 1
        }
        headers = {
            "User-Agent": GLOBAL_USERAGENT
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data[0]
    
    def update_cross_pointer(self):
        try:
            lat, lon = self.map_widget.get_position()

            if self.cross is None:
                self.cross = self.map_widget.set_marker(lat, lon, icon=self.cross_image)
                self.cross_loc = [lat, lon]
            else:
                if self.cross_loc != [lat, lon]:
                    self.cross.set_position(lat, lon)
                    self.cross_loc = [lat, lon]

            self.after(1, self.update_cross_pointer)
        except:
            return

    def format_address(self, data):
        address = data["address"]

        parts = [
            address.get("house_number", ""),
            address.get("road", ""),
            address.get("suburb", ""),
            address.get("state", ""),
            address.get("postcode", ""),
            address.get("country", "")
        ]

        formatted_address = ", ".join(filter(None, parts))

        return formatted_address

    def set_marker_event(self):
        current_position = self.map_widget.get_position()
        lat, lon = self.map_widget.get_position()
        self.marker_list.append(self.map_widget.set_marker(current_position[0], current_position[1], text=self.format_address(self.getAddress(f"{lat}, {lon}"))))

    def clear_marker_event(self):
        for marker in self.marker_list:
            marker.delete()

    def change_appearance_mode(self, new_appearance_mode: str):
        set_appearance_mode(new_appearance_mode)

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

class SourceExtractor(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.image_list = []

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = CTkFrame(self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = CTkFrame(self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        self.frame_left.grid_rowconfigure(2, weight=1)

        self.button_1 = CTkButton(self.frame_left, text="Extract Sources", command=self.fetch_sources)
        self.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.ImageList = CTkListbox(self.frame_right)
        self.ImageList.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))
        self.ImageList.bind("<<ListboxSelect>>", self.load)

    def fetch_sources(self):
        global DRIVER
        self.image_list.clear()
        try: self.ImageList.delete("all")
        except: pass
        
        pattern = r'(https?://[^\s"\'>]+)'
        img_urls = re.findall(pattern, DRIVER.page_source)

        for idx, img_url in enumerate(img_urls):
            self.image_list.append(img_url)
            self.ImageList.insert("END", img_url)

    def load(self, event):
        url = self.ImageList.get()
        DRIVER.execute_script(f"""window.open("{url}", "_blank");""")

class SitemapExtractor(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.visited_links = set()
        self.max_links = 100  # Default limit for number of links to crawl

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = CTkFrame(self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = CTkFrame(self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        self.frame_left.grid_rowconfigure(2, weight=1)

        self.button_1 = CTkButton(self.frame_left, text="Generate Sitemap", command=self.fetch_sitemap)
        self.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        # Dropdown for limiting the number of links to crawl
        self.dropdown = CTkComboBox(self.frame_left, values=["5", "15", "25", "50", "100"], command=self.set_limit)
        self.dropdown.set("100")  # Set default value
        self.dropdown.grid(pady=(10, 0), padx=(20, 20), row=1, column=0)

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        bg_color = self.parent._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self.parent._apply_appearance_mode(ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = self.parent._apply_appearance_mode(ThemeManager.theme["CTkButton"]["fg_color"])

        treestyle = Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0)
        treestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
        self.parent.bind("<<TreeviewSelect>>", lambda event: self.parent.focus_set())

        self.progressBar = Progressbar(self.frame_right)
        self.progressBar.pack(fill=X, pady=30)

        self.TreeviewFrame = CTkFrame(self.frame_right)
        self.TreeviewFrame.pack_configure(fill=BOTH, expand=True)

        self.treeview = Treeview(self.TreeviewFrame)
        self.treeview.pack(fill=BOTH, expand=True, side="left")

        self.scrollbar = Scrollbar(self.TreeviewFrame, orient=VERTICAL, command=self.treeview.yview)
        self.scrollbar.pack(fill=Y, side="left")

        self.treeview.configure(yscrollcommand=self.scrollbar.set)

    def set_limit(self, value):
        self.max_links = int(value)  # Set the link limit based on the dropdown selection

    def fetch_sitemap(self):
        self.progressBar.config(maximum=self.max_links, value=0)
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        self.visited_links = set()

        start_url = DRIVER.current_url
        extracted = tldextract.extract(start_url)
        self.root_domain = "{}.{}".format(extracted.domain, extracted.suffix)
        root_node = self.treeview.insert("", "end", text=start_url, open=True)

        Thread(target=self.get_links, daemon=True, args=(start_url, root_node)).start()

    def get_links(self, url, node):
        try:
            headers = {
                "User-Agent": GLOBAL_USERAGENT
            }

            r = requests.get(url, timeout=5, headers=headers)
            r.raise_for_status()
            pattern = r'(https?://[^\s"\'>]+)'
            links = re.findall(pattern, r.text)

            # If link limit has been reached, stop processing
            if len(self.visited_links) >= self.max_links:
                return

            for link in links:
                found_domain = tldextract.extract(link)
                domain = "{}.{}".format(found_domain.domain, found_domain.suffix)

                if domain != self.root_domain: 
                    continue

                if link not in self.visited_links:
                    self.visited_links.add(link)
                    self.progressBar.config(value=len(self.visited_links))

                    child = self.treeview.insert(node, "end", text=link, open=True)

                    Thread(target=self.get_links, daemon=True, args=(link, child,)).start()

        except requests.exceptions.RequestException as e:
            print(f"[DEBUG] Error fetching {url}: {e}")
        except Exception as e:
            print(f"[DEBUG] Unexpected error with {url}: {e}")

class HomePage(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.parent = parent
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Load Icon Image
        ImagePath = ICON_PATH
        centerImg = CTkImage(
            light_image=Image.open(ImagePath),
            dark_image=Image.open(ImagePath),
            size=(200, 200),
        )
        self.Imagebox = CTkLabel(self.parent, image=centerImg, text='')
        self.Imagebox.pack_configure(anchor="n", pady=30)
        self.Imagebox.pack()

        label1 = CTkLabel(self.parent, text="O.S.E.", font=("Arial", 30, "bold"))
        label1.pack_configure(anchor="n")
        label1.pack()

        label = CTkLabel(self.parent, text="OSINT Search Engine", font=("Arial", 20, "bold"))
        label.pack_configure(anchor="n")
        label.pack()

        # System Information
        system_info_frame = CTkFrame(self, corner_radius=15)
        system_info_frame.grid(row=1, column=0, pady=(10, 20), padx=20, sticky="nsew")

        info_labels = [
            ("OS:", platform.system()),
            ("OS Version:", platform.version()),
            ("Architecture:", platform.architecture()[0]),
            ("Processor:", platform.processor()),
            ("RAM:", f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB"),
        ]

        info_title = CTkLabel(system_info_frame, text="Running Environment:", font=("Arial", 16, "bold"), anchor="w")
        info_title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        for i, (key, value) in enumerate(info_labels):
            i = i + 1
            label_title = CTkLabel(system_info_frame, text=key, font=("Arial", 15, "bold"), anchor="w")
            label_title.grid(row=i, column=0, padx=10, pady=0, sticky="w")

            label_value = CTkLabel(system_info_frame, text=value, font=("Arial", 15), anchor="w")
            label_value.grid(row=i, column=1, padx=10, pady=0, sticky="w")

class GUI:
    def __init__(self):
        set_appearance_mode("Dark")
        set_default_color_theme("blue")

        self.root = CTk()
        self.root.geometry("1500x800")
        self.root.title("O.S.E. v3.2.0")
        self.root.wm_attributes("-transparentcolor", "pink")

        self.root.iconbitmap(ICON_PATH)

        self.loadMenu()
        self.loadTabs()

        self.root.protocol("WM_DELETE_WINDOW", self.closingEvent)
        self.root.mainloop()

    def loadMenu(self):
        self.Menu = CTkTitleMenu(self.root)
        self.ProgramMenu = self.Menu.add_cascade("Program")
        self.BrowserMenu = self.Menu.add_cascade("OSE Browser")
        self.HelpMenu = self.Menu.add_cascade("Help")

        # -------------------------------------------------------------------------------------

        # Program Menu
        self.ProgramDropDown = CustomDropdownMenu(self.ProgramMenu)
        self.ProgramDropDown.add_option(option="Version", command=lambda: Version())
        self.ProgramDropDown.add_option(option="License", command=lambda: License())
        self.ProgramDropDown.add_separator()

        self.ProgramDropDown_Proxy = self.ProgramDropDown.add_submenu(submenu_name="Proxy")
        self.ProgramDropDown_Proxy.add_option(option="Proxy Configuration")
        self.ProgramDropDown_Proxy.add_option(option="Proxy Test")
        self.ProgramDropDown.add_separator()

        self.ProgramDropDown.add_option(option="System Theme", command=lambda: set_appearance_mode("system"))
        self.ProgramDropDown.add_option(option="Light Theme", command=lambda: set_appearance_mode("light"))
        self.ProgramDropDown.add_option(option="Dark Theme", command=lambda: set_appearance_mode("dark"))
        self.ProgramDropDown.add_separator()

        self.ProgramDropDown.add_option(option="Exit", command=lambda: sys.exit(0))

        # -------------------------------------------------------------------------------------

        # OSE Browser
        self.BrowserDropDown = CustomDropdownMenu(self.BrowserMenu)
        self.BrowserDropDown.add_option(option="Start Browser", command=self.StartBrowser_OpenDriver)
        self.BrowserDropDown.add_option(option="Close Browser", command=self.StopBrowser_CloseDriver)
        self.BrowserDropDown.add_separator()
        self.BrowserDropDown.add_option(option="Browser Settings")

    def loadTabs(self):
        self.Tabs = CTkTabview(self.root)
        self.Tabs.add("Home")
        self.HomeTab = self.Tabs.tab("Home")
        self.HomePageTab = HomePage(self.HomeTab)
        self.HomePageTab.pack(fill="both", expand=True)

        self.Tabs.add("Sitemap Tree")
        self.SitemapTab = self.Tabs.tab("Sitemap Tree")
        self.SitemapViewer = SitemapExtractor(self.SitemapTab)
        self.SitemapViewer.pack(fill="both", expand=True)

        self.Tabs.add("Source Extractor")
        self.SourceExtractorTab = self.Tabs.tab("Source Extractor")
        self.SrcExtractor = SourceExtractor(self.SourceExtractorTab)
        self.SrcExtractor.pack(fill="both", expand=True)

        self.Tabs.add("Location Viewer")
        self.LocationViewerTab = self.Tabs.tab("Location Viewer")
        self.location_viewer = LocationViewer(self.LocationViewerTab)
        self.location_viewer.pack(fill="both", expand=True)

        self.Tabs.pack_configure(fill="both", expand=True)
        self.Tabs.pack()

    def StartBrowser_OpenDriver(self):
        global DRIVER
        DRIVER = webdriver.Chrome()
        DRIVER.get("https://google.com")

    def StopBrowser_CloseDriver(self):
        global DRIVER
        if DRIVER != None:
            DRIVER.close()

    def closingEvent(self):
        try:
            global DRIVER
            if DRIVER != None: DRIVER.close()
            sys.exit(0)
        except:
            sys.exit(1)

        
if __name__ == "__main__":
    GUI()