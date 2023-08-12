<template>
  <div
    style="
      background: url(https://images.unsplash.com/photo-1478760329108-5c3ed9d495a0?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1674&q=80);
    "
    class="jumbotron bg-cover text-white"
  >
    <div class="container py-5 text-center">
      <h1 class="display-4 font-weight-bold pb-4">Welcome, Admin</h1>
      <a href="/summary" role="button" class="btn btn-primary px-5">Summary</a>
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
  name: "AdminDashboardBanner",
};
</script>
