<template>
  <div class="rate-show">
    <RateShowBanner />
    <RateShowForm />
  </div>
</template>

<script>
import RateShowBanner from "@/components/RateShowBanner";
import RateShowForm from "@/components/RateShowForm";

export default {
  name: "RateShowView",
  components: {
    RateShowBanner,
    RateShowForm,
  },
};
</script>
