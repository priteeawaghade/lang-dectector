// Handle image input change and display the selected image
document.getElementById('imageInput').addEventListener('change', function() {
    const file = this.files[0];
    const imagePreview = document.getElementById('imagePreview');

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block'; // Show the image preview
        };
        reader.readAsDataURL(file);
    } else {
        imagePreview.src = '';
        imagePreview.style.display = 'none'; // Hide the image preview if no file selected
    }
});

// Extract text from the image using Tesseract.js with multi-language support
document.getElementById('extractText').addEventListener('click', function () {
    const imageInput = document.getElementById('imageInput');
    const loadingSpinner = document.getElementById('loadingSpinner');

    if (imageInput.files.length === 0) {
        alert('Please select an image file first.');
        return;
    }

    const file = imageInput.files[0];

    // Show the loading spinner
    loadingSpinner.style.display = 'block';

    Tesseract.recognize(
        file,
        'eng+spa+mar+fra', // Support for English, Spanish, Marathi, and French
        {
            logger: info => console.log(info) // Log progress
        }
    ).then(({ data: { text } }) => {
        // Hide the loading spinner once text extraction is complete
        loadingSpinner.style.display = 'none';
        
        document.getElementById('extractedText').textContent = text;

        // Enable the "Detect Language" button after text extraction
        document.getElementById('detectLanguage').disabled = false;
    }).catch(error => {
        console.error(error);
        
        // Hide the spinner in case of an error
        loadingSpinner.style.display = 'none';
    });
});

// Detect language of the extracted text
document.getElementById('detectLanguage').addEventListener('click', function () {
    const extractedText = document.getElementById('extractedText').textContent;

    if (!extractedText) {
        alert('No text available for language detection.');
        return;
    }

    // Send extracted text to the server for language detection
    fetch('http://localhost:5000/detect_language', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: extractedText })
    })
    .then(response => response.json())
    .then(data => {
        if (data.language) {
            document.getElementById('detectedLanguage').textContent = `Detected language: ${data.language}`;
        } else {
            document.getElementById('detectedLanguage').textContent = 'Language detection failed.';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('detectedLanguage').textContent = 'Error detecting language.';
    });
});
