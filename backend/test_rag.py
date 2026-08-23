import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.rag import RAGPipeline


pipeline = RAGPipeline()

while True:
    question = input("\nAsk Question (type 'exit' to quit): ")

    if question.lower() == "exit":
        break

    result = pipeline.ask(question)

    print("\nAnswer:\n")
    print(result["answer"])

    print("\nSources:\n")

    for doc in result["sources"]:
        print(
             f"{Path(doc['file']).name} "
             f"(Page {doc['page']})"
             )
