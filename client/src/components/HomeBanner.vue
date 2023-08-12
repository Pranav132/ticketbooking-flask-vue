<template>
  <header class="masthead">
    <div class="container h-100">
      <div class="row h-100 align-items-center">
        <div class="col-12 text-center">
          <h1 class="fw-light text-white">Ticket Booking</h1>
          <p class="lead text-white">All your movie tickets, in one place.</p>
          <router-link :to="bookingLink">
            <button type="button" class="btn btn-dark">
              {{ bookingText }}
            </button>
          </router-link>
        </div>
      </div>
    </div>
  </header>
</template>

<style>
.masthead {
  height: 85vh;
  min-height: 500px;
  background-image: url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1770&q=80");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
</style>

<script>
export default {
  data() {
    return {
      bookingLink: "/dashboard",
      bookingText: "Book",
    };
  },
  created() {
    const adminLocalStorage = localStorage.getItem("isAdmin");
    const isAdmin =
      adminLocalStorage &&
      adminLocalStorage ===
        "a4f2b74b8fc1042a8082699c749ef0f19ca201c6f3f147dfa5226f0928e8c6b1";

    this.bookingLink = isAdmin ? "/admin" : "/dashboard";
    this.bookingText = isAdmin ? "Admin Dashboard" : "Book";
  },
  name: "HomeBanner",
};
</script>
