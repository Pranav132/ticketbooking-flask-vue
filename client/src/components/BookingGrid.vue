<template>
  <div class="container">
    <div v-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
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
    <!-- No bookings found -->
    <div
      v-else-if="bookings.length === 0"
      class="d-flex justify-content-center align-items-center"
      style="height: 300px"
    >
      <h1>No bookings found.</h1>
    </div>
    <!-- Display bookings -->
    <div v-else class="row pt-4">
      <div
        v-for="booking in bookings"
        :key="booking.booking_id"
        class="col-sm-4 py-2"
      >
        <div class="card h-100">
          <div class="card-body">
            <h4 class="card-title">{{ booking.show_name }}</h4>
            <p class="card-text">Time: {{ booking.show_timing }}</p>
            <p class="card-text">Theatre: {{ booking.theatre_name }}</p>
            <p class="card-text">Place: {{ booking.theare_place }}</p>
            <p class="card-text">Tickets: {{ booking.number_of_tickets }}</p>
            <router-link
              :to="'/rate_show/' + booking.booking_id"
              v-if="canRateShow(booking)"
            >
              <button class="btn btn-primary">Rate</button>
            </router-link>
            <button class="btn btn-secondary" v-else disabled>Rate</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { BASE_URL } from "../../globals.js";

export default {
  name: "BookingsGrid",
  data() {
    return {
      bookings: [],
      loading: true,
      errorMessage: "",
    };
  },
  async created() {
    try {
      const token = localStorage.getItem("jwt");

      const response = await fetch(BASE_URL + "user/bookings", {
        headers: {
          Authorization: "Bearer " + token,
          "Content-Type": "application/json",
        },
      });

      await response.json().then((res) => {
        if (response.ok) {
          this.bookings = res;
          this.errorMessage = "";
        } else {
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
      });
    } catch (error) {
      console.error("Error fetching booking data:", error);
      this.errorMessage = error.toString();
    } finally {
      this.loading = false;
    }
  },
  methods: {
    canRateShow(booking) {
      const showEndTime = new Date(booking.show_timing);
      showEndTime.setHours(showEndTime.getHours() + booking.show_duration);
      return new Date() > showEndTime;
    },
  },
};
</script>
