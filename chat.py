import ollama
import time, os, shutil

class Chat:
    def __init__(self, message: str, image_path: str = None, save_name: str = None, user: str = "user"):
        self.role: str = user
        self.message: str = message
        self.image_path: str = image_path
        self.save_name: str = save_name
        
class Model:
    def __init__(self, model: str, save_directory: str = None):
        self.model: str = model
        self.image_analysis: bool = self.model == 'llama3.2-vision'
        self.save_directory = save_directory or f"{self.model.replace(':', '-')}_chat_logs"
        self.save_directory = f"E:\\Users\\Trevor\\ollama_logs\\{self.save_directory}"
        os.makedirs(self.save_directory, exist_ok=True)
        if self.image_analysis:
            os.makedirs(f"{self.save_directory}/image_logs", exist_ok=True)
    
    def chat(self, chat: Chat):
        curr_date, curr_time = time.strftime("%y-%m-%d"), time.strftime("%H-%M-%S")
        with open(
                f"{self.save_directory}/{curr_date}_{chat.save_name.replace(' ', '-') or self.model.replace(':', '-') + '-chat'}_{curr_time}.md", 'w'
            ) as f:
            f.write(f"# Prompt:\n\n{chat.message}\n\n")
            if self.image_analysis and chat.image_path:
                image = os.path.join(os.getcwd(), chat.image_path)
                copied_image_name = f"{curr_date}_{os.path.splitext(os.path.basename(chat.image_path))[0]}_{curr_time}{os.path.splitext(chat.image_path)[1]}"
                shutil.copy(
                    chat.image_path, 
                    f"{self.save_directory}/image_logs/{copied_image_name}"
                )
                f.write(f"![Attached image](image_logs/{os.path.basename(copied_image_name)})\n\n")
            f.write("# Response:\n\n")
            for response in ollama.chat(
                model=self.model,
                messages=[{
                    'role': chat.role,
                    'content': chat.message,
                    'images': [image] if self.image_analysis else [''],
                }],
                stream=True
            ):
                f.write(response['message']['content'])
                yield response['message']['content']
            f.write("\n")

def _test():    
    llama32 = Model("llama3.2")
    query = Chat("What is in this file?") 

    for line in llama32.chat(query):
        print(line, end='', flush=True)
        