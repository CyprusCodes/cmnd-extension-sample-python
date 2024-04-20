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
