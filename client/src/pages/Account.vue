<template>
    <div class="container">
      <h1>Welcome, {{ username }}</h1>
      <h3>Your Playlists</h3>
      <div class="buttons">
        <router-link to="/playlist/new" class="btn btn-light border" role="button">Create a new Playlist</router-link>
      </div>
      <br>
      <br>
      <div v-if="data.length === 0">
        <h4>You haven't created any Playlists yet.</h4>
      </div>
      <div v-else>
        <div v-for="playlist in data" :key="playlist.id">
          <router-link :to="'/playlist/'+playlist.id" style="text-decoration: none; color:#212529">
            <div class="card w-75">
              <div class="card-body">
                <h5 class="card-title mb-1">{{ playlist.playlist_name }}</h5>
                <p class="card-text mb-3">{{ playlist.playlist_desc }}</p>
                <router-link :to="'/playlist/update/'+playlist.id" class="btn btn-primary mx-2">Update</router-link>
                <div @click.stop.prevent="deletePlaylist(playlist.id)" class="btn btn-primary">Delete</div>
              </div>
            </div>
          </router-link>
          <br>
        </div>
      </div>
    </div>
  </template>

<script>

import axios from 'axios';
import { mapGetters } from 'vuex';
import {GET_USER_TOKEN} from '../store/storeconstants';

export default {
    data () {
        return {
            data: [],
            username: '',
        };
    },
    computed: {
        ...mapGetters('auth', {
            token: GET_USER_TOKEN
        }),
    },
    mounted () {
        this.username = localStorage.getItem("username");
        axios.get(`${import.meta.env.VITE_SERVER_URL}/account`, 
        { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
        .then(response => {
          this.data = response.data
          console.log(response.data)
        })
    },
    methods: {
      deletePlaylist(id){
        axios.get(`${import.meta.env.VITE_SERVER_URL}/playlist/${id}/delete`,
        { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
        .then(() => {
          location.reload();
        })
      }
    }
}
</script>