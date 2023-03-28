import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("My Web Page")

        # Add CSS
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("./style.css")


        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_child(main_box)
        
        # First row
        combo_box = Gtk.ComboBoxText()
        combo_box.append_text("GPT-3")
        combo_box.append_text("GPT-3.5")
        combo_box.append_text("GPT-4")
        combo_box.set_active(0)

        combo_box_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, halign=Gtk.Align.CENTER, valign=Gtk.Align.CENTER)
        combo_box_box.append(combo_box)
        main_box.append(combo_box_box)

        # Second row
        content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        main_box.append(content_box)

        left_spacer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        left_spacer.set_hexpand(True)
        left_spacer.set_css_classes(["bg-gray"])

        content_box.append(left_spacer)

        content_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, halign=Gtk.Align.CENTER, valign=Gtk.Align.CENTER)
        content_box.append(content_area)

        label = Gtk.Label(label="Hello, World!")
        content_area.append(label)

        text_view = Gtk.TextView()
        content_area.append(text_view)

        button = Gtk.Button(label="Submit")
        content_area.append(button)

        right_spacer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        right_spacer.set_hexpand(True)
        right_spacer.set_css_classes(["bg-gray"])

        content_box.append(right_spacer)

class Application(Gtk.Application):
    def __init__(self):
        super().__init__()

    def do_activate(self):
        win = MainWindow(self)
        win.show()

app = Application()
app.run()
