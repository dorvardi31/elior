
<template>
  <div id="app">
    <router-view /> <!-- Dynamic rendering based on routes -->
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
/* Global styles go here */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f8f8f8;
}
#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}
</style>
