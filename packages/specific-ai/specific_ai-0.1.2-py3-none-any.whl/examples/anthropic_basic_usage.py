from specific_ai import Anthropic
import logging

def classification_example():
    """Example of using specific_ai.Anthropic for text classification."""

    # This is an example of how to use Anthropic with the SpecificAI SDK.
    # As default, it sends requests to the Anthropic API, and only traces the results 
    # to the configured SpecificAI model with the given project and task name.

    # For example, let's write a prompt for classification of a question to one of two categories:
    PROMPT_TEMPLATE = """
given the example, classify the reviews to one of two options according to their content, the optional categories are: 
Label 0: Negative 
Label 1: Positive 

always return only the numerical value for each review, meaning you will return a number either 0 or 1. 
for example: 0, another example: 1. no other talks.

"""
    prompt = f"{PROMPT_TEMPLATE}This movie was terrible!"


    # To capture logs from the SDK, configure logging in your application
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Initialize the Anthropic client with SpecificAI integration
    client = Anthropic(
        specific_ai_url="<your-specific-ai-service-URL>",
        api_key="<your-anthropic-api-key>",
        use_specific_ai_inference=True,  # Set to true once you successfully deployed the model through the SpecificAI platform
    )

    # Sends a request to the Anthropic API
    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        messages=[
            {"role": "user", "content": prompt},
        ],
        max_tokens=20000,
        specific_ai={  # SpecificAI's parameters
            "task_name": "classification-example",  # choose any name you prefer
        },
    )

    print(f"Classification result: {response.content[0].text}")


if __name__ == "__main__":
    classification_example()
