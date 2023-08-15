<template>
  <div class="rating-form container mt-5">
    <div v-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>
    <div v-if="successMessage" class="alert alert-success" role="alert">
      {{ successMessage }}
    </div>

    <main>
      <div class="rating-block card shadow">
        <div class="card-body">
          <div v-if="show" class="text-left">
            <h2 class="mb-4">Rate {{ show.name }}</h2>
            <p><strong>Time:</strong> {{ show.start_time }}</p>
            <p><strong>Duration:</strong> {{ show.duration }}</p>
            <p><strong>Your Rating:</strong></p>
            <input
              type="number"
              v-model="rating"
              min="1"
              max="5"
              step="1"
              class="form-control mb-4"
              @change="ensureInteger"
            />
            <textarea
              v-model="reviewText"
              class="form-control mb-4"
              placeholder="Share your thoughts about the show..."
            ></textarea>
            <button
              @click="submitRating"
              class="btn btn-primary btn-block mt-4"
            >
              Submit Rating
            </button>
          </div>

          <div v-else class="text-center">
            <div class="spinner-border text-primary" role="status">
              <span class="sr-only">Loading...</span>
            </div>
            <p>Loading show details...</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { BASE_URL } from "../../globals.js";
const token = localStorage.getItem("jwt");

const getShowDetails = (showId) => {
  return fetch(BASE_URL + "show/" + showId, {
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token,
    },
  }).then((response) =>
    response.json().then((data) => ({
      data: data,
      status: response.status,
    }))
  );
};

const postRating = (showId, rating, reviewText) => {
  return fetch(BASE_URL + "shows/" + showId + "/review", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token,
    },
    body: JSON.stringify({ rating, text: reviewText }),
  }).then((response) =>
    response.json().then((data) => ({
      data: data,
      status: response.status,
    }))
  );
};

const getBookingDetails = (bookingId) => {
  return fetch(BASE_URL + "booking/" + bookingId, {
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token,
    },
  }).then((response) =>
    response.json().then((data) => ({
      data: data,
      status: response.status,
    }))
  );
};

export default {
  data() {
    return {
      show: null,
      rating: 1,
      reviewText: "",
      errorMessage: "",
      successMessage: "",
    };
  },
  methods: {
    fetchBookingAndShowDetails() {
      getBookingDetails(this.$route.params.id).then((res) => {
        if (res.status === 200) {
          const showId = res.data.show_id;
          this.fetchShowDetails(showId);
        } else {
          if (res.data.msg) {
            if (res.data.msg === "Token has expired") {
              this.errorMessage = "Token has expired. Please log in again.";
              this.successMessage = "";
            } else {
              this.errorMessage = res.data.msg;
              this.successMessage = "";
            }
          } else {
            this.errorMessage = res.data.message;
            this.successMessage = "";
          }
        }
      });
    },
    fetchShowDetails(showId) {
      getShowDetails(showId).then((res) => {
        if (res.status === 200) {
          this.show = res.data;
        } else {
          if (res.data.msg) {
            if (res.data.msg === "Token has expired") {
              this.errorMessage = "Token has expired. Please log in again.";
              this.successMessage = "";
            } else {
              this.errorMessage = res.data.msg;
              this.successMessage = "";
            }
          } else {
            this.errorMessage = res.data.message;
            this.successMessage = "";
          }
        }
      });
    },
    submitRating() {
      postRating(this.show.id, this.rating, this.reviewText).then((res) => {
        if (res.status === 201) {
          this.successMessage = "Your review has been submitted!";
          this.errorMessage = "";
        } else {
          this.errorMessage = res.data.message || "Error occurred!";
          this.successMessage = "";
        }
      });
    },
    ensureInteger() {
      this.rating = Math.round(this.rating);
      if (this.rating < 1) {
        this.rating = 1;
      }
      if (this.rating > 5) {
        this.rating = 5;
      }
    },
  },
  mounted() {
    this.fetchBookingAndShowDetails();
  },
};
</script>
