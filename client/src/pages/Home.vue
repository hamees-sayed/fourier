<template>
  <div class="container vertical-center d-flex flex-column align-items-center" v-if="!isAuthenticated">
    <img src="../assets/logo.png" width="300" height="190" />
    <h3>Dive into the world of Music today.</h3>
    <div class="buttons">
      <router-link to="/register" class="btn btn-light border mx-2" role="button">Register</router-link>
      <router-link to="/login" class="btn btn-light border" role="button">Login</router-link>
    </div>
  </div>
  <div v-if="isAuthenticated">
    Logged In Welcome
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { IS_AUTHENTICATED } from '../store/storeconstants';

export default {
  computed: {
    ...mapGetters('auth', {
      isAuthenticated: IS_AUTHENTICATED,
    })
  }
};

</script>