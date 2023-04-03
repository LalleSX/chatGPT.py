import tkinter
import tkinter.messagebox
import customtkinter
import openai
import requests

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")
with open("src/apikey.txt", "r") as f:
    openai.api_key = f.read()
    f.close()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()


        self.configure_window()
        self.create_sidebar()
        self.create_main_content()

        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("Default")
        self.combobox_1.set("Choose model")
        self.textbox.insert("0.0", "Your message here!.\n\n")

    def configure_window(self):
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

    def create_sidebar(self):
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="ChatGPT.py", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text="+ New chat")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))

        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

    def create_main_content(self):
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Send a message...")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(self, border_width=2, text="Submit", command=self.submit_button_event)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        

        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.textbox.configure(state="disabled")

        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Options")
        self.tabview.tab("Options").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Options"), dynamic_resizing=False, values=["Default"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        models = ["GPT-3", "GPT-4"]
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("Options"), values=models)
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        
    def sidebar_button_event(self):
        print("Sidebar button clicked!")

    def submit_button_event(self):
        message = self.entry.get()
        if message:
            self.textbox.configure(state="normal")
            self.textbox.insert(tkinter.END, f"""You: {message}\n""")
            self.textbox.configure(state="disabled")
            self.entry.delete(0, tkinter.END)
            print("Message submitted: ", message)
if __name__ == "__main__":
    app = App()
    app.mainloop()

