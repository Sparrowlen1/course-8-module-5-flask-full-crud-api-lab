from flask import Flask, jsonify, request

app = Flask(__name__)

class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

def find_event(event_id):
    for index, event in enumerate(events):
        if event.id == event_id:
            return event, index
    return None, None

@app.route('/')
def welcome():
    return jsonify({"message": "Welcome to the Event Management API"})

@app.route('/events', methods=['GET'])
def get_events():
    return jsonify([e.to_dict() for e in events])

@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Request must contain JSON"}), 400
    if "title" not in data:
        return jsonify({"error": "Missing 'title' field"}), 400

    new_id = max([e.id for e in events], default=0) + 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201

@app.route('/events/<int:event_id>', methods=['PATCH'])
def update_event(event_id):
    event, index = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Request must contain JSON"}), 400
    if "title" not in data:
        return jsonify({"error": "Missing 'title' field"}), 400

    event.title = data["title"]
    return jsonify(event.to_dict()), 200

@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event, index = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    del events[index]   # remove from the list

    # 🔑 REST convention: 204 No Content – empty response body
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)   # debug=True is fine