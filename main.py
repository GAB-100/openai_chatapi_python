from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Set your OpenAI API key
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

PROMPT_TEXT_CHARACTER_LIMIT = 4000   # Should be 4096, But giving the model room to breath

def get_chat_completion(prompt, model="gpt-3.5-turbo", choices=4):
    """
    Get a chat completion response from the OpenAI API.

    Args:
        prompt (str): The input prompt for the chat completion.
        model (str): The OpenAI model to use (default is "gpt-3.5-turbo").
        choices (int): The number of choices to generate (default is 4).

    Returns:
        dict: The response generated by the ChatCompletion API.
    """
    try:
        response = client.chat.completions.create(
            messages=[{
                'role': 'user',
                'content': prompt
            }],
            model=model
        )
        return {
            "response": response,
            "success": True
        }
    except Exception as e:
        return {
            "response": e,
            "success": False
        }


def has_exceeded_max_length(prompt):
    """
    :param prompt:
    :return: Boolean based on whether the prompt exceeds the limit or not
    """
    global PROMPT_TEXT_CHARACTER_LIMIT
    return len(prompt) > PROMPT_TEXT_CHARACTER_LIMIT

def get_response_content(response):
    """
    :param response:
    :return: A dictionary with 3 keys, successful_generation (boolean), message (string), content_to_display (string)
    """
    #extract the content from the display
    content_to_display = response['choices'][0]['message']['content']

    # Check of generation finished successfully
    final_response = process_finish_reason(response['choices'][0]['finish_reason'])

    # Add the content to display to the response dictionary
    final_response['content_to_display'] = content_to_display

    return final_response

def process_finish_reason(finish_reason):
    """
    Checks the finish reason value from the api response to determine whether the generation was successful or not.
    :param finish_reason:
    :return:  A dictionary with 2 keys, successful_generation (boolean), message (string)
    """
    successful_generation = False
    if finish_reason == 'stop':
        successful_generation = True
        message = ""
    elif finish_reason == 'length':
        message = "Max tokens for text generation have expired"
    else:
        message = "Something went wrong. PLease try again later or reload the page and try again."

    return {
        'successful_generation': successful_generation,
        'message': message
    }

def main():
    # Create a prompt for the ChatCompletion API

    prompt = input("Enter propmt: ")

    # Make sure prompt doesn't exceed max length
    if has_exceeded_max_length(prompt):
        return {'successful_generation': False, 'message': "The message you submitted was too long. Please bundle your messages in short texts. Thank you."}

    # Generate a response using the ChatCompletion API
    completion_response = get_chat_completion(prompt)
    if not completion_response['success']:
        print(completion_response['response'])
        return completion_response['response']

    # Generate simpler response for Frontend
    response_to_user = get_response_content(completion_response['response'])
    # Print the response
    print(completion_response['response'])
    print(response_to_user)


if __name__ == "__main__":
    main()

# Sample Response from openai.ChatCompletion.create()
# <OpenAIObject chat.completion id=chatcmpl-7UkgnSDzlevZxiy0YjZcLYdUMz5yZ at 0x118e394f0> JSON: {
#   "id": "chatcmpl-7UkgnSDzlevZxiy0YjZcLYdUMz5yZ",
#   "object": "chat.completion",
#   "created": 1687563669,
#   "model": "gpt-3.5-turbo-0301",
#   "choices": [
#     {
#       "index": 0,
#       "message": {
#         "role": "assistant",
#         "content": "Orange who?"
#       },
#       "finish_reason": "stop"
#     }
#   ],
#   "usage": {
#     "prompt_tokens": 39,
#     "completion_tokens": 3,
#     "total_tokens": 42
#   }
# }

# Taken from url https://cookbook.openai.com/examples/how_to_format_inputs_to_chatgpt_models