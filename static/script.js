// Get the image element
const videoElement = document.getElementById('video-stream');

// Function to update the image source with the video stream
function updateVideoStream() {
    fetch('http://127.0.0.1:5000/video')  // Fetch the video stream from the /video endpoint
        .then(response => {
            // console.log(response)
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            let blb = response.blob();
            
            return blb;  // Convert the response to a Blob
        })
        .then(blob => {
            console.log(blob)
            const blobUrl = URL.createObjectURL(blob);  // Create a URL for the Blob
            videoElement.src = blobUrl;  // Set the image source to the Blob URL
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

// Call the updateVideoStream function to start streaming the video
updateVideoStream();
