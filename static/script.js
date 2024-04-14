const inputTxt = document.getElementById("input");
const loadingImg = document.getElementById("loading");
const imageContainer = document.getElementById("image-container");
const image = document.getElementById("image");
const depthButton = document.getElementById("depth-button");
const objFileLink = document.getElementById("obj-file-link");
const imageDownload = document.getElementById("image-download");
const button = document.getElementById("btn");

let errorCount = 0;

button.addEventListener('click', async function () {
    // Show loading image
    loadingImg.style.display = 'block';
    imageContainer.style.display = 'none'; // Hide image and buttons

    try {
        const response = await fetch('/generate_depth', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ input: inputTxt.value })
        });

        if (!response.ok) {
            throw new Error('Internal Server Error');
        }

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
        objFileLink.href = `static/${result.obj_file}`;
        imageDownload.href = `static/${result.image}`;
    } catch (error) {
        // Increment error count
        errorCount++;

        if (errorCount < 3) {
            // Hide loading image
            loadingImg.style.display = 'none';
            // Display error message to the user
            alert('Internal Server Error. Please restart the server and try again.');
        } else {
            // Hide loading image
            loadingImg.style.display = 'none';
            // Display alternative error message to the user
            alert('Restarting the server seems not to be working. Please delete the generated_image.jpg file in the static folder and try again.');
        }
    }
});

// Add event listener for clicking on the download link for the .obj file
objFileLink.addEventListener('click', function() {
    
});
