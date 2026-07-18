document.addEventListener('DOMContentLoaded', function() {
  // Toggle password visibility
  document.querySelectorAll('[data-password-toggle]').forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      var targetSelector = btn.getAttribute('data-password-toggle');
      var input = document.querySelector(targetSelector);
      if (!input) return;
      if (input.type === 'password') {
        input.type = 'text';
        btn.innerHTML = '<i class="bi bi-eye-slash"></i>';
      } else {
        input.type = 'password';
        btn.innerHTML = '<i class="bi bi-eye"></i>';
      }
    });
  });
});
