<template>
    <div class="container">
      <form @submit.prevent="handleSubmit">
        <fieldset class="form-group">
          <legend class="border-bottom mb-2">Create a new Account</legend>
          <div v-if="serverError" class="alert alert-danger">
            {{ serverError }}
          </div>
          <div class="form-group">
            <label class="form-control-label">Username</label>
            <input v-model="username" type="text" class="form-control form-control-lg" :class="{ 'is-invalid': usernameError }">
            <div class="invalid-feedback" v-if="usernameError">
              <span>{{ usernameError }}</span>
            </div>
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
          <div class="form-group">
            <label class="form-control-label">Confirm Password</label>
            <input v-model="confirmPassword" type="password" class="form-control form-control-lg" :class="{ 'is-invalid': confirmPasswordError }">
            <div class="invalid-feedback" v-if="confirmPasswordError">
              <span>{{ confirmPasswordError }}</span>
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
        Have an account? <a class="text-decoration-none" href="{{ url_for('login') }}">Login</a>
      </small>
    </div>
  </template>
  
  <script>
  import { mapActions } from 'vuex';
  import { REGISTER_ACTION } from '../store/storeconstants';
  export default {
    data() {
      return {
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        usernameError: '',
        emailError: '',
        passwordError: '',
        confirmPasswordError: '',
        serverError: '',
      };
    },
    methods: {
      ...mapActions('auth', {
        register: REGISTER_ACTION
      }),
      handleSubmit() {
        // Perform form submission logic here
        if (!this.username) {
          this.usernameError = 'Username is required';
        } else {
          this.usernameError = '';
        }
  
        if (!this.email) {
          this.emailError = 'Email is required';
        } else if (!this.isValidEmail(this.email)) {
          this.emailError = 'Invalid email format';
        } else {
          this.emailError = '';
        }
  
        if (!this.password) {
          this.passwordError = 'Password is required';
        } else {
          this.passwordError = '';
        }
  
        if (this.password !== this.confirmPassword) {
          this.confirmPasswordError = 'Passwords do not match';
        } else {
          this.confirmPasswordError = '';
        }
  
        if (this.username && this.email && this.password && this.password === this.confirmPassword) {
          this.register({ username: this.username, email: this.email, password: this.password })
            .then(() => {this.$router.push('/login')})
            .catch(error => {
              this.serverError = this.getErrorMessage(error.response.data.error.message);
          })
        }
      },
      isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
      },
      getErrorMessage(error) {
        switch(error) {
          case "USER ALREADY EXISTS" : return "User already exists, change Username or Email.";
          default: return "Unexpected error occurred. Please try again later.";
        }
      },
    },
  };
</script>
  
  <style scoped>
  .invalid-feedback {
    color: red;
  }
  </style>
  