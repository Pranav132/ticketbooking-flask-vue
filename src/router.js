import { createRouter, createWebHistory } from 'vue-router';
import Login from "./screens/Login.vue"
import Vue from 'vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  // other routes here
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
