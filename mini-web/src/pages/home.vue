<template>
    <v-card
    class="mx-auto"
    max-width="300"
  >
    <v-list>
        <v-list-item @click="goSignListPage">
            签到消息
        </v-list-item>
    </v-list>
  </v-card>
</template>

<script setup>

import { useAppStore } from '@/stores/app';
import { useRouter } from 'vue-router';

const router = useRouter();

const appStore = useAppStore();

const goSignListPage = () => {
    router.push('/signList')
}

</script>