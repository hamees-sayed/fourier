<template>
    <div class="container">
      <!-- <h1>User: {{ currentUser.username }}</h1> -->
      <h3>Your Playlists</h3>
      <div class="buttons">
        <router-link to="#" class="btn btn-light border" role="button">Create a new Playlist</router-link>
      </div>
      <br>
      <br>
      <div v-if="data.length === 0">
        <h4>You haven't created any Playlists yet.</h4>
      </div>
      <div v-else>
        <div v-for="playlist in data" :key="playlist.id">
          <router-link to="#" style="text-decoration: none; color:#212529">
            <div class="card w-75">
              <div class="card-body">
                <h5 class="card-title mb-1">{{ playlist.playlist_name }}</h5>
                <p class="card-text mb-3">{{ playlist.playlist_desc }}</p>
                <router-link to="#" class="btn btn-primary mx-2">Update</router-link>
                <button class="btn btn-primary">Delete</button>
              </div>
            </div>
          </router-link>
          <br>
        </div>
      </div>
    </div>
  </template>

<script>
// import { mapState } from 'vuex';
// export default {
//     computed: {
//         ...mapState('auth', {
//             name: state => state.name
//         })
//     }
// }
import axios from 'axios';
import { mapGetters } from 'vuex';
import {GET_USER_TOKEN} from '../store/storeconstants';

export default {
    data () {
        return {
            data: []
        };
    },
    computed: {
        ...mapGetters('auth', {
            token: GET_USER_TOKEN
        })
    },
    mounted () {
        console.log(this.token)
        axios.get("https://psychic-space-giggle-xjwg96gg4pcv4vv-5000.app.github.dev/account", 
        { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
        .then(response => this.data = response.data)
    }
}
</script>