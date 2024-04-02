<template>
    Home Page 
    <br>
    
</template>

<script>
// import { mapState } from 'vuex';
// export default {
//     computed: {
//         ...mapState('auth', {
//             name: state => state.name
//         })
//     }
// }
import axios from 'axios';
import { mapGetters } from 'vuex';
import {GET_USER_TOKEN} from '../store/storeconstants';

export default {
    data () {
        return;
    },
    computed: {
        ...mapGetters('auth', {
            token: GET_USER_TOKEN
        })
    },
    mounted () {
        axios.get("https://psychic-space-giggle-xjwg96gg4pcv4vv-5000.app.github.dev/account", 
        { headers: { Authorization: `Bearer ${this.token}` } })
        .then(response => console.log(response))
    }
}
</script>