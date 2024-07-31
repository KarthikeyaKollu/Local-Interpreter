import time
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live

def typing_effect(response, delay=0.0014):
    console = Console()
    typed_text = ""
    with Live(console=console, refresh_per_second=10) as live:
        for char in response:
            typed_text += char
            updated_markdown = Markdown(typed_text)
            panel = Panel(
                updated_markdown,
                title="Assistant Information",
                style="white",
                padding=(1, 2)
            )
            live.update(panel)
            time.sleep(delay)

def display_markdown(response):
    print("\n\n")
    s = response.replace("```\n", "```").replace("Copy code`", "\n").replace("`\n```","\n```\n")
    typing_effect(s)
    print("\n\n")  

       
text = """
 Here's a simple Bash script that prints the numbers from 1 to 100:


```
bashCopy code`#!/bin/bash

for i in {1..100}
do
    echo $i
done`
```
You can save this script to a file and execute it. Here are the steps:

1. Save the script to a file named `print_numbers.sh`:


```
bashCopy code`echo '#!/bin/bash

for i in {1..100}
do
    echo $i
done' > print_numbers.sh`
```
2. Make the script executable:


```
bashCopy code`chmod +x print_numbers.sh`
```
3. Execute the script:


```
bashCopy code`./print_numbers.sh`
```
Would you like any further customization or assistance with this script?


 """   
    
    
# display_markdown(text)

