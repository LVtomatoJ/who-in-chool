<template>
  <el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="列表" name="list">
      <el-table table-layout="auto" :data="store.Works" border style="width: 100%;margin-top: 20px;">
        <el-table-column type="index"></el-table-column>
        <el-table-column prop="workid" label="任务id" width="120" />
        <el-table-column prop="status" label="状态" width="70" />
        <el-table-column prop="bindid" label="绑定用户id" />
        <el-table-column prop="starttime" label="开始时间" width="160" />
        <el-table-column prop="endtime" label="结束时间" width="160" />
        <el-table-column fixed="right" label="操作" width="70">
          <template #default="scope">
            <el-button link type="primary" size="small" @click="deleteWork(scope.$index)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-tab-pane>
    <el-tab-pane label="添加任务" name="add">


      <el-form :model="form" label-width="100px" style="margin-top:20px">
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
          <el-date-picker
        v-model="form.starttime"
        type="datetime"
        placeholder="Pick a Date"
        format="YYYY/MM/DD hh:mm:ss"
        value-format="YYYY-MM-DD hh:m:s"
        @change="timeChange"
      />
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
          <el-date-picker
        v-model="form.endtime"
        type="datetime"
        placeholder="Pick a Date"
        format="YYYY/MM/DD hh:mm:ss"
        value-format="YYYY-MM-DD hh:m:s"
        @change="timeChange"
      />
        </el-form-item>
        <el-form-item label="任务模板">
          <el-select v-model="form.templateid" clearable placeholder="Select">
            <el-option v-for="template in templates" :key="template.templateid" :label="template.name"
              :value="template.templateid" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onAddWork">添加/执行任务</el-button>
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
  type: '1',
  starttime: "",
  endtime:'',
  templateid: ''
})
const templates = reactive<any[]>([]);
const showTimeSet = ref(false)
const handleClick = (tab: TabsPaneContext, event: Event) => {
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

const deleteWork = (index:number) =>{

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
      store.Works = response.data['data']['works']
      // console.log(r_binds)
    } else {
      // router.replace('/login')
    }

    // UserInfo.email="123"
    // console.log(UserInfo)
  })
}
const onAddWork = () => {
  if(form.type=='1'){
    axios({
      method:'get',
      url:'/v2/quickwork',
      headers: { Authorization: 'Bearer ' + store.Authorization },
      params:{'bindid':form.bindid,'templateid':form.templateid}
    }).then(res=>{
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
        message: "执行成功",
        grouping: true,
        type: 'success',
      })
    }
    })
  }else{
    axios({
      method:'get',
      url:'/v2/addwork',
      headers: { Authorization: 'Bearer ' + store.Authorization },
      params:{'bindid':form.bindid,'templateid':form.templateid,'starttime':form.starttime,'endtime':form.endtime}
    }).then(res=>{
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