<!-- WordList.vue -->
<template>
    <ul>
      <li v-for="word in words" :key="word.id" @click="$emit('show-context', word)">
        {{ word.text }}
      </li>
    </ul>
  </template>
  
  <script>
  export default {
    props: {
      words: Array,
    },
  };
  </script>
  
  <style>
  ul {
  list-style-type: none;
  padding: 0;
}

li {
  background-color: #f8f9fa;
  margin-bottom: 5px;
  padding: 10px;
  border: 1px solid #ddd;
  cursor: pointer;
}

li:hover {
  background-color: #e9ecef;
}

  </style>
  