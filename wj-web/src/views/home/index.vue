// wj-web/src/views/home/index.vue
<template>
  <div class="w-home">
    <!--操作栏-->
    <w-slider class="home-slider" @wjClick="wjClick"></w-slider>
    <!-- 设计界面 -->
    <div class="home-right">
      <!--标签页-->
      <el-tabs type="border-card" v-model="activeName">
        <el-tab-pane label="问卷设计" name="design">
          <!--内容区域-->
          <div class="card-content">
            <div v-if="!isSelectWj">请先选择问卷</div>
            <w-design v-else class="home-design" :wjItem="nowSelect"></w-design>
          </div>
        </el-tab-pane>
        <el-tab-pane label="回答统计" name="datashow">
          <div class="card-content" ref="pdf">
            <div v-if="!isSelectWj">请先选择问卷</div>
            <w-data-show v-else :wjItem="nowSelect"></w-data-show>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>
<script>
import WDesign from "@/views/home/WDesign";
import WSlider from "@/views/home/WSlider";
import WDataShow from "./WDataShow.vue";
export default {
  components: {
    WDesign,
    WSlider,
    WDataShow,
  },
  data() {
    return {
      activeName: "design",
      nowSelect: {},
    };
  },
  computed: {
    isSelectWj() {
      return this.nowSelect.id != 0 && this.nowSelect.id != null;
    },
  },
  methods: {
    wjClick(wjItem) {
      this.nowSelect = wjItem;
      // 预留初始化问卷题目信息
    },
  },
};
</script>
<style scope>
.w-home {
  position: absolute;
  left: 0;
  top: 60px;
  width: 100%;
  height: calc(100vh - 60px);
  /* color: #fff; */
}
.home-slider {
  position: relative;
  width: 400px;
  height: 100%;
  /* background-color: red; */
  display: inline-block;
  vertical-align: top;
}
.home-right {
  position: relative;
  width: calc(100% - 400px);
  height: calc(100vh - 60px);
  /* background-color: green; */
  display: inline-block;
}
.card-content {
  height: calc(100vh - 134px);
  overflow-x: hidden;
  overflow-y: scroll;
}
</style>
<style>
.home-right .el-tabs--border-card {
  box-shadow: none !important;
}
</style>