import os
import ollama
import tkinter as tk
from tkinter import filedialog
import chat as ollama_chat

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ollama GUI")
        self.geometry("800x600")
        self.resizable(False, False)
        self.iconbitmap(f"{os.getcwd()}/assets/ollama_icon.ico")
        self.default_text = "Type your message here..."
        self.box_width = 50
        self.target_directory = os.path.expanduser("~")
        self.selected_file = None
        self.setup_ui()
    
    def setup_ui(self):
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.right_frame = tk.Frame(self, width=200, bg="#f0f0f0")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        self.top_section()
        self.chat_box()
        self.response_box()
        self.right_column_content()
    
    def top_section(self):
        frame = tk.Frame(self.main_frame)
        frame.pack(fill=tk.X, pady=5)

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

        tk.Label(frame, text="Model", font=("Arial", 10, "bold")).pack(anchor="w")
        model_menu = tk.OptionMenu(frame, self.model_var, *model_names)
        model_menu.pack(fill=tk.X)

        send_button = tk.Button(frame, text="Send", width=40, command=self.receive_chat)
        send_button.pack(side=tk.RIGHT, fill=tk.X, pady=5)
        
        self.save_file_name = tk.Entry(frame, width=45, fg="gray")
        self.save_file_name.pack(side=tk.LEFT, fill=tk.X, pady=6)
        self.save_file_name.insert(tk.END, "Save with filename...")
        self.save_file_name.bind("<FocusIn>", self.clear_default_text_save)
        self.save_file_name.bind("<Return>", self.on_enter_press)
        
    def chat_box(self):
        tk.Label(self.main_frame, text="Prompt:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.chat_box = tk.Text(self.main_frame, height=10, width=self.box_width, fg="gray", wrap="word")
        self.chat_box.pack(fill=tk.X, pady=5)
        self.chat_box.insert(tk.END, self.default_text)
        self.chat_box.bind("<FocusIn>", self.clear_default_text_chat)
        self.chat_box.bind("<Return>", self.on_enter_press)
    
    def on_enter_press(self, event):
        try:
            if event.state & 0x1: return
            self.receive_chat()
            return "break"
        except Exception:
            pass
    
    def response_box(self):
        tk.Label(self.main_frame, text="Response:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.prompt_display = tk.Text(self.main_frame, height=60, width=self.box_width, fg="black", state=tk.DISABLED, wrap="word")
        self.prompt_display.pack(fill=tk.X, pady=5)

    def receive_chat(self):
        user_message = self.chat_box.get("1.0", tk.END).strip()
        if not user_message or user_message == self.default_text:
            return
        
        save_name = self.save_file_name.get().strip() if self.save_file_name.get().strip() != "Save with filename..." else None            

        model = ollama_chat.Model(self.model_var.get())
        if model.image_analysis and self.selected_file:
            query = ollama_chat.Chat(user_message, image_path=self.selected_file, save_name=save_name)
        elif self.selected_file:
            with open(self.selected_file, 'r') as f:
                context = f.read()
            user_message = f"*Context:*\n```\n{context}\n```\n\n{user_message}"
            query = ollama_chat.Chat(user_message, save_name=save_name)
        else:
            query = ollama_chat.Chat(user_message, save_name=save_name)

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
            self.update_file_list()
            pass
        
    def clear_default_text_chat(self, event):
        try:
            if self.chat_box.get("1.0", tk.END).strip() == self.default_text:
                self.chat_box.delete("1.0", tk.END)
                self.chat_box.config(fg="black")
        except Exception as e:
            pass
    
    def clear_default_text_save(self, event):
        try:
            if self.save_file_name.get().strip() == "Save with filename...":
                self.save_file_name.delete(0, tk.END)
                self.save_file_name.config(fg="black")
        except Exception as e:
            pass
            
    def right_column_content(self):
        tk.Label(self.right_frame, text="File Explorer", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w")

        self.file_listbox = tk.Listbox(self.right_frame, height=30, width=30)
        self.file_listbox.pack(fill=tk.Y, pady=5)

        dir_frame = tk.Frame(self.right_frame, bg="#f0f0f0")
        dir_frame.pack(fill=tk.X, padx=5, pady=2)
        browse_button = tk.Button(dir_frame, text="Browse", width=9, command=self.on_browse)
        browse_button.pack(side=tk.RIGHT, padx=2)
        go_button = tk.Button(dir_frame, text="Select", width=9, command=self.on_file_select)
        go_button.pack(side=tk.LEFT, padx=2)
        self.current_file_button = tk.Button(self.right_frame, text="Select a file...", state=tk.DISABLED, command=self.show_selected_file)
        self.current_file_button.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        self.update_file_list()
        self.file_listbox.bind("<Double-Button-1>", self.on_file_select)
        
    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        try:
            files = ['.','..'] + os.listdir(self.target_directory)
            for file in files:
                self.file_listbox.insert(tk.END, file)
        except Exception as e:
            self.file_listbox.insert(tk.END, f"Error: {e}")
            pass
    
    def on_browse(self):
        try:
            new_directory = filedialog.askdirectory()
            if new_directory:
                self.target_directory = new_directory
                self.update_file_list()
        except Exception:
            pass

    def on_file_select(self, event=None):
        try:
            selected_file = self.file_listbox.get(self.file_listbox.curselection())
            if os.path.isdir(os.path.join(self.target_directory, selected_file)):
                self.target_directory = os.path.join(self.target_directory, selected_file)
                self.update_file_list()
            else:
                self.selected_file = os.path.join(self.target_directory, selected_file)
                self.current_file_button.config(text=selected_file, state=tk.NORMAL)
        except Exception:
            pass
    
    def show_selected_file(self):
        try:
            if self.selected_file:
                os.startfile(self.selected_file)
        except Exception:
            pass
    
    def run(self):
        self.mainloop()

def launch():        
    Window().run()