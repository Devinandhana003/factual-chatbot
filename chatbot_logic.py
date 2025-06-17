from transformers import pipeline

# Load QA pipeline model
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

def get_factual_answer(question: str, context: str) -> str:
    greetings = ["hi", "hello", "hey", "how are you", "good morning", "good evening"]
    lower_question = question.lower().strip()

    # Respond to greetings or casual messages
    if any(greet in lower_question for greet in greetings):
        return "Hello! How can I help you with factual information?"

    # Use QA model only for actual factual questions
    result = qa_pipeline(question=question, context=context)
    return result["answer"]
