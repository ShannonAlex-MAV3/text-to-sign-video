const videoElement = document.getElementById("stream");

// Function to update the image source with the video stream
function updateVideoStream() {
  fetch("http://127.0.0.1:5000/video")
    .then((response) => {
      // console.log(response)
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      return response.blob(); // Convert the response to a Blob
    })
    .then((blob) => {
      // const blobUrl = URL.createObjectURL(blob);  // Create a URL for the Blob

      // videoElement.src = blobUrl;  // Set the image source to the Blob URL
    //   processData(blob);
      console.log(blob);
      extractMultipartDataV2(blob)
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
}

updateVideoStream();

// let img = document.getElementById('stream');

// img.onerror = function() {
//     img.src = '';
//     setTimeout(() => img.src = 'http://127.0.0.1:5000/video', 1000);
// };




