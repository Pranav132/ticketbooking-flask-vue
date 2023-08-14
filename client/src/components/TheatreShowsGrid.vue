<template>
  <div class="container">
    <div v-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>
    <div v-if="successMessage" class="alert alert-success" role="alert">
      {{ successMessage }}
    </div>

    <div class="row my-3">
      <div class="col-md-3">
        <input
          v-model="searchName"
          class="form-control my-2"
          placeholder="Search by name"
        />
      </div>
      <div class="col-md-3">
        <input
          v-model="searchTag"
          class="form-control my-2"
          placeholder="Search by tag"
        />
      </div>
      <div class="col-md-3">
        <input
          v-model="searchRating"
          class="form-control my-2"
          type="number"
          placeholder="Min rating"
        />
      </div>
      <div class="col-md-3">
        <input
          v-model="searchMaxPrice"
          class="form-control my-2"
          type="number"
          placeholder="Max price"
        />
      </div>
    </div>

    <div class="row my-2">
      <div class="col-md-12">
        <button class="btn btn-primary" @click="fetchShows">Search</button>
      </div>
    </div>

    <div
      v-if="loading"
      class="d-flex justify-content-center align-items-center"
      style="height: 300px"
    >
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div
      v-else-if="shows.length === 0"
      class="d-flex justify-content-center align-items-center"
      style="height: 300px"
    >
      <h1>No shows found.</h1>
    </div>

    <div v-else class="row pt-4">
      <div v-for="show in shows" :key="show.id" class="col-sm-4 py-2">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ show.name }}</h5>
            <p class="card-text">
              Tags: {{ show.tags.map((tag) => tag.name).join(", ") }}
            </p>
            <p class="card-text">Duration: {{ show.duration }}</p>
            <p class="card-text">Start Time: {{ show.start_time }}</p>
            <p class="card-text">Price: ₹{{ show.ticket_price }}</p>
            <p class="card-text">{{ averageRating(show.reviews) }}</p>

            <router-link v-if="canBook(show) === 1" :to="'/book/' + show.id">
              <button class="btn btn-success">Book</button>
            </router-link>
            <button v-else class="btn btn-secondary" disabled>
              Booking closed
            </button>

            <router-link :to="'/ratings/' + show.id">
              <button
                v-if="reviews && !(reviews.length === 0)"
                class="btn btn-primary"
              >
                View Ratings
              </button>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { BASE_URL } from "../../globals.js";

export default {
  name: "TheatreShowGrid",
  data() {
    return {
      shows: [],
      loading: true,
      errorMessage: "",
      successMessage: "",
      searchName: "",
      searchTag: "",
      searchRating: null,
      searchMaxPrice: null,
    };
  },
  methods: {
    async fetchShows() {
      this.loading = true;

      // Create a params object to store the query parameters
      let params = {
        theatre_id: this.$route.params.id,
        name: this.searchName,
        rating: this.searchRating,
        max_price: this.searchMaxPrice,
      };

      // Convert searchTag string into a comma-separated list
      if (this.searchTag && this.searchTag != "") {
        params.tag = this.searchTag
          .split(",")
          .map((tag) => tag.trim())
          .filter((tag) => tag !== "")
          .join(",");
      }

      // Build the query string dynamically
      let query = Object.keys(params)
        .filter(
          (key) =>
            params[key] !== null &&
            params[key] !== undefined &&
            params[key] !== ""
        )
        .map(
          (key) =>
            `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`
        )
        .join("&");

      // Construct the final URL
      const url = `${BASE_URL}search/show?${query}`;
      try {
        const token = localStorage.getItem("jwt");

        const response = await fetch(url, {
          headers: {
            Authorization: "Bearer " + token,
            "Content-Type": "application/json",
          },
        });

        const res = await response.json();

        if (response.ok) {
          // Sorting the shows so that bookable shows come first
          this.shows = res.sort((a, b) => this.canBook(b) - this.canBook(a));
          this.errorMessage = "";
        } else {
          console.error("Failed to fetch theatre data");
          // Safely access the message property
          if (res.msg) {
            if (res.msg === "Token has expired") {
              this.errorMessage = "Token has expired. Please log in again.";
              this.successMessage = "";
            } else {
              this.errorMessage = res.msg;
              this.successMessage = "";
            }
          } else {
            this.errorMessage = res.message;
            this.successMessage = "";
          }
        }
      } catch (error) {
        console.error("Error fetching show data:", error);
        this.errorMessage = error.toString();
      } finally {
        this.loading = false;
      }
    },
    canBook(show) {
      const currentTime = new Date();
      const showStartTime = new Date(show.start_time);
      const timeDifference = (showStartTime - currentTime) / 60000; // difference in minutes

      return timeDifference > 30 ? 1 : 0;
    },
    averageRating(reviews) {
      if (!reviews || reviews.length === 0) return "No Ratings yet";

      const totalRating = reviews.reduce(
        (total, review) => total + review.rating,
        0
      );
      const avgRating = totalRating / reviews.length;

      return isNaN(avgRating) ? "No Ratings yet" : "Rating" + avgRating;
    },
  },
  created() {
    this.fetchShows();
  },
};
</script>
