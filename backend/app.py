from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from txtai.embeddings import Embeddings

app = Flask(__name__)
CORS(app)

notes = [
    {
        "id": 1,
        "title": "Quantum Computing Breakthrough",
        "content": "Recent developments in quantum computing have demonstrated significant advances in error correction algorithms. These breakthroughs could accelerate the commercialization of quantum technology and enhance computational speeds exponentially.",
        "tags": ["quantum computing", "technology", "breakthroughs", "error correction", "future tech"],
        "created_at": "2024-09-18T09:00:00Z",
        "updated_at": "2024-09-18T09:00:00Z"
    },
    {
        "id": 2,
        "title": "Morning Routine for Productivity",
        "content": "Wake up at 6:00 AM, 20 minutes of meditation, 15 minutes of stretching, then a healthy breakfast. Follow this with a clear focus on the top three tasks of the day. Avoid distractions and focus on deep work sessions using the Pomodoro technique or uninterrupted work blocks.",
        "tags": ["productivity", "routines", "deep work", "morning habits"],
        "created_at": "2024-09-18T07:30:00Z",
        "updated_at": "2024-09-18T07:30:00Z"
    },
    {
        "id": 3,
        "title": "The Nature of Creativity in Software Development",
        "content": "Creativity in software development stems from problem-solving in unique and unconventional ways. It’s not just about writing code; it’s about envisioning how the system interacts with users, anticipating future needs, and thinking holistically about performance, security, and scalability.",
        "tags": ["creativity", "software development", "problem-solving", "systems thinking"],
        "created_at": "2024-09-18T08:00:00Z",
        "updated_at": "2024-09-18T08:00:00Z"
    },
    {
        "id": 4,
        "title": "Kafka on the Shore - Themes",
        "content": "Haruki Murakami's *Kafka on the Shore* explores the interplay between consciousness and the unconscious, memory, fate, and free will. The novel blurs the lines between reality and dream, encouraging the reader to contemplate the meaning of identity and destiny.",
        "tags": ["literature", "Murakami", "Kafka on the Shore", "philosophy", "identity", "fate"],
        "created_at": "2024-09-18T06:45:00Z",
        "updated_at": "2024-09-18T06:45:00Z"
    },
    {
        "id": 5,
        "title": "Essential Nutrients for Brain Health",
        "content": "Omega-3 fatty acids, B vitamins, and antioxidants are critical for brain function. Foods rich in these nutrients include fatty fish, leafy greens, and berries. Regular consumption can improve cognitive function, memory, and overall brain health.",
        "tags": ["health", "nutrition", "brain health", "omega-3", "vitamins", "antioxidants"],
        "created_at": "2024-09-18T05:00:00Z",
        "updated_at": "2024-09-18T05:00:00Z"
    },
    {
        "id": 6,
        "title": "Machine Learning and Pattern Recognition",
        "content": "The core of machine learning is the ability to recognize patterns in vast datasets. Algorithms such as neural networks, decision trees, and clustering models work together to identify trends, correlations, and anomalies, driving automation in industries from finance to healthcare.",
        "tags": ["machine learning", "AI", "pattern recognition", "automation", "neural networks"],
        "created_at": "2024-09-18T06:15:00Z",
        "updated_at": "2024-09-18T06:15:00Z"
    },
    {
        "id": 7,
        "title": "Climate Change and Ocean Acidification",
        "content": "Ocean acidification is one of the most pressing yet often overlooked consequences of climate change. Increased CO2 levels cause a drop in pH, threatening marine ecosystems, particularly coral reefs.",
        "tags": ["climate change", "ocean acidification", "environment", "marine biology", "CO2"],
        "created_at": "2024-09-18T08:30:00Z",
        "updated_at": "2024-09-18T08:30:00Z"
    },
    {
        "id": 8,
        "title": "John’s Feedback on UI Design (Meeting 09/17)",
        "content": "John mentioned that the UI feels too cluttered on mobile devices. He suggested simplifying the layout by reducing the number of elements visible on the main screen and focusing on a single call-to-action at a time.",
        "tags": ["UI design", "feedback", "mobile", "UX", "meeting notes"],
        "created_at": "2024-09-18T10:15:00Z",
        "updated_at": "2024-09-18T10:15:00Z"
    },
    {
        "id": 9,
        "title": "My Thoughts on Pantheism",
        "content": "Pantheism resonates with me because it encapsulates a worldview where everything is interconnected. The universe, nature, and consciousness are all one entity. This perspective aligns with my belief in the inherent order of things, even when we can’t see it immediately.",
        "tags": ["philosophy", "pantheism", "spirituality", "worldview", "interconnectedness"],
        "created_at": "2024-09-18T07:00:00Z",
        "updated_at": "2024-09-18T07:00:00Z"
    },
    {
        "id": 10,
        "title": "Exploring Docker for DevOps Automation",
        "content": "Docker containers simplify the deployment process by allowing developers to package applications with all dependencies in one environment. This automation reduces the time spent debugging platform-specific issues, streamlines development, and improves consistency across different environments.",
        "tags": ["DevOps", "Docker", "automation", "containers", "development"],
        "created_at": "2024-09-18T09:30:00Z",
        "updated_at": "2024-09-18T09:30:00Z"
    }
]

# Initialize txtai embeddings
embeddings = Embeddings({"path": "sentence-transformers/all-MiniLM-L6-v2"})

def update_embeddings():
    texts = [f"{note['title']} {note['content']} {' '.join(note['tags'])}" for note in notes]
    embeddings.index(texts)

update_embeddings()

@app.route('/api/notes', methods=['GET'])
def get_notes():
    return jsonify(notes)

@app.route('/api/notes', methods=['POST'])
def add_note():
    new_note = request.json
    new_note['id'] = max([note['id'] for note in notes] + [0]) + 1
    new_note['created_at'] = datetime.utcnow().isoformat() + 'Z'
    new_note['updated_at'] = new_note['created_at']
    notes.append(new_note)
    update_embeddings()
    return jsonify(new_note), 201

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = next((note for note in notes if note['id'] == note_id), None)
    if note:
        updated_note = request.json
        updated_note['id'] = note_id
        updated_note['created_at'] = note['created_at']
        updated_note['updated_at'] = datetime.utcnow().isoformat() + 'Z'
        notes[notes.index(note)] = updated_note
        update_embeddings()
        return jsonify(updated_note)
    return jsonify({"error": "Note not found"}), 404

@app.route('/api/search', methods=['GET'])
def search_notes():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    results = embeddings.search(query, len(notes))
    search_results = [notes[i] for i, _ in results]
    return jsonify(search_results)

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = next((note for note in notes if note['id'] == note_id), None)
    if note:
        notes.remove(note)
        update_embeddings()
        return jsonify(note)
    return jsonify({"error": "Note not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)