from pathlib import Path

from backend.llm import GeminiLLM
from backend.prompts import RAG_PROMPT
from backend.retriever import Retriever


class RAGPipeline:

    def __init__(self):

        self.retriever = Retriever()

        self.llm = GeminiLLM()

    def ask(self,question):

        if not question.strip():

            raise ValueError("Question cannot be empty.")

        docs = self.retriever.retrieve(question)

        if not docs:

            return {
                "answer":"No relevant information found.",
                "sources":[]
            }

        context = ""

        sources = []

        for i,doc in enumerate(docs,1):

            filename = Path(
                doc.metadata["source"]
            ).name

            page = doc.metadata["page"] + 1

            context += f"""
               Document {i}

               Source : {filename}

               Page : {page}

               {doc.page_content}

                   """

            sources.append(
                {
                    "file":filename,
                    "page":page,
                    "content":doc.page_content
                }
            )

        prompt = RAG_PROMPT.format(
            context=context,
            question=question
        )

        answer = self.llm.generate(prompt)

        return {
            "answer":answer,
            "sources":sources
        }
