from sentence_transformers import SentenceTransformer


# Load the Sentence Transformer model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text):
    """
    Convert text into a 384-dimensional embedding.
    """
    return model.encode(text)