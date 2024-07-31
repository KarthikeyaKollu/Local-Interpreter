from bs4 import BeautifulSoup
from markdownify import markdownify
import requests
import json
import time
import socketio
from user_proxy import execute_shell_commands
from utils.display_markdown import display_markdown
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()
sio = socketio.Client()
data_response = ''


@sio.on('response')
def on_response(msg):
    global data_response
    data_response = msg


def connect_to_server(url):
    sio.connect(url)


def extract_code_from_html(html_code):
    soup = BeautifulSoup(html_code, 'html.parser')
    code_blocks = soup.find_all('code')
    code_list = []

    for code in code_blocks:
        class_attr = code.get('class', [])
        language_class = next((cls for cls in class_attr if cls.startswith('language-')), '')
        language = language_class.replace('language-', '')
        code_text = code.get_text()
        
        if language == "bash":
            code_list.append(code_text.strip())

    return code_list


def send_message_to_endpoint(url, message, status):
    data = {'message': message}

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task(status, start=False)
            progress.start_task(task)

            response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))

            if response.status_code != 200:
                raise Exception(f'HTTP error! Status: {response.status_code}')

            return response.text
    except Exception as error:
        console.print('Error sending message to endpoint:', style="bold red")
        console.print(error, style="bold red")
        return None


def process_response(response):
    soup = BeautifulSoup(response, 'html.parser')
    assistant = markdownify(str(soup))
    display_markdown(assistant)
    return extract_code_from_html(response)


def handle_commands(commands):
    if 'DONE' in commands and not commands:
        return
    
    responses = execute_shell_commands(commands)
    flattened_string = ''.join(f"Command: {item['command']}\nResult: {item['result']}\n" for item in responses)
    return flattened_string

def process_commands(user_input, status, count=0, max_count=20):
    response = send_message_to_endpoint('http://localhost:3000/generate', user_input, status)
    
    if response:
        commands = process_response(response)
        
        if 'DONE' in response and not commands:
            return

        feedback = handle_commands(commands)
        
        if feedback:
            time.sleep(0.5)
            next_input = f'{feedback}\n### If a command executes successfully and satisfies the given condition: if there are no ongoing tasks associated with the previous conversation, such as summarizing or processing the output. If there is an ongoing task, do not output "DONE" else output "DONE" with some summary accordingly: ignore the unwanted logs'
            
            if count < max_count:
                process_commands(next_input, "Sending feedback...", count + 1, max_count)






def startInterpreter(max_count):
    connect_to_server('http://localhost:3000')
    
    while True:
        initial_input = input("\n>>>> ")
        if initial_input.lower() != 'y':
            process_commands(initial_input,"Sending message...",max_count=max_count)
        else:
            break

    sio.wait()


