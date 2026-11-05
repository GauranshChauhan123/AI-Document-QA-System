from backend.rag import RAGPipeline
from dotenv import load_dotenv
from openai import OpenAI
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import ContextualRelevancyMetric,AnswerRelevancyMetric,FaithfulnessMetric
from deepeval.models import DeepEvalBaseLLM
from deepeval.evaluate.configs import CacheConfig
from backend.retriever import Retriever

load_dotenv()


import os
import sys
import json
import asyncio

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class AgentRouterJudge(DeepEvalBaseLLM):
    def __init__(self, model_name="gpt-5.6-sol", *args, **kwargs):
        self.model_name = model_name
        super().__init__(model=model_name, *args, **kwargs)

    def load_model(self):
        return OpenAI(
            base_url="https://agentrouter.org/v1",
            api_key=os.environ.get("OPENCODE_API_KEY"),
            default_headers={"User-Agent": "opencode/1.17.12"}
        )

    def generate(self, prompt: str, schema=None, *args, **kwargs) -> str:
        client = self.model
        response = client.responses.create(
            model=self.model_name,
            input=prompt,
            timeout=120
        )
        return response.output_text

    async def a_generate(self, prompt: str, schema=None, *args, **kwargs) -> str:
        return await asyncio.to_thread(self.generate, prompt, schema, *args, **kwargs)

    def get_model_name(self) -> str:
        return self.model_name



eval_judge = AgentRouterJudge()



contextual_relevancy= ContextualRelevancyMetric(
    threshold=0.7,
    include_reason=True,
    model=eval_judge,
)

faithfullness= FaithfulnessMetric(
    threshold=0.7,
    include_reason=True,
    model=eval_judge,
)

answer_relevancy= AnswerRelevancyMetric(
    threshold=0.7,
    include_reason=True,
    model=eval_judge,
)



data_path = os.path.join(os.path.dirname(__file__), "..", "golden_dataset", "eval.json")

with open(data_path, "r", encoding="utf-8") as f:
    dataset = json.load(f)

dataset=dataset[:5]
rag=RAGPipeline()
test_cases = []

for item in dataset:
    question = item["input"]
    output = rag.ask(question)

    test_case = LLMTestCase(
        input=question,
        actual_output=output["answer"],
        retrieval_context=output["retrieval_context"]
    )

    test_cases.append(test_case)


evaluate(
    test_cases=test_cases,
    metrics=[
        contextual_relevancy,
        faithfullness,
        answer_relevancy
    ],
    hyperparameters={
        "embedding_model": "all-MiniLM-L6-v2",
        "chunk_size": 1000,
        "chunk_overlap": 200,
        "top_k": 6,
        "hybrid_search":"mmr and bm25",
        "fetch_k": 10,
        "evaluation_model": "gpt-5.6-sol",
        "generator_model": "gemini-2.5-flash"
    },
    cache_config=CacheConfig(write_cache=False, use_cache=False)
)
