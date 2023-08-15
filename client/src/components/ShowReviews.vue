<template>
  <div class="container pt-5">
    <div v-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>
    <div v-if="successMessage" class="alert alert-success" role="alert">
      {{ successMessage }}
    </div>

    <h2 class="pb-3">Reviews for {{ showName }}</h2>
    <div v-if="loading">Loading reviews...</div>
    <div v-else-if="reviews.length === 0">No reviews for this show yet.</div>
    <div v-else>
      <div v-for="review in reviews" :key="review.id" class="review-box">
        <strong>User {{ review.user_id }}:</strong> {{ review.text }}
        <div>Rating: {{ review.rating }} / 5</div>
      </div>
    </div>
  </div>
</template>

<script>
import { BASE_URL } from "../../globals.js";

export default {
  data() {
    return {
      reviews: [],
      showName: "", // placeholder for the show's name
      loading: true,
      errorMessage: "",
      successMessage: "",
    };
  },
  methods: {
    async fetchReviews() {
      try {
        const token = localStorage.getItem("jwt");

        const response = await fetch(
          `${BASE_URL}show/${this.$route.params.id}/reviews`,
          {
            headers: {
              Authorization: "Bearer " + token,
              "Content-Type": "application/json",
            },
          }
        );

        await response.json().then((res) => {
          if (response.ok) {
            this.reviews = res.reviews;
            // assuming the show name is available in the response; adjust as needed
            this.showName = res.show_name;
            this.errorMessage = "";
            this.successMessage = "";
          } else {
            if (res.msg) {
              this.errorMessage =
                res.msg === "Token has expired"
                  ? "Token has expired. Please log in again."
                  : res.msg;
              this.successMessage = "";
            } else {
              this.errorMessage = res.message;
              this.successMessage = "";
            }
          }
        });
      } catch (error) {
        this.errorMessage = "Error: " + error.toString();
      } finally {
        this.loading = false;
      }
    },
  },
  mounted() {
    this.fetchReviews();
  },
};
</script>

<style scoped>
.review-box {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}
</style>
