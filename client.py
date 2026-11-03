import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    base_url="https://agentrouter.org/v1",
    api_key=os.environ.get("OPENCODE_API_KEY"),
    default_headers={"User-Agent": "opencode/1.17.12"}
)

response = client.responses.create(
    model="gpt-5.6-sol",
    input="what is rag evaluation"
)

print(response.output_text)
