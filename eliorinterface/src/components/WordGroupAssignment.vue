<template>
    <div class="word-group-assignment">
      <div class="word-list">
        <div v-for="word in words" :key="word" 
             :class="['word-item', { 'selected': selectedWords.includes(word) }]" 
             @click="toggleWordSelection(word)">
          {{ word }}
        </div>
      </div>
      <div class="group-name-input">
        <input type="text" v-model="groupName" placeholder="Enter Group Name" class="group-input">
        <button @click="assignGroup" class="group-button">Assign Group</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        words: [],           // List of words fetched from the API
        selectedWords: [],   // Words selected by the user
        groupName: ''        // Group name entered by the user
      };
    },
    mounted() {
      this.fetchWords();    // Fetch the list of words when the component is mounted
    },
    methods: {
      fetchWords() {
        // Fetch words from the API
        axios.get('http://127.0.0.1:5001/api/words')
          .then(response => {
            this.words = response.data;
          })
          .catch(error => {
            console.error('Error fetching words:', error);
            // Handle the error appropriately
          });
      },
      toggleWordSelection(word) {
        if (this.selectedWords.includes(word)) {
            this.selectedWords = this.selectedWords.filter(w => w !== word);
        } else {
            this.selectedWords.push(word);
        }
        },
      assignGroup() {
        // Check if at least one word is selected and a group name is entered
        if (this.selectedWords.length === 0 || this.groupName.trim() === '') {
          alert('Please select at least one word and enter a group name.');
          return;
        }
  
        const payload = {
          words: this.selectedWords,
          new_group: this.groupName
        };
  
        // Make a POST request to assign the group to the selected words
        axios.post('http://127.0.0.1:5001/api/assign_group', payload)
          .then(response => {
            // Display success message from the server or a default message
            alert(response.data.message || 'Group assigned successfully');
            this.selectedWords = [];  // Clear the selected words
            this.groupName = '';      // Clear the group name input
          })
          .catch(error => {
            // Display error message
            console.error('Error assigning group:', error);
            alert('Error assigning group: ' + (error.response?.data?.error || 'Unknown error'));
          });
      }
    }
  };
  </script>
  
  <style>
  .word-group-assignment {
    max-width: 600px; /* Adjust as needed */
    margin: auto;
    padding: 20px;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .word-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 20px;
  }
  
  .word-item {
    display: flex;
    align-items: center;
    background-color: #f7f7f7;
    border-radius: 20px;
    padding: 8px 15px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: background-color 0.2s, box-shadow 0.2s;
    cursor: pointer;
  }
  
  .word-item:hover {
    background-color: #e7e7e7;
    box-shadow: 0 3px 6px rgba(0,0,0,0.15);
  }
  
  .word-checkbox {
    margin-right: 8px;
    cursor: pointer;
  }
  
  .word-label {
    margin: 0;
    cursor: pointer;
    user-select: none; /* Prevent text selection */
  }
  
  .group-name-input {
    display: flex;
    gap: 10px;
  }
  
  .group-input {
    flex-grow: 1;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 16px;
  }
  
  .group-button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .group-button:hover {
    background-color: #0056b3;
  }
  .word-item {
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .word-item.selected {
    background-color: #007bff;
    color: white;
  }
  </style>