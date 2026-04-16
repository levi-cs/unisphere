document.addEventListener('DOMContentLoaded', function () {

  /* ─── TIME GREETING ─── */
  var greetEl = document.getElementById('greeting-text');
  if (greetEl) {
    var h = new Date().getHours();
    greetEl.textContent = h < 12 ? 'Good Morning,' : h < 17 ? 'Good Afternoon,' : 'Good Evening,';
  }

  /* ─── CLICK OUTSIDE SIDEBAR ─── */
  document.addEventListener('click', function (e) {
    var sb = document.getElementById('sidebar');
    var overlay = document.getElementById('sidebar-overlay');
    if (!sb) return;
    var btn = document.querySelector('.hamburger');
    if (!sb.contains(e.target) && btn && !btn.contains(e.target)) {
      sb.classList.remove('open');
      if (overlay) overlay.classList.remove('visible');
    }
  });

  /* ─── OTP AUTO-FOCUS ─── */
  var otpInputs = document.querySelectorAll('.otp-input');
  otpInputs.forEach(function (inp, i) {
    inp.addEventListener('input', function () {
      this.value = this.value.replace(/\D/g, '');
      if (this.value && i < otpInputs.length - 1) otpInputs[i + 1].focus();
    });
    inp.addEventListener('keydown', function (e) {
      if (e.key === 'Backspace' && !this.value && i > 0) otpInputs[i - 1].focus();
    });
  });

  /* ─── PROGRESS BAR ANIMATION ─── */
  setTimeout(function () {
    document.querySelectorAll('.progress-fill').forEach(function (el) {
      var target = el.style.width;
      el.style.width = '0%';
      setTimeout(function () { el.style.width = target; }, 80);
    });
  }, 200);

  /* ─── AUTO-DISMISS ALERTS ─── */
  setTimeout(function () {
    document.querySelectorAll('.alert').forEach(function (el) {
      el.style.transition = 'opacity 0.5s ease';
      el.style.opacity = '0';
      setTimeout(function () { el.style.display = 'none'; }, 500);
    });
  }, 5000);

});

/* ─── SIDEBAR TOGGLE ─── */
function toggleSidebar() {
  var sb = document.getElementById('sidebar');
  var overlay = document.getElementById('sidebar-overlay');
  if (!sb) return;
  sb.classList.toggle('open');
  if (overlay) overlay.classList.toggle('visible');
}

function closeSidebar() {
  var sb = document.getElementById('sidebar');
  var overlay = document.getElementById('sidebar-overlay');
  if (sb) sb.classList.remove('open');
  if (overlay) overlay.classList.remove('visible');
}
