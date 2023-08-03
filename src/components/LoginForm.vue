<template>
  <div>
    <b-form @submit="onSubmit">
      <b-form-group label="Username">
        <b-form-input v-model="username"></b-form-input>
      </b-form-group>
      <b-form-group label="Password">
        <b-form-input type="password" v-model="password"></b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Login</b-button>
    </b-form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginForm", // Name of the component
  data() {
    return {
      username: "",
      password: ""
    };
  },
  methods: {
    async onSubmit(evt) {
      evt.preventDefault();

      try {
        const response = await axios.post("/login", {
          username: this.username,
          password: this.password
        });
        // Store the access token and redirect
        localStorage.setItem("token", response.data.access_token);
        this.$router.push("/");
      } catch (error) {
        console.error("An error occurred while logging in:", error);
      }
    }
  }
};
</script>
