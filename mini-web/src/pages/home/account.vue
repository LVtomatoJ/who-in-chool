
<template>
    <v-list>
        <v-list-item>
            <v-list-item-content>
                <v-list-item-title>
                    昵称
                </v-list-item-title>
            </v-list-item-content>
            <template v-slot:append>
                <v-btn text @click="dialog=true">
                    {{ nick_name?nick_name:'未设置' }}
                </v-btn>
            </template>
        </v-list-item>
    </v-list>
        <v-dialog
      v-model="dialog"
      width="auto"
    >
      <v-card
        min-width="300"
        prepend-icon="mdi-update"
        title="修改昵称"
      >
      <v-card-text>
        <v-text-field
          v-model="nick_name"
          label="新昵称"
          required
        ></v-text-field>
      </v-card-text>
        <template v-slot:actions>
          <v-btn
            class="ms-auto"
            text="确定"
            @click="updateName()"
          ></v-btn>
        </template>
      </v-card>
    </v-dialog>
<UserFooter  page-value='account'/>

</template>

<script setup>

import {ref,onMounted} from 'vue'
import { updateNickNameAPI,getUserInfoAPI } from '@/request/api/user'

const dialog = ref(false)
const nick_name = ref('')

const initUseInfo = async()=>{
    const {data,error} = await getUserInfoAPI()
    if(error.value!=null){
        console.log('出错啦',error.value)
    }else{
        nick_name.value = data.value.nick_name
    }
}

onMounted(()=>{
    initUseInfo()
})

const updateName = async() => {
  const {data,error} = await updateNickNameAPI(nick_name.value)
    dialog.value = false
  if(error.value!=null){
    console.log('出错啦',error.value)
  }else{
    console.log('修改成功',data.value)
  }
}

</script>