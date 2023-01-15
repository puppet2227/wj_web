// wj-web/src/components/HelloWorld.vue
<template>
  <div>
    <el-button type="primary" @click="hello">点我</el-button>
  </div>
</template>
<script>
export default {
  methods: {
    hello() {
      this.$message.success("helloworld");
    },
  },
};
</script>