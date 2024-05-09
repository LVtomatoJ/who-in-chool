<template>
    <v-alert v-if="errorMessage" title="错误" :text="errorMessage" type="error"></v-alert>
    <v-alert v-if="successMessage" title="成功" :text="successMessage" type="success"></v-alert>
    <v-dialog v-model="doSigndialog" width="auto">
      <v-card
        max-width="400"
        prepend-icon="mdi-update"
        title="提交签到"
      >
        <template v-slot:text>
            签到位置：<br />
            {{pointLocation.latlng.lat}} <br /> 
            {{pointLocation.latlng.lng}} <br />
            签到地点：<br />
            {{pointLocation.poiaddress}} <br />
            {{pointLocation.poiname}}
            
        </template>
        <template v-slot:actions>
            <v-spacer></v-spacer>
        <v-btn
            class="ms-auto"
            text="取消"
            @click="doSigndialog = false"
          ></v-btn>
          <v-btn
           :loading="signLoading"
            class="ms-auto"
            text="确定"
            @click="doSign"
          ></v-btn>
        </template>
      </v-card>
    </v-dialog>
    <iframe v-if='showLocation' id="mapPage" width="100%" height="100%" frameborder=0
        :src="`https://apis.map.qq.com/tools/locpicker?search=1&type=1&key=${tencentMapKey}&referer=myapp`">
    </iframe>
    <template v-else="!showLocation">
        <v-list lines="two">
            <v-list-subheader>签到列表</v-list-subheader>
            <template v-for="(item, index) in signList" :key="index">
                <v-list-item >
                    <v-list-item-content>
                        <v-list-item-title>{{ item.signTitle }}</v-list-item-title>
                        <v-list-item-subtitle>
                            <!-- 时间戳转string -->
                            开始时间：{{ new Date(item.start).toLocaleString() }} 
                            <br>结束时间： {{ new Date(item.end).toLocaleString() }}
                           
                        </v-list-item-subtitle>
                    </v-list-item-content>
                    <template v-slot:append>
                            <v-btn v-if="item.signStatus != 2"  @click="handleShowLocation(item.id)">校区暴力签到</v-btn>
                            <v-btn variant="text" v-else>已签到</v-btn>
                    </template>
                </v-list-item>
            </template>
        </v-list>
        <v-btn block v-if="haveMore" @click="getSignList">加载更多</v-btn>
    </template>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";

import { useRouter } from "vue-router";
import { useAppStore } from "@/stores/app";

import { getSignListAPI, doSignAPI } from "@/request/api/proxy";

const tencentMapKey = import.meta.env.VITE_TENCENT_MAP_KEY;

const errorMessage = ref("");
const successMessage = ref("");

const router = useRouter();
const appStore = useAppStore();

const signList = ref([]);
const page = ref(1);

const haveMore = ref(true);

const showLocation = ref(false);
const doSigndialog = ref(false);

const latitude = ref(0);
const longitude = ref(0);

const pointLocation = ref({
	cityname: "",
	latlng: {
		lat: 0,
		lng: 0,
	},
	poiaddress: "",
	poiname: "",
});

const handleShowLocation = (id) => {
	selectId.value = id;
	showLocation.value = true;
};

const scrollToTop = () => {
	// 平滑滚动页面到顶部
	window.scrollTo({
		top: 0,
		behavior: "smooth",
	});
};

const selectId = ref(0);

const getSignList = async () => {
	const { data, error } = await getSignListAPI(
		page.value,
		10,
		appStore.jwSession,
	);
	if (error.value != null) {
		console.log("失败啦", error.value.detail);
		errorMessage.value = error.value.detail;
	} else {
		errorMessage.value = "";
		console.log("1");
		console.log(data.value);
		console.log("1");
		signList.value = signList.value.concat(data.value.data);
		console.log("2");
		if (data.value.data.length < 10) {
			console.log("3");
			haveMore.value = false;
		}
		console.log("4");
		page.value++;
		console.log("5");
	}
};

const signLoading = ref(false);

const doSign = async () => {
	signLoading.value = true;
	const signInfo = signList.value.find((item) => item.id === selectId.value);
	const { data, error } = await doSignAPI(
		appStore.jwSession,
		selectId.value,
		signInfo.signId,
		signInfo.schoolId,
		pointLocation.value.latlng.lat,
		pointLocation.value.latlng.lng,
	);
	doSigndialog.value = false;
	signLoading.value = false;
	if (error.value != null) {
		console.log("失败啦", error.value.detail);
		scrollToTop();
		errorMessage.value = error.value.detail;
		setTimeout(() => {
			errorMessage.value = "";
		}, 3000);
	} else {
		successMessage.value = "签到成功";
		setTimeout(() => {
			successMessage.value = "";
		}, 3000);
	}
};

onMounted(() => {
	getSignList();
});

window.addEventListener(
	"message",
	(event) => {
		// 接收位置信息，用户选择确认位置点后选点组件会触发该事件，回传用户的位置信息
		const loc = event.data;
		if (loc && loc.module === "locationPicker") {
			//防止其他应用也会向该页面post信息，需判断module是否为'locationPicker'
			console.log("location", loc);
			pointLocation.value = loc;
			//   doSign(loc.id)
			showLocation.value = false;
			doSigndialog.value = true;
		}
	},
	false,
);
</script>

