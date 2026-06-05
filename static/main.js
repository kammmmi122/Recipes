// -------------------------------
// Konfiguracja kolorów kategorii
// -------------------------------
const CATEGORY_COLORS = {
  "Dania glowne": "#ff6b6b",
  "Makaron": "#ffa94d",
  "Zupy": "#4dabf7",
  "Sałatki": "#69db7c",
  "Desery": "#f06595",
  "Śniadania": "#ffd43b",
  "Przekąski": "#845ef7"
};

// -------------------------------
// Wczytywanie listy przepisów
// -------------------------------
// Każdy plik .adoc w folderze Przepisy powinien mieć:
// :title: Nazwa przepisu
// :category: Dania glowne
// :thumbnail: static/images/xxx.jpg

async function loadRecipeList() {
  const response = await fetch("recipes.json");
  const recipes = await response.json();
  renderRecipes(recipes);
  setupSearch(recipes);
}

// -------------------------------
// Renderowanie kart przepisów
// -------------------------------
function renderRecipes(recipes) {
  const container = document.querySelector(".cards-grid");
  container.innerHTML = recipes.map(createCardHTML).join("");
}

function createCardHTML(recipe) {
  const color = CATEGORY_COLORS[recipe.category] || "#999";

  return `
    <article class="card">
      <div class="card-category-label" style="background:${color}">
        ${recipe.category}
      </div>

      <img src="${recipe.thumbnail}" alt="${recipe.title}" class="card-image">

      <div class="card-content">
        <h3 class="card-title">${recipe.title}</h3>
        <a class="card-link" href="${recipe.url}">Zobacz przepis ></a>
      </div>
    </article>
  `;
}

// -------------------------------
// Wyszukiwarka
// -------------------------------
function setupSearch(recipes) {
  const input = document.querySelector(".search-input");
  if (!input) return;

  input.addEventListener("input", () => {
    const q = input.value.toLowerCase();
    const filtered = recipes.filter(r =>
      r.title.toLowerCase().includes(q) ||
      r.category.toLowerCase().includes(q)
    );
    renderRecipes(filtered);
  });
}

// -------------------------------
// Start
// -------------------------------
loadRecipeList();
