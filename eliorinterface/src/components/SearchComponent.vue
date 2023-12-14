<template>
    <div class="word-list-container">
      <h1>Word List</h1>
      <ul>
        <li v-for="word in words" :key="word">{{ word }}</li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        words: [], // This should be populated with words from the backend
      };
    },
    mounted() {
      // Implement logic to fetch words from the backend
    },
  };
  </script>
  
  <style>

  </style>
  