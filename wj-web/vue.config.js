// wj-web/vue.config.js
module.exports = {
  publicPath: "/",
  productionSourceMap: false,
  devServer: {
    host: "0.0.0.0",
    port: 8080,
    disableHostCheck: true,
    historyApiFallback: true,
    proxy: {
      // 请求前缀
      "/api": {
        target: "http://127.0.0.1:8000", //转发请求到本地的8000端口
        changeOrigin: true, // 用于控制请求头中的host值
      },
    },
  },
  lintOnSave: false,
};