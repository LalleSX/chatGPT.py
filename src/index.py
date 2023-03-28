import gi
import openai
import os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class CommentSectionApp(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Comment Section")
        ## Header bar
        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.props.title = "ChatGPT.py"
        self.set_titlebar(header_bar)
        # Main vertical box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)
        # User input box
        self.entry = Gtk.Entry()
        self.entry.set_text("")
        vbox.pack_start(self.entry, False, False, 0)

        # Submit button
        submit_button = Gtk.Button(label="Submit")
        submit_button.connect("clicked", self.on_submit_clicked)
        vbox.pack_start(submit_button, False, False, 0)

        # Scrolled window for comments
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(scrolled_window, True, True, 0)
        # Comment list box
        self.comment_list_box = Gtk.ListBox()
        scrolled_window.add(self.comment_list_box)

    def on_submit_clicked(self, button):
        # Get user input
        user_input = self.entry.get_text()

        # Create a label for the comment
        comment_label = Gtk.Label()
        comment_label.set_line_wrap(True)
        comment_label.set_text(user_input)

        # Add comment to the list box
        self.comment_list_box.add(comment_label)
        self.comment_list_box.show_all()

        # Clear the input field
        self.entry.set_text("")

# Run the application
app = CommentSectionApp()
app.connect("destroy", Gtk.main_quit)
app.show_all()
Gtk.main()