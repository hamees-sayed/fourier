import { GET_USER_TOKEN, IS_AUTHENTICATED, IS_CREATOR, IS_ADMIN } from "../../storeconstants";

export default {
    [GET_USER_TOKEN]: (state) => {
        return state.token;
    },

    [IS_AUTHENTICATED]: () => {
        return localStorage.getItem('token') !== null;
    },
    
    [IS_CREATOR]: () => {
        return localStorage.getItem("is_creator")==='true';
    },
    
    [IS_ADMIN]: () => {
        return localStorage.getItem("is_admin")==='true';
    }
};