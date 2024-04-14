<template>
    <div class="container">
      <form @submit.prevent="updateSong" enctype="multipart/form-data">
        <fieldset class="form-group">
          <legend class="border-bottom mb-2">Update Song</legend>
          <div class="form-group">
            <label class="form-control-label">Song Title:</label>
            <input v-model="formData.song_title" type="text" class="form-control form-control-lg" :class="{ 'is-invalid': formErrors.song_title }">
            <div class="invalid-feedback" v-if="formErrors.song_title">
              <span>{{ formErrors.song_title }}</span>
            </div>
          </div>
          <div class="form-group">
            <label class="form-control-label">Genre:</label>
            <input v-model="formData.genre" type="text" class="form-control form-control-lg" :class="{ 'is-invalid': formErrors.genre }">
            <div class="invalid-feedback" v-if="formErrors.genre">
              <span>{{ formErrors.genre }}</span>
            </div>
          </div>
          <div class="form-group">
            <label class="form-control-label">Lyrics:</label>
            <textarea v-model="formData.lyrics" class="form-control form-control-lg" :class="{ 'is-invalid': formErrors.lyrics }"></textarea>
            <div class="invalid-feedback" v-if="formErrors.lyrics">
              <span>{{ formErrors.lyrics }}</span>
            </div>
          </div>
          <div class="form-group">
            <label class="form-control-label">Albums:</label>
            <select v-model="formData.album_id" class="form-control" :class="{ 'is-invalid': formErrors.album }">
                <option v-for="album in albums" :key="album.id" :value="album.id">{{ album.title }}</option>
            </select>
            <div class="invalid-feedback" v-if="formErrors.album">
              <span>{{ formErrors.album }}</span>
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
    import axios from 'axios';
    import { mapActions } from 'vuex';
    import { UPDATE_SONG_ACTION } from '../store/storeconstants';
    
    export default {
        data() {
          return {
            formData: {
              song_title: '',
              genre: '',
              lyrics: '',
              album_id: 0
            },
            formErrors: {},
            albums: [],
          };
        },
        methods: {
            ...mapActions('auth', {
                update_song_action: UPDATE_SONG_ACTION
            }),
            updateSong() {
                // Perform form validation
                this.formErrors = {};
        
                if (!this.formData.song_title.trim()) {
                    this.formErrors.song_title = 'Song Title is required';
                }
        
                if (!this.formData.genre.trim()) {
                    this.formErrors.genre = 'Genre is required';
                }
        
                if (this.formData.album_id === 0) {
                    this.formErrors.album = 'Album is required';
                }
        
                if (Object.keys(this.formErrors).length === 0) {
                    this.update_song_action({ title: this.formData.song_title, genre: this.formData.genre, lyrics: this.formData.lyrics, album_id: this.formData.album_id, song_id: parseInt(this.$route.params.id) })
                    .then(() => this.$router.push('/creator/songs'));
                }
            }
        },
        mounted() {
          axios.get(`${import.meta.env.VITE_SERVER_URL}/song`, 
          { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
          .then(response => {
              const song = response.data.find(song => song.id === parseInt(this.$route.params.id));
              this.formData.song_title = song.title;
              this.formData.genre = song.genre;
              this.formData.lyrics = song.lyrics;
              this.formData.album_id = song.album_id});
              
          axios.get(`${import.meta.env.VITE_SERVER_URL}/album`, 
          { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
          .then(response => {
            this.albums = [{id: 0, title: "Release as Single", genre: "None"}, ...response.data];
          });
        },
    }
</script>
  