<!-- src/App.vue -->
<template>
  <router-view />
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App'
})
</script>

<style>
#app {
  background-color: #ebe1d7; /* 背景颜色 */
  min-height: 100vh; /* 确保背景颜色覆盖整个视窗高度 */
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-left: 0px;
  padding: 0;
}
</style>
