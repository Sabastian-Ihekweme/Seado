const whiteboard = document.getElementById('whiteboard');
const endButton = document.getElementById('endButton');
const studentCount = document.getElementById('studentCount');

// Connect to WebSocket server
const socket = io();
let isTeacher = true; // This is the teacher's view
let sessionActive = true;
let currentPaths = {};
let isDrawing = false;
let currentPathId = null;

// Initialize whiteboard dimensions
function initWhiteboard() {
    whiteboard.style.width = whiteboard.offsetWidth + 'px';
    whiteboard.style.height = whiteboard.offsetHeight + 'px';
}

// WebSocket event handlers
function setupSocketEvents() {
    socket.on('connect', () => {
        console.log('Connected to WebSocket server');
        socket.emit('join_session', { isTeacher: isTeacher });
    });
    
    socket.on('student_count_update', (data) => {
        studentCount.value = data.count;
    });
    
    socket.on('drawing_data', (data) => {
        if (!sessionActive) return;
        
        if (data.action === 'start') {
            startRemotePath(data);
        } else if (data.action === 'draw') {
            continueRemotePath(data);
        } else if (data.action === 'end') {
            endRemotePath(data);
        }
    });
    
    socket.on('clear_whiteboard', () => {
        clearWhiteboard();
    });
    
    socket.on('session_ended', () => {
        sessionActive = false;
        alert('The session has been ended by the teacher.');
        window.location.href = '/session_ended';
    });
}

// Drawing functions
function startRemotePath(data) {
    const path = document.createElement('div');
    path.className = 'drawing-path';
    path.id = `path-${data.pathId}`;
    path.style.backgroundColor = data.color || '#000000';
    whiteboard.appendChild(path);
    currentPaths[data.pathId] = path;
    addDotToPath(data.pathId, data.x, data.y);
}

function continueRemotePath(data) {
    addDotToPath(data.pathId, data.x, data.y);
}

function endRemotePath(data) {
    // No special handling needed for path end
}

function addDotToPath(pathId, x, y) {
    const path = currentPaths[pathId];
    if (path) {
        const dot = document.createElement('div');
        dot.className = 'drawing-dot';
        dot.style.left = x + 'px';
        dot.style.top = y + 'px';
        dot.style.backgroundColor = path.style.backgroundColor;
        path.appendChild(dot);
    }
}

function clearWhiteboard() {
    whiteboard.innerHTML = '';
    currentPaths = {};
}

// Local drawing event handlers
function setupDrawingEvents() {
    whiteboard.addEventListener('mousedown', startDrawing);
    whiteboard.addEventListener('mousemove', draw);
    whiteboard.addEventListener('mouseup', stopDrawing);
    whiteboard.addEventListener('mouseout', stopDrawing);
}

function startDrawing(e) {
    if (!isTeacher || !sessionActive) return;
    
    isDrawing = true;
    currentPathId = Date.now().toString();
    
    const rect = whiteboard.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    socket.emit('drawing_data', {
        action: 'start',
        pathId: currentPathId,
        x: x,
        y: y,
        color: '#000000' // Default black
    });
    
    startRemotePath({
        pathId: currentPathId,
        x: x,
        y: y
    });
}

function draw(e) {
    if (!isDrawing || !isTeacher || !sessionActive) return;
    
    const rect = whiteboard.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    socket.emit('drawing_data', {
        action: 'draw',
        pathId: currentPathId,
        x: x,
        y: y
    });
    
    continueRemotePath({
        pathId: currentPathId,
        x: x,
        y: y
    });
}

function stopDrawing() {
    if (!isDrawing || !isTeacher || !sessionActive) return;
    
    isDrawing = false;
    socket.emit('drawing_data', {
        action: 'end',
        pathId: currentPathId
    });
    
    endRemotePath({
        pathId: currentPathId
    });
}

// End button functionality
function setupEndButton() {
    endButton.addEventListener('click', function() {
        if (confirm('Are you sure you want to end the session for all participants?')) {
            socket.emit('end_session');
            sessionActive = false;
            window.location.href = '/session_ended';
        }
    });
}

// Initialize the application
function init() {
    initWhiteboard();
    setupSocketEvents();
    setupDrawingEvents();
    setupEndButton();
    
    // Handle window resize
    window.addEventListener('resize', initWhiteboard);
}

// Start the application when DOM is loaded
document.addEventListener('DOMContentLoaded', init);