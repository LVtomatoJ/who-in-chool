import { useMyFetch } from "../useMyFetch";

const updateNickNameAPI = (nickName) => {
	return useMyFetch(`/user/change_nick_name?nick_name=${nickName}`).get().json();
};

const getUserInfoAPI = () => {
	return useMyFetch("/user").get().json();
};

export { updateNickNameAPI, getUserInfoAPI };