// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../views/home/MainLayout.vue'
import TestVue from '../views/home/TestVue.vue'
import InfoVideo from '../views/home/InfoVideo.vue'
import LoginPage from '../views/login/LoginPage.vue'
import SignPage from '../views/login/SignPage.vue'

const routes = [
  {
    // 登陆界面
    path: '/',
    name: 'sign',
    component: SignPage
  },
  {
    // 注册界面
    path: '/login',
    name: 'login',
    component: LoginPage
  },
  {
    // 学生主页
    path: '/student',
    name: 'student_home',
    component: MainLayout
  },
  {
    // 视频中心
    path: '/info_video',
    name: 'info_video',
    component: InfoVideo
  },
  {
    // 测试界面
    path: '/test',
    name: 'Test',
    component: TestVue
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // 使用 import.meta.env.BASE_URL
  routes
})

export default router
