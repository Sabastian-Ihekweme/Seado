const canvas = document.getElementById('whiteboardCanvas');
const ctx = canvas.getContext('2d');
canvas.width = canvas.offsetWidth;
canvas.height = canvas.offsetHeight;

let drawing = false;
const socket = io();

const sessionId = window.location.pathname.split('/').pop();
socket.emit('join', { room: sessionId });

socket.on('user_count', data => {
  document.getElementById('studentCount').value = data.count;
});

canvas.addEventListener('mousedown', () => drawing = true);
canvas.addEventListener('mouseup', () => drawing = false);
canvas.addEventListener('mouseout', () => drawing = false);

canvas.addEventListener('mousemove', e => {
  if (!drawing) return;
  const x = e.offsetX;
  const y = e.offsetY;
  ctx.lineTo(x, y);
  ctx.stroke();
  socket.emit('draw', { x, y, room: sessionId });
});

socket.on('draw', data => {
  ctx.lineTo(data.x, data.y);
  ctx.stroke();
});

document.getElementById('endButton').addEventListener('click', () => {
  socket.emit('end_session', { room: sessionId });
  alert('Session ended.');
  window.location.href = '/tutor-dashboard'; // or wherever you want to redirect
});

socket.on('session_ended', () => {
  alert("Tutor ended the session");
  window.location.href = '/student-dashboard';
});
