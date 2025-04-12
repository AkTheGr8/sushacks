document.querySelectorAll(".btn-secondary").forEach(button => {
    button.addEventListener("click", () => {
      const productName = button.parentElement.querySelector("h3").textContent;
      alert(`${productName} added to cart!`);
    });
  });
  document.getElementById("toggle-theme").addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
  });
  document.querySelector(".search-btn").addEventListener("click", () => {
    const term = document.getElementById("searchInput").value.trim();
    if (term) {
      alert(`Searching for "${term}"...`);
    }
  });