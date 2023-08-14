<template>
  <div class="theatre-form">
    <div v-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>
    <div v-if="successMessage" class="alert alert-success" role="alert">
      {{ successMessage }}
    </div>
    <div class="row m-3 background-white">
      <div class="col d-flex justify-content-end">
        <router-link to="/admin">
          <button class="btn btn-primary">Dashboard</button>
        </router-link>
      </div>
    </div>
    <main>
      <div class="theatreform-block">
        <h1>ADD A THEATRE</h1>

        <form @submit.prevent="handleSubmit">
          <hr class="hr-xs" />

          <div class="form-group">
            <div class="input-group">
              <input
                type="text"
                class="form-control"
                placeholder="Theatre Name"
                v-model="name"
                required
              />
            </div>
          </div>

          <hr class="hr-xs" />

          <div class="form-group">
            <div class="input-group">
              <input
                type="text"
                class="form-control"
                placeholder="Theatre Place"
                v-model="place"
                required
              />
            </div>
          </div>

          <hr class="hr-xs" />

          <div class="form-group">
            <div class="input-group">
              <input
                type="number"
                class="form-control"
                placeholder="Capacity"
                v-model="capacity"
                required
              />
            </div>
          </div>

          <hr class="hr-xs" />

          <button class="btn btn-primary btn-block" type="submit">Add</button>
        </form>
      </div>
    </main>
  </div>
</template>

<style>
.theatre-form {
  height: 80vh;
}
.theatreform-block {
  padding: 20px 100px !important;
}
.theatreform-page main {
  width: 100%;
  max-width: 460px;
  margin: 8% auto 5%;
}
.theatreform-block {
  background-color: #fff;
  padding: 30px;
  -webkit-box-shadow: 0 3px 50px 0 rgba(0, 0, 0, 0.1);
  box-shadow: 0 3px 50px 0 rgba(0, 0, 0, 0.1);
  text-align: center;
  border-radius: 5px;
}
.theatreform-block h1,
.theatreform-block h6 {
  font-family: Open Sans, sans-serif;
  color: #96a2b2;
  letter-spacing: 1px;
}
.theatreform-block h1 {
  font-size: 22px;
  margin-bottom: 60px;
  margin-top: 40px;
}
.theatreform-block h6 {
  font-size: 11px;
  text-transform: uppercase;
  margin-top: 0;
}
.theatreform-block .form-group {
  margin-top: 15px;
  margin-bottom: 15px;
}
.theatreform-block .form-control,
.theatreform-block .form-control:focus,
.theatreform-block .input-group-addon,
.theatreform-block .input-group-addon:focus {
  background-color: transparent;
  border: none;
}
.theatreform-block .form-control {
  font-size: 17px;
  border-radius: 0px;
}
.theatreform-block input:-webkit-autofill {
  -webkit-box-shadow: 0 0 0 1000px #fff inset;
  -webkit-text-fill-color: #818a91;
  -webkit-transition: none;
  -o-transition: none;
  transition: none;
}
.theatreform-block .input-group-addon {
  color: #29aafe;
  font-size: 19px;
  opacity: 0.5;
}
.theatreform-block .btn-block {
  margin-top: 30px;
  padding: 15px;
  background: #29aafe;
  border-color: #29aafe;
}
.theatreform-block .hr-xs {
  margin-top: 5px;
  margin-bottom: 5px;
}
.theatreform-footer {
  margin-top: 60px;
  opacity: 0.5;
  -webkit-transition: opacity 0.3s ease-in-out;
  -o-transition: opacity 0.3s ease-in-out;
  transition: opacity 0.3s ease-in-out;
}
.theatreform-footer:hover {
  opacity: 1;
}
.theatreform-links {
  padding: 15px 5px 0;
  font-size: 13px;
  color: #96a2b2;
}
.theatreform-links:after {
  content: "";
  display: table;
  clear: both;
}
.theatreform-links a {
  color: #96a2b2;
  opacity: 0.9;
}
.theatreform-links a:hover {
  color: #29aafe;
  opacity: 1;
}
@media (max-width: 767px) {
  .theatreform-page main {
    position: static;
    top: auto;
    left: auto;
    -webkit-transform: none;
    -o-transform: none;
    transform: none;
    padding: 30px 15px;
  }
  .theatreform-block {
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

<script>
import { BASE_URL } from "../../globals.js";
const token = localStorage.getItem("jwt");

const addTheatre = (data) => {
  return fetch(BASE_URL + "theatre", {
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

export default {
  name: "TheatreForm",
  data() {
    return {
      name: "",
      place: "",
      capacity: "",
      errorMessage: "",
      successMessage: "",
    };
  },
  methods: {
    handleSubmit() {
      const data = {
        name: this.name,
        place: this.place,
        capacity: this.capacity,
      };

      addTheatre(data).then((res) => {
        console.log(res);
        if (res.status === 201) {
          this.errorMessage = ""; // Clear any error messages
          this.successMessage = "Theatre added!";
        } else {
          this.successMessage = "";
          if (res.data.msg) {
            if (res.data.msg === "Token has expired") {
              this.errorMessage = "Token has expired. Please log in again.";
            } else {
              this.errorMessage = res.data.msg;
            }
          } else {
            this.errorMessage = res.data.message;
          }
        }
      });
    },
  },
};
</script>
