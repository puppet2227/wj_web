// wj-web/src/components/Layout.vue
<template>
  <div class="main">
    <el-container>
      <el-header>
        <div class="logo">
          <img :src="logoImg" class="logo-img" />
          <span class="logo-text">C++</span>
          <span class="logo-text-sub">——信奥在线答题系统</span>
        </div>
        <div class="nav-div">
          <!-- 未登录显示 -->
          <template v-if="!username">
            <el-button type="primary" plain class="nav-button" @click="toLogin"
              >登录{{ username }}</el-button
            >
            <el-button plain class="nav-button" @click="toRegister"
              >注册</el-button
            >
          </template>
          <!-- 登录时显示 -->
          <template v-else>
            <!-- 登录成功，显示用户名 -->
            <el-dropdown trigger="click" @command="handleCommand">
              <span class="el-dropdown-link">
                {{ username }}<i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <!-- 退出登录 -->
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="a">问卷管理</el-dropdown-item>
                <el-dropdown-item command="b">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </template>
        </div>
      </el-header>
      <el-main style="padding: 0">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>
<script>
import logoImg from "@/assets/logo.png";
export default {
  name: "Layout",
  data() {
    return {
      logoImg: logoImg,
      username: "",
    };
  },
  mounted() {
    this.username = sessionStorage.getItem("username");
    // 路由守卫
    this.$router.afterEach((to, from) => {
      this.username = sessionStorage.getItem("username");
    });
  },
  methods: {
    toLogin() {
      this.$router.push({ path: "/login" });
    },
    toRegister() {
      this.$router.push({ path: "/register" });
    },
    toHome() {
      this.$router.push({ path: "/home" });
    },
    logout() {
      sessionStorage.removeItem("username");
      this.$request({
        url: "/api/user/logout",
        method: "post",
        data: {},
      }).then((data) => {
        if (data.code == 0) {
          this.$message.success("已退出登录");
          this.toLogin();
        }
      });
    },
    handleCommand(command) {
      if (command == "a") {
        this.toHome();
      } else if (command == "b") {
        this.logout();
      }
    },
  },
};
</script>
<style scoped>
.main {
  position: absolute;
  width: 100%;
  height: 100%;
}
.logo-img {
  width: 30px;
  margin-right: 5px;
  vertical-align: middle;
}
.logo-text {
  color: #303133;
}
.logo-text-sub {
  font-size: 13px;
  margin-left: 5px;
  color: #606266;
}
.logo {
  height: 60px;
  display: inline-block;
  line-height: 60px;
  font-size: 20px;
  position: absolute;
  left: 100px;
  color: #303133;
  cursor: pointer;
}
.nav-div {
  float: right;
  margin-right: 50px;
  line-height: 60px;
}
.nav-button {
  font-size: 15px;
}
.el-header {
  border-bottom: 2px solid #409eff;
  background-color: white;
}
</style>