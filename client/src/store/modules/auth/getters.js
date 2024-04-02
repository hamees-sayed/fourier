import { GET_USER_TOKEN } from "../../storeconstants";

export default {
    [GET_USER_TOKEN]: (state) => {
        return state.token;
    }
};