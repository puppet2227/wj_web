// wj-web/src/views/home/WDesign/QAddDialog.vue
<template>
  <el-dialog
    :title="title"
    :visible.sync="dialogShow"
    :close-on-click-modal="false"
    class="q-add-dialog"
    @open="openHandle"
  >
    <el-form ref="form" :model="qInfo" label-width="80px">
      <el-form-item label="题目类型" style="width: 100%">
        <el-select
          v-model="qInfo.type"
          placeholder="请选择题目类型"
          @change="typeChange"
        >
          <el-option
            v-for="item in allType"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="是否必填" style="width: 100%">
        <el-checkbox v-model="qInfo.must">必填</el-checkbox>
      </el-form-item>
      <el-form-item label="题目标题" style="width: 100%">
        <el-input v-model="qInfo.title" placeholder="请输入标题"></el-input>
      </el-form-item>

      <template v-if="qInfo.type == 'radio' || qInfo.type == 'checkbox'">
        <el-form-item
          :label="'选项' + (index + 1)"
          v-for="(item, index) in qInfo.options"
          :key="'op' + index"
        >
          <el-row>
            <el-col :span="16">
              <el-input
                v-model="item.title"
                placeholder="请输入选项名"
                style="width: 90%"
              ></el-input>
            </el-col>
            <el-col :span="8">
              <el-button
                type="danger"
                plain
                class=""
                @click="deleteOption(index)"
                >删除选项</el-button
              >
            </el-col>
          </el-row>
        </el-form-item>
        <el-button
          type="primary"
          plain
          class="add-option-button"
          @click="addOption"
          >新增选项</el-button
        >
      </template>
      <template v-if="qInfo.type == 'text'">
        <el-form-item label="填空">
          <el-input
            type="textarea"
            :rows="qInfo.attrs.row"
            style="width: 80%"
            resize="none"
          ></el-input>
        </el-form-item>
        <el-form-item label="行数">
          <el-input-number
            v-model="qInfo.attrs.row"
            :min="1"
            :max="10"
            label="描述文字"
          ></el-input-number>
        </el-form-item>
      </template>
    </el-form>
    <br />
    <div style="width: 100%; text-align: right">
      <el-button style="margin-left: 10px" @click="dialogShow = false"
        >取消</el-button
      >
      <el-button
        type="primary"
        style="margin-left: 10px"
        @click="addQuestionAck"
        >完成</el-button
      >
    </div>
  </el-dialog>
</template>
<script>
var defaultQInfo = {
  id: 0,
  type: "radio",
  title: "",
  must: true,
  options: [
    {
      id: 0,
      title: "",
    },
  ],
  attrs: {
    row: 1,
  },
};
export default {
  props: {
    show: { default: false },
    wjId: {},
  },
  computed: {
    dialogShow: {
      get() {
        return this.show;
      },
      set(val) {
        this.$emit("update:show", val);
      },
    },
  },
  data() {
    return {
      editQInfo: {},
      isEdit: false,
      title: "添加题目",
    };
  },
  methods: {
    openDialog(qInfo = null, isEdit = false) {
      this.isEdit = isEdit;
      this.editQInfo = qInfo;
      this.dialogShow = true;
      this.title = isEdit ? "修改题目" : "添加题目";
    },
    openHandle() {
      console.log("open");
      this.qInfo = JSON.parse(JSON.stringify(defaultQInfo));
      if (this.isEdit) {
        this.qInfo = JSON.parse(JSON.stringify(this.editQInfo));
      } else {
        this.qInfo = JSON.parse(JSON.stringify(defaultQInfo));
      }
      this.isEdit = false;
    },
    typeChange(value) {
      let title = this.qInfo.title;
      let tmp = JSON.parse(JSON.stringify(defaultQInfo));
      tmp.type = value;
      tmp.title = title;
      this.qInfo = tmp;
    },
    addQuestionAck() {
      console.log(this.qInfo);
      // 预留请求后端接口 todo
      this.$request({
      url: "/api/wj/add_question",
      method: "post",
      data: {
          wjId: this.wjId,
          qInfo: this.qInfo,
      },
      }).then((data) => {
      this.$message.success("添加成功");
      this.$emit("initQList");
      this.dialogShow = false;
      });
    },
    addOption() {
      this.qInfo.options.push({
        title: "",
        id: 0,
      });
    },
    deleteOption(index) {
      this.qInfo.options.splice(index, 1);
    },
    
  },
};
</script>
<style scope>
.q-add-dialog {
  text-align: left;
}
.add-option-button {
  display: inline-block !important;
  margin-left: 80px !important;
}
</style>