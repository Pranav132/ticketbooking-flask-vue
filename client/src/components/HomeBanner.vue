<template>
  <header class="masthead">
    <div class="container h-100">
      <div class="row h-100 align-items-center">
        <div class="col-12 text-center">
          <h1 class="fw-light">Ticket Booking</h1>
          <p class="lead">All your movie tickets, in one place.</p>
          <router-link to="/about"
            ><button type="button" class="btn btn-dark">
              Book
            </button></router-link
          >
        </div>
      </div>
    </div>
  </header>
</template>

<style>
.masthead {
  height: 85vh;
  min-height: 500px;
  background-image: url("https://source.unsplash.com/BtbjCFUvBXs/1920x1080");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
</style>

<script>
export default {
  // eslint-disable-next-line
  name: "HomeBanner",
};
</script>
