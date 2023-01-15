// wj-web/src/views/home/Display.vue
<template>
  <div class="display">
    <div class="display-content">
      <h3>{{ title }}</h3>
      <div class="wj-desc" v-if="desc != ''">
        {{ desc }}
      </div>
      wjId：{{ wjId }}
      <br />
      qList：{{ qList }}
      <br />
      answer：{{ answer }}
      <br />
      <q-item
        v-for="(qItem, index) in qList"
        :key="qItem.id"
        :data="qItem"
        :index="index"
        v-model="answer[qItem.id]"
        :showButton="false"
      ></q-item>

      <el-button
        type="primary"
        style="margin: 5px"
        @click="submit"
        :loading="submitLoading"
        >{{ submitText }}</el-button
      >
    </div>
  </div>
</template>
<script>
import QItem from "./WDesign/QItem.vue";
export default {
  components: { QItem },
  data() {
    return {
      wjId: "",
      title: "测试问卷标题",
      desc: "感谢您能抽时间参与本次问卷，您的意见和建议就是我们前行的动力！",
      qList: [],
      answer: {},
      submitText: "提交",
      submitLoading: false,
      startTimestamp: 0,
    };
  },
  created() {
    this.wjId = this.$route.params.id;
    console.log("问卷id", this.wjId);
  },
  async mounted() {
    await this.initWjInfo();
    await this.initQList();
    this.startTimestamp = new Date().getTime();
  },
  methods: {
    initWjInfo() {
      this.$request({
        url: "/api/wj/get_wj_info",
        method: "post",
        data: {
          wj_id: this.wjId,
        },
      }).then((data) => {
        this.title = data.detail.title;
        this.desc = data.detail.desc;
      });
    },
    initQList() {
      this.$request({
        url: "/api/wj/get_question_list",
        method: "post",
        data: {
          wj_id: this.wjId,
        },
      }).then((data) => {
        this.qList = data.detail;

        for (let i = 0; i < this.qList.length; i++) {
          let item = this.qList[i];
          if (item.type == "checkbox") {
            this.$set(this.answer, item.id, []);
          } else {
            this.$set(this.answer, item.id, "");
          }
        }
      });
    },
    submit() {
      this.submitLoading = true;
      this.submitText = "提交中";
      let useTime = parseInt(
        (new Date().getTime() - this.startTimestamp) / 1000
      ); //填写问卷用时 秒
      // 预留请求后端提交接口 todo
      this.$request({
        url: "/api/wj/submit_wj",
        method: "post",
        data: {
          wj_id: this.wjId,
          use_time: useTime,
          answers: this.answer,
        },
      })
        .then((data) => {
          this.submitLoading = false;
          this.submitText = "提交";
          this.$router.push({
            path: "/success",
          });
        })
        .catch((e) => {
          this.submitLoading = false;
          this.submitText = "提交";
        });
    },
  },
};
</script>
<style scope>
.display {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #f8f8f8;
  height: 100%;
  overflow-y: scroll;
  overflow-x: hidden;
}
.display-content {
  position: relative;
  max-width: 800px;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 10px 50px 10px;
}
</style>