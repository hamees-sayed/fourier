import Axios from "axios";
import { REGISTER_ACTION, SET_USER_INFO_MUTATION, LOGIN_ACTION, REGISTER_CREATOR_ACTION, CREATE_PLAYLIST_ACTION } from "../../storeconstants";

export default {
    async [LOGIN_ACTION](context, payload){
        let postData = {
            email: payload.email,
            password: payload.password
        }
        let response = await Axios.post("https://miniature-space-trout-gv5pxqq6457cvj4w-5000.app.github.dev//login", postData);
        if (response.status === 201) {
            console.log(response.data);
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
        let response = await Axios.post("https://miniature-space-trout-gv5pxqq6457cvj4w-5000.app.github.dev//register", postData);
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
        let response = await Axios.post("https://miniature-space-trout-gv5pxqq6457cvj4w-5000.app.github.dev/register_creator", 
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
        let response = await Axios.post("https://miniature-space-trout-gv5pxqq6457cvj4w-5000.app.github.dev/playlist/new", 
        postData,
        { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } });
        if (response.status === 201) {
            console.log(response.data)
        }
    }
};