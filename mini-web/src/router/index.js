/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from "vue-router/auto";
import { setupLayouts } from "virtual:generated-layouts";
import { useAppStore } from "@/stores/app";

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	extendRoutes: setupLayouts,
});

router.beforeEach(async (to, from) => {
	const appStore = useAppStore();
	console.log("to");
	console.log(to);
	console.log(appStore.jwSession);
	if (
		// make sure the user is authenticated
		appStore.jwSession === "" &&
		// ❗️ Avoid an infinite redirect
		to.path !== "/login" &&
		to.path !== "/"
	) {
		// redirect the user to the login page
		return { path: "/login" };
	}
});

export default router;
