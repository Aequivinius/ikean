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
    const mainImage = document.getElementById(id).querySelector('img');
    const temp = mainImage.src;
    mainImage.src = thumbnail.src;
    thumbnail.src = temp;
}
