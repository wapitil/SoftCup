<template>
  <el-row justify="end" style="background-color:black">
    <el-col :span="2" class="icon-col">
      <el-button size="large" circle>
        <el-icon :size="23"><HomeFilled /></el-icon>
      </el-button>
      <el-button size="large" circle>
        <el-icon :size="23"><UserFilled /></el-icon>
      </el-button>
      <el-button size="large" circle>
        <el-icon :size="23"><Setting /></el-icon>
      </el-button>
    </el-col>
  </el-row>
</template>
<script setup lang="ts"></script>
<style scoped>
/* 控制图标之间的间距 */
.icon-col {
  display: flex;
  justify-content: center;
  margin: 10px;
}
</style>
