<template>
  <div class="file-upload-wrapper">
    <input type="file" ref="fileInput" @change="handleFileUpload" />
    <button @click="uploadFile">Upload File</button>
    <div v-if="uploadStatus" class="upload-status">{{ uploadStatus }}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFile: null,
      uploadStatus: '', // Add upload status message
    };
  },
  methods: {
    handleFileUpload() {
      this.selectedFile = this.$refs.fileInput.files[0];
      this.uploadStatus = ''; // Reset upload status message
    },
    uploadFile() {
      if (!this.selectedFile) {
        this.uploadStatus = 'Please select a file.';
        return;
      }

      const formData = new FormData();
      formData.append('file', this.selectedFile);

      axios.post('http://localhost:5001/api/upload', formData, { 
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      .then(response => {
        this.uploadStatus = 'File uploaded successfully.';
        console.log('File uploaded successfully', response);
      })
      .catch(error => {
        this.uploadStatus = 'Error uploading file. Please try again.';
        console.error('Error uploading file', error);
      });
    },
  },
};
</script>


<style>
  /* File Upload Component Styles */
  .file-upload-wrapper {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 20px;
      margin: 20px auto;
      border-radius: 12px;
      background: linear-gradient(145deg, #e6e6e6, #ffffff);
      box-shadow: 8px 8px 16px #d6d6d6, -8px -8px 16px #ffffff;
      max-width: 400px; /* Adjust to fit your design */
  }

  .file-upload-wrapper input[type="file"] {
      padding: 10px;
      margin-bottom: 20px;
      border: 2px solid #ddd;
      border-radius: 8px;
      box-shadow: inset 4px 4px 8px #d1d1d1, inset -4px -4px 8px #ffffff;
      transition: border-color 0.3s;
  }

  .file-upload-wrapper input[type="file"]:hover,
  .file-upload-wrapper input[type="file"]:focus {
      border-color: #00BCD4; /* Highlight color */
  }

  .file-upload-wrapper button {
      padding: 10px 20px;
      border: none;
      border-radius: 8px;
      background-color: #00BCD4; /* Cyan color */
      color: white;
      cursor: pointer;
      font-weight: 600;
      transition: background-color 0.3s;
      box-shadow: 4px 4px 8px #c4c4c4;
  }

  .file-upload-wrapper button:hover {
      background-color: #00ACC1;
      box-shadow: 2px 2px 4px #c4c4c4;
  }
  .upload-status {
    margin-top: 20px;
    color: #28a745; 
    font-weight: bold;
  }
</style>