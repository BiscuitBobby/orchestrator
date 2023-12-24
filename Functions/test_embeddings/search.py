from sentence_transformers import SentenceTransformer, util

def compute_top_similarities(model, query, passages, top_k=3):
    # Encode the query and passages
    query_embedding = model.encode(query)
    passage_embeddings = model.encode(passages)

    # Compute the similarities
    similarities = [util.dot_score(query_embedding, passage_emb) for passage_emb in passage_embeddings]

    # Find the indices of the top-k passages with the highest similarities
    top_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)[:top_k]

    # Return the top indices and their corresponding similarity values
    return [(index, similarities[index]) for index in top_indices]

# Example usage for one query
model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

query = 'what is london known for'
passages_set = [
    'London has 9,787,426 inhabitants at the 2011 census',

    'London is known for its financial district',

    '''Below is a simple example of a PyQt application that creates a basic window with a button. When the button is clicked, a message box will appear.
    ```
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create a button
        button = QPushButton('Click me', self)
        button.clicked.connect(self.show_message_box)

        # Set up the layout
        layout = self.layout()
        layout.addWidget(button)

        # Set up the main window
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Simple PyQt App')

        self.show()

    def show_message_box(self):
        # Show a message box when the button is clicked
        QMessageBox.information(self, 'Message', 'Button Clicked!')

app = QApplication(sys.argv)
ex = SimpleApp()
sys.exit(app.exec_())
    ```
'''
]

top_similarities = compute_top_similarities(model, query, passages_set, top_k=3)

# Print the top 3 passages with their similarity values
print(f"Query: {query}")
for rank, (index, similarity) in enumerate(top_similarities, 1):
    print(f"Rank {rank}:")
    print(f"  Passage: {passages_set[index]}")
    print(f"  Similarity: {similarity}")
    print()
