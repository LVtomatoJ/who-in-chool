<template>
    hello index
</template>

<script lang="ts" setup>
import {store} from '../store'
import axios from 'axios'
const Authorization = store.Authorization
const getdata = ()=>{
    axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/v2/getuserinfo',
        headers: { Authorization: 'Bearer ' + store.Authorization }
    }).then(function (response) {
        console.log(response.data)
    })
}
    
</script>