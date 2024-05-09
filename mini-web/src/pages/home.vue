<template>
    <v-list :items="functionList">
      <v-list-subheader>功能</v-list-subheader>
      <v-list-item title='签到' @click="goSignListPage">
              <template v-slot:prepend>
                <v-icon icon="mdi-clock"></v-icon>
              </template>
      </v-list-item>
    </v-list>
</template>

<script setup>

import { useAppStore } from '@/stores/app';
import { useRouter } from 'vue-router';

const router = useRouter();

const appStore = useAppStore();

const functionList = ref([
          {
          title: '签到',
          value: 1,
          props: {
            prependIcon: 'mdi-clock',
          }}
        ])

const goSignListPage = () => {
  router.push('/signList')
}

</script>