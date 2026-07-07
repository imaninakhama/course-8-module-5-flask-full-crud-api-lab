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
    Event(2, "Python Workshop"),
]

# Keeps track of the next id to assign so ids stay unique
# even after events have been deleted.
next_id = 3


# ----------------------------
# Helper functions
# ----------------------------
def find_event(event_id):
    """Return the Event with the given id, or None if it doesn't exist."""
    return next((event for event in events if event.id == event_id), None)


# ----------------------------
# Routes
# ----------------------------
@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Welcome to the Event Management API"}), 200


@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200


@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True)

    if not data or not data.get("title"):
        return jsonify({"error": "The 'title' field is required."}), 400

    global next_id
    new_event = Event(next_id, data["title"])
    events.append(new_event)
    next_id += 1

    return jsonify(new_event.to_dict()), 201


@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)

    if event is None:
        return jsonify({"error": f"Event with id {event_id} not found."}), 404

    data = request.get_json(silent=True)

    if not data or not data.get("title"):
        return jsonify({"error": "The 'title' field is required."}), 400

    event.title = data["title"]

    return jsonify(event.to_dict()), 200


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)

    if event is None:
        return jsonify({"error": f"Event with id {event_id} not found."}), 404

    events.remove(event)

    return jsonify({"message": f"Event with id {event_id} deleted."}), 200


if __name__ == "__main__":
    app.run(debug=True)