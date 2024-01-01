<template>
  <div id="app">
    <nav>
      <router-link to="/">DataTableView</router-link>
      <router-link to="/word-group-assignment">WordGroupAssignment</router-link>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
nav {
  background-color: #4293c9; /* Dark background */
  padding: 1rem; /* Padding around the nav */
  text-align: center; /* Center the links */
}

nav a {
  color: white; /* Light text color for contrast */
  margin: 0 1rem; /* Spacing between links */
  text-decoration: none; /* Remove underline from links */
  font-size: 1.2rem; /* Slightly larger font size */
  transition: color 0.3s; /* Smooth transition for hover effect */
}

nav a:hover {
  color: #20118e; /* Change color when hovering */
}

nav a.router-link-active {
  color: #d2ff8e; /* Green color for the active link */
  font-weight: bold; /* Make the active link bold */
}

</style>