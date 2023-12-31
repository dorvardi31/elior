<!-- ContextModal.vue -->
<template>
    <div class="modal">
      <h3>Context for {{ word.text }}</h3>
      <p>{{ word.context }}</p>
      <button @click="$emit('close-modal')">Close</button>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      word: Object,
    },
  };
  </script>
  
  <style>
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  z-index: 1000;
}

h3 {
  margin-top: 0;
}

button {
  background-color: #dc3545;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 20px;
}

button:hover {
  background-color: #c82333;
}

  </style>
  