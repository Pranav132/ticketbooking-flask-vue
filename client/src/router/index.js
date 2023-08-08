import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path:'/login',
    name: 'login',
    component: <div>Login</div>,
    meta: {
      requiresVisitor: true,
    },
  },
  {
    path:'/admin-login',
    name: 'admin-login',
    component: <div>Admin Login</div>,
    meta: {
      requiresVisitor: true,
    },
  },
  {
    path: '/protected',
    name: 'Protected',
    component: <div>Protected View</div>,
    meta: {
      requiresAuth: true,
    },
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem('jwt');  // change this according to how you are storing user login information
  
  if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
    next('/login');
    return;
  }

  if (to.matched.some(record => record.meta.requiresVisitor) && loggedIn) {
    next('/'); // redirect to home if logged in
    return;
  }
  
  next();
});


export default router
