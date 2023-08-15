<template>
  <div class="show-reviews">
    <RatingsBanner />
    <ShowReviews />
  </div>
</template>

<script>
import ShowReviews from "@/components/ShowReviews";
import RatingsBanner from "@/components/RatingsBanner";

export default {
  name: "ShowReviewsView",
  components: {
    ShowReviews,
    RatingsBanner,
  },
};
</script>
