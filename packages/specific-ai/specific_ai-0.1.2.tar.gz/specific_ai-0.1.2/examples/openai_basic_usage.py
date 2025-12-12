from specific_ai import OpenAI
import logging


def classification_example():
    """Example of using optune.OpenAI for text classification."""

    # This is an example of how to use OpenAI with the Optune SDK.
    # As default, it sends requests to the OpenAI API, and only traces the results 
    # to the configured optune model with the given project and task name.

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

    # Initialize the OpenAI client with SpecificAI integration
    client = OpenAI(
        specific_ai_url="<your-specific-ai-service-URL>",
        api_key="<your-openai-api-key>",
        use_specific_ai_inference=True,  # Set to true once you successfully deployed the model through the SpecificAI platform
    )

    # Sends a request to the OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=1,
        specific_ai={  # SpecificAI's parameters
            "task_name": "classification-example",  # choose any name you prefer
        },
    )

    print(f"Classification result: {response.choices[0].message.content}")


if __name__ == "__main__":
    classification_example()
