from backend.rag import RAGPipeline
from pathlib import Path


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
