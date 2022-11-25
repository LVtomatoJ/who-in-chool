<template>
  <el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="列表" name="list">
      <el-button type="primary" @click="getWorks" style="justify-content:flex-end">刷新</el-button>
      <el-table table-layout="auto" :data="store.Works" border style="width: 100%;margin-top: 20px;"
        :row-class-name="tableRowClassName">
        <el-table-column type="index" />
        <el-table-column prop="workid" label="任务id" />
        <el-table-column label="状态">
          <!-- <template #default="scope">
 
          </template> -->
          <template #default="scope">

            <div v-if="scope.row.status === 1">
              运行
            </div>
            <div v-else>
              暂停
            </div>
          </template>


        </el-table-column>
        <el-table-column prop="bindid" label="绑定用户id" />
        <el-table-column prop="starttime" label="开始时间" />
        <el-table-column prop="endtime" label="结束时间" />

        <el-table-column fixed="right" label="操作" width="auto">
          <template #default="scope">
            <!-- <el-button link type="primary" size="small" @click="testeWork(scope.row)">
              test
            </el-button> -->
            <div style="display: flex; align-items: center">
              <el-button link type="warning" size="small" v-if="scope.row.status === 1"
                @click="stopWork(scope.row.workid)">
                暂停
              </el-button>
              <el-button link type="primary" size="small" v-else @click="runWork(scope.row.workid)">
                运行
              </el-button>
              <el-button link type="danger" size="small" @click="deleteWork(scope.row.workid)">
                删除
              </el-button>
            </div>
          </template>
        </el-table-column>

      </el-table>
    </el-tab-pane>
    <el-tab-pane label="添加任务" name="add">


      <el-form :label-position="labelPosition" :model="form" label-width="100px" style="margin-top:20px">
        <el-form-item label="任务账号">
          <el-select v-model="form.bindid" placeholder="选择任务账号">
            <template v-for="bind in store.Binds">
              <el-option v-bind:label="bind['bindid']" v-bind:value="bind['bindid']" />

            </template>

          </el-select>
        </el-form-item>
        <el-form-item label="任务类型">

          <el-radio-group v-model="form.type" @change="typeChange">
            <el-radio border label='1'>立即执行</el-radio>
            <el-radio border label='2'>每日执行</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="任务开始时间" v-if="showTimeSet">
          <!-- <el-time-select @change="timeChange"
      v-model="form.time"
      start="01:00"
      setp="00:15"
      end="23:30"
      placeholder="选择每日任务执行时间"
    /> -->
          <!-- <el-time-picker @change="timeChange" v-model="form.time" placeholder="选择每日任务执行时间" /> -->
          <el-date-picker v-model="form.starttime" type="datetime" placeholder="Pick a Date"
            format="YYYY/MM/DD HH:mm:ss" value-format="YYYY-MM-DD HH:m:s" @change="timeChange" />
        </el-form-item>
        <el-form-item label="任务结束时间" v-if="showTimeSet">
          <!-- <el-time-select @change="timeChange"
      v-model="form.time"
      start="01:00"
      setp="00:15"
      end="23:30"
      placeholder="选择每日任务执行时间"
    /> -->
          <!-- <el-time-picker @change="timeChange" v-model="form.time" placeholder="选择每日任务执行时间" /> -->
          <el-date-picker v-model="form.endtime" type="datetime" placeholder="Pick a Date" format="YYYY/MM/DD hh:mm:ss"
            value-format="YYYY-MM-DD hh:m:s" @change="timeChange" />
        </el-form-item>
        <el-form-item label="任务模板">
          <el-select v-model="form.templateid" clearable placeholder="Select">

            <el-option v-for="template in templates" :key="template.templateid" :label="template.name"
              :value="template.templateid" :disabled="template.type != 1 ? true : false" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onAddWork">添加/执行任务</el-button>
        </el-form-item>
      </el-form>


    </el-tab-pane>
    <el-tab-pane label="任务日志" name="log">
      <el-button type="primary" @click="getWorkLogs" style="justify-content:flex-end">刷新</el-button>
      <el-table table-layout="auto" :data="store.WorkLogs" border style="width: 100%;margin-top: 20px;"
        :row-class-name="logtableRowClassName">
        <el-table-column type="index" />
        <el-table-column prop="time" label="运行时间" />
        <el-table-column prop="bindid" label="绑定" />
        <el-table-column prop="msg" label="提示" />
        <el-table-column prop="workid" label="任务id" />
        <el-table-column prop="code" label="返回码"  width="auto"/>

      </el-table>
    </el-tab-pane>
    <el-tab-pane label="签到" name="sign">
      <el-form :label-position="labelPosition" :model="form" label-width="100px" style="margin-top:20px">
        <el-form-item label="任务账号">
          <el-select v-model="form.bindid" placeholder="选择任务账号">
            <template v-for="bind in store.Binds">
              <el-option v-bind:label="bind['bindid']" v-bind:value="bind['bindid']" />
            </template>

          </el-select>
        </el-form-item>
        <el-form-item label="任务类型">

          <el-radio-group v-model="form.type" @change="typeChange">
            <el-radio border label='1'>立即执行</el-radio>
            <el-radio border label='2' :disabled="true">每周执行</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="任务开始时间" v-if="showTimeSet">
          <el-date-picker v-model="form.starttime" type="datetime" placeholder="Pick a Date"
            format="YYYY/MM/DD HH:mm:ss" value-format="YYYY-MM-DD HH:m:s" @change="timeChange" />
        </el-form-item>
        <el-form-item label="任务结束时间" v-if="showTimeSet">
          <el-date-picker v-model="form.endtime" type="datetime" placeholder="Pick a Date" format="YYYY/MM/DD hh:mm:ss"
            value-format="YYYY-MM-DD hh:m:s" @change="timeChange" />
        </el-form-item>
        <el-form-item label="任务模板">
          <el-select v-model="form.templateid" clearable placeholder="Select">

            <el-option v-for="template in templates" :key="template.templateid" :label="template.name"
              :value="template.templateid" :disabled="template.type != 2 ? true : false" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onAddSignWork">添加/执行任务</el-button>
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

const labelPosition = ref('left')

const activeName = ref('list')
const form = reactive({
  bindid: '',
  type: '1',
  starttime: "",
  endtime: '',
  templateid: ''
})
const templates = reactive<any[]>([]);
const showTimeSet = ref(false)
const handleClick = (tab: TabsPaneContext, event: Event) => {
  form.templateid = ""
  console.log("123")
  // console.log(tab, event)
}
const typeChange = (value: any) => {
  // console.log('change')
  if (value == 1) {
    showTimeSet.value = false
  } else {
    showTimeSet.value = true
  }
  // console.log(value)
}
const timeChange = (value: any) => {
  console.log("time:")
  console.log(value)
}
// const works = reactive<any[]>([]);
onBeforeMount(() => {
  //   console.log(store.Authorization)
  // getWorks()
  // console.log("worktest:")
  // console.log(store.Binds)
  getTemplates()
  getWorks()
})

const testeWork = (rr: any) => {
  console.log(rr)
  if (rr['status'] === 1) {
    return true
  } else {
    return false
  }
}

interface Work {

  workid: string
  status: number
  starttime: string
  endtime: string
  bindid: string

}
interface Log {

time: string
code: number
workid: string
msg: string
bindid: string

}


const tableRowClassName = ({
  row,
  rowIndex,
}: {
  row: Work
  rowIndex: number
}) => {
  // console.log(row.status=="出错暂停")
  if (row.status === 2) {
    return 'warning-row'
  } else if (row.status === 1) {
    return 'success-row'
  }
  return ''
}

const logtableRowClassName = ({
  row,
  rowIndex,
}: {
  row: Log
  rowIndex: number
}) => {
  // console.log(row.status=="出错暂停")
  if (row.code != 0) {
    return 'warning-row'
  } else if (row.code === 0) {
    return 'success-row'
  }
  return ''
}

const getTemplates = () => {
  axios({
    method: 'get',
    url: '/v2/gettemplates',
    headers: { Authorization: 'Bearer ' + store.Authorization }
  }).then(function (response) {
    // console.log(typeof(response))
    // console.log(response)

    templates.slice(0)
    let r_templates = response.data['data']['templates']
    r_templates.forEach((e: any) => {
      templates.push(e)
    });
    // console.log(r_binds)
    // UserInfo.email="123"
    console.log('templates:')
    console.log(templates)
  })
}


const deleteWork = (workid: string) => {
  axios({
    method: 'get',
    url: '/v2/delwork',
    headers: { Authorization: 'Bearer ' + store.Authorization },
    params: { 'workid': workid }
  }).then(res => {
    console.log(res)
    const code = res.data.code
    if (code != 0) {
      ElMessage({
        message: res.data.message,
        grouping: true,
        type: 'error',
      })
    } else {
      ElMessage({
        message: "删除成功",
        grouping: true,
        type: 'success',
      })
    }
  })
}
const runWork = (workid: string) => {
  axios({
    method: 'get',
    url: '/v2/updateworkstatus',
    headers: { Authorization: 'Bearer ' + store.Authorization },
    params: { 'workid': workid, 'status': 1 }
  }).then(res => {
    console.log(res)
    const code = res.data.code
    if (code != 0) {
      ElMessage({
        message: res.data.message,
        grouping: true,
        type: 'error',
      })
    } else {
      ElMessage({
        message: "启动任务成功",
        grouping: true,
        type: 'success',
      })
    }
  })
  getWorks()
}
const stopWork = (workid: string) => {
  axios({
    method: 'get',
    url: '/v2/updateworkstatus',
    headers: { Authorization: 'Bearer ' + store.Authorization },
    params: { 'workid': workid, 'status': 2 }
  }).then(res => {
    console.log(res)
    const code = res.data.code
    if (code != 0) {
      ElMessage({
        message: res.data.message,
        grouping: true,
        type: 'error',
      })
    } else {
      ElMessage({
        message: "暂停任务成功",
        grouping: true,
        type: 'success',
      })
    }
  })
  getWorks()
}

const getWorks = () => {
  axios({
    method: 'get',
    url: '/v2/getworks',
    headers: { Authorization: 'Bearer ' + store.Authorization }
  }).then(function (response) {
    // console.log(typeof(response))
    // console.log(response)
    if (response) {
      let r_works: any[] = response.data['data']['works']
      // r_works.forEach(work=>{
      //   if(work['status']==1){
      //     work['status']="运行中"
      //   }else if(work['status']==2){
      //     work['status']="出错暂停"
      //   }
      // })
      store.Works = r_works
      // console.log(r_binds)
    } else {
      // router.replace('/login')
    }

    // UserInfo.email="123"
    // console.log(UserInfo)
  })
}
const getWorkLogs = () => {
  axios({
    method: 'get',
    url: '/v2/getworklogs',
    headers: { Authorization: 'Bearer ' + store.Authorization }
  }).then(function (response) {
    let r_works: any[] = response.data['data']['worklogs']
    store.WorkLogs = r_works
  })
}

const onAddSignWork = () => {
  if (form.type == '1') {
    axios({
      method: 'get',
      url: '/v2/dolatestsign',
      headers: { Authorization: 'Bearer ' + store.Authorization },
      params: { 'bindid': form.bindid, 'templateid': form.templateid }
    }).then(res => {
      console.log(res)
      const code = res.data.code
      if (code != 0) {
        ElMessage({
          message: res.data.msg,
          grouping: true,
          type: 'error',
        })
      } else {
        ElMessage({
          message: "执行成功",
          grouping: true,
          type: 'success',
        })
      }
    })
  } else {

  }
}

const onAddWork = () => {
  if (form.type == '1') {
    axios({
      method: 'get',
      url: '/v2/quickwork',
      headers: { Authorization: 'Bearer ' + store.Authorization },
      params: { 'bindid': form.bindid, 'templateid': form.templateid }
    }).then(res => {
      console.log(res)
      const code = res.data.code
      if (code != 0) {
        ElMessage({
          message: res.data.msg,
          grouping: true,
          type: 'error',
        })
      } else {
        ElMessage({
          message: "执行成功",
          grouping: true,
          type: 'success',
        })
      }
    })
  } else {
    axios({
      method: 'get',
      url: '/v2/addwork',
      headers: { Authorization: 'Bearer ' + store.Authorization },
      params: { 'bindid': form.bindid, 'templateid': form.templateid, 'starttime': form.starttime, 'endtime': form.endtime }
    }).then(res => {
      console.log(res)
      const code = res.data.code
      if (code != 0) {
        ElMessage({
          message: res.data.msg,
          grouping: true,
          type: 'error',
        })
      } else {
        ElMessage({
          message: "添加任务成功",
          grouping: true,
          type: 'success',
        })
      }
    })
  }


  // console.log(form)
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