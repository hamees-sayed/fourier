<template>
    <div class="container">
      <form @submit.prevent="rateSong" class="needs-validation" novalidate>
        <fieldset class="form-group">
          <legend class="border-bottom mb-2">Rate Song</legend>
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
    };
  },
  methods: {
    rateSong() {
      axios.post(`https://miniature-space-trout-gv5pxqq6457cvj4w-5000.app.github.dev${this.$route.path}`, 
      { rating: this.selected },
      { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
      .then(() => {this.$router.push("/")})
    }
  }
};
</script>
