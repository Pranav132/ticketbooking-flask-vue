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
          v-model="searchLocation"
          class="form-control my-2"
          placeholder="Search by location"
        />
      </div>
      <div class="col-md-3">
        <input
          v-model="searchCapacity"
          class="form-control my-2"
          type="number"
          placeholder="Minimum capacity"
        />
      </div>
      <div class="col-md-3">
        <button class="btn btn-primary my-2" @click="fetchTheatres">
          Search
        </button>
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
    <div v-else class="row pt-4">
      <div v-for="theatre in theatres" :key="theatre.id" class="col-sm-4 py-2">
        <TheatreCard :theatre="theatre" />
      </div>
    </div>
  </div>
</template>

<script>
import { BASE_URL } from "../../globals.js";
import TheatreCard from "./TheatreCard.vue";

export default {
  name: "UserTheatreGrid",
  components: {
    TheatreCard,
  },
  data() {
    return {
      theatres: [],
      loading: true,
      errorMessage: "",
      successMessage: "",
      searchName: "",
      searchLocation: "",
      searchCapacity: null,
    };
  },
  methods: {
    async fetchTheatres() {
      this.loading = true;
      try {
        const token = localStorage.getItem("jwt");
        const url = `${BASE_URL}search/theatre?name=${this.searchName}&location=${this.searchLocation}&capacity=${this.searchCapacity}`;

        const response = await fetch(url, {
          headers: {
            Authorization: "Bearer " + token,
            "Content-Type": "application/json",
          },
        });

        const res = await response.json();

        if (response.ok) {
          this.theatres = res;
          this.errorMessage = "";
        } else {
          if (res.msg) {
            if (res.msg === "Token has expired") {
              this.errorMessage = "Token has expired. Please log in again.";
            } else {
              this.errorMessage = res.msg;
            }
          } else {
            this.errorMessage = res.message || "Error fetching theatres.";
          }
        }
      } catch (error) {
        console.error("Error fetching theatre data:", error);
        this.errorMessage = error.toString();
      } finally {
        this.loading = false;
      }
    },
  },
  created() {
    this.fetchTheatres();
  },
};
</script>
