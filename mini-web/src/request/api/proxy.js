import { useMyFetch } from "../useMyFetch";

const getSchoolListAPI = () => {
	return useMyFetch("/proxy/get_school_list").get().json();
};

const loginAPI = (phoneNumber, password, schoolId) => {
	return useMyFetch(
		`/proxy/login?phone_number=${phoneNumber}&password=${password}&school_id=${schoolId}`,
	)
		.get()
		.json();
};

const getSignListAPI = (page, limit, jwSession) => {
	return useMyFetch(
		`/proxy/sign/list?page=${page}&limit=${limit}&jw_session=${jwSession}`,
	)
		.get()
		.json();
};

const doSignAPI = (jwSession, id, signId, schoolID, latitude, longitude) => {
	return useMyFetch(
		`/proxy/sign/do?jw_session=${jwSession}&id=${id}&sign_id=${signId}&school_id=${schoolID}&latitude=${latitude}&longitude=${longitude}`,
	)
		.get()
		.json();
};

export { getSchoolListAPI, loginAPI, getSignListAPI, doSignAPI };
