import Axios from "axios";
import { REGISTER_ACTION, SET_USER_INFO_MUTATION, LOGIN_ACTION } from "../../storeconstants";

export default {
    async [LOGIN_ACTION](context, payload){
        let postData = {
            email: payload.email,
            password: payload.password
        }
        let response = await Axios.post("https://didactic-halibut-jp4gr5597x4cvr7-5000.app.github.dev/login", postData);
        if (response.status === 200) {
            context.commit(LOGIN_ACTION, {
                email: response.data.email,
                id: response.data.id,
            })
        }
    },
    async [REGISTER_ACTION](context, payload){
        let postData = {
            username: payload.username,
            email: payload.email,
            password: payload.password
        }
        let response = await Axios.post("https://didactic-halibut-jp4gr5597x4cvr7-5000.app.github.dev/register", postData);
        if (response.status === 200) {
            context.commit(SET_USER_INFO_MUTATION, {
                name: response.data.name,
                email: response.data.email,
                id: response.data.id,
            })
        }
    },
};