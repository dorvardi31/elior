<!-- WordGroups.vue -->
<template>
    <div>
      <input v-model="newGroup" placeholder="New group name" />
      <button @click="addGroup">Add Group</button>
      <div v-for="group in groups" :key="group.name">
        {{ group.name }} ({{ group.words.length }} words)
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      groups: Array,
    },
    data() {
      return {
        newGroup: '',
      };
    },
    methods: {
      addGroup() {
        // Add group logic
        this.$emit('update-groups');
      },
    },
  };
  </script>
  
  <style>
  div {
  margin-bottom: 20px;
}

input {
  padding: 10px;
  width: calc(100% - 22px);
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-right: 10px;
}

button {
  background-color: #17a2b8;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #138496;
}

  </style>
  