import { useMyFetch } from "../useMyFetch";

const getMessageListAPI = (page,limit) => {
	return useMyFetch(`/message_board/get_message_list?page=${page}&limit=${limit}`).get().json();
};

const publishMessageAPI = (content) => {
	return useMyFetch(`/message_board/publish_message?content=${content}`).get().json();
};

export {
	getMessageListAPI,
	publishMessageAPI
}