import json
import argparse
import requests
import datetime
import yaml


def get_config(config: str):
    # Reads a YAML configuration file.
    with open(f"config/{config}.yaml", "r") as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def read_prompt(file_name: str):
    with open(file_name, "r") as file:
        contents = file.read()
    return contents


def load_json(file_path: str):
    with open(file_path, 'r') as file:
        return json.load(file)


def create_headers(config: dict):
    # getting info of Huggingface inference endpoint
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {config['token']}",
        "Content-Type": "application/json"
    }
    return headers


def query(payload: dict, API_URL: str, headers: dict):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


# Submits a prompt (combination of system prompt and user prompt) to the model for generation.
def submit_prompt(system_prompt: str, prompt: str, config: dict, return_only_generated: bool = False):

    # Combine system and user prompts to form a single turn prompt with input template
    single_turn_prompt = f"{system_prompt}<|end_of_turn|>GPT4 Correct User: {prompt}" \
                         f"<|end_of_turn|>GPT4 Correct Assistant:"

    # Construct payload to be sent to the model
    payload = {
        "inputs": single_turn_prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 768
        }
    }

    # Send the payload to the model via the query function
    completion = query(payload=payload, API_URL=config['API_URL'], headers=create_headers(config))
    print(completion)
    if isinstance(completion, list) and len(completion) > 0 and 'generated_text' in completion[0]:
        # Extract the generated text from the completion
        result = completion[0]['generated_text']
        if return_only_generated:
            result = result.split("<|end_of_turn|>GPT4 Correct Assistant:")[-1]
        return result
    else:
        # Print an error message if something went wrong
        return print('Something went wrong:\n', completion)


def write_results(result: str, result_file_name: str):
    file_path = f"results/{result_file_name}"
    with open(file_path, "w") as file:
        file.write(result)


def main(sys_prompt, user_prompt, config_name, result_file_name):
    # Setting configuration for inference
    config = get_config(config_name)

    # Load system prompt and user prompt - text input
    sys_prompt = read_prompt(f"system_prompt/{sys_prompt}")
    user_prompt = read_prompt(f"user_prompt/{user_prompt}")

    result = submit_prompt(sys_prompt, user_prompt, config)
    write_results(result, result_file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate email.')
    parser.add_argument('--sys_prompt', type=str, help='Path to the JSON file containing system prompt.',
                        default="seb_example")
    parser.add_argument('--user_prompt', type=str, help='Path to the JSON file containing user prompt.',
                        default="seb_example")
    parser.add_argument('--config_name', type=str, help='Name of the Yaml file containing inference config',
                        default="openchat-3-5-extended")
    parser.add_argument("--result_file_name", type=str, help="Name of the file to write the email text to",
                        default=f'results-{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}.txt')

    args = parser.parse_args()
    main(args.sys_prompt, args.user_prompt, args.config_name, args.result_file_name)
