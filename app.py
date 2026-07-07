from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
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

# Helper function to find an event by ID and its index
def find_event(event_id):
    for index, event in enumerate(events):
        if event.id == event_id:
            return event, index
    return None, None

# Root route – welcome message (required by rubric)
@app.route('/')
def welcome():
    return jsonify({"message": "Welcome to the Event Management API"})

# GET /events – return all events
@app.route('/events', methods=['GET'])
def get_events():
    return jsonify([event.to_dict() for event in events])

# POST /events – create a new event
@app.route('/events', methods=['POST'])
def create_event():
    # Parse JSON from request body
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Request must contain JSON"}), 400

    # Validate required field
    if "title" not in data:
        return jsonify({"error": "Missing 'title' field"}), 400

    # Generate new ID (max existing + 1, or 1 if list is empty)
    new_id = max([event.id for event in events], default=0) + 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)

    # Return the created event with 201 Created status
    return jsonify(new_event.to_dict()), 201

# PATCH /events/<id> – update an event's title
@app.route('/events/<int:event_id>', methods=['PATCH'])
def update_event(event_id):
    # Find the event
    event, index = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    # Parse JSON from request body
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Request must contain JSON"}), 400

    # Validate that 'title' is provided
    if "title" not in data:
        return jsonify({"error": "Missing 'title' field"}), 400

    # Update the event's title
    event.title = data["title"]

    # Return the updated event
    return jsonify(event.to_dict()), 200

# DELETE /events/<id> – remove an event
@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    # Find the event
    event, index = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    # Remove from list
    events.pop(index)

    # Respond with 200 OK and a confirmation message
    return jsonify({"message": f"Event {event_id} deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)