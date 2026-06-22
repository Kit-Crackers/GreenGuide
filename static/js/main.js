const track = document.getElementById("factsTrack");
let scroll = 0;

setInterval(() => {
  scroll += 1;
  track.scrollLeft = scroll;

  if (scroll >= track.scrollWidth - track.clientWidth) {
    scroll = 0;
  }
}, 30);

function scrollToWhy() {
  document.getElementById("why-section").scrollIntoView({
    behavior: "smooth"
  });
}


/* ================= AUTH MODAL SCRIPT ================= */

function openLogin() {
  document.getElementById("loginModal").style.display = "block";
  document.getElementById("overlay").style.display = "block";
}

function openRegister() {
  document.getElementById("registerModal").style.display = "block";
  document.getElementById("overlay").style.display = "block";
}

function closeModal() {
  document.getElementById("loginModal").style.display = "none";
  document.getElementById("registerModal").style.display = "none";
  document.getElementById("overlay").style.display = "none";
}

function switchToRegister() {
  document.getElementById("loginModal").style.display = "none";
  document.getElementById("registerModal").style.display = "block";
}

function switchToLogin() {
  document.getElementById("registerModal").style.display = "none";
  document.getElementById("loginModal").style.display = "block";
}