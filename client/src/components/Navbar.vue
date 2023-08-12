<template>
  <nav class="navbar navbar-expand navbar-light bg-light">
    <div class="container-fluid">
      <div class="navbar-brand">Ticket Booking</div>
      <ul class="navbar-nav ms-auto">
        <li class="nav-item">
          <router-link class="nav-link" to="/">Home</router-link>
        </li>
        <router-link class="nav-item nav-link" to="/login" v-if="!loggedIn"
          >Login</router-link
        >
        <router-link class="nav-item nav-link" to="/register" v-if="!loggedIn"
          >Register</router-link
        >
        <router-link
          class="nav-item nav-link"
          to="/dashboard"
          v-if="loggedIn && !isAdmin"
          >User Dashboard</router-link
        >
        <router-link
          class="nav-item nav-link"
          to="/admin"
          v-if="loggedIn && isAdmin"
          >Admin Dashboard</router-link
        >
        <div
          class="nav-item nav-link btn btn-danger text-white"
          to="/logout"
          @click="logout"
          v-if="loggedIn"
        >
          Logout
        </div>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      loggedIn: false,
      isAdmin: false,
    };
  },
  methods: {
    checkUserStatus() {
      const jwt = localStorage.getItem("jwt");
      this.loggedIn = !!jwt; // The user is logged in if there is a JWT

      const isAdmin = localStorage.getItem("isAdmin");
      this.isAdmin =
        isAdmin &&
        isAdmin ===
          "a4f2b74b8fc1042a8082699c749ef0f19ca201c6f3f147dfa5226f0928e8c6b1";
    },
    logout() {
      localStorage.removeItem("jwt");
      localStorage.removeItem("isAdmin");
      this.loggedIn = false;
      this.isAdmin = false;
      window.location = "/";
    },
  },
  created() {
    this.checkUserStatus();
  },
  // eslint-disable-next-line
  name: "Navbar",
};
</script>
