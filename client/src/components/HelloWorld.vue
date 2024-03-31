<script setup>
import { ref } from 'vue'

defineProps({
  msg: String,
})

const count = ref(0)
let api = ref(null)

fetch("https://didactic-halibut-jp4gr5597x4cvr7-5000.app.github.dev/abc")
  .then(response => response.json())
  .then(data => api.value = data)
  
</script>

<template>
  <h1>{{ api.message }}</h1>
  

  <div class="card">
    <button type="button" @click="count++">count is {{ count }}</button>
    <p>
      Edit
      <code>components/HelloWorld.vue</code> to test HMR
    </p>
  </div>

  <p>
    Check out
    <a href="https://vuejs.org/guide/quick-start.html#local" target="_blank"
      >create-vue</a
    >, the official Vue + Vite starter
  </p>
  <p>
    Install
    <a href="https://github.com/vuejs/language-tools" target="_blank">Volar</a>
    in your IDE for a better DX
  </p>
  <p class="read-the-docs">Click on the Vite and Vue logos to learn more</p>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
