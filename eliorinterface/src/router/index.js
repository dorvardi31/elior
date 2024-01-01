import { createRouter, createWebHashHistory } from 'vue-router';
import DataTableView from '@/components/DataTableView.vue';
import WordGroupAssignment from '@/components/WordGroupAssignment.vue';

const routes = [
  { path: '/', component: DataTableView },
  { path: '/word-group-assignment', component: WordGroupAssignment },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
