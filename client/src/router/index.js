import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AdminLoginView from '../views/AdminLoginView.vue'
import AdminDashboardView from '../views/AdminDashboardView.vue'
import AddTheatreView from '../views/AddTheatreView.vue'
import TheatreView from '../views/TheatreView.vue'
import EditTheatreView from '../views/EditTheatreView.vue'
import AddShowView from '../views/AddShowView.vue'
import EditShowView from '../views/EditShowView.vue'
import UserDashboardView from '../views/UserDashboardView.vue'
import UserTheatreView from '../views/UserTheatreView.vue'
import TheatreWithShowsView from '../views/TheatreWithShowsView.vue'
import BookShowView from '../views/BookShowView.vue'
import RateShowView from '../views/RateShowView.vue'
import ShowReviewsView from '../views/ShowReviewsView.vue'
import SummaryView from '../views/SummaryView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
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
    component: UserDashboardView,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/theatres',
    name: 'theatres',
    component: UserTheatreView,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/view-theatre/:id',
    name: 'view-theatre',
    component: TheatreWithShowsView,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/book/:id',
    name: 'book-show',
    component: BookShowView,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/rate_show/:id',
    name: 'rate-show',
    component: RateShowView,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/ratings/:id',
    name: 'ratings',
    component: ShowReviewsView,
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
  {
    path: '/theatre/:id',
    name: 'theatre-admin',
    component: TheatreView,
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    },
  },
  {
    path: '/edit-theatre/:id',
    name: 'edit-theatre-admin',
    component: EditTheatreView,
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    },
  },
  {
    path: '/add-show/:theatreId',
    name: 'add-show',
    component: AddShowView,
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    },
  },
  {
    path: '/edit-show/:id',
    name: 'edit-show',
    component: EditShowView,
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/summary',
    name: 'summary',
    component: SummaryView,
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem('jwt'); 
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
