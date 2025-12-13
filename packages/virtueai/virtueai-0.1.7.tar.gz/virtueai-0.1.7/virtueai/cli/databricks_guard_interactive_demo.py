import argparse
import asyncio
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from virtueai.guard import GuardDatabricks, GuardDatabricksConfig
from virtueai.models import VirtueAIModel, DatabricksDbModel


async def chat():
    """Interactive chat prompt"""
    session = PromptSession(history=InMemoryHistory())

    print("Interactive Chat (type 'exit' or 'quit' to stop)\n")

    while True:
        try:
            user_input = await session.prompt_async("You: ")

            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break

            if not user_input.strip():
                continue

            # Return user input for processing
            yield user_input

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


async def main(databricks_api_key: str, databricks_url: str, virtueai_api_key: str, safety_check_query: bool, safety_check_response: bool):
    config = GuardDatabricksConfig(
        databricks_api_key=databricks_api_key,
        databricks_url=databricks_url,
        databricks_db_model=DatabricksDbModel.META_LLAMA_3_1_8B_INSTRUCT,
        safety_model=VirtueAIModel.VIRTUE_GUARD_TEXT_LITE,
        virtueai_api_key=virtueai_api_key,
        safety_check_query=safety_check_query,
        safety_check_response=safety_check_response,
    )
    guard = GuardDatabricks(config)

    async for user_message in chat():
        messages = [{"role": "user", "content": user_message}]
        response = await guard(messages)

        if response.validated_output:
            print(f"Assistant: {response.validated_output}\n")
        else:
            print(f"Assistant: {response.message}\n")


def main_cli():
    parser = argparse.ArgumentParser(description="Interactive Databricks Guard Demo")
    parser.add_argument("--databricks-api-key", required=True, help="Databricks API key")
    parser.add_argument("--databricks-url", required=True, help="Databricks URL")
    parser.add_argument("--virtueai-api-key", required=True, help="VirteuAI API key")
    parser.add_argument("--disable-safety-check-query", action="store_true", help="Safety check query")
    parser.add_argument("--disable-safety-check-response", action="store_true", help="Safety check response")
    args = parser.parse_args()

    asyncio.run(main(
        databricks_api_key=args.databricks_api_key,
        databricks_url=args.databricks_url,
        virtueai_api_key=args.virtueai_api_key,
        safety_check_query=not args.disable_safety_check_query,
        safety_check_response=not args.disable_safety_check_response,
    ))


if __name__ == "__main__":
    main_cli()