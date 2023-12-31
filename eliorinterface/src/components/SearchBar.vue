<!-- SearchBar.vue -->
<template>
  <div>
    <input v-model="searchTerm" placeholder="Search..." />
    <button @click="emitSearch">Search</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchTerm: '',
    };
  },
  methods: {
    emitSearch() {
      this.$emit('search', this.searchTerm);
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
  background-color: #28a745;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #218838;
}

</style>
