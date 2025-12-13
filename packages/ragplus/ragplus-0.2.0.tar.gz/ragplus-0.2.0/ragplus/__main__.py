from .pipeline import rag_answer

def _demo_llm(prompt: str) -> str:
    """Demo LLM that just echoes the prompt."""
    return "DEMO RESPONSE:\n" + prompt[:500]

def main():
    """Run a simple RAGKit demo."""
    print("Running ragplus demo...\n")

    doc = """
    Vacuum brazing uses a filler metal and a vacuum furnace
    to join materials with minimal distortion and high clean quality.
    """

    answer = rag_answer(
        query="What is vacuum brazing?",
        documents=doc,
        llm_fn=_demo_llm
    )

    print(answer)

if __name__ == "__main__":
    main()
