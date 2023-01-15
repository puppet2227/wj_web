//wj-web/src/views/home/WSlider.vue
<template>
  <div class="w-slider">
    <w-nav-bar :nowSelect="nowSelect" @initWjList="initWjList"></w-nav-bar>
    <el-menu
      :default-active="defaultActive"
      v-loading="loading"
      class="w-slider-menu"
    >
      <!-- 没有问卷时展示的提示内容 -->
      <div v-if="wjList.length == 0" class="wj-list-empty">
        点击上方&nbsp;+&nbsp;创建第一个问卷
      </div>
      <el-menu-item
        v-for="(item, index) in wjList"
        :key="item.id"
        :index="(index + 1).toString()"
        @click="wjClick(item.id, index)"
      >
        <i class="el-icon-tickets"></i>
        <span slot="title" style="display: inline-block">
          {{ item.title }}
          <span style="color: #f56c6c; font-size: 13px" v-if="item.status == 0">
            <i class="el-icon-link wj-status-icon" style="color: #f56c6c"></i>
            未发布
          </span>
          <span style="color: #67c23a; font-size: 13px" v-if="item.status == 1">
            <i class="el-icon-link wj-status-icon" style="color: #67c23a"></i>
            已发布
          </span>
        </span>
      </el-menu-item>
    </el-menu>
  </div>
</template>
<script>
import WNavBar from "./WNavBar.vue";
export default {
  components: {
    WNavBar,
  },
  data() {
    return {
      loading: false,
      wjList: [],
      defaultActive: null,
      nowSelect: {},
    };
  },
  mounted() {
    this.initWjList();
  },
  methods: {
    wjClick(index) {
      this.defaultActive = (index + 1).toString();
      this.nowSelect = this.wjList[index];
      this.$emit("wjClick", this.nowSelect);
    },
    // 模拟初始化问卷列表
    initWjList() {
      this.loading = true;
      this.$request({
        url: "/api/wj/get_wj_list",
        method: "post",
        data: {},
      }).then((data) => {
        console.log("data=", data);
        this.wjList = data.detail;
        this.initWjListEnd();
        this.loading = false;
      });
    },
    initWjListEnd() {
      if (this.wjList.length > 0) {
        this.defaultActive = "1";
        this.nowSelect = this.wjList[0];
      }
    },
    mounted() {
    this.initWjList();
    },
  },
};
</script>
<style scope>
.w-slider {
  position: relative;
  text-align: left;
  height: 100%;
}
.w-slider-menu {
  position: relative;
  height: calc(100% - 40px);
  overflow-y: scroll;
  overflow-x: hidden;
}
.wj-status-icon {
  margin: 0 !important;
  font-size: 13px !important;
  width: 10px !important;
}
.wj-list-empty {
  width: 100%;
  text-align: center;
  font-size: 15px;
  line-height: 20px;
  margin-top: 20px;
  color: #303133;
}
</style>