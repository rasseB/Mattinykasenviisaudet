from flask import Flask, request, jsonify, render_template, render_template_string
from flask_socketio import SocketIO, emit
from pathlib import Path
import json, random, itertools

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

DATA_FILE = Path("quotes.json")

def load_db():
    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as f:
            raw = json.load(f)
            return {int(k): v for k, v in raw.items()}
    return {}

def save_db(db):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in db.items()}, f, ensure_ascii=False, indent=2)


IMG_LIST = [
  'mattinykanen1.jpg',
  'mattinykanen2.jpg',
  'mattinykanen3.jpg',
  'mattinykanen4.jpg',
  'mattinykanen5.jpg'
]
current_img_idx = 0
current_number = 0

counter = itertools.count(start=(max(load_db().keys()) + 1) if load_db() else 1)

@app.get("/")
def root():
  """Näyttää satunnaiset 5 sitaattia HTML-sivuna ja lomakkeen uuden lisäämiseen."""
  quotes = list(load_db().values())
  picks = random.sample(quotes, 5)
  return render_template("index.html", quotes=picks, total=len(quotes))

@app.post("/add")
def add():
  """
  Lisää sitaatin kokoelmaan.
  Odottaa JSONia: {"quote": "...", "source": "..."}.
  source voi olla "Tuntematon"/"Unknown" jos ei tiedossa.
  Palauttaa luodun kohteen: {"id": n, "quote": "...", "source": "..."}.
  """
  try:
    payload = request.get_json(force=True, silent=False) or {}
  except Exception:
    return jsonify(error="Invalid JSON"), 400

  text = (payload.get("quote") or "").strip()
  source = (payload.get("source") or "Tuntematon").strip() or "Tuntematon"
  if not text:
    return jsonify(error="Field 'quote' is required"), 400

  db = load_db()
  for q in db.values():
    if q["text"].strip() == text:
      return jsonify(error="Quote already exists", quote=text), 409

  _id = next(counter)
  db[_id] = {"text": text, "source": source}
  save_db(db)
  return jsonify(id=_id, quote=text, source=source), 201

@app.get("/daily")
def daily():
  """Palauttaa satunnaisen sitaatin JSON-muodossa (id, quote, source)."""
  from flask import make_response
  db = load_db()
  if not db:
    return jsonify(error="No quotes yet"), 404
  _id = random.choice(list(db.keys()))
  item = db[_id]
  response = make_response(jsonify(id=_id, quote=item["text"], source=item["source"]))
  response.headers["Content-Type"] = "application/json; charset=utf-8"
  return response

@socketio.on('connect')
def handle_connect():
  emit('update', {
    'img': IMG_LIST[current_img_idx],
    'number': current_number
  })

@socketio.on('new_data')
def handle_new_data(data):
  global current_img_idx, current_number
  img = data.get('img', IMG_LIST[0])
  number = data.get('number', 0)
  if img in IMG_LIST:
    current_img_idx = IMG_LIST.index(img)
  else:
    current_img_idx = 0
  current_number = number
  socketio.emit('update', {'img': img, 'number': number})

if __name__ == "__main__":
  import os
  port = int(os.environ.get("PORT", 5000))
  socketio.run(app, host="0.0.0.0", port=port, debug=True)
