// wj-web/src/views/home/WDesign/QItem.vue
<template>
  <div class="q-item">
    <el-card class="box-card" style="margin: 10px">
      <div slot="header" class="clearfix">
        <div class="questionTitle">
          <!--显示必填标识-->
          <span style="color: #f56c6c">
            <span v-if="data.must">*</span>
            <span v-else>&nbsp;</span>
          </span>
          <span style="color: black; margin-right: 3px">{{
            index + 1 + "."
          }}</span>
          {{ data.title }}
        </div>
        // wj-web/src/views/home/WDesign/QItem.vue
        <div class="right-button" v-if="showButton">
          <el-button style="padding: 2px" type="text" @click="editQuestion"
            >编辑</el-button
          >
          <el-button
            style="padding: 2px; color: #f56c6c"
            type="text"
            @click="deleteQuestion"
            >删除</el-button
          >
        </div>
      </div>

      <!-- 单选题 -->
      <template v-if="data.type == 'radio'">
        <el-radio-group v-model="myValue">
          <el-radio
            :label="option.id"
            v-for="(option,index) in data.options"
            :key="option.id"
            class="radio-item"
            >{{ option.title }}</el-radio
          >
        </el-radio-group>
      </template>

      <!-- 多选题 -->
      <template v-if="data.type == 'checkbox'">
        <el-checkbox-group v-model="myValue">
          <div
            class="text item"
            v-for="(option, index) in data.options"
            :key="option.id"
          >
            <el-checkbox :label="option.id" style="margin: 5px">{{
              option.title
            }}</el-checkbox>
          </div>
        </el-checkbox-group>
      </template>

      <!-- 填空题 -->
      <template v-if="data.type == 'text'">
        <el-input
          type="textarea"
          :rows="textRow"
          resize="none"
          v-model="myValue"
        >
        </el-input>
      </template>
    </el-card>
  </div>
</template>

<script>
export default {
  props: {
    data: {},
    index: {},
    value: {
      default: "",
    },
    showButton: {
      default: true,
    },
  },
  computed: {
    myValue: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit("input", val);
      },
    },
    textRow() {
      if (this.data && this.data.attrs && this.data.attrs.row) {
        return this.data.attrs.row;
      }
      return 1;
    },
  },
  data() {
    return {};
  },
  methods: {
    editQuestion() {
      this.$emit("edit", this.index);
    },
    deleteQuestion() {
      this.$emit("delete", this.index);
    },
  },
};
</script>
<style scope>
.q-item .box-card {
  text-align: left;
}
.q-item .clearfix {
  display: flex;
  justify-content: space-between;
}
.q-item .right-button {
  width: 80px;
  flex-shrink: 0;
}
.q-item .radio-item {
  display: block;
  margin: 5px;
}
</style>