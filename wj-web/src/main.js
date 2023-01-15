// wj-web/src/main.js
import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import request from "@/utils/request";

Vue.use(ElementUI);
Vue.config.productionTip = false;
Vue.prototype.$request = request;

new Vue({
  render: (h) => h(App),
  router,
}).$mount("#app");