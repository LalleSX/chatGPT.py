import os
import json
from time import strftime
from pathlib import Path
from tkinter import END

import customtkinter
import openai

# Set API key at the start
openai.api_key = os.getenv("OPENAI_API_KEY")

# Constants
DEFAULT_OPTIONS = ["gpt-3.5-turbo", "gpt-4"]
DEFAULT_SIZE = (1100, 580)
CHAT_PATTERN = "chat_*.json"

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


def fetch_response(model, chat_history):
    """
    Fetch the response from OpenAI's API given the chat history.
    """
    response = openai.ChatCompletion.create(
        model=model,
        messages=chat_history,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n"],
    )
    return response.choices[0].message.content


class CommentSectionApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Comment Section")
        self.setup_main_layout()
        self.chat_files_combo = customtkinter.CTkComboBox(self, values=[])

    def setup_main_layout(self):
        self.configure_layout()
        self.setup_comment_section()
        self.setup_new_chat_button()
        self.setup_user_input_box()
        self.setup_model_options()
        self.setup_submit_button()
        self.setup_sidebar()

    def configure_layout(self):
        self.title("ChatGPT.py")
        self.geometry(f"{1100}x{580}")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

    def setup_sidebar(self):
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="ChatGPT.py",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

    def setup_user_input_box(self):
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Send a message...")
        self.entry.grid(
            row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew"
        )

    def setup_model_options(self):
        options = ["gpt-3.5-turbo", "gpt-4"]
        self.combo = customtkinter.CTkComboBox(self, values=options)
        self.combo.set(options[0])
        self.combo.grid(row=0, column=3, padx=(20, 0), pady=(20, 20), sticky="ew")

    def setup_submit_button(self):
        submit_button = customtkinter.CTkButton(
            self, border_width=2, text="Submit", command=self.on_submit_clicked
        )
        submit_button.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def setup_comment_section(self):
        self.comment_list_box = customtkinter.CTkTextbox(self, state="disabled")
        self.comment_list_box.grid(
            row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )
        self.load_chat()

    def setup_new_chat_button(self):
        new_chat_button = customtkinter.CTkButton(
            self, border_width=2, text="Start a new chat", command=self.start_new_chat
        )
        new_chat_button.grid(row=1, column=3, sticky="ew", padx=10, pady=10)

    ## Frontend to backend
    def get_chat_history(self):
        chat_history: list = []
        for comment in self.comment_list_box.get("0.0", "end").splitlines():
            if comment.startswith("You: "):
                chat_history.append({"role": "user", "content": comment[5:]})
            elif comment.startswith("Assistant: "):
                chat_history.append({"role": "assistant", "content": comment[11:]})
        return chat_history

    def get_response(self, user_input):
        model = self.combo.get()
        chat_history = self.get_chat_history()
        chat_history.append({"role": "user", "content": user_input})
        response_text = fetch_response(model, chat_history)
        return response_text

    def on_submit_clicked(self):
        user_input = self.entry.get()
        if user_input:
            self.update_comment_list_box(f"You: {user_input}")
            response_text = self.get_response(user_input)
            self.update_comment_list_box(f"Assistant: {response_text}")
            self.entry.delete(0, "end")

    def update_comment_list_box(self, text):
        self.comment_list_box.configure(state="normal")
        self.comment_list_box.insert(END, text + "\n")
        self.comment_list_box.configure(state="disabled")

    def start_new_chat(self):
        self.comment_list_box.configure(state="normal")
        self.comment_list_box.delete("0.0", "end")
        self.comment_list_box.configure(state="disabled")

    def save_chat(self):
        file_name = f"chat_{int(strftime('%d%m%y'))}.json"
        chat_data = {"comments": self.comment_list_box.get("0.0", "end").splitlines()}
        with open(file_name, "w") as f:
            json.dump(chat_data, f)

    def load_chat(self):
        chat_files = sorted(Path().glob(CHAT_PATTERN))
        for file_name in chat_files:
            self.chat_files_combo.add(file_name.name)
        if chat_files:
            self.chat_files_combo.set(chat_files[-1].name)
            self.load_chat_file()

    def load_chat_file(self):
        file_name = self.chat_files_combo.get()
        with open(file_name, "r") as f:
            chat_data = json.load(f)
        self.comment_list_box.configure(state="normal")
        self.comment_list_box.delete("0.0", "end")
        for comment in chat_data["comments"]:
            self.comment_list_box.insert(END, comment + "\n")
        self.comment_list_box.configure(state="disabled")


def main():
    app = CommentSectionApp()
    app.mainloop()


if __name__ == "__main__":
    main()
