<template>
    <div class="container">
      <form @submit.prevent="handleSubmit">
        <fieldset class="form-group">
          <legend class="border-bottom mb-2">Log In</legend>
          <div v-if="serverError" class="alert alert-danger">
            {{ serverError }}
          </div>
          <div class="form-group">
            <label class="form-control-label">Email</label>
            <input v-model="email" type="email" class="form-control form-control-lg" :class="{ 'is-invalid': emailError }">
            <div class="invalid-feedback" v-if="emailError">
              <span>{{ emailError }}</span>
            </div>
          </div>
          <div class="form-group">
            <label class="form-control-label">Password</label>
            <input v-model="password" type="password" class="form-control form-control-lg" :class="{ 'is-invalid': passwordError }">
            <div class="invalid-feedback" v-if="passwordError">
              <span>{{ passwordError }}</span>
            </div>
          </div>
        </fieldset>
        <br>
        <div class="form-group">
          <button type="submit" class="btn btn-outline-info">Submit</button>
        </div>
      </form>
    </div>
    <div class="container">
      <small>
        Don't have an account? <RouterLink class="text-decoration-none" to="/register">Register</RouterLink>
      </small>
    </div>
  </template>
  
  <script>
  import { RouterLink } from 'vue-router';
  import { mapActions } from 'vuex';
  import { LOGIN_ACTION } from '../store/storeconstants';

  export default {
    data() {
      return {
        email: '',
        password: '',
        emailError: '',
        passwordError: '',
        serverError: '',
      };
    },
    methods: {
      ...mapActions('auth', {
        login: LOGIN_ACTION
      }),
      handleSubmit() {
        // Perform form submission logic here
        if (!this.email) {
          this.emailError = 'Email is required';
        } else {
          this.emailError = '';
        }
  
        if (!this.password) {
          this.passwordError = 'Password is required';
        } else {
          this.passwordError = '';
        }
  
        if (this.email && this.password) {
          this.login({ email: this.email, password: this.password })
            .then(() => {
              this.$router.push('/');
              location.reload();
            })
            .catch(error => {
              this.serverError = this.getErrorMessage(error.response.data.error.message);
          })
        }
      },
      getErrorMessage(error) {
        switch(error) {
          case "INVALID CREDENTIALS" : return "Invalid Credentials, Check Username or Password.";
          default: return "Unexpected error occurred. Please try again later.";
        }
      },
    },
    mounted() {
      if (localStorage.getItem('token') && localStorage.getItem('token').length > 0) {
        this.$router.push('/');
      }
    }
  };
  </script>
  
  <style scoped>
  .invalid-feedback {
    color: red;
  }
  </style>
  