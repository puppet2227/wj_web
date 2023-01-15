// wj-web/src/components/Login.vue
<template>
  <div class="login">
    <div class="main-login">
      <div class="title">登 录</div>
      <el-row type="flex" justify="center">
        <el-form ref="loginForm" :rules="rules" :model="loginForm">
          <el-form-item prop="username">
            <el-input
              icon="el-icon-search"
              placeholder="请输入用户名"
              v-model="loginForm.username"
            >
              <i class="el-icon-user" slot="prefix"> </i>
            </el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              placeholder="请输入密码"
              v-model="loginForm.password"
              show-password
            >
              <i class="el-icon-lock" slot="prefix"> </i>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              @click="login"
              style="text-align: center; width: 150px"
              >登 录</el-button
            >
          </el-form-item>
        </el-form>
      </el-row>
      <div class="link">
        <el-link type="primary" :underline="false" href="/register"
          >注册新账号</el-link
        >
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "Login",
  data() {
    return {
      loginForm: {
        username: "",
        password: "",
      },
      rules: {
        username: [
          { required: true, message: "账号不能为空", trigger: "blur" },
          { max: 20, message: "账号长度最长20位", trigger: "blur" },
        ],

        password: [
          { required: true, message: "密码不能为空", trigger: "blur" },
          { min: 6, message: "密码长度最少为6位", trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    login() {
      // 请求前表单验证
      this.$refs.loginForm.validate((valid) => {
        if (!valid) {
          return false;
        }
        this.$request({
          url: "/api/user/login",
          method: "post",
          data: {
            username: this.loginForm.username,
            password: this.loginForm.password,
          },
        }).then((data) => {
          if (data.code == 0) {
            this.$message.success("登录成功");
            sessionStorage.setItem("username", this.loginForm.username);
            this.$router.push({ path: "home" });
          }
        });
      });
    },
  },
};
</script>
<style scoped>
.login {
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: #e4e7ed;
}
.title {
  font-size: large;
  font-weight: bolder;
  text-align: center;
  color: black;
}
.main-login {
  position: absolute;
  left: 48%;
  top: 40%;
  width: 320px;
  height: 250px;
  margin: -190px 0 0 -190px;
  padding: 40px;
  border-radius: 5px;
  background: #f2f6fc;
}
.el-form {
  padding-top: 5%;
  padding-left: 10%;
  padding-right: 10%;
  width: 280px;
}
.el-row {
  height: 100%;
  width: 100%;
}
.link {
  margin-top: -13%;
  text-align: center;
  margin-left: -5%;
}
.el-link {
  margin-left: 8px;
  line-height: 20px;
  font-size: 8px;
}
</style>