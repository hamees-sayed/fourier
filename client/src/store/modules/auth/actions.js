import Axios from "axios";
import { REGISTER_ACTION, SET_USER_INFO_MUTATION, LOGIN_ACTION } from "../../storeconstants";

export default {
    async [LOGIN_ACTION](context, payload){
        let postData = {
            email: payload.email,
            password: payload.password
        }
        let response = await Axios.post("https://psychic-space-giggle-xjwg96gg4pcv4vv-5000.app.github.dev/login", postData);
        if (response.status === 201) {
            console.log(response.data);
            localStorage.setItem("token", response.data.token);
            context.commit(LOGIN_ACTION, {
                name: response.data.username,
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
        let response = await Axios.post("https://psychic-space-giggle-xjwg96gg4pcv4vv-5000.app.github.dev/register", postData);
        if (response.status === 200) {
            context.commit(SET_USER_INFO_MUTATION, {
                name: response.data.username,
                email: response.data.email,
                id: response.data.user_id,
                token: response.data.token,
            })
        }
    },
};