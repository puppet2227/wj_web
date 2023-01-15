// wj-web/src/utils/request.js
// 引入axios
import router from "@/router";
import axios from "axios";
import { Message } from "element-ui";

// 创建axios实例
const instance = axios.create({
  timeout: 5000, //请求超时时间
});
// 添加请求拦截器
instance.interceptors.request.use(
  (config) => {
    // 在发送请求之前做些什么
    return config;
  },
  (error) => {
    // 对请求错误做些什么
    return Promise.reject(error);
  }
);

// 添加响应拦截器
instance.interceptors.response.use(
  (response) => {
    // 对响应数据做点什么
    const res = response.data;
    if (res.code != 0) {
      Message({
        message: res.msg || "Error",
        type: "error",
        duration: 3 * 1000,
      });
      // 如果登录过期（身份验证失败），跳转到登录页面
      if (res.code == 100) {
        sessionStorage.removeItem("username");
        router.push({ path: "/login" });
        location.reload();
      }
      return Promise.reject(new Error(res.HEAD.msg || "Error"));
    }
    return res;
  },
  (error) => {
    // 对响应错误做点什么
    return Promise.reject(error);
  }
);

//导出axios实例
export default instance;