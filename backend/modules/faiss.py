import faiss
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer
import pandas as pd

class ScamFAISS:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initializes the FAISS-based scam retrieval system.
        """
        self.embed_model = SentenceTransformer(model_name)
        self.faiss_index = None
        self.texts = []
        self.df = None

    def load_data(self, csv_path):
        """
        Loads scam data from a CSV file.
        """
        self.df = pd.read_csv(csv_path)
        self.texts = self.df["TEXT"].tolist()

    def create_faiss_index(self):
        """
        Converts scam text to embeddings and creates a FAISS index.
        """
        if self.df is None:
            raise ValueError("Data not loaded. Run load_data() first.")

        self.embeddings = np.array(self.embed_model.encode(self.texts, convert_to_numpy=True))

        index_file = "scam_faiss.index"
        if not os.path.exists(index_file):
            dimension = self.embeddings.shape[1]
            self.faiss_index = faiss.IndexFlatL2(dimension)
            self.faiss_index.add(self.embeddings)
            faiss.write_index(self.faiss_index, index_file)

            with open("scam_texts.pkl", "wb") as f:
                pickle.dump(self.texts, f)
        else:
            self.load_faiss_index()

    def load_faiss_index(self, index_path="scam_faiss.index", texts_path="scam_texts.pkl"):
        """
        Loads the FAISS index and scam texts if they exist.
        """
        if not os.path.exists(index_path) or not os.path.exists(texts_path):
            raise FileNotFoundError("FAISS index or stored texts not found. Run create_faiss_index() first.")

        self.faiss_index = faiss.read_index(index_path)
        with open(texts_path, "rb") as f:
            self.texts = pickle.load(f)

    def search_similar_text(self, query_text, top_k=3):
        """
        Searches for the most similar scam texts using FAISS.
        """
        query_embedding = np.array(self.embed_model.encode([query_text], convert_to_numpy=True))
        distances, indices = self.faiss_index.search(query_embedding, top_k)

        similar_texts = [self.texts[i] for i in indices[0] if i < len(self.texts)]
        return similar_texts
