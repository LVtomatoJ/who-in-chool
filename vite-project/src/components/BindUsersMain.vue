<template>
  <el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="列表" name="list">
      <el-button type="primary" @click="getBinds" style="justify-content:flex-end">刷新</el-button>
      <el-table table-layout="auto" :data="store.Binds" border style="width: 100%;margin-top: 20px;"
        :row-class-name="tableRowClassName">
        <el-table-column type="index"></el-table-column>
        <el-table-column prop="bindid" label="用户id" width="auto" />
        <el-table-column prop="status" label="状态" width="auto">
          <template #default="scope">

            <div v-if="scope.row.status === 1">
              正常
            </div>
            <div v-else>
              失效
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="school" label="学校" />
        <el-table-column prop="notes" label="备注" width="auto" />
        <el-table-column fixed="right" label="操作" width="auto">
          <template #default="scope">
            <el-button link type="danger" size="small" @click="deleteBind(scope.$index)">
              删除
            </el-button>
            <el-button link type="success" size="small" @click="reBind(scope.$index)">
              刷新
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-tab-pane>
    <el-tab-pane label="添加绑定" name="add" style="text-align:center;">
      <el-form :label-position="labelPosition" style="width: 100%;" :model="form" label-width="100px" label-suffix=":">
        <el-form-item label="手机号">
          <el-input v-model="form.bindid"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input type="password" v-model="form.password" show-password></el-input>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.notes"></el-input>
        </el-form-item>
        <el-form-item>
          <!-- <el-button type="primary" @click="onSubmit">登录</el-button> -->
          <!-- <el-button type="primary" @click="onHello">Hello</el-button> -->
          <el-button type="primary" style="width: 70%" @click="onAddBindUser">添加</el-button>
        </el-form-item>
      </el-form>

    </el-tab-pane>
  </el-tabs>

</template>
<script lang="ts" setup>
import { onBeforeMount } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus'
import { ref, reactive } from 'vue'
import type { TabsPaneContext } from 'element-plus'
import axios from '../defaultaxios';
import { store } from '../store'

const activeName = ref('list')
const form = reactive({
  bindid: '',
  password: '',
  notes: '',
})
const labelPosition = ref('left')

interface Bind {

  status: number
  notes: string
  school: string
  bindid: string

}

const tableRowClassName = ({
  row,
  rowIndex,
}: {
  row: Bind
  rowIndex: number
}) => {
  if (row.status === 2) {
    return 'warning-row'
  } else if (row.status === 1) {
    return 'success-row'
  }
  return ''
}


// const binds = reactive<any[]>([]);

// const binds:any = store.Binds

onBeforeMount(() => {
  //   console.log(store.Authorization)
  // getBinds()
})

const handleClick = (tab: TabsPaneContext, event: Event) => {
  // console.log(tab, event)
}
const deleteBind = (index: number) => {
  axios({
    method: 'get',
    url: '/v2/delbind',
    headers: { Authorization: 'Bearer ' + store.Authorization },
    params: {
      bindid: store.Binds[index].bindid
    },
  }).then(function (response) {
    if (response.data['code'] == 0) {
      ElMessage({
        message: "删除成功",
        grouping: true,
        type: 'success',
      })
      store.Binds.splice(index, 1)
    } else {
      ElMessage({
        message: "删除失败," + response.data['msg'],
        grouping: true,
        type: 'error',
      })
    }
  })
  // binds.splice(index, 1)
}

const reBind = (index: number) => {
  axios({
    method: 'get',
    url: '/v2/rebind',
    headers: { Authorization: 'Bearer ' + store.Authorization },
    params: {
      bindid: store.Binds[index].bindid
    },
  }).then(function (response) {
    if (response.data['code'] == 0) {
      ElMessage({
        message: "刷新绑定成功",
        grouping: true,
        type: 'success',
      })
      // store.Binds.splice(index, 1)
    } else {
      ElMessage({
        message: "刷新失败," + response.data['msg'],
        grouping: true,
        type: 'error',
      })
    }
  })
  // binds.splice(index, 1)
}

const onAddBindUser = () => {
  console.log("start")
  axios({
    method: 'post', url: 'https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username',
    // headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    params: {
      username: form.bindid,
      password: form.password,
    },
  }).then(function (res) {
    const code = res.data.code
    if (code != 0) {
      ElMessage({
        message: res.data.message,
        grouping: true,
        type: 'error',
      })
    } else {
      ElMessage({
        message: "验证通过添加中...",
        grouping: true,
        type: 'success',
      })
      // 添加用户
      axios({
        method: 'get',
        url: '/v2/addbind',
        params: {
          bindid: form.bindid,
          password: form.password,
          notes: form.notes
        },
        headers: { Authorization: 'Bearer ' + store.Authorization }
      }).then(res => {

        const code = res.data.code
        if (code != 0) {
          ElMessage({
            message: res.data.msg,
            grouping: true,
            type: 'error',
          })
        } else {
          ElMessage({
            message: "添加成功",
            grouping: true,
            type: 'success',
          })
        }
      })
    }
  })
  console.log('end')
}

const getBinds = () => {
  axios({
    method: 'get',
    url: '/v2/getbinds',
    headers: { Authorization: 'Bearer ' + store.Authorization }
  }).then(function (response) {
    // console.log(typeof(response))
    // console.log(response)
    if (response) {
      store.Binds = response.data['data']['binds']
    } else {
      // router.replace('/login')
    }

    // UserInfo.email="123"
    // console.log(UserInfo)
  })
}
</script>

<style>
.el-table .warning-row {
  --el-table-tr-bg-color: var(--el-color-error-light-9);
}

.el-table .success-row {
  --el-table-tr-bg-color: var(--el-color-success-light-9);
}
</style>