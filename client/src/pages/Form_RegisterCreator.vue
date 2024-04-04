<template>
    <div class="container">
        <div v-if="serverError" class="alert alert-danger">
            {{ serverError }}
        </div>
      <form @submit.prevent="handleSubmit">
        <fieldset class="form-group">
          <legend class="border-bottom mb-2">Register as creator</legend>
          <div class="form-group">
            <label class="form-control-label">Creator Name/Username: </label>
            <input v-model="username" type="text" class="form-control form-control-lg" :class="{ 'is-invalid': serverError }">
            <div v-if="username" class="invalid-feedback">
              <span>{{ username }}</span>
            </div>
          </div>
        </fieldset>
        <br>
        <div class="form-group">
          <button type="submit" class="btn btn-outline-info">Submit</button>
        </div>
      </form>
    </div>
  </template>


<script>
  import { mapActions } from 'vuex';
  import { REGISTER_CREATOR_ACTION } from '../store/storeconstants';
  
  export default {
    data() {
      return {
        username: localStorage.getItem("username"),
        serverError: ''
      };
    },
    methods: {
      ...mapActions('auth', {
        register: REGISTER_CREATOR_ACTION
      }),
      handleSubmit() {
        if (!this.username) {
          this.usernameError = 'Username is required';
        } else {
          this.usernameError = localStorage.getItem("username");
        }
  
        if (this.username) {
          this.register({ username: this.username })
            .then(() => {this.$router.push('/account');})
        }
      },
    },
    mounted(){
        if (localStorage.getItem('is_creator')==='true') {
            this.$router.push('/account');
        }
    }
  };
</script>