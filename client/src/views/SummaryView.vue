<template>
  <div class="summary">
    <SummaryBanner />
    <SummaryData />
  </div>
</template>

<script>
import SummaryData from "@/components/SummaryData";
import SummaryBanner from "@/components/SummaryBanner";

export default {
  name: "SummaryView",
  components: {
    SummaryData,
    SummaryBanner,
  },
};
</script>
