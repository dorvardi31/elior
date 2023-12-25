<!-- StatisticalData.vue -->
<template>
    <div>
      <!-- Display statistical data here -->
      <div v-for="(value, key) in data" :key="key">
        <strong>{{ key }}:</strong> {{ value }}
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      data: Object,
    },
  };
  </script>
  
  <style>
 div {
  background-color: #f7f7f7;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

strong {
  color: #333;
}

  </style>
  