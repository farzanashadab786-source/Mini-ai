
import json
import math
import os
import re
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_FILE = os.path.join(ROOT, "knowledge.json")
STARTER_FILE = os.path.join(ROOT, "data", "starter_knowledge.json")

def words(text):
    return re.findall(r"[a-z0-9']+", text.lower())

class TinyLocalAI:
    """
    A tiny offline retrieval chatbot.
    It ranks stored Q&A examples using TF-IDF-style cosine similarity.
    It is not a neural network or a general-purpose reasoning model.
    """

    def __init__(self):
        self.knowledge = []
        self._load()

    def _load(self):
        if os.path.exists(KNOWLEDGE_FILE):
            try:
                with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
                    self.knowledge = json.load(f)
                return
            except (OSError, json.JSONDecodeError):
                pass

        try:
            with open(STARTER_FILE, "r", encoding="utf-8") as f:
                self.knowledge = json.load(f)
        except (OSError, json.JSONDecodeError):
            self.knowledge = []

    def _save(self):
        with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.knowledge, f, ensure_ascii=False, indent=2)

    def teach(self, question, answer):
        self.knowledge.append({
            "question": question.strip(),
            "answer": answer.strip()
        })
        self._save()

    def _vector(self, text, document_frequency, total_docs):
        tokens = words(text)
        counts = Counter(tokens)
        vector = {}
        length = max(1, len(tokens))
        for token, count in counts.items():
            tf = count / length
            idf = math.log((1 + total_docs) / (1 + document_frequency[token])) + 1
            vector[token] = tf * idf
        return vector

    @staticmethod
    def _cosine(a, b):
        if not a or not b:
            return 0.0
        dot = sum(value * b.get(key, 0.0) for key, value in a.items())
        norm_a = math.sqrt(sum(v * v for v in a.values()))
        norm_b = math.sqrt(sum(v * v for v in b.values()))
        if not norm_a or not norm_b:
            return 0.0
        return dot / (norm_a * norm_b)

    def reply(self, question):
        q = question.strip()
        if not self.knowledge:
            return ("I don't know yet. Use /teach to teach me a question and answer.", 0)

        docs = [item["question"] for item in self.knowledge]
        df = Counter()
        for doc in docs:
            df.update(set(words(doc)))

        qv = self._vector(q, df, len(docs))
        best_item, best_score = None, 0.0

        for item in self.knowledge:
            dv = self._vector(item["question"], df, len(docs))
            score = self._cosine(qv, dv)
            if score > best_score:
                best_item, best_score = item, score

        if best_item and best_score >= 0.20:
            return best_item["answer"], best_score

        return (
            "I don't have a reliable answer for that yet. "
            "You can teach me with /teach, then ask again.",
            best_score
        )

    def forget(self, question):
        if not self.knowledge:
            return False
        docs = [item["question"] for item in self.knowledge]
        df = Counter()
        for doc in docs:
            df.update(set(words(doc)))
        qv = self._vector(question, df, len(docs))
        scored = [
            (self._cosine(qv, self._vector(item["question"], df, len(docs))), i)
            for i, item in enumerate(self.knowledge)
        ]
        score, index = max(scored, default=(0, -1))
        if index >= 0 and score >= 0.20:
            self.knowledge.pop(index)
            self._save()
            return True
        return False

    @staticmethod
    def help_text():
        return (
            "\nCommands:\n"
            "  /teach  Add a question and the answer you want me to learn\n"
            "  /list   Show saved Q&A knowledge\n"
            "  /forget Remove the closest matching question\n"
            "  /help   Show this help\n"
            "  /quit   Exit\n\n"
            "Ask normally to search the knowledge I already have.\n"
        )
