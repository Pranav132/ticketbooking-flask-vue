<template>
  <div class="view-theatre">
    <TheatreWithShowsBanner />
    <TheatreShowsGrid />
  </div>
</template>

<script>
import TheatreWithShowsBanner from "@/components/TheatreWithShowsBanner";
import TheatreShowsGrid from "@/components/TheatreShowsGrid";

export default {
  name: "TheatreWithShowsView",
  components: {
    TheatreWithShowsBanner,
    TheatreShowsGrid,
  },
};
</script>
