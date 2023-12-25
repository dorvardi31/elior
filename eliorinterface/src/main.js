import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import App from './App.vue'
import DashboardView from './components/DashboardView.vue' // Import the DashboardView component
import FileUpload from './components/FileUpload.vue'

const routes = [
  { path: '/', component: DashboardView }, // Use DashboardView here
  { path: '/upload', component: FileUpload },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

const app = createApp(App)
app.use(router)
app.mount('#app')
