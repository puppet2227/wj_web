// wj-web/src/views/home/WNavBar.vue
<template>
  <div class="w-nav-bar">
    <el-tooltip
      class="item"
      effect="dark"
      content="创建问卷"
      placement="bottom"
    >
      <el-button
        icon="el-icon-plus"
        type="text"
        class="rightButton"
        @click="addWjClick"
      ></el-button>
    </el-tooltip>
    <el-tooltip
      class="item"
      effect="dark"
      content="编辑问卷"
      placement="bottom"
    >
      <el-button
        icon="el-icon-edit"
        type="text"
        class="rightButton"
        @click="editWjClick"
        :disabled="nowSelect.id == 0 || nowSelect.id == null"
      ></el-button>
    </el-tooltip>
    <el-tooltip
      class="item"
      effect="dark"
      :content="nowSelect.status == 0 ? '发布问卷' : '暂停问卷'"
      placement="bottom"
    >
      <el-button
        :icon="
          nowSelect.status == 0 ? 'el-icon-video-play' : 'el-icon-video-pause'
        "
        type="text"
        class="rightButton"
        @click="pushWjClick"
        :disabled="nowSelect.id == 0 || nowSelect.id == null"
      ></el-button>
    </el-tooltip>
    <el-tooltip
      class="item"
      effect="dark"
      content="预览问卷"
      placement="bottom"
    >
      <el-button
        icon="el-icon-view"
        type="text"
        class="rightButton"
        @click="previewWjClick"
        :disabled="nowSelect.id == 0 || nowSelect.id == null"
      ></el-button>
    </el-tooltip>
    <el-tooltip
      class="item"
      effect="dark"
      content="删除问卷"
      placement="bottom"
    >
      <el-button
        icon="el-icon-delete"
        type="text"
        class="rightButton"
        @click="deleteWjClick"
        :disabled="nowSelect.id == 0 || nowSelect.id == null"
      ></el-button>
    </el-tooltip>
    <el-tooltip
      class="item"
      effect="dark"
      content="分享问卷"
      placement="bottom"
    >
      <el-button
        icon="el-icon-share"
        type="text"
        class="rightButton"
        @click="shareWjClick"
        :disabled="nowSelect.id == 0 || nowSelect.id == null"
      ></el-button>
    </el-tooltip>
    <!--添加问卷弹窗-->
    <el-dialog
      :title="addWjDialogTitle"
      :visible.sync="addWjDialogShow"
      :close-on-click-modal="false"
      class="dialog"
    >
      <el-form ref="form" :model="wjInfo" label-width="80px">
        <el-form-item label="问卷标题" style="width: 100%" required>
          <el-input
            v-model="wjInfo.title"
            placeholder="请输入问卷标题"
          ></el-input>
        </el-form-item>
        <el-form-item label="问卷描述" style="width: 100%">
          <el-input
            v-model="wjInfo.desc"
            type="textarea"
            placeholder="请输入问卷描述"
            rows="5"
          ></el-input>
        </el-form-item>
      </el-form>
      <div style="width: 100%; text-align: right">
        <el-button style="margin-left: 10px" @click="addWjDialogShow = false"
          >取消</el-button
        >
        <el-button type="primary" style="margin-left: 10px" @click="addWjHandle"
          >确定</el-button
        >
      </div>
    </el-dialog>
    <!--分享问卷弹窗-->
    <el-dialog
      title="分享问卷"
      :visible.sync="shareWjDialogShow"
      :close-on-click-modal="true"
      class="dialog"
      @opened="makeQrcode"
    >
      <el-form ref="form" :model="shareInfo" label-width="80px">
        <el-form-item label="问卷链接" style="width: 100%">
          <el-row>
            <el-col :span="16">
              <el-input v-model="shareInfo.url" readonly></el-input>
            </el-col>
            <el-col :span="8">
              <el-button
                style="margin-left: 5px"
                v-clipboard:copy="shareInfo.url"
                v-clipboard:success="copySuccess"
                v-clipboard:error="copyError"
                >复制</el-button
              >
              <el-button style="margin-left: 5px" @click="openShareUrl"
                >打开</el-button
              >
            </el-col>
          </el-row>
        </el-form-item>
        <el-form-item label="二维码" style="width: 100%">
          <canvas id="canvas" style="width: 150px; height: 150px"></canvas>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>
<script>
import QRCode from "qrcode";
export default {
  props: {
    nowSelect: {},
  },
  data() {
    return {
      addWjDialogShow: false,
      wjInfo: {},
      addWjDialogTitle: "添加问卷",
      shareWjDialogShow: false,
      shareInfo: {
        url: "111",
      },
    };
  },
  methods: {
    addWjClick() {
      this.addWjDialogTitle = "添加问卷";
      this.wjInfo = {};
      this.addWjDialogShow = true;
    },
    editWjClick() {
      this.addWjDialogTitle = "编辑问卷";
      this.wjInfo = JSON.parse(JSON.stringify(this.nowSelect));
      this.addWjDialogShow = true;
    },
    addWjHandle() {
      this.$request({
        url: "/api/wj/add_wj",
        method: "post",
        data: {
          id: this.wjInfo.id,
          title: this.wjInfo.title,
          desc: this.wjInfo.desc,
        },
      }).then((data) => {
        if (this.wjInfo.id) {
          this.$message.success("保存成功");
        } else {
          this.$message.success("添加成功");
        }
        this.$emit("initWjList");
        this.addWjDialogShow = false;
      });
    },
    pushWjClick() {
    // 预留请求后端代码 pass
    this.$request({
    url: "/api/wj/push_wj",
    method: "post",
    data: {
        wj_id: this.nowSelect.id,
        status: this.nowSelect.status == 0 ? 1 : 0,
    },
    }).then((data) => {
    this.nowSelect.status = data.status;
    if (this.nowSelect.status == 1) {
        this.$message.success("发布成功！");
    } else {
        this.$message.success("暂停成功！");
      }
      });
    },
    previewWjClick() {
      this.$router.push({
        path: "/display/" + this.nowSelect.id,
      });
    },
    deleteWjClick() {
    this.$confirm(
    "确定删除" + this.nowSelect.title + "? 删除后不可恢复！",
    "提示",
    {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
    }
    ).then(() => {
    console.log("删除点击确定");
    // 预留请求后端代码 pass
    this.$request({
        url: "/api/wj/delete_wj",
        method: "post",
        data: {
        id: this.nowSelect.id,
        },
    }).then((data) => {
        this.$message({
        type: "success",
        message: "删除成功!",
        });
        this.$emit("initWjList");
      });
      });
    },
    shareWjClick() {
      let routeData = this.$router.resolve({
        path: "/display/" + this.nowSelect.id,
      });
      this.shareInfo.url = window.location.origin + routeData.href; //问卷链接
      this.shareDialogShow = true;
      this.shareWjDialogShow = true;
    },
    //生成二维码
    makeQrcode() {
      var canvas = document.getElementById("canvas");
      QRCode.toCanvas(canvas, this.shareInfo.url);
    },
    //复制分享链接成功
    copySuccess(e) {
      console.log(e);
      this.$message({
        type: "success",
        message: "已复制链接到剪切板",
      });
    },
    //复制分享链接失败
    copyError(e) {
      console.log(e);
      this.$message({
        type: "error",
        message: "复制失败",
      });
    },
    //打开分享链接
    openShareUrl() {
      window.open(this.shareInfo.url);
    },
  },
};
</script>
<style scope>
.w-nav-bar {
  position: relative;
  background-color: #fafafa;
  text-align: center;
  height: 40px;
}
.w-nav-bar .dialog {
  text-align: left;
}
</style>