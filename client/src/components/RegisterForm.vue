<template>
  <div class="register-page">
    <div v-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>
    <div v-if="successMessage" class="alert alert-success" role="alert">
      {{ successMessage }}
    </div>
    <main>
      <div class="register-block">
        <h1>REGISTER</h1>

        <form @submit.prevent="handleSubmit">
          <hr class="hr-xs" />

          <div class="form-group">
            <div class="input-group">
              <input
                type="text"
                class="form-control"
                placeholder="Choose a username"
                v-model="username"
              />
            </div>
          </div>

          <hr class="hr-xs" />

          <div class="form-group">
            <div class="input-group">
              <input
                type="text"
                class="form-control"
                placeholder="Your email address"
                v-model="email"
              />
            </div>
          </div>

          <hr class="hr-xs" />

          <div class="form-group">
            <div class="input-group">
              <input
                type="password"
                class="form-control"
                placeholder="Choose a password"
                v-model="password"
              />
            </div>
          </div>

          <hr class="hr-xs" />

          <button class="btn btn-primary btn-block" type="submit">
            Register
          </button>
        </form>
      </div>
    </main>
  </div>
</template>

<style>
.register-page main {
  width: 100%;
  max-width: 460px;
  margin: 8% auto 5%;
}
.register-block {
  background-color: #fff;
  padding: 30px;
  -webkit-box-shadow: 0 3px 50px 0 rgba(0, 0, 0, 0.1);
  box-shadow: 0 3px 50px 0 rgba(0, 0, 0, 0.1);
  text-align: center;
  border-radius: 5px;
}
.register-block h1,
.register-block h6 {
  font-family: Open Sans, sans-serif;
  color: #96a2b2;
  letter-spacing: 1px;
}
.register-block h1 {
  font-size: 22px;
  margin-bottom: 60px;
  margin-top: 40px;
}
.register-block h6 {
  font-size: 11px;
  text-transform: uppercase;
  margin-top: 0;
}
.register-block .form-group {
  margin-top: 15px;
  margin-bottom: 15px;
}
.register-block .form-control,
.register-block .form-control:focus,
.register-block .input-group-addon,
.register-block .input-group-addon:focus {
  background-color: transparent;
  border: none;
}
.register-block .form-control {
  font-size: 17px;
  border-radius: 0px;
}
.register-block input:-webkit-autofill {
  -webkit-box-shadow: 0 0 0 1000px #fff inset;
  -webkit-text-fill-color: #818a91;
  -webkit-transition: none;
  -o-transition: none;
  transition: none;
}
.register-block .input-group-addon {
  color: #29aafe;
  font-size: 19px;
  opacity: 0.5;
}
.register-block .btn-block {
  margin-top: 30px;
  padding: 15px;
  background: #29aafe;
  border-color: #29aafe;
}
.register-block .hr-xs {
  margin-top: 5px;
  margin-bottom: 5px;
}
.register-footer {
  margin-top: 60px;
  opacity: 0.5;
  -webkit-transition: opacity 0.3s ease-in-out;
  -o-transition: opacity 0.3s ease-in-out;
  transition: opacity 0.3s ease-in-out;
}
.register-footer:hover {
  opacity: 1;
}
.register-links {
  padding: 15px 5px 0;
  font-size: 13px;
  color: #96a2b2;
}
.register-links:after {
  content: "";
  display: table;
  clear: both;
}
.register-links a {
  color: #96a2b2;
  opacity: 0.9;
}
.register-links a:hover {
  color: #29aafe;
  opacity: 1;
}
@media (max-width: 767px) {
  .register-page main {
    position: static;
    top: auto;
    left: auto;
    -webkit-transform: none;
    -o-transform: none;
    transform: none;
    padding: 30px 15px;
  }
  .register-block {
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
function validateEmail(email) {
  var regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
  return regex.test(email);
}

import { BASE_URL } from "../../globals.js";

const fetchRegister = (credentials) => {
  return fetch(BASE_URL + "signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  }).then((response) =>
    response.json().then((data) => ({
      data: data,
      status: response.status,
    }))
  );
};

export default {
  // eslint-disable-next-line
  name: "RegisterForm",
  data() {
    return {
      username: "",
      password: "",
      email: "",
      errorMessage: "",
      successMessage: "",
    };
  },
  methods: {
    handleSubmit() {
      const credentials = {
        username: this.username,
        password: this.password,
        email: this.email,
      };

      if (!validateEmail(this.email)) {
        this.errorMessage = "Please enter a valid email";
        return;
      }

      fetchRegister(credentials).then((res) => {
        if (res.status === 201) {
          this.errorMessage = ""; // Clear any error messages
          this.successMessage = "You have been registered! Please log in now.";
        } else {
          this.successMessage = "";
          this.errorMessage = res.data.message;
        }
      });
    },
  },
};
</script>
