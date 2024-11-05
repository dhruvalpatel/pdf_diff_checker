import random
class Classify:
    """This class is used to classify the PDFs."""

    @staticmethod
    def classify():
        statuses = ["warranty", "transaction", "troubleshooting", "unknown"]
        return random.choice(statuses)
