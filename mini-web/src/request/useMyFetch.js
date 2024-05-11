import { createFetch } from "@vueuse/core";
import { useAppStore } from "@/stores/app";

const useMyFetch = createFetch({
	baseUrl: import.meta.env.VITE_API_URL,
	combination: "overwrite",

	options: {
		async beforeFetch({ options }) {
			const appStore = useAppStore();
			options.headers.Authorization = `Bearer ${appStore.token}`;
			return { options };
		},
		onFetchError(ctx) {
			if (ctx.data) {
				ctx.error = ctx.data;
				return ctx;
			}
		},
	},
});
export { useMyFetch };
