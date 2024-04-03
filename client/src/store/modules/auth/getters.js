import { GET_USER_TOKEN, IS_AUTHENTICATED } from "../../storeconstants";

export default {
    [GET_USER_TOKEN]: (state) => {
        return state.token;
    },

    [IS_AUTHENTICATED]: (state) => {
        return localStorage.getItem('token') !== null;
    }
};