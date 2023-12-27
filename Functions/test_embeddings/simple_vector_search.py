from sentence_transformers import SentenceTransformer, util


def compute_top_similarities(model, query, threshold=0.2, top_k=3):
    # Encode the query and passages
    query_embedding = model.encode(query)


    # Compute the similarities
    similarities = [util.dot_score(query_embedding, passage_emb) for passage_emb in passage_embeddings]

    # Find the indices of passages with similarity values greater than the threshold
    top_indices = [i for i, sim in enumerate(similarities) if sim > threshold]

    # Sort the top indices based on similarity values
    top_indices = sorted(top_indices, key=lambda i: similarities[i], reverse=True)[:top_k]

    # Return the top indices and their corresponding similarity values
    return [(index, similarities[index]) for index in top_indices]


def vector_search(query):
    # Example usage for one query
    top_similarities = compute_top_similarities(model, query, top_k=3)

    # Print the top 3 passages with their similarity values
    print(f"Query: {query}")
    response = []
    for rank, (index, similarity) in enumerate(top_similarities, 1):
        print(f"Rank {rank}:")
        print(f"  Info: {knowledgebase[index]}")
        print(f"  Similarity: {similarity}")
        print()
        response.append(knowledgebase[index])
    return response


knowledgebase = [
    'Lemonade is in the fridge',

    'Icht will nicht',

    'There is no purpose in life, just give up on your dreams and die',

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
model = SentenceTransformer('all-MiniLM-L6-v2')
passage_embeddings = model.encode(knowledgebase)

#print(vector_search('pyqt app'))
