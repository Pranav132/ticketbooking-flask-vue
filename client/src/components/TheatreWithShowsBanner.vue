<template>
  <div class="theatre-banner">
    <div
      v-if="loading"
      class="d-flex justify-content-center align-items-center"
    >
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>
    <div v-if="successMessage" class="alert alert-success" role="alert">
      {{ successMessage }}
    </div>
    <div
      style="
        background: url(https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1770&q=80);
      "
      class="jumbotron bg-cover text-white"
    >
      <div v-if="!loading" class="container py-5 text-center">
        <h1 class="display-4 font-weight-bold pb-4">{{ theatre.name }}</h1>
        <p>{{ theatre.place }} | Capacity: {{ theatre.capacity }}</p>

        <div v-if="errorMessage" class="alert alert-danger mt-4" role="alert">
          {{ errorMessage }}
        </div>
        <div
          v-if="successMessage"
          class="alert alert-success mt-4"
          role="alert"
        >
          {{ successMessage }}
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.bg-cover {
  background-size: cover !important;
  height: 35vh !important;
  display: flex;
  background-color: rgba(255, 255, 255, 0.4);
  -webkit-backdrop-filter: blur(5px);
  backdrop-filter: blur(5px);
  justify-content: center;
  align-items: center;
}
</style>

<script>
import { BASE_URL } from "../../globals.js";

export default {
  name: "TheatreBanner",
  data() {
    return {
      theatre: {},
      loading: true,
      errorMessage: "",
      successMessage: "",
    };
  },
  async mounted() {
    const theatreId = this.$route.params.id;
    try {
      const token = localStorage.getItem("jwt");

      const response = await fetch(BASE_URL + "theatre/" + theatreId, {
        headers: {
          Authorization: "Bearer " + token,
          "Content-Type": "application/json",
        },
      });

      await response.json().then((res) => {
        if (response.ok) {
          this.theatre = res;
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
};
</script>
