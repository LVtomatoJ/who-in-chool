import { createFetch } from "@vueuse/core";
const useMyFetch = createFetch({
	baseUrl: import.meta.env.VITE_API_URL,
	combination: "overwrite",
	options: {
		onFetchError(ctx) {
			if (ctx.data) {
				ctx.error = ctx.data;
				return ctx;
			}
		},
	},
});
export { useMyFetch };
