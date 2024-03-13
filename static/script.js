function fetchFrames() {
    const videoContainer = document.getElementById('video-container');

    fetch('http://127.0.0.1:5000/video')
        .then(response => {
            const reader = response.body.getReader();

            const readStream = () => {
                reader.read()
                    .then(({ done, value }) => {
                        if (done) {
                            console.log('Stream complete');
                            return;
                        }

                        const img = document.createElement('img');
                        img.src = URL.createObjectURL(new Blob([value], { type: 'image/jpeg' }));

                        videoContainer.appendChild(img);
                        
                        // readStream(); // Continue reading next frame
                    })
                    .catch(error => {
                        console.error('Error reading frame:', error);
                    });
            };

            readStream(); // Start reading frames
        })
        .catch(error => {
            console.error('Error fetching frames:', error);
        });
}

fetchFrames();