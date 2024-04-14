import Axios from "axios";
import { REGISTER_ACTION, SET_USER_INFO_MUTATION, LOGIN_ACTION, REGISTER_CREATOR_ACTION, CREATE_PLAYLIST_ACTION, UPDATE_PLAYLIST_ACTION, ADD_SONG_TO_PLAYLIST_ACTION, CREATE_NEW_ALBUM_ACTION, UPDATE_ALBUM_ACTION, CREATE_NEW_SONG_ACTION, UPDATE_SONG_ACTION } from "../../storeconstants";

export default {
    async [LOGIN_ACTION](context, payload){
        let postData = {
            email: payload.email,
            password: payload.password
        }
        let response = await Axios.post(`${import.meta.env.VITE_SERVER_URL}/login`, postData);
        if (response.status === 201) {
            localStorage.setItem("token", response.data.token);
            localStorage.setItem("username", response.data.username);
            localStorage.setItem("is_admin", response.data.is_admin);
            localStorage.setItem("is_creator", response.data.is_creator);
            context.commit(LOGIN_ACTION, {
                name: response.data.username,
                is_admin: response.data.is_admin,
                is_creator: response.data.is_creator,
                email: response.data.email,
                id: response.data.user_id,
                token: response.data.token,
            })
        }
    },
    async [REGISTER_ACTION](context, payload){
        let postData = {
            username: payload.username,
            email: payload.email,
            password: payload.password
        }
        let response = await Axios.post(`${import.meta.env.VITE_SERVER_URL}/register`, postData);
        if (response.status === 200) {
            context.commit(SET_USER_INFO_MUTATION, {
                name: response.data.username,
                is_admin: response.data.is_admin,
                is_creator: response.data.is_creator,
                email: response.data.email,
                id: response.data.user_id,
                token: response.data.token,
            })
        }
    },
    async [REGISTER_CREATOR_ACTION](_, payload){
        let postData = {
            username: payload.username,
        }
        let response = await Axios.post(`${import.meta.env.VITE_SERVER_URL}/register_creator`, 
        postData,
        { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } });
        if (response.status === 201) {
            localStorage.setItem("username", response.data.username);
            localStorage.setItem("is_creator", response.data.is_creator);
            location.reload();
        }
    },
    async [CREATE_PLAYLIST_ACTION](_, payload){
        let postData = {
            playlist_name: payload.playlist_name,
            playlist_desc: payload.playlist_desc
        }
        let response = await Axios.post(`${import.meta.env.VITE_SERVER_URL}/playlist/new`, 
        postData,
        { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } });
        if (response.status === 201) {
            console.log(response.data)
        }
    },
    async [UPDATE_PLAYLIST_ACTION](_, payload){
        let postData = {
            playlist_name: payload.playlist_name,
            playlist_desc: payload.playlist_desc
        }
        let response = await Axios.post(`${import.meta.env.VITE_SERVER_URL}/playlist/${payload.playlist_id}/update`, 
        postData,
        { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } });
        if (response.status === 201) {
            console.log(response.data)
        }
    },
    async [ADD_SONG_TO_PLAYLIST_ACTION](_, payload){
        let postData = {
            playlist_id: payload.playlist_id,
        }
        let response = await Axios.post(`${import.meta.env.VITE_SERVER_URL}/playlist/add/${payload.song_id}`, 
        postData,
        { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } });
        if (response.status === 201) {
            console.log(response.data)
        }
    },
    async [CREATE_NEW_ALBUM_ACTION](_, payload){
        let postData = {
            album_name: payload.title,
            album_genre: payload.genre
        }
        let response = await Axios.post(`${import.meta.env.VITE_SERVER_URL}/album/new`,
        postData,
        {headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } });
    },
    async [UPDATE_ALBUM_ACTION](_, payload){
        let postData = {
            album_name: payload.title,
            album_genre: payload.genre
        }
        let response = await Axios.post(`${import.meta.env.VITE_SERVER_URL}/album/${payload.album_id}/update`,
        postData,
        {headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } });
    },
    async [CREATE_NEW_SONG_ACTION](_, payload){
        let postData = {
            song_title: payload.title,
            song_genre: payload.genre,
            album_id: payload.album_id,
            lyrics: payload.lyrics,
            song_file: payload.song_file,
        }
        let response = await Axios.post(`${import.meta.env.VITE_SERVER_URL}/song/new`,
        postData,
        {headers: { Authorization: `Bearer ${localStorage.getItem("token")}`, 'Content-Type': 'multipart/form-data' } });
    },
    async [UPDATE_SONG_ACTION](_, payload){
        let postData = {
            song_title: payload.title,
            song_genre: payload.genre,
            album_id: payload.album_id,
            song_lyrics: payload.lyrics,
        }
        let response = await Axios.post(`${import.meta.env.VITE_SERVER_URL}/song/${payload.song_id}/update`,
        postData,
        {headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } });
    }
};