<template>
  <div class="dashboard-view">
    <h1>Welcome to the Dashboard</h1>
    <FileUpload @file-uploaded="fetchData" />
    <SearchBar @search="performSearch" />

    <div v-if="isLoading">
      <p>Loading data...</p>
    </div>
    <div v-else>
      <ul class="data-list">
        <li v-for="item in filteredData" :key="item.id" @click="selectItem(item)">
          {{ item.name }}
        </li>
      </ul>
    </div>

    <ItemModal v-if="selectedItem" :item="selectedItem" @close-modal="selectedItem = null" />
  </div>
</template>

<script>
import FileUpload from './FileUpload.vue';
import SearchBar from './SearchBar.vue';
import { queryView } from './apiService'; // Replace with your actual API call function


export default {
  name: 'DashboardView',
  components: {
    FileUpload,
    SearchBar
    
  },
  data() {
    return {
      allData: [],
      filteredData: [],
      isLoading: false,
      selectedItem: null,
    };
  },
  methods: {
    async fetchData() {
  this.isLoading = true;
  try {
    const data = await queryView();
    this.allData = data;
    this.filteredData = data;
  } catch (error) {
    console.error('Failed to fetch data:', error);
    // Optionally, set an error state and display an error message in your template
  } finally {
    this.isLoading = false;
  }
},
    selectItem(item) {
      this.selectedItem = item;
    },
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<style scoped>
.dashboard-view {
  max-width: 1200px;
  margin: auto;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  text-align: center;
}

h1 {
  color: #333;
  font-size: 2em;
  margin-bottom: 20px;
}

.data-list {
  list-style: none;
  padding: 0;
  text-align: left;
  max-width: 600px;
  margin: 20px auto;
}

.data-list li {
  cursor: pointer;
  background-color: #f9f9f9;
  margin: 10px 0;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.data-list li:hover {
  background-color: #eef2f7;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.loading-state {
  color: #666;
  font-size: 1.2rem;
}

/* Style for other components like SearchBar, FileUpload, ItemModal if needed */
</style>

