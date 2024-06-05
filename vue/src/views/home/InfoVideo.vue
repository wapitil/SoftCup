<template>
  <div>
    <HeaderComponent />
    <!-- 走马灯 -->
    <el-carousel :interval="4000" type="card" height="300px">
      <el-carousel-item v-for="item in 4" :key="item">
        <h3 text="2xl" justify="center">{{ item }}</h3>
      </el-carousel-item>
    </el-carousel>
    <!-- 走马灯 -->
    <!--最近观看 -->
    <el-row>
      <el-col :span="4" :offset="2"> <h1 class="custom-title">最近观看</h1></el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="4" :offset="2">
        <v-skeleton-loader :elevation="4" type="card"></v-skeleton-loader>
      </el-col>
      <el-col :span="4">
        <v-skeleton-loader :elevation="4" type="card"></v-skeleton-loader>
      </el-col>
    </el-row>
    <!--最近观看 -->
    <div class="custom-divider"></div>
    <!--资源库 -->
    <el-row>
      <el-col :span="4" :offset="2"> <h1 class="custom-title">资源库</h1></el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="4" :offset="2">
        <v-skeleton-loader :elevation="4" type="card"></v-skeleton-loader>
      </el-col>
      <el-col :span="4">
        <v-skeleton-loader :elevation="4" type="card"></v-skeleton-loader>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import HeaderComponent from './HeaderComponent.vue'
</script>
<style scoped>
/* 标题 */
.custom-title {
  /* margin-left: 100px; */
  margin: 10px auto;
  text-align: left;
}
/* 分割线 */
.custom-divider {
  height: 2px;
  /* background-color: #5c5c5c; */
  width: 65%; /* 设置宽度为50% */
  margin: 20px auto; /*居中对齐并添加上下间距*/
  /* margin-left: 20px; 居中对齐并添加上下间距 */
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
/* 走马灯 */
.el-carousel__item h3 {
  color: #5f5c59;
  opacity: 0.75;
  line-height: 300px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #e6e4e0;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #f5f4f1;
}
</style>
