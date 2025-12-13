import argparse
import asyncio
from re import S
from virtueai import GuardDatabricks, GuardDatabricksConfig, VirtueAIModel, DatabricksDbModel, VirtueAIResponseStatus, VirtueAIResponse


def test_databricks_guard(databricks_api_key: str, databricks_url: str, virtueai_api_key: str, safety_check_query: bool, safety_check_response: bool):
    config = GuardDatabricksConfig(
        databricks_api_key=databricks_api_key,
        databricks_url=databricks_url,
        databricks_db_model="databricks-meta-llama-3-1-8b-instruct", # DatabricksDbModel.META_LLAMA_3_1_8B_INSTRUCT,
        safety_model=VirtueAIModel.VIRTUE_GUARD_TEXT_LITE,
        virtueai_api_key=virtueai_api_key,
        safety_check_query=safety_check_query,
        safety_check_response=safety_check_response,
    )
    guard: GuardDatabricks = GuardDatabricks(config)
    response: VirtueAIResponse = asyncio.run(guard([{"role": "user", "content": "hey"}])) # safe
    # response: VirtueAIResponse = asyncio.run(guard([{"role": "user", "content": "how to make a bomb"}])) # unsafe
    # response: VirtueAIResponse = await guard([{"role": "user", "content": "Hello, how are you?"}])
    # assert response.status == VirtueAIResponseStatus.SUCCESS
    print(f"Response validated output: {response.validated_output}")
    print(f"Response status: {response.status}")
    print(f"Response message: {response.message}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Databricks Guard")
    parser.add_argument("--databricks-api-key", required=True, help="Databricks API key")
    parser.add_argument("--databricks-url", required=True, help="Databricks URL")
    parser.add_argument("--virtueai-api-key", required=True, help="VirtueAI API key")
    parser.add_argument("--disable-safety-check-query", action="store_true", help="Safety check query")
    parser.add_argument("--disable-safety-check-response", action="store_true", help="Safety check response")
    args = parser.parse_args()

    print(f"Safety check query: {not args.disable_safety_check_query}")
    print(f"Safety check response: {not args.disable_safety_check_response}")

    test_databricks_guard(
        databricks_api_key=args.databricks_api_key,
        databricks_url=args.databricks_url,
        virtueai_api_key=args.virtueai_api_key,
        safety_check_query=not args.disable_safety_check_query,
        safety_check_response=not args.disable_safety_check_response,
    )
