<template>
  <div class="dashboard-view">
    <h1>Welcome to the Dashboard</h1>
    <p>{{ message }}</p>
    <button @click="updateMessage">Update Message</button>
    <button @click="fetchData">Fetch Data</button>
  </div>
</template>

<script>
export default {
  name: 'DashboardView',
  data() {
    return {
      message: 'This is your dashboard content.',
      fetchedData: '',
    };
  },
  methods: {
    updateMessage() {
      this.message = 'Message updated!';
    },
    fetchData() {
      // Simulate fetching data from an API
      setTimeout(() => {
        this.fetchedData = 'Fetched data from API.';
      }, 1000);
    },
  },
  computed: {
    // You can add computed properties here
  },
  mounted() {
    // Add any initialization logic here
    this.fetchData(); // Fetch data when the component is mounted
  },
};
</script>

<style scoped>
.dashboard-view {
  text-align: center;
  margin: 20px;
}

button {
  margin: 10px;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
}
</style>
