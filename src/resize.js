function handleResizeAndReload() {
    var windowWidth = window.innerWidth;

    if (windowWidth > 768) {
        var detailsElements = document.querySelectorAll('details');
        detailsElements.forEach(function (detailsElement) {
            detailsElement.setAttribute('open', 'open');
        });
    } else {
        var detailsElements = document.querySelectorAll('details');

        detailsElements.forEach(function (detailsElement) {
            detailsElement.removeAttribute('open');
        });
    }
}

window.addEventListener('resize', handleResizeAndReload);
window.addEventListener('load', handleResizeAndReload);
