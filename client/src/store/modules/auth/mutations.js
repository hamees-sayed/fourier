import { SET_USER_INFO_MUTATION, LOGIN_ACTION } from "../../storeconstants";

export default {
    [SET_USER_INFO_MUTATION](state, payload){
        state.username = payload.username;
        state.email = payload.email;
        state.id = payload.id;
    },
    [LOGIN_ACTION](state, payload){
        state.email = payload.email;
        state.id = payload.id;
    }
};