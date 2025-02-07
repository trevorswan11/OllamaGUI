import ollama
import tkinter as tk
import chat as ollama_chat

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ollama GUI")
        self.geometry("800x600")
        self.resizable(False, False)
        self.iconbitmap("C:\\Users\\Trevor\\ollama_gui\\assets\\ollama_icon.ico")
        self.default_text = "Type your message here..."
        self.box_width = 97
        self.top_section()
        self.chat_box()
        self.response_box()
    
    def top_section(self):
        frame = tk.Frame(self)
        frame.pack(pady=10)

        models = ollama.list()
        model_names = [
            str(model['model']).removesuffix(':latest')
            for model in models.get('models', [])
            if model['model'] != 'nomic-embed-text:latest'
        ]

        if not model_names:
            model_names.append("No models found")

        self.model_var = tk.StringVar(self)
        self.model_var.set(model_names[0])

        model_menu = tk.OptionMenu(frame, self.model_var, *model_names)
        model_menu.pack(side=tk.LEFT, padx=5)

        send_button = tk.Button(frame, text="Send", command=self.receive_chat)
        send_button.pack(side=tk.LEFT, padx=5)
    
    def chat_box(self):
        tk.Label(self, text="Prompt:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
        self.chat_box = tk.Text(self, height=10, width=self.box_width, fg="gray", wrap="word")
        self.chat_box.pack(pady=10)
        self.chat_box.insert(tk.END, self.default_text)
        self.chat_box.bind("<FocusIn>", self.clear_default_text)
        
    def response_box(self):
        tk.Label(self, text="Response:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
        self.prompt_display = tk.Text(self, height=20, width=self.box_width, fg="black", state=tk.DISABLED, wrap="word")
        self.prompt_display.pack(pady=10)

    def clear_default_text(self, event):
        if self.chat_box.get("1.0", tk.END).strip() == self.default_text:
            self.chat_box.delete("1.0", tk.END)
            self.chat_box.config(fg="black")

    def receive_chat(self):
        user_message = self.chat_box.get("1.0", tk.END).strip()
        if not user_message or user_message == self.default_text:
            return

        model = ollama_chat.Model(self.model_var.get())
        query = ollama_chat.Chat(user_message)

        self.prompt_display.config(state=tk.NORMAL)
        self.prompt_display.delete("1.0", tk.END)

        self.response_generator = model.chat(query)
        self.print_next_word()

    def print_next_word(self):
        try:
            word = next(self.response_generator)
            self.prompt_display.insert(tk.END, word)
            self.prompt_display.yview(tk.END)

            self.after(1, self.print_next_word)
        except StopIteration:
            self.prompt_display.config(state=tk.DISABLED)
            pass
    
    def run(self):
        self.mainloop()