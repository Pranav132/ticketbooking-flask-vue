import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AdminLoginView from '../views/AdminLoginView.vue'
import AdminDashboardView from '../views/AdminDashboardView.vue'
import AddTheatreView from '../views/AddTheatreView.vue'

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
    component: LoginView,
    meta: {
      requiresVisitor: true,
    },
  },
  {
    path:'/admin-login',
    name: 'admin-login',
    component: AdminLoginView,
    meta: {
      requiresVisitor: true,
    },
  },
  {
    path:'/register',
    name: 'register',
    component: RegisterView,
    meta: {
      requiresVisitor: true,
    },
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminDashboardView,
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    },
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: <div>Dashboard</div>,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/add-theatre',
    name: 'add-theatre',
    component: AddTheatreView,
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    },
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem('jwt');  // change this according to how you are storing user login information
  const adminLocalStorage = localStorage.getItem('isAdmin');
  const isAdmin =  adminLocalStorage &&
  adminLocalStorage ===
    "a4f2b74b8fc1042a8082699c749ef0f19ca201c6f3f147dfa5226f0928e8c6b1";
  
  if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
    next('/login');
    return;
  }

  if (to.matched.some(record => record.meta.requiresVisitor) && loggedIn) {
    next('/'); // redirect to home if logged in
    return;
  }

  if (to.matched.some(record => record.meta.requiresAdmin) && !isAdmin) {
    next('/'); // only admins can access protected routes
    return;
  }
  
  next();
});


export default router
