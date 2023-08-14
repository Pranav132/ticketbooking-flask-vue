<template>
  <div class="theatre">
    <UserTheatreBanner />
    <UserTheatreGrid />
  </div>
</template>

<script>
import UserTheatreBanner from "@/components/UserTheatreBanner";
import UserTheatreGrid from "@/components/UserTheatreGrid";

export default {
  name: "UserTheatreView",
  components: {
    UserTheatreBanner,
    UserTheatreGrid,
  },
};
</script>
