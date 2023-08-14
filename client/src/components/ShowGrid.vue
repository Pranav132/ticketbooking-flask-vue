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
        <router-link :to="'/add-show/' + $route.params.id">
          <button class="btn btn-primary">Add Show</button>
        </router-link>
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
        <div class="card h-100 position-relative">
          <button
            class="btn btn-danger position-absolute btn-sm top-0 end-0 m-1"
            @click="deleteShow(show.id)"
            style="width: 30px; height: 30px"
          >
            <i class="bi bi-trash"></i>
          </button>
          <div class="card-body">
            <h3 class="card-title pb-2">{{ show.name }}</h3>
            <p class="card-text">
              <strong>Price: </strong>{{ show.ticket_price }}
            </p>
            <p class="card-text">
              <strong>Start Time: </strong> {{ show.start_time }}
            </p>
            <p class="card-text">
              <strong>Duration: </strong> {{ show.duration }}
            </p>
            <p class="card-text">
              <strong>Tags: &nbsp;</strong>
              <span v-for="(tag, index) in show.tags" :key="tag.id">
                {{ tag.name
                }}<span v-if="index !== show.tags.length - 1">,</span>
                {{ " " }}
              </span>
            </p>
            <router-link
              :to="'/edit-show/' + show.id"
              class="btn btn-outline-secondary"
              >Edit</router-link
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
  name: "ShowGrid",
  data() {
    return {
      shows: [],
      loading: true,
      errorMessage: "",
      successMessage: "",
    };
  },
  async created() {
    try {
      const token = localStorage.getItem("jwt");

      const response = await fetch(
        `${BASE_URL}get_theatre_shows/${this.$route.params.id}`,
        {
          headers: {
            Authorization: "Bearer " + token,
            "Content-Type": "application/json",
          },
        }
      );

      await response.json().then((res) => {
        if (response.ok) {
          this.shows = res;
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
  methods: {
    async deleteShow(showId) {
      try {
        const token = localStorage.getItem("jwt");
        const response = await fetch(BASE_URL + "show/" + showId, {
          method: "DELETE",
          headers: {
            Authorization: "Bearer " + token,
            "Content-Type": "application/json",
          },
        });

        const res = await response.json();

        if (response.ok) {
          this.shows = this.shows.filter((show) => show.id !== showId);
          this.successMessage = res.message;
        } else {
          this.errorMessage =
            res.msg === "Token has expired"
              ? "Token has expired. Please log in again."
              : res.msg;
          this.successMessage = "";
        }
      } catch (error) {
        this.errorMessage = "Error: " + error.toString();
        this.successMessage = "";
      }
    },
  },
};
</script>
