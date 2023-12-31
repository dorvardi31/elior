<template>
    <div class="upload-container">
      <h1>Upload Document</h1>
      <input type="file" @change="handleFileUpload" accept=".txt" />
      <button @click="submitFile">Upload</button>
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
      handleFileUpload(event) {
        this.selectedFile = event.target.files[0];
      },
      submitFile() {
        // Implement file upload logic
      },
    },
  };
  </script>
  
  <style>

  </style>
  