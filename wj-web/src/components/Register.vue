// wj-web/src/components/Register.vue
<template>
  <div class="register">
    <div class="main-register">
      <div class="title">注 册</div>
      <el-row>
        <el-form
          :model="registerForm"
          status-icon
          :rules="rules"
          size="medium"
          ref="registerForm"
          label-width="100px"
          class="demo-registeForm"
        >
          <el-form-item prop="username" label="用户名">
            <el-input
              @keyup.enter.native="Register"
              v-model="registerForm.username"
              placeholder="请输入用户名"
            ></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="pass">
            <el-input
              @keyup.enter.native="Register"
              v-model="registerForm.pass"
              autocomplete="off"
              placeholder="请输入密码(不少于6位)"
              show-password
            >
            </el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="checkPass">
            <el-input
              @keyup.enter.native="Register"
              v-model="registerForm.checkPass"
              autocomplete="off"
              placeholder="请再次输入密码"
              show-password
            >
            </el-input>
          </el-form-item>
          <el-form-item style="margin-left: -25%">
            <el-button type="primary" @click="Register">注册</el-button>
            <el-button @click="resetForm" style="margin-right: -5%"
              >重置</el-button
            >
          </el-form-item>
        </el-form>
      </el-row>
      <div class="link">
        <el-link type="primary" :underline="false" href="/login"
          >已有账号?去登录</el-link
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Register",
  data() {
    var validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        if (this.registerForm.checkPass !== "") {
          this.$refs.registerForm.validateField("checkPass");
        }
        callback();
      }
    };
    var validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.registerForm.pass) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    return {
      registerForm: {
        username: "",
        pass: "",
        checkPass: "",
      },
      rules: {
        username: [
          { required: true, message: "账号不能为空", trigger: "blur" },
          { max: 20, message: "账号长度最长20位", trigger: "blur" },
        ],
        pass: [
          { required: true, validator: validatePass, trigger: "blur" },
          { min: 6, message: "密码长度最少为6位", trigger: "blur" },
          { max: 16, message: "密码长度不能超过16位", trigger: "blur" },
        ],
        checkPass: [
          { required: true, validator: validatePass2, trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    // wj-web/src/components/Register.vue
    Register() {
      // 请求前表单验证
      this.$refs.registerForm.validate((valid) => {
        if (!valid) {
          return false;
        }
        this.$request({
          url: "/api/user/register",
          method: "post",
          data: {
            username: this.registerForm.username,
            password: this.registerForm.pass,
          },
        }).then((data) => {
          console.log("ddd=", data);
          if (data.code == 0) {
            this.$message.success("注册成功");
            this.$router.push({ path: "/login" });
          }
        });
      });
    },
    resetForm() {
      this.$refs.registerForm.resetFields();
    },
  },
};
</script>

<style scoped>
.register {
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
.main-register {
  position: absolute;
  left: 48%;
  top: 40%;
  width: 350px;
  height: 300px;
  margin: -190px 0 0 -190px;
  padding: 40px;
  border-radius: 5px;
  background: #f2f6fc;
}
.el-form {
  padding-top: 5%;
  padding-right: 10%;
}
.el-form-item {
  margin-left: -10%;
}
.el-row {
  height: 100%;
  width: 100%;
}
.link {
  margin-top: -12%;
  text-align: center;
  margin-left: -5%;
}
.el-link {
  margin-left: 8px;
  line-height: 20px;
  font-size: 8px;
}
</style>