<template>
  <div
    style="
      background: url(https://plus.unsplash.com/premium_photo-1682309543429-6aaa6d792dae?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1824&q=80);
    "
    class="jumbotron bg-cover text-white"
  >
    <div class="container py-5 text-center">
      <h1 class="display-4 font-weight-bold pb-4">Summary</h1>
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
  name: "SummaryBanner",
};
</script>
