
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