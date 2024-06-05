<template>
  <el-row :gutter="20" class="center-content">
    <el-col :span="7">
      <div class="grid-content ep-bg-purple">
        <button class="custom-button primary" @click="study_click">信息中心</button>
      </div>
    </el-col>
    <el-col :span="7">
      <div class="grid-content ep-bg-purple">
        <button class="custom-button primary" @click="code_click">刷题中心</button>
      </div>
    </el-col>
    <el-col :span="7">
      <div class="grid-content ep-bg-purple">
        <button class="custom-button primary" @click="video_click">视频中心</button>
      </div>
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
// 按钮点击重定向
const study_click = () => {
  window.location.href = 'https://www.baidu.com'
}
const code_click = () => {
  window.location.href = 'http://127.0.0.1:5500/test/test.html'
}
const video_click = () => {
  window.location.href = 'http://localhost:5173/info_video'
}
</script>

<style scoped>
.center-content {
  width: 100%; /* 确保内容的宽度100% */
  display: flex;
  justify-content: center; /* 水平居中对齐子元素 */
}

.grid-content {
  background: #ffffff;
  border-radius: 10px;
  height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.ep-bg-purple {
  background: #f3f3f3;
}

/* 按钮 */
.custom-button {
  width: 100%;
  height: 100%;
  border: none;
  border: 1px solid #ccc; /* 添加边框 */
  color: rgb(0, 0, 0);
  font-size: 25px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  /* box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);浅色投影  */
}

/* 根据不同类名设置背景颜色 */
.custom-button.primary {
  background-color: #f6f5f0;
}

/* hover 悬停界面 */
.custom-button.primary:hover {
  background-color: #eae7d8;
}
</style>
