<template>
  <div class="container mt-4">
    <!-- Alerts for Success and Error Messages -->
    <div v-if="successMessage" class="alert alert-success" role="alert">
      {{ successMessage }}
    </div>
    <div v-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>

    <!-- Summary Data Display -->
    <div class="row my-4">
      <!-- Summary Card -->
      <div class="col-lg-4 mb-4">
        <div class="card">
          <div class="card-header">Summary</div>
          <ul class="list-group list-group-flush">
            <li class="list-group-item">Total Users: {{ total_users }}</li>
            <li class="list-group-item">
              Total Theatres: {{ total_theatres }}
            </li>
            <li class="list-group-item">Total Shows: {{ total_shows }}</li>
            <li class="list-group-item">
              Total Bookings: {{ total_bookings }}
            </li>
            <li class="list-group-item">Total Reviews: {{ total_reviews }}</li>
            <li class="list-group-item">
              Average Rating: {{ average_rating }}
            </li>
          </ul>
        </div>
      </div>

      <!-- Top Shows Card -->
      <div class="col-lg-4 mb-4">
        <div class="card">
          <div class="card-header">Top Shows</div>
          <ul class="list-group list-group-flush">
            <li
              v-for="show in top_shows"
              :key="show.show_id"
              class="list-group-item"
            >
              <strong>{{ show.show_name }}</strong> - Tickets Booked:
              {{ show.tickets_booked }}
            </li>
          </ul>
        </div>
      </div>

      <!-- Top Reviewers Card -->
      <div class="col-lg-4 mb-4">
        <div class="card">
          <div class="card-header">Top Reviewers</div>
          <ul class="list-group list-group-flush">
            <li
              v-for="reviewer in top_reviewers"
              :key="reviewer.user_id"
              class="list-group-item"
            >
              <strong>{{ reviewer.user_name }}</strong> - Reviews Written:
              {{ reviewer.reviews_written }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { BASE_URL } from "../../globals.js";

export default {
  data() {
    return {
      total_users: 0,
      total_theatres: 0,
      total_shows: 0,
      total_bookings: 0,
      total_reviews: 0,
      average_rating: 0,
      top_shows: [],
      top_reviewers: [],
      errorMessage: "",
      successMessage: "",
    };
  },
  created() {
    this.fetchSummary();
  },
  methods: {
    async fetchSummary() {
      try {
        const token = localStorage.getItem("jwt");

        const response = await fetch(BASE_URL + "summary", {
          headers: {
            Authorization: "Bearer " + token,
            "Content-Type": "application/json",
          },
        });

        const res = await response.json();

        if (response.ok) {
          this.total_users = res.total_users;
          this.total_theatres = res.total_theatres;
          this.total_shows = res.total_shows;
          this.total_bookings = res.total_bookings;
          this.total_reviews = res.total_reviews;
          this.average_rating = res.average_rating;
          this.top_shows = res.top_shows;
          this.top_reviewers = res.top_reviewers;
          this.errorMessage = "";
        } else {
          this.successMessage = "";
          if (res.msg) {
            if (res.msg === "Token has expired") {
              this.errorMessage = "Token has expired. Please log in again.";
            } else {
              this.errorMessage = res.msg;
            }
          } else {
            this.errorMessage = res.message;
          }
        }
      } catch (error) {
        this.successMessage = "";
        this.errorMessage = "Error: " + error.toString();
      }
    },
  },
};
</script>
