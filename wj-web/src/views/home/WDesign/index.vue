// wj-web/src/views/home/WDesign/index.vue
<template>
  <div class="w-design">
    <h3>{{ wjTitle }}</h3>
    <div class="wj-desc" v-if="desc != ''">
      {{ wjDesc }}
    </div>

    题目数据：{{ qList }} <br />
    回答:{{ answer }}
    <q-item
      v-for="(qItem, index) in qList"
      :key="qItem.id"
      :data="qItem"
      :index="index"
      v-model="answer[qItem.id]"
      @edit="qItemEdit"
      @delete="qItemDelete"
    ></q-item>
    <br />
    <el-button
      icon="el-icon-circle-plus"
      @click="addQuestion"
      style="margin-top: 10px"
      >添加题目</el-button
    >
    <q-add-dialog
      @addQuestion="addQuestionHandle"
      :show.sync="addDialogShow"
      ref="addDialogRef"
      :wjId="wjId"
      @initQList="initQList"
    ></q-add-dialog>
  </div>
</template>
<script>
import QAddDialog from "./QAddDialog.vue";
import QItem from "./QItem.vue";
export default {
  props: {
    wjItem: {},
  },
  computed: {
    wjId() {
      return this.wjItem.id;
    },
    wjTitle() {
      return this.wjItem.title;
    },
    wjDesc() {
      return this.wjItem.desc;
    },
  },
  watch: {
    wjId: {
      handler(val) {
        this.initQList();
      },
    },
  },
  components: { QAddDialog, QItem },
  data() {
    return {
      title: "测试问卷标题",
      desc: "感谢您能抽时间参与本次问卷，您的意见和建议就是我们前行的动力！",
      qList: [],
      answer: {},
      addDialogShow: false,
    };
  },
  mounted() {
    this.initQList();
  },
  methods: {
    initQList() {
      this.$request({
      url: "/api/wj/get_question_list",
      method: "post",
      data: {
          wj_id: this.wjId,
      },
      }).then((data) => {
      this.qList = data.detail;
      this.answer = {};
      for (let i = 0; i < this.qList.length; i++) {
          let item = this.qList[i];
          if (item.type == "checkbox") {
          this.answer[item.id] = [];
          } else {
          this.answer[item.id] = "";
          }
      }
      });
    },
    qItemDelete(index) {
    this.$confirm("确定删除此题目?", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
    }).then(() => {
    let qId = this.qList[index].id;
    // 请求后端删除问题接口
    this.$request({
        url: "/api/wj/delete_question",
        method: "post",
        data: {
            q_id: qId,
        },
    }).then((data) => {
        this.$message.success("删除成功");
        this.initQList();
    });
    });
    },
  },
};
</script>
<style scope>
.wj-desc {
  color: #606266;
  margin-left: 20px;
  padding: 0 10px 10px 10px;
  border-bottom: 3px solid #409eff;
  font-size: 15px;
  line-height: 22px;
  text-align: left;
}
</style>