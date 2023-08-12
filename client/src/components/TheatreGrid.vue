<template>
  <div class="container">
    <div v-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>
    <div class="row my-3">
      <div class="col d-flex justify-content-end">
        <router-link to="/add-theatre">
          <button class="btn btn-primary">Add Theatre</button>
        </router-link>
      </div>
    </div>
    <!-- Loading state with Bootstrap spinner -->
    <div
      v-if="loading"
      class="d-flex justify-content-center align-items-center"
      style="height: 300px"
    >
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <!-- No theatres found -->
    <div
      v-else-if="theatres.length === 0"
      class="d-flex justify-content-center align-items-center"
      style="height: 300px"
    >
      <h1>No theatres found.</h1>
    </div>
    <!-- Display theatres -->
    <div v-else class="row pt-3">
      <div v-for="theatre in theatres" :key="theatre.id" class="col-sm-4 py-2">
        <div class="card h-100">
          <div class="card-body">
            <h3 class="card-title">{{ theatre.name }}</h3>
            <p class="card-text">{{ theatre.place }}</p>
            <p class="card-text">Capacity: {{ theatre.capacity }}</p>
            <router-link to="#" class="btn btn-outline-secondary"
              >View</router-link
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { BASE_URL } from "../../globals.js";

export default {
  name: "TheatreGrid",
  data() {
    return {
      theatres: [],
      loading: true,
      errorMessage: "",
    };
  },
  async created() {
    try {
      const token = localStorage.getItem("jwt");

      const response = await fetch(BASE_URL + "search/theatre", {
        headers: {
          Authorization: "Bearer " + token,
          "Content-Type": "application/json",
        },
      });

      // Always parse the JSON response first
      await response.json().then((res) => {
        console.log(res);
        if (response.ok) {
          this.theatres = res;
          this.errorMessage = "";
        } else {
          console.error("Failed to fetch theatre data");
          // Safely access the message property
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
      });
    } catch (error) {
      console.error("Error fetching theatre data:", error);
      this.errorMessage = error.toString();
    } finally {
      this.loading = false;
    }
  },
};
</script>
