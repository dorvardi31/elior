<template>
    <div class="group-assignment-section">
      <input v-model="newGroupName" placeholder="Enter New Group Name" />
      <button @click="assignGroup">Assign Group</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'GroupAssignment',
    props: {
      selectedWords: Array
    },
    data() {
      return {
        newGroupName: ''
      };
    },
    methods: {
      assignGroup() {
        if (!this.newGroupName || this.selectedWords.length === 0) {
          alert('Please select words and enter a group name');
          return;
        }
        this.$emit('assign-group', { 
          words: this.selectedWords, 
          new_group: this.newGroupName 
        });
        this.newGroupName = '';
      }
    }
  };
  </script>
  
  <style>
  .group-assignment-section {
    margin: 20px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .group-assignment-section input {
    width: 70%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .group-assignment-section button {
    padding: 10px 15px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  </style>
  