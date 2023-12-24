from sentence_transformers import SentenceTransformer, util

def compute_similarity(model, query, passages):
    # Encode the query and passages
    query_embedding = model.encode(query)
    passage_embeddings = model.encode(passages)

    # Compute the similarities
    similarities = [util.dot_score(query_embedding, passage_emb) for passage_emb in passage_embeddings]

    # Find the index of the passage with the highest similarity
    max_similarity_index = similarities.index(max(similarities))

    # Return the index and the similarity value
    return max_similarity_index, similarities[max_similarity_index]

# Example usage for one query
model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

query = 'How to make a pyqt app'
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

max_similarity_index, max_similarity_value = compute_similarity(model, query, passages_set)

# Print the result with the highest similarity
print(f"Query: {query}")
print(f"Passage with Highest Similarity: {passages_set[max_similarity_index]}")
print(f"Highest Similarity Value: {max_similarity_value}")