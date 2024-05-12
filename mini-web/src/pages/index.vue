<template>
  <!-- <HelloWorld /> -->
   <v-card
   style="margin-top: 40px;"
   prepend-icon="mdi-account"
     
        subtitle="剔除臃肿 极简便利"
        text="去除所有不必要的功能 即签即用！"
        title="你在校园"
      >
    <template v-slot:append>
      <div @click="goLoginPage">
        立即登录
          <v-icon icon="mdi-chevron-right"></v-icon>
      </div>
        </template>
    </v-card>

        <v-card
      style="margin-top: 40px;"
        subtitle=""
        title="教程"
      >
      <template #text>
        <!-- 下面做一步一步的教程 -->
        <v-list lines="two">

          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                1. 登录
              </v-list-item-title>
              <v-list-item-subtitle>
                输入你的手机号和密码，然后点击登录 密码错误请在忘记密码里修改哦
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
            <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                2. 选择功能
              </v-list-item-title>
              <v-list-item-subtitle>
                目前只有签到啦
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                3. 进行签到
              </v-list-item-title>
              <v-list-item-subtitle>
                地图选点签到！我说在哪就在哪！
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                4. 反馈
              </v-list-item-title>
              <v-list-item-subtitle>
                有任何问题可以在留言里留下问题哦（留言板块是本校可见！
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </template>
    </v-card>
      <v-btn  @click="goLoginPage" block>立即体验</v-btn>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter()
const goLoginPage = () => {
  router.push('/login')
}
</script>
