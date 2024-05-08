import { createFetch } from "@vueuse/core";
const useMyFetch = createFetch({
	baseUrl: "http://127.0.0.1:8000/api/v1",
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
