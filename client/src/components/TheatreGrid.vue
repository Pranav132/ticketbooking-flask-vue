<template>
  <div class="container">
    <div v-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>
    <div v-if="successMessage" class="alert alert-success" role="alert">
      {{ successMessage }}
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
    <div v-else class="row pt-4">
      <div v-for="theatre in theatres" :key="theatre.id" class="col-sm-4 py-2">
        <div class="card h-100 position-relative">
          <!-- Delete button -->
          <button
            class="btn btn-danger position-absolute btn-sm top-0 end-0 m-1"
            @click="deleteTheatre(theatre.id)"
            style="width: 30px; height: 30px"
          >
            <i class="bi bi-trash"></i>
          </button>

          <div class="card-body">
            <h3 class="card-title">{{ theatre.name }}</h3>
            <p class="card-text">{{ theatre.place }}</p>
            <p class="card-text">Capacity: {{ theatre.capacity }}</p>
            <router-link
              :to="'/theatre/' + theatre.id"
              class="btn btn-outline-secondary"
              >View</router-link
            >
            <button class="btn btn-primary m-3" @click="getReport(theatre.id)">
              Export csv
            </button>
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
      successMessage: "",
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
          this.successMessage = "";
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
      });
    } catch (error) {
      console.error("Error fetching theatre data:", error);
      this.errorMessage = error.toString();
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async deleteTheatre(theatreId) {
      try {
        const token = localStorage.getItem("jwt");
        const response = await fetch(BASE_URL + "theatre/" + theatreId, {
          method: "DELETE",
          headers: {
            Authorization: "Bearer " + token,
            "Content-Type": "application/json",
          },
        });

        const res = await response.json();

        if (response.ok) {
          // Filter out the deleted theatre from the list without fetching all theatres again
          this.theatres = this.theatres.filter(
            (theatre) => theatre.id !== theatreId
          );
          this.successMessage = res.message;
        } else {
          console.error("Failed to fetch theatre data");
          this.successMessage = "";
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
        this.successMessage = "";
        console.error("Error deleting theatre:", error);
        this.errorMessage = "Error: " + error.toString();
      }
    },
    async getReport(theatreId) {
      try {
        const token = localStorage.getItem("jwt");
        const response = await fetch(
          BASE_URL + "export_theatre_as_csv/" + theatreId,
          {
            method: "GET",
            headers: {
              Authorization: "Bearer " + token,
              "Content-Type": "application/json",
            },
          }
        );
        const res = await response.json();

        if (response.ok) {
          this.successMessage = "Check your email for the report!";
          this.errorMessage = "";
        } else {
          console.error("Failed to fetch theatre data");
          this.successMessage = "";
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
        this.successMessage = "";
        this.errorMessage = "Error: " + error.toString();
      }
    },
  },
};
</script>
