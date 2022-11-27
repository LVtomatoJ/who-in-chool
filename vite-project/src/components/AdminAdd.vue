<template>
  <el-form label-width="120px" label-position="right" label-suffix=":">
    <el-form-item label="添加类型">
      <el-select v-model="addtype">
        <el-option label="模板" value="template" />
        <el-option label="公告" value="notic" />
      </el-select>
    </el-form-item>
    <block v-if="addtype == 'notic'">
      <el-form-item label="noticid">
        <el-input v-model="noticform.noticid" />
      </el-form-item>
      <el-form-item label="title">
        <el-input v-model="noticform.title" />
      </el-form-item>
      <el-form-item label="time">
        <el-input v-model="noticform.time" />
      </el-form-item>
      <el-form-item label="show">
        <el-input v-model="noticform.show" />
      </el-form-item>
      <el-form-item label="content">
        <el-input v-model="noticform.content" />
      </el-form-item>
      <el-form-item>
        <el-button size="small" @click="addNotic">添加</el-button>
      </el-form-item>
    </block>
  </el-form>
</template>


<script lang="ts" setup>
import { ElMessage } from 'element-plus';
import { ref, reactive } from 'vue'
import axios from '../defaultaxios';
import { store } from '../store';

const addtype = ref()

const noticform = reactive({
  title: '',
  content: '',
  time: '',
  show: 0,
  noticid: '',
})

const addNotic = () => {
  const title = noticform.title
  const content = noticform.content
  const time = noticform.time
  const show = noticform.show
  const noticid = noticform.noticid
  axios({
    method: 'get',
    url: '/v2/admin/addnotic',
    headers: { Authorization: 'Bearer ' + store.Authorization },
    params: {
      title: title, content: content, time: time, show: show, noticid: noticid
    },
  }).then(function (response) {
    if (response.data['code'] == 0) {
      ElMessage({
        message: "添加成功",
        grouping: true,
        type: 'success',
      })
    } else {
      ElMessage({
        message: "添加失败：," + response.data['msg'],
        grouping: true,
        type: 'error',
      })
    }
  })
}

</script>