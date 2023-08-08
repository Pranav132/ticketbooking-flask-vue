<template>
  <nav class="navbar navbar-expand navbar-light bg-light">
    <div class="container-fluid">
      <div class="navbar-brand">Ticket Booking</div>
      <ul class="navbar-nav ms-auto">
        <li class="nav-item">
          <router-link class="nav-link" to="/">Home</router-link>
        </li>
        <a class="nav-item nav-link" href="/login" v-if="!loggedIn">Login</a>
        <a class="nav-item nav-link" href="/register" v-if="!loggedIn"
          >Register</a
        >
        <a class="nav-item nav-link" href="" v-if="loggedIn && !isAdmin"
          >User Dashboard</a
        >
        <a class="nav-item nav-link" href="#" v-if="loggedIn && isAdmin"
          >Admin Dashboard</a
        >
        <a class="nav-item nav-link" href="#" @click="logout" v-if="loggedIn"
          >Logout</a
        >
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

      // To check whether the user is an admin, you could look at the JWT payload
      // if it contains role information, or make a request to your server.
      // For simplicity, here we just randomly assign admin status:
      this.isAdmin = Math.random() < 0.5;
    },
    logout() {
      localStorage.removeItem("jwt");
      this.loggedIn = false;
      this.isAdmin = false;
    },
  },
  created() {
    this.checkUserStatus();
  },
  // eslint-disable-next-line
  name: "Navbar",
};
</script>
