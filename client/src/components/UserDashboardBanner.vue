<template>
  <div
    style="
      background: url(https://plus.unsplash.com/premium_photo-1686195842977-cf9e434d9a49?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2232&q=80);
    "
    class="jumbotron bg-cover text-white"
  >
    <div class="container py-5 text-center">
      <h1 class="display-4 font-weight-bold pb-4">Welcome, User</h1>
      <a href="/theatres" role="button" class="btn btn-primary px-5 mx-3 my-3"
        >View Theatres</a
      >
    </div>
  </div>
</template>

<style>
.bg-cover {
  background-size: cover !important;
  height: 35vh !important;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>

<script>
export default {
  name: "UserDashboardBanner",
};
</script>
