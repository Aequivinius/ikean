function handleResizeAndReload() {
    const windowWidth = window.innerWidth;
    const detailsElements = document.querySelectorAll('details');

    detailsElements.forEach(detailsElement => {
        if (windowWidth > 768) {
            detailsElement.setAttribute('open', 'open');
        } else {
            detailsElement.removeAttribute('open');
        }
    });
}

window.addEventListener('resize', handleResizeAndReload);
window.addEventListener('load', handleResizeAndReload);

function changeMainImage(id, thumbnail) {
    const main = document.getElementById(id).querySelector('.gallery__main');
    const modelViewer = main.querySelector('.gallery__main-model');
    const mainImage = main.querySelector('.gallery__main-img');
    const isPoster = thumbnail.classList.contains('gallery__poster');

    if (isPoster) {
        modelViewer.style.display = 'block';
        mainImage.style.display = 'none';

        thumbnail.src = mainImage.src;
        console.log(thumbnail.classList);
        thumbnail.classList.remove('gallery__poster');
        console.log(thumbnail.classList);

    } else {
        /* leaving model viewer */
        if (modelViewer && modelViewer.style.display !== 'none') {
            modelViewer.style.display = 'none';
            mainImage.style.display = 'block';
            thumbnail.classList.add('gallery__poster');
        }
        const temp = mainImage.src;
        mainImage.src = thumbnail.src;
        thumbnail.src = temp;
    }
}

window.addEventListener('hashchange', () => {
    const menuLanguages = document.querySelectorAll('.menu__language');
    menuLanguages.forEach(menuLanguage => {
        menuLanguage.href = `${menuLanguage.href}${window.location.hash}`;
    });
});

window.addEventListener('load', () => {
    const menuLanguages = document.querySelectorAll('.menu__language');
    menuLanguages.forEach(menuLanguage => {
        menuLanguage.href = `${menuLanguage.href}${window.location.hash}`;
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const menuCategories = document.querySelector('#menu__categories');
    const figures = document.querySelectorAll('figure');


    menuCategories.addEventListener('change', (event) => {
        const selectedCategory = event.target.value;

        /* we're working with .hidden as not to interfere with the search */
        figures.forEach(figure => {
            if (figure.getAttribute('category') === selectedCategory || selectedCategory === 'all') {
                figure.classList.remove('hidden');
            } else {
                figure.classList.add('hidden');
            }
        });
    });
});
