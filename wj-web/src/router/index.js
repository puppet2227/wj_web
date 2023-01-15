// wj-web/src/router/index.js
import Vue from "vue";
import Router from "vue-router";
import HelloWorld from "@/components/HelloWorld.vue";
import Layout from "@/components/Layout.vue";
import Login from "@/components/Login";
import Register from "@/components/Register";
import Home from "@/views/home/index.vue";
import Display from "@/views/home/Display.vue";
import Success from "@/views/home/Success.vue";

Vue.use(Router);
export default new Router({
  routes: [
    {
      path: "/",
      component: HelloWorld,
    },
    {
      path: "/",
      component: Layout,
      // 此处配置的路由组件会直接在Layout的router-view部分展示
      children: [
        {
          path: "/login",
          name: "Login",
          component: Login,
        },
        {
          path: "/register",
          name: "Register",
          component: Register,
        },
        {
          path: "/home",
          name: "Home",
          component: Home,
        },
      ],
    },
    {
      path: "/display/:id",
      component: Display,
    },
    {
      path: "/success",
      component: Success,
    },
  ],
});