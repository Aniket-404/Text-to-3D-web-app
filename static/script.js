const inputTxt = document.getElementById("input");
const loadingImg = document.getElementById("loading");
const imageContainer = document.getElementById("image-container");
const image = document.getElementById("image");
const depthButton = document.getElementById("depth-button");
const pointCloudLink = document.getElementById("point-cloud-link");
const imageDownload = document.getElementById("image-download");
const button = document.getElementById("btn");

button.addEventListener('click', async function () {
    // Show loading image
    loadingImg.style.display = 'block';
    imageContainer.style.display = 'none'; // Hide image and buttons

    const response = await fetch('/generate_depth', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input: inputTxt.value })
    });

    const result = await response.json();
    image.onload = function () {
        // Hide loading image and show image and buttons
        loadingImg.style.display = 'none';
        imageContainer.style.display = 'block';
    };

    // Clear the previous image src
    image.src = '';

    // Load the new image with cache busting
    const timestamp = new Date().getTime();
    image.src = `static/${result.image}?t=${timestamp}`;

    depthButton.onclick = function () {
        window.open(`static/${result.depth}`, '_blank');
    };
    pointCloudLink.href = `static/${result.point_cloud}`;
    imageDownload.href = `static/${result.image}`;
});
