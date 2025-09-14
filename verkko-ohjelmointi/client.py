import json
import urllib.request
import threading
import time
import random

SERVER = "http://127.0.0.1:5000"

def get_server_quotes():
    """Hakee kaikki sitaatit palvelimen HTML-sivulta."""
    try:
        import re
        with urllib.request.urlopen(f"{SERVER}/") as html_resp:
            html = html_resp.read().decode("utf-8")
            return set(re.findall(r'“(.*?)”', html))
    except Exception:
        return set()

def post_json(url, data):
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8")), resp.status

# Socket.IO-asiakas
def socketio_sender():
    import socketio
    IMG_LIST = [
        'mattinykanen1.jpg',
        'mattinykanen2.jpg',
        'mattinykanen3.jpg',
        'mattinykanen4.jpg',
        'mattinykanen5.jpg'
    ]
    sio = socketio.Client()

    @sio.event
    def connect():
        print('SocketIO-yhteys muodostettu!')

    @sio.event
    def disconnect():
        print('SocketIO-yhteys katkaistu.')

    def send_loop():
        idx = 0
        while True:
            img = IMG_LIST[idx % len(IMG_LIST)]
            number = random.randint(1, 100)
            sio.emit('new_data', {'img': img, 'number': number})
            print(f'SocketIO lähetetty: {img}, {number}')
            idx += 1
            time.sleep(5)

    sio.connect(SERVER)
    send_loop()

def main():
    # Sitaattien lähetys
    sent = get_server_quotes()
    print("Lisää lempi Matti Nykäsen sitaatti palvelimelle.")
    count = 0
    while count < 3:
        quote = input(f"Anna sitaatti {count+1}: ").strip()
        if not quote:
            print("Tyhjä syöte, lopetetaan.")
            break
        if quote in sent:
            print("Sitaatti on jo palvelimella.")
            continue
        source = input("Anna lähde (tai jätä tyhjäksi): ").strip() or "Tuntematon"
        resp, status = post_json(f"{SERVER}/add", {"quote": quote, "source": source})
        if status == 201:
            print("Lisäys onnistui!")
            sent.add(quote)
            count += 1
        else:
            print(f"Virhe: {resp.get('error', 'Tuntematon virhe')}")

    # Socket.IO-kuva+numero lähetys omassa säikeessä
    t = threading.Thread(target=socketio_sender, daemon=True)
    t.start()
    print("Kuvan ja numeron lähetys käynnissä taustalla. Paina Ctrl+C lopettaaksesi.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Ohjelma lopetettu.")

if __name__ == "__main__":
    main()
