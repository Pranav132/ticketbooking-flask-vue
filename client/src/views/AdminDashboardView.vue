<template>
  <div class="about">
    <AdminDashboardBanner />
    <TheatreGrid />
  </div>
</template>

<script>
import AdminDashboardBanner from "@/components/AdminDashboardBanner";
import TheatreGrid from "@/components/TheatreGrid";

export default {
  name: "AdminLoginView",
  components: {
    AdminDashboardBanner,
    TheatreGrid,
  },
};
</script>
