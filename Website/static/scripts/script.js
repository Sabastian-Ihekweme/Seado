
//Auto dismiss flash messages
document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        let flashMessages = document.querySelectorAll(".flash-message");
        flashMessages.forEach(function (msg) {
            msg.style.opacity = "0";
            setTimeout(() => msg.remove(), 500);
        });
    }, 10000); // Auto dismiss after 5 seconds
});

function updateTime() {
    const timeElement = document.getElementById("live-time");
    const now = new Date();

    let hours = now.getHours();
    let minutes = now.getMinutes();
    let seconds = now.getSeconds();

    // Add leading zeroes if minutes or seconds are single digits
    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;

    // Format time in 12-hour format
    let ampm = hours >= 12 ? "PM" : "AM";
    hours = hours % 12;
    hours = hours ? hours : 12; // Adjust for 12 AM and 12 PM

    // Update the live time text
    timeElement.innerHTML = `${hours}:${minutes}:${seconds} ${ampm}`;
}

// Update the time every second
setInterval(updateTime, 1000);

// Call updateTime once to set the initial time
updateTime();

function scrollLeft() {
    document.getElementById("scrollable").scrollBy({ left: -100, behavior: "smooth" });
}

function scrollRight() {
    document.getElementById("scrollable").scrollBy({ left: 100, behavior: "smooth" });
}

