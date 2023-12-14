<template>
  <div class="file-upload">
    <input type="file" ref="fileInput" @change="selectFile" />
    <button @click="uploadFile">Upload File</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
    };
  },
  methods: {
    selectFile(event) {
      this.selectedFile = event.target.files[0];
    },
    uploadFile() {
      // Log before sending the request
      console.log('Sending POST request to /upload');

      if (!this.selectedFile) {
        console.error('No file selected.');
        return;
      }

      const formData = new FormData();
      formData.append('file', this.selectedFile);

      // Make an HTTP POST request to the backend endpoint
      fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          // Log after receiving the response
          console.log('Response from /upload:', data);

          // Handle the response data from the backend
          console.log('Handling response data:', data);
        })
        .catch((error) => {
          // Log if there is an error
          console.error('Error:', error);
        });
    },
  },
};
</script>
