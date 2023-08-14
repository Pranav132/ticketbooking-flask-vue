<template>
  <div class="theatre">
    <TheatreBanner />
    <ShowGrid />
  </div>
</template>

<script>
import TheatreBanner from "@/components/TheatreBanner";
import ShowGrid from "@/components/ShowGrid";

export default {
  name: "TheatreView",
  components: {
    TheatreBanner,
    ShowGrid,
  },
};
</script>
