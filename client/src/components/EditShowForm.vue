<template>
  <div class="showform">
    <div v-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>
    <div v-if="successMessage" class="alert alert-success" role="alert">
      {{ successMessage }}
    </div>
    <div class="row m-3 background-white">
      <div class="col d-flex justify-content-end">
        <router-link :to="'/theatre/' + show.theatre_id">
          <button class="btn btn-primary">Back to Theatre</button>
        </router-link>
      </div>
    </div>
    <main>
      <div class="showform-block">
        <h1>EDIT SHOW</h1>

        <form @submit.prevent="handleUpdate">
          <div class="form-group">
            <input
              type="text"
              class="form-control"
              placeholder="Show Name"
              v-model="show.name"
              required
            />
          </div>

          <div class="form-group">
            <input
              type="text"
              class="form-control"
              placeholder="Tags (comma separated)"
              v-model="tags"
              required
            />
          </div>

          <div class="form-group">
            <input
              type="number"
              step="0.01"
              class="form-control"
              placeholder="Ticket Price"
              v-model="show.ticket_price"
              required
            />
          </div>

          <div class="form-group">
            <input
              type="datetime-local"
              class="form-control"
              placeholder="Start Time"
              v-model="show.start_time"
              required
            />
          </div>

          <div class="form-group">
            <input
              type="text"
              class="form-control"
              placeholder="Duration (HH:MM)"
              v-model="durationFormatted"
              required
            />
          </div>

          <button class="btn btn-primary btn-block" type="submit">
            Save Changes
          </button>
        </form>
      </div>
    </main>
  </div>
</template>

<script>
import { BASE_URL } from "../../globals.js";

export default {
  name: "EditShowForm",
  data() {
    return {
      show: {
        name: "",
        ticket_price: "",
        start_time: "",
        duration: "",
        theatre_id: "",
      },
      tags: "",
      errorMessage: "",
      successMessage: "",
    };
  },
  computed: {
    durationFormatted: {
      get() {
        return this.show.duration ? this.show.duration.substring(0, 5) : "";
      },
      set(value) {
        this.show.duration = value;
      },
    },
  },
  async created() {
    const showId = this.$route.params.id;
    try {
      const token = localStorage.getItem("jwt");
      const response = await fetch(BASE_URL + "show/" + showId, {
        headers: {
          Authorization: "Bearer " + token,
          "Content-Type": "application/json",
        },
      });
      const res = await response.json();

      if (response.ok) {
        this.show = res;
        this.tags = res.tags.map((tag) => tag.name).join(", ");
      } else {
        this.handleFetchError(response, res);
      }
    } catch (error) {
      this.errorMessage = "Error fetching show data: " + error.toString();
    }
  },
  methods: {
    async handleUpdate() {
      const showId = this.$route.params.id;
      const data = {
        name: this.show.name,
        tags: this.tags.split(",").map((tag) => tag.trim()),
        ticketPrice: this.show.ticket_price,
        startTime: this.show.start_time,
        duration: this.show.duration.match(/\d{2}:\d{2}:\d{2}/)
          ? this.show.duration.slice(0, -3)
          : this.show.duration,
      };
      try {
        const token = localStorage.getItem("jwt");
        const response = await fetch(BASE_URL + "show/" + showId, {
          method: "PUT",
          headers: {
            Authorization: "Bearer " + token,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });
        const res = await response.json();

        if (response.ok) {
          this.errorMessage = "";
          this.successMessage = "Show updated successfully!";
        } else {
          this.handleFetchError(response, res);
        }
      } catch (error) {
        this.errorMessage = "Error updating show: " + error.toString();
      }
    },
    handleFetchError(response, res) {
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
    },
  },
};
</script>

<style>
.show-form {
  height: 80vh;
}
.showform-block {
  padding: 20px 100px !important;
}
.showform-page main {
  width: 100%;
  max-width: 460px;
  margin: 8% auto 5%;
}
.showform-block {
  background-color: #fff;
  padding: 30px;
  -webkit-box-shadow: 0 3px 50px 0 rgba(0, 0, 0, 0.1);
  box-shadow: 0 3px 50px 0 rgba(0, 0, 0, 0.1);
  text-align: center;
  border-radius: 5px;
}
.showform-block h1,
.showform-block h6 {
  font-family: Open Sans, sans-serif;
  color: #96a2b2;
  letter-spacing: 1px;
}
.showform-block h1 {
  font-size: 22px;
  margin-bottom: 60px;
  margin-top: 40px;
}
.showform-block h6 {
  font-size: 11px;
  text-transform: uppercase;
  margin-top: 0;
}
.showform-block .form-group {
  margin-top: 15px;
  margin-bottom: 15px;
}
.showform-block .form-control,
.showform-block .form-control:focus,
.showform-block .input-group-addon,
.showform-block .input-group-addon:focus {
  background-color: transparent;
  border: none;
}
.showform-block .form-control {
  font-size: 17px;
  border-radius: 0px;
}
.showform-block input:-webkit-autofill {
  -webkit-box-shadow: 0 0 0 1000px #fff inset;
  -webkit-text-fill-color: #818a91;
  -webkit-transition: none;
  -o-transition: none;
  transition: none;
}
.showform-block .input-group-addon {
  color: #29aafe;
  font-size: 19px;
  opacity: 0.5;
}
.showform-block .btn-block {
  margin-top: 30px;
  padding: 15px;
  background: #29aafe;
  border-color: #29aafe;
}
.showform-block .hr-xs {
  margin-top: 5px;
  margin-bottom: 5px;
}
.showform-footer {
  margin-top: 60px;
  opacity: 0.5;
  -webkit-transition: opacity 0.3s ease-in-out;
  -o-transition: opacity 0.3s ease-in-out;
  transition: opacity 0.3s ease-in-out;
}
.showform-footer:hover {
  opacity: 1;
}
.showform-links {
  padding: 15px 5px 0;
  font-size: 13px;
  color: #96a2b2;
}
.showform-links:after {
  content: "";
  display: table;
  clear: both;
}
.showform-links a {
  color: #96a2b2;
  opacity: 0.9;
}
.showform-links a:hover {
  color: #29aafe;
  opacity: 1;
}
@media (max-width: 767px) {
  .showform-page main {
    position: static;
    top: auto;
    left: auto;
    -webkit-transform: none;
    -o-transform: none;
    transform: none;
    padding: 30px 15px;
  }
  .showform-block {
    padding: 20px;
  }
}
.social-icons {
  padding-left: 0;
  margin-bottom: 0;
  list-style: none;
}
.social-icons li {
  display: inline-block;
  margin-bottom: 4px;
}
.social-icons li.title {
  margin-right: 15px;
  text-transform: uppercase;
  color: #96a2b2;
  font-weight: 700;
  font-size: 13px;
}
.social-icons a {
  background-color: #eceeef;
  color: #818a91;
  font-size: 16px;
  display: inline-block;
  line-height: 44px;
  width: 44px;
  height: 44px;
  text-align: center;
  margin-right: 8px;
  border-radius: 100%;
  -webkit-transition: all 0.2s linear;
  -o-transition: all 0.2s linear;
  transition: all 0.2s linear;
}
.social-icons a:active,
.social-icons a:focus,
.social-icons a:hover {
  color: #fff;
  background-color: #29aafe;
}
.social-icons.size-sm a {
  line-height: 34px;
  height: 34px;
  width: 34px;
  font-size: 14px;
}
.social-icons a.facebook:hover {
  background-color: #3b5998;
}
.social-icons a.rss:hover {
  background-color: #f26522;
}
.social-icons a.google-plus:hover {
  background-color: #dd4b39;
}
.social-icons a.twitter:hover {
  background-color: #00aced;
}
.social-icons a.linkedin:hover {
  background-color: #007bb6;
}
</style>
