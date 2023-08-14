<template>
  <div class="user-dashboard">
    <UserDashboardBanner />
    <BookingGrid />
  </div>
</template>

<script>
import UserDashboardBanner from "@/components/UserDashboardBanner";
import BookingGrid from "@/components/BookingGrid";

export default {
  name: "UserDashboardView",
  components: {
    UserDashboardBanner,
    BookingGrid,
  },
};
</script>
