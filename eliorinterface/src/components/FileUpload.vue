<template>
  <div>
    <input type="file" ref="fileInput" @change="handleFileUpload" />
    <button @click="uploadFile">Upload File</button>
  </div>
</template>

<script>
import axios from 'axios'; // Import Axios
export default {
  methods: {
    handleFileUpload() {
      // Retrieve the selected file from the input element
      this.selectedFile = this.$refs.fileInput.files[0];
    },
    uploadFile() {
      if (!this.selectedFile) {
        alert('Please select a file.');
        return;
      }


      const formData = new FormData();
      formData.append('file', this.selectedFile);
     

      axios.post('http://localhost:5001/api/upload', formData, {headers: { 'Content-Type': 'multipart/form-data' }})
        .then(response => {

          console.log('File uploaded successfully', response);
        })
        .catch(error => {
          // Handle errors
          console.error('Error uploading file', error);
        });
    },
  },
  data() {
    return {
      selectedFile: null,
    };
  },
};
</script>
