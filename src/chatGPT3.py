import gi
import openai
import requests
import os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib
openai.api_key = "API_KEY HERE"


class CommentSectionApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Comment Section")
        self.setup_header_bar()
        self.setup_main_layout()

    def setup_header_bar(self):
        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.props.title = "ChatGPT.py"
        self.set_titlebar(header_bar)

    def setup_main_layout(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        self.setup_user_input_box(vbox)
        self.setup_model_options(vbox)
        self.setup_submit_button(vbox)
        self.setup_comment_section(vbox)

    def setup_user_input_box(self, vbox):
        self.entry = Gtk.Entry()
        self.entry.set_text("")
        vbox.pack_start(self.entry, False, False, 0)

    def setup_model_options(self, vbox):
        options = ["GPT-3", "GPT-3.5", "GPT-4"]
        self.combo = Gtk.ComboBoxText()
        for option in options:
            self.combo.append_text(option)
        self.combo.set_active(0)
        vbox.pack_start(self.combo, False, False, 0)

    def setup_submit_button(self, vbox):
        submit_button = Gtk.Button(label="Submit")
        submit_button.connect("clicked", self.on_submit_clicked)
        vbox.pack_start(submit_button, False, False, 0)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("./src/style.css")

        context = submit_button.get_style_context()
        context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def setup_comment_section(self, vbox):
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(scrolled_window, True, True, 0)

        self.comment_list_box = Gtk.ListBox()
        scrolled_window.add(self.comment_list_box)

    def fetch_response(self, user_input):
        model = self.combo.get_active_text().lower()
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {openai.api_key}"},
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.8,
                "max_tokens": 100,
            }
        ).json()
        return response["choices"][0]["message"]["content"].strip()  # Fixed KeyError

    def on_submit_clicked(self, button):
        user_input = self.entry.get_text()

        if user_input == "":
            return

        comment_label = Gtk.Label()
        comment_label.set_line_wrap(True)
        comment_label.set_text(user_input)

        self.comment_list_box.add(comment_label)
        self.comment_list_box.show_all()

        self.entry.set_text("")

        def get_response_and_update():
            response_text = self.fetch_response(user_input)
            ai_comment_label = Gtk.Label()
            ai_comment_label.set_line_wrap(True)
            ai_comment_label.set_text(response_text)

            self.comment_list_box.add(ai_comment_label)
            self.comment_list_box.show_all()

        Gdk.threads_add_idle(GLib.PRIORITY_DEFAULT_IDLE, get_response_and_update)

def main():
    app = CommentSectionApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
