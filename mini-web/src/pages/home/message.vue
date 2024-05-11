<template>
<div>
  <v-infinite-scroll mode="manual" :height="scrollHeight" :items="messageList" :onLoad="load">
    <v-list lines="two">
      <template v-for="(item, index) in messageList" :key="index">
        <v-list-item>
          <v-list-item-content>
              <v-list-item-title style="white-space:normal;display: -webkit-box;-webkit-line-clamp: 2;-webkit-box-orient: vertical;" >{{ item.content }}</v-list-item-title>
              <v-list-item-subtitle>
                 {{ item.user.nick_name }}
                 <div>
                    <!-- 时间戳转string -->
                  {{ new Date(item.send_time * 1000).toLocaleString() }}
                 </div>
              </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </template>
    </v-list>
  </v-infinite-scroll>
  <v-text-field
    v-model="message"
    label="我也要留言！"
    hide-details
    append-icon="mdi-send"
    @click:append="sendMessage"
    type="text"
    variant="filled"
  >
</v-text-field>

</div>

<UserFooter  page-value='message'/>
</template>

<script setup>
import {ref,onMounted} from 'vue';
import { useRouter} from 'vue-router';
import { publishMessageAPI , getMessageListAPI } from '@/request/api/message'
const message = ref('')
const scrollHeight = ref(0)

const router = useRouter()
const sending = ref(false)

onMounted(()=>{
  scrollHeight.value = window.innerHeight-56-56
})

const messageList = ref([])


const page = ref(1)

async function load({ done }) {
  const {data,error} = await getMessageListAPI(page.value,10)
  if (error.value != null) {
    done('error')
  }else{
    messageList.value = messageList.value.concat(data.value.data)
    if (data.value.data.length === 0) {
      done('empty')
    }else{
      page.value += 1
      done('ok')
    }
  }
}

const sendMessage = async()=>{
  console.log(message.value)
  const { data, error } = await publishMessageAPI(message.value)
  message.value = ''
  if (error.value != null) {
    console.log('出错啦',error.value)
  }else{
    messageList.value = [data.value].concat(messageList.value)
  }
}


</script>


<route lang="yaml">
    meta:
      layout: home
</route>