function sendQuote(e) {
  e.preventDefault();
  const quote = document.getElementById('quote').value.trim();
  const source = document.getElementById('source').value.trim() || 'Tuntematon';
  if (!quote) {
    showMsg('Sitaatti ei voi olla tyhjä.', true);
    return;
  }
  fetch('/add', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({quote, source})
  })
  .then(r => r.json().then(data => ({status: r.status, data})))
  .then(res => {
    if (res.status === 201) {
      showMsg('Sitaatti lisätty!');
      document.getElementById('quote').value = '';
      document.getElementById('source').value = '';
    } else {
      showMsg(res.data.error || 'Virhe lisäyksessä.', true);
    }
  })
  .catch(() => showMsg('Palvelinvirhe.', true));
}
function showMsg(msg, err) {
  document.getElementById('msg').textContent = msg;
  document.getElementById('msg').className = err ? 'err' : 'msg';
}

if (typeof io !== 'undefined') {
  const socket = io();
  socket.on('update', function(data) {
    let imgsrc = '';
    if (data.img) {
      imgsrc = '/static/kuvat/' + data.img;
    }
    const imgEl = document.getElementById('liveimg');
    if (imgEl) imgEl.src = imgsrc;
    const numEl = document.getElementById('livenum');
    if (numEl) numEl.textContent = data.number;
  });
}
