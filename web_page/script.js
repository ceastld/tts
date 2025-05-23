document.addEventListener('DOMContentLoaded', () => {
    const fileListElement = document.getElementById('file-list');
    const downloadAllButton = document.getElementById('download-all-btn'); // Get the download button
    let currentlyPlayingAudio = null;

    // Function to stop currently playing audio
    function stopCurrentAudio() {
        if (currentlyPlayingAudio) {
            currentlyPlayingAudio.pause();
            currentlyPlayingAudio.currentTime = 0; // Optional: Reset audio to start
            currentlyPlayingAudio = null;
        }
    }

    // Function to fetch and display file content
    async function fetchAndDisplayFile(container, filePath, type) {
        try {
            if (type === 'text') {
                // Fetch text content and display it in a <p> element
                const response = await fetch(filePath);
                if (!response.ok) {
                    console.error(`Error fetching ${filePath}: ${response.statusText}`);
                    const errorElement = document.createElement('p');
                    errorElement.textContent = `无法加载 ${filePath.split('/').pop()} (${response.statusText})`;
                    errorElement.style.color = 'red';
                    container.appendChild(errorElement);
                    return;
                }
                const text = await response.text();
                const textElement = document.createElement('p');
                // The class '.file-item p' from style.css should apply to this <p>
                // If you want specific class for these text paragraphs, you can add it here e.g.:
                // textElement.classList.add('audio-text-content'); 
                textElement.textContent = text;
                container.appendChild(textElement);

            } else if (type === 'audio') {
                const audioElement = document.createElement('audio');
                audioElement.controls = true;
                audioElement.src = filePath; // This should work for relative paths under file:///

                // Add event listener to handle playback
                audioElement.addEventListener('play', () => {
                    if (currentlyPlayingAudio && currentlyPlayingAudio !== audioElement) {
                        stopCurrentAudio();
                    }
                    currentlyPlayingAudio = audioElement;
                });
                container.appendChild(audioElement);
            }
        } catch (error) {
            console.error(`Error processing file ${filePath}:`, error);
            const errorElement = document.createElement('p');
            errorElement.textContent = `加载 ${filePath.split('/').pop()} 时出错: ${error.message}`;
            errorElement.style.color = 'red';
            container.appendChild(errorElement);
        }
    }

    // This is a placeholder. In a real scenario, you'd get this list from a server or a static list.
    // For this example, we'll hardcode the file names based on the provided list.
    const files = [
        '001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011', '012'
    ];

    if (files.length === 0) {
        fileListElement.innerHTML = '<p>在 audio 文件夹中没有找到文件。</p>';
        downloadAllButton.style.display = 'none'; // Hide button if no files
        return;
    }

    files.forEach(baseName => {
        const fileItemElement = document.createElement('div');
        fileItemElement.classList.add('file-item');

        const titleElement = document.createElement('h2');
        titleElement.textContent = `文件: ${baseName}`;
        fileItemElement.appendChild(titleElement);

        // Display text content
        fetchAndDisplayFile(fileItemElement, `./audio/${baseName}.txt`, 'text');

        // Display audio player
        fetchAndDisplayFile(fileItemElement, `./audio/${baseName}.wav`, 'audio');

        fileListElement.appendChild(fileItemElement);
    });

    // Event listener for the download all button
    downloadAllButton.addEventListener('click', async () => {
        if (typeof JSZip === 'undefined') {
            alert('JSZip library not loaded. Cannot create ZIP file.');
            return;
        }

        const zip = new JSZip();
        const audioFolder = zip.folder("audio"); // Create a folder named 'audio' in the ZIP
        let filesProcessed = 0;
        const totalFilesToProcess = files.length * 2; // Each baseName has a .txt and a .wav

        downloadAllButton.textContent = '正在打包... (0%)';
        downloadAllButton.disabled = true;

        for (const baseName of files) {
            const txtFilePath = `./audio/${baseName}.txt`;
            const wavFilePath = `./audio/${baseName}.wav`;

            try {
                // Fetch and add .txt file
                const txtResponse = await fetch(txtFilePath);
                if (txtResponse.ok) {
                    const txtBlob = await txtResponse.blob();
                    audioFolder.file(`${baseName}.txt`, txtBlob);
                } else {
                    console.warn(`Skipping ${txtFilePath} due to fetch error: ${txtResponse.statusText}`);
                }
            } catch (e) {
                console.warn(`Error fetching ${txtFilePath}:`, e);
            }
            filesProcessed++;
            downloadAllButton.textContent = `正在打包... (${Math.round((filesProcessed / totalFilesToProcess) * 100)}%)`;

            try {
                // Fetch and add .wav file
                const wavResponse = await fetch(wavFilePath);
                if (wavResponse.ok) {
                    const wavBlob = await wavResponse.blob();
                    audioFolder.file(`${baseName}.wav`, wavBlob);
                } else {
                    console.warn(`Skipping ${wavFilePath} due to fetch error: ${wavResponse.statusText}`);
                }
            } catch (e) {
                console.warn(`Error fetching ${wavFilePath}:`, e);
            }
            filesProcessed++;
            downloadAllButton.textContent = `正在打包... (${Math.round((filesProcessed / totalFilesToProcess) * 100)}%)`;
        }

        downloadAllButton.textContent = '生成 ZIP...';

        zip.generateAsync({ type: "blob" })
            .then(function(content) {
                // Trigger download
                const link = document.createElement('a');
                link.href = URL.createObjectURL(content);
                link.download = "audio_files.zip";
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(link.href); // Clean up
                downloadAllButton.textContent = '打包下载全部';
                downloadAllButton.disabled = false;
            })
            .catch(err => {
                console.error("Error generating ZIP file:", err);
                alert("创建 ZIP 文件失败: " + err.message);
                downloadAllButton.textContent = '打包下载全部';
                downloadAllButton.disabled = false;
            });
    });
}); 