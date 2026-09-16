document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("navToggle");
  const sidebar = document.getElementById("sidebar");

  if (!toggle || !sidebar) return;

  toggle.addEventListener("click", () => {
    const isOpen = sidebar.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(isOpen));
  });

  // Close the mobile nav after choosing a link
  sidebar.querySelectorAll(".nav-link").forEach((link) => {
    link.addEventListener("click", () => {
      sidebar.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    });
  });
});
