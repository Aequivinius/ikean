document.addEventListener('DOMContentLoaded', () => {

const searchInput = document.getElementById('menu__search_input');
const figures = document.querySelectorAll('figure');

// Add an event listener for input changes
searchInput.addEventListener('input', () => {
    const searchTerm = searchInput.value.toLowerCase();
    console.log(searchTerm);

    // Loop through each figure and check if it matches the search term
    figures.forEach(figure => {
        const keywords = figure.getAttribute("keywords").split(" ");
        const match = keywords.some(keyword => keyword.startsWith(searchTerm));
        figure.style.display = match ? "" : "none";
    });
});
});
