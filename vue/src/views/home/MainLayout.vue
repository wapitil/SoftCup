<template>
  <el-container class="full-height-container">
    <!-- Header -->
    <HeaderComponent />
    <!-- Header -->
    <el-main>
      <!-- StudentMainPage -->
      <CenterComponent />
      <!-- <InfoComponent /> -->
      <AiComponent />
      <!-- StudentMainPage -->
    </el-main>
    <!-- <el-footer class="footer">Footer</el-footer> -->
  </el-container>
</template>

<script lang="ts" setup>
import HeaderComponent from './HeaderComponent.vue'
import CenterComponent from './CenterComponent.vue'
import AiComponent from './AiComponent.vue'
// import InfoComponent from './InfoComponent.vue'
// import TestVue from './TestVue'
</script>

<style scoped>
/* 容器为 display: flex 并将 flex-direction 设置为 column，使其内部的子元素按列方向排列。 */
.full-height-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* 设置 .el-main 为 flex: 1，使其在容器中进行扩展，占据剩余的可用空间。 */
/* flex: 1 应该只用于那些需要扩展以填充可用空间的元素（例如主内容区）。 */
.el-main {
  flex: 1;
}
</style>
