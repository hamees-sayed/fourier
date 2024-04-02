<template>
  <Navbar />
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <div>
          <router-view></router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import Navbar from './components/Navbar.vue';
  export default {
    name: 'App',
    components: {
      Navbar
    },
  }
</script>
