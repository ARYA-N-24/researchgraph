from langchain_ollama import OllamaLLM

from app.config import settings


class LLMModel:
    """
    Handles response generation
    using local LLM (Ollama).
    """

    def __init__(self):

        self.llm = OllamaLLM(
            model="phi3"
        )

    def generate_answer(
            self,
            query,
            retrieved_chunks
        ):

            """
            Generate multi-modal answer.
            """

            context = "\n\n".join(

                chunk["content"]

                for chunk in retrieved_chunks

            )

            prompt = f"""
        You are an intelligent research assistant.

        Use the provided context to answer the question.

        The context may contain:

        - Text explanations
        - Image descriptions
        - Table data

        If the question relates to:

        - Figures → use image descriptions
        - Tables → analyze table values
        - Concepts → use text

        Always give clear and accurate answers.

        Context:
        {context}

        Question:
        {query}

        Answer:
        """

            response = self.llm.invoke(
                prompt
            )

            return response