import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

def display(results):
    for result in results:
        command_panel = Panel(
            result['result'],
            title=f"[bold cyan]Result for Command:[/bold cyan] {result['command']}",
            style="grey35"
        )
        console.print(command_panel)

def execute_shell_commands(commands):
    results = []
    plain_results = []
    
    for command in commands:
        command = command.strip()
        result, result_plain = run_command(command)
        results.append({'command': command, 'result': result})
        plain_results.append({'command': command, 'result': result_plain})
    
    display(results)
    return plain_results

def run_command(command):
    with console.status(f"Running command: {command}", spinner="dots") as status:
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = capture_output(process)
            
            return_code = process.wait()
            if return_code == 0:
                result_text = format_output('Command executed successfully', output, "green")
                result_plain = f'Command executed successfully\n### output\n{output}'
            else:
                result_text = format_output(f'Command failed with return code {return_code}', error, "red")
                result_plain = f'Command failed with return code {return_code}\n### error\n{error}'
                
        except Exception as e:
            result_text = format_output('Error', str(e), "bold red")
            result_plain = f'### Error\n{str(e)}'

        return result_text, result_plain

def capture_output(process):
    output = []
    error = []

    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        if line:
            output.append(line.strip())

    while True:
        err_line = process.stderr.readline()
        if not err_line and process.poll() is not None:
            break
        if err_line:
            error.append(err_line.strip())

    return '\n'.join(output), '\n'.join(error)

def format_output(title, content, style):
    return Markdown(f'**{title}**\n\n```output\n{content}\n```', style=style)

# commands = ["ls", "pwd", "echo 'Hello World'"]
# results = execute_shell_commands(commands)
