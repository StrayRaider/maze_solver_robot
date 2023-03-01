import gi
import requests

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class FileChs(Gtk.VBox):
    def __init__(self,parent):
        Gtk.VBox.__init__(self)
        self.parent = parent
        self.label = Gtk.Label("select url")
        self.pack_start(self.label,0,0,5)
        
        self.select_url_but = Gtk.Button()
        self.select_url_but.set_label("select url")
        self.select_url_but.connect("clicked",self.select_url_but_clicked)
        self.pack_start(self.select_url_but,0,0,5)

        self.text=Gtk.Entry()
        self.text.set_activates_default(True)
        self.pack_start(self.text,0,0,5)

        
    def select_url_but_clicked(self,widget):
        URL = self.text.get_text()
        print(URL)
        try:
            response = requests.get(URL)
            print(response)
            open('./mz_lib/map.txt', 'wb').write(response.content)
        except:
            pass
        self.parent.stack.set_visible_child_name("game")