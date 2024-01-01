import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Adjust the import path if needed

const app = createApp(App);
app.use(router);
app.mount('#app');
