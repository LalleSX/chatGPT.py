import glob
import json
from tkinter import *
from tkinter.ttk import *
from time import strftime

from api import get_api_key, fetch_response

class CommentSectionApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Comment Section")
        self.setup_main_layout()

    def setup_main_layout(self):
        self.setup_user_input_box()
        self.setup_model_options()
        self.setup_submit_button()
        self.setup_comment_section()
        self.setup_new_chat_button()

    def setup_user_input_box(self):
        self.entry = Entry(self)
        self.entry.pack(padx=10, pady=10)

    def setup_model_options(self):
        options = ["GPT-3.5-turbo", "GPT-4"]
        self.combo = Combobox(self, values=options, state="readonly")
        self.combo.set(options[0])
        self.combo.pack(padx=10, pady=10)

    def setup_submit_button(self):
        submit_button = Button(self, text="Submit", command=self.on_submit_clicked)
        submit_button.pack(padx=10, pady=10)

    def setup_comment_section(self):
        self.scrolled_window = Scrollbar(self)
        self.scrolled_window.pack(side=RIGHT, fill=Y)

        self.comment_list_box = Listbox(self, yscrollcommand=self.scrolled_window.set)
        self.comment_list_box.pack(fill=BOTH, expand=True)

        self.scrolled_window.config(command=self.comment_list_box.yview)

        self.load_chat()

    def setup_new_chat_button(self):
        new_chat_button = Button(self, text="New Chat", command=self.start_new_chat)
        new_chat_button.pack(padx=10, pady=10)
    
    ## Frontend to backend
    def get_chat_history(self):
        chat_history = []
        for comment_text in self.comment_list_box.get(0, END):
            role = "user" if "You:" in comment_text else "assistant"
            content = comment_text.replace("You: ", "").replace("Assistant: ", "")
            chat_history.append({"role": role, "content": content})
        return chat_history

    def fetch_response(self, user_input):
        model = self.combo.get().lower()
        chat_history = self.get_chat_history()
        chat_history.append({"role": "user", "content": user_input})
        return fetch_response(get_api_key(), model, chat_history)

    def on_submit_clicked(self):
        user_input = self.entry.get()

        if user_input == "":
            return None

        self.comment_list_box.insert(END, "You: " + user_input)

        self.entry.delete(0, END)

        response_text = self.fetch_response(user_input)
        self.comment_list_box.insert(END, "Assistant: " + response_text)
        self.save_chat()

    def start_new_chat(self):
        self.comment_list_box.delete(0, END)
    
    def save_chat(self):
        file_name = f"chat_{int(strftime('%d%m%y'))}.json"
        chat_data = {"comments": []}
        for i in range(self.comment_list_box.size()):
            comment_text = self.comment_list_box.get(i)
            chat_data["comments"].append(comment_text)
        with open(file_name, "w") as f:
            json.dump(chat_data, f)

    def load_chat(self):
        chat_files = sorted(glob.glob("chat_*.json"))
        for file_name in chat_files:
            with open(file_name, "r") as f:
                chat_data = json.load(f)
                for comment_text in chat_data["comments"]:
                    self.comment_list_box.insert(END, comment_text)
