# CMND.ai Extension

## Concepts: 
- **LLM**: A type of AI, like ChatGPT, trained on vast amounts of text data to generate human-like responses based on text inputs.

- **Assistants**: Digital or virtual agents designed to assist users in performing a wide range of tasks via conversational interfaces. These assistants use an LLM as their core intelligence.

- **Tools**: Pre-defined functions or APIs that extend the capabilities of an LLM to perform specific tasks beyond its abilities.
- **RAG**: A technique that enhances Large Language Models by enabling them to access and utilize foundational knowledge.

- **Assistants With Tools**: Digital agents equipped with functionalities that LLMs alone cannot perform, such as accessing real-time data.

- **Assistants With RAG**: Digital agents equipped with the capability to acquire external knowledge and use it to enhance it's capabilites.
  

## Introduction

### Assistants:
computer programs that serve as virtual assistants and communicate with users through text-based interfaces on websites, social media platforms and messaging apps. These chatbots can assist customers, respond to inquiries or start a discussion with them. By equiping the asssitant with tools, the asssitant will be able to perform tasks that the LLM cannot do, and give it's result to the LLM to give you the final answer.

### Tools:
allows you to describe functions to the Assistants API and have it intelligently return the functions that need to be called along with their arguments.

![src/assistants.png](src/assistants.png)

### Create Assistant Exampele
```python
from openai import OpenAI
client = OpenAI()
  
assistant = client.beta.assistants.create(
  name="Math Tutor",
  instructions="You are a personal math tutor. Write and run code to answer math questions.",
  tools=[{"type": "code_interpreter"}],
  model="gpt-4-turbo",
```
In this code, there is tools attribute, where you pass the tools that you have created

### Create Tools Example 

```python
from openai import OpenAI
client = OpenAI()

assistant = client.beta.assistants.create(
  instructions="You are a weather bot. Use the provided functions to answer questions.",
  model="gpt-4-turbo",
  tools=[
    {
      "type": "function",
      "function": {
        "name": "get_current_temperature",
        "description": "Get the current temperature for a specific location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state, e.g., San Francisco, CA"
            },
            "unit": {
              "type": "string",
              "enum": ["Celsius", "Fahrenheit"],
              "description": "The temperature unit to use. Infer this from the user's location."
            }
          },
          "required": ["location", "unit"]
        }
      }
    }
  }
```

## Getting Started: 
This repository hosts a FastAPI and Flask applications, both designed to execute various server-side tools  and add them to CMND.ai dynamically based on requests. It allows users to query tool information and run specific tools by passing parameters.

1. Clone the repository:
```bash
git clone git@github.com:CyprusCodes/cmnd-extension-sample-python.git
``` 

3. Install the requirements
```bash
pip install requirements.txt
```

5. Navigate to the cloned directory:
```bash
cmnd-extension-sample-python
```

7. Determine whether you are using FastAPI or Flask, and navigate to the chosen directory.

8. Navigate to the tools file

9. Within the tool.py, create your tool definition by specifying its name, description, parameters, and the runCmd)Within the tool.py, create your tool definition by specifying its name, description, parameters, and the runCmd, which is the function itself, below is an example of function definition.

```python
def run_json_file_reader(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return json.dumps(data)
    except Exception as error:
        return f"An error occurred while reading the file: {str(error)}"
 
tools = [
    {
        "name": "json_file_reader",
        "description": "Reads JSON file content",
        "parameters": GetFilePathSchema,
        "runCmd": run_json_file_reader
    }
]
````
7. Run your app (server):
``` bash
python3 main.py
```
8. Any API Keys needed for your own tools they should be in your .env file

The rest is about endpints and some functions to help this endpoints, so you'r not going to play with the main in any case, you will only modify the tools.py where you will first add your tools schema definition, tool implementations, and at the end the tool configration
