<template>
    <div class="container">
      <form @submit.prevent="rateSong" class="needs-validation" novalidate>
        <fieldset class="form-group">
          <legend class="border-bottom mb-2">Rate Song</legend>
          <div v-if="serverError" class="alert alert-danger">
            {{ serverError }}
          </div>
          <div class="form-group">
            <br>
            <select v-model="selected">
                <option>1</option>
                <option>2</option>
                <option>3</option>
                <option>4</option>
                <option>5</option>
            </select>
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
import axios from 'axios';

export default {
  data() {
    return {
      selected: 1,
      serverError: '',
    };
  },
  methods: {
    rateSong() {
      axios.post(`${import.meta.env.VITE_SERVER_URL}${this.$route.path}`, 
      { rating: this.selected },
      { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
      .then(() => {
              this.$router.push('/');
            })
            .catch(error => {
              this.serverError = this.getErrorMessage(error.response.data.error.message);
          })
    },
    getErrorMessage(error) {
        switch(error) {
          case "ALREADY RATED" : return "Already Rated.";
          default: return "Unexpected error occurred. Please try again later.";
        }
    },
  }
};
</script>

  <style scoped>
  .invalid-feedback {
    color: red;
  }
  </style>