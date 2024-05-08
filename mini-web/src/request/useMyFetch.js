import { createFetch } from "@vueuse/core";
const useMyFetch = createFetch({
	baseUrl: "http://1.15.172.238:8000/api/v1",
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
