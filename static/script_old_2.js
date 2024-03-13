let frames = []; // Array to store the frames
let frameIndex = 0; // Index of the current frame
// let imgElement = document.getElementById("stream"); // The img element to display the frames

fetch("http://127.0.0.1:5000/video")
  .then((response) => response.body)
  .then((rb) => {
    const reader = rb.getReader();

    return new ReadableStream({
      start(controller) {
        function push() {
          reader.read().then(({ done, value }) => {
            if (done) {
              controller.close();
              return;
            }

            // Create a Blob from the value and store it in the frames array
            let blob = new Blob([value], { type: "image/jpeg" });
            frames.push(blob);

            controller.enqueue(value);
            push();
          });
        }
        push();
      },
    });
  })
  .then(() => {
    console.log("frames", frames);
    let blobUrl = URL.createObjectURL(frames[1]);
    console.log(blobUrl);
    // setTimeout(playFrames, 1000); // Start playing after 1 second
  });

// fetch('http://127.0.0.1:5000/video').then(res => {
//     return res.body
// }).then(readableStream => {
//     const reader = readableStream.getReader()

// })

// // Function to play the frames
function playFrames() {
  //   debugger;
  if (frameIndex >= frames.length) {
    frameIndex = 0; // Loop back to the start
  }

  //   let blobUrl = URL.createObjectURL(frames[frameIndex]);
  //   imgElement.src = blobUrl;

  blobToDataURL(frames[frameIndex], function (dataUrl) {
    console.log(dataUrl); // This will log the data URL to the console
    imgElement.src = dataUrl;
  });
  frameIndex++;

  //   setTimeout(playFrames, 1000 / 30); // Play at 30 FPS
}

function blobToDataURL(blob, callback) {
  let reader = new FileReader();
  reader.onload = function (e) {
    callback(e.target.result);
  };
  reader.readAsDataURL(blob);
}
