<template>
  <div class="booking-form container mt-5">
    <div v-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>
    <div v-if="successMessage" class="alert alert-success" role="alert">
      {{ successMessage }}
    </div>

    <main>
      <div class="booking-block card shadow">
        <div class="card-body">
          <div v-if="show" class="text-left">
            <h2 class="mb-4">Booking for {{ show.name }}</h2>
            <p><strong>Time:</strong> {{ show.start_time }}</p>
            <p><strong>Duration:</strong> {{ show.duration }}</p>
            <p>{{ averageRating(show.reviews) }}</p>
            <p><strong>Price per Ticket:</strong> ${{ show.ticket_price }}</p>
            <p><strong>Seats Remaining:</strong> {{ show?.capacity }}</p>

            <div class="input-group mb-3">
              <input
                type="number"
                class="form-control"
                v-model="numTickets"
                min="1"
                step="1"
                placeholder="Number of Tickets"
                @change="ensureInteger"
              />
              <div class="input-group-append">
                <span class="input-group-text">Tickets</span>
              </div>
            </div>

            <p><strong>Total Price:</strong> ${{ totalPrice }}</p>

            <button @click="bookShow" class="btn btn-primary btn-block mt-4">
              Book Now
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

const bookTheShow = (data) => {
  return fetch(BASE_URL + "book", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token,
    },
    body: JSON.stringify(data),
  }).then((response) =>
    response.json().then((data) => ({
      data: data,
      status: response.status,
    }))
  );
};

const getTheatreDetails = (theatreId) => {
  return fetch(BASE_URL + "theatre/" + theatreId, {
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
      theatre: null,
      numTickets: 0,
      errorMessage: "",
      successMessage: "",
    };
  },
  computed: {
    totalPrice() {
      return this.numTickets * (this.show ? this.show.ticket_price : 0);
    },
  },
  methods: {
    fetchShowDetails() {
      getShowDetails(this.$route.params.id).then((res) => {
        if (res.status === 200) {
          this.show = res.data;
          getTheatreDetails(this.show.theatre_id).then((theatreRes) => {
            if (theatreRes.status === 200) {
              this.theatre = theatreRes.data;
            } else {
              this.errorMessage = "Failed to fetch theatre details.";
            }
          });
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
    bookShow() {
      const data = {
        show_id: this.show.id,
        num_tickets: this.numTickets,
      };
      bookTheShow(data).then((res) => {
        if (res.status === 200) {
          this.successMessage = res.data.message;
          this.errorMessage = "";
        } else {
          // Safely access the message property
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
    ensureInteger() {
      this.numTickets = Math.round(this.numTickets);
      if (this.numTickets < 1) {
        this.numTickets = 1;
      }
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
  mounted() {
    this.fetchShowDetails();
  },
};
</script>
