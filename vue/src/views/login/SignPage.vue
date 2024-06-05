<template>
  <div class="sign-container">
    <div class="sign-form" v-if="!showFaceScanner">
      <!-- 输入用户名 -->
      <h1>Sign In!</h1>
      <el-input v-model="input.username" class="input-field" placeholder="Please input username">
        <template #prepend>
          <el-icon :size="18"><User /></el-icon>
        </template>
      </el-input>
      <!-- 输入密码 -->
      <el-input
        v-model="input.password"
        class="input-field"
        type="password"
        placeholder="Please input password"
        show-password
      >
        <template #prepend>
          <el-icon :size="18"><Lock /></el-icon>
        </template>
      </el-input>
      <!-- 忘记密码？ -->
      <div style="text-align: right; margin-top: 10px">
        <el-button type="primary" key="primary" link> 忘记密码？ </el-button>
      </div>
      <!-- 登陆 -->
      <a-button
        type="primary"
        style="background-color: cornflowerblue; width: 340px; margin-top: 10px"
        @click="signin"
        >登陆</a-button
      >
      <el-divider>
        <p>Or</p>
      </el-divider>
      <!-- 人脸登陆 -->
      <el-button type="warning" circle @click="toggleFaceLogin">
        <el-icon :size="18"><View /></el-icon>
      </el-button>
      <label style="margin-left: 13px">人脸登陆</label>

      <div style="text-align: right; margin-top: 10px">
        <label>没有账户？</label>
        <el-button type="primary" key="primary" link @click="login"> 注册账号 </el-button>
      </div>
    </div>
    <div v-else>
      <FaceScanner />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import axios from 'axios'
import FaceScanner from './FaceScanner.vue'

// 输入
const input = reactive({
  username: '',
  password: ''
})

// 显示人脸识别组件的状态
const showFaceScanner = ref(false)

// 切换人脸识别组件的显示状态
const toggleFaceLogin = () => {
  showFaceScanner.value = !showFaceScanner.value
}

// 跳转注册账号界面
const login = () => {
  window.location.href = 'http://localhost:5173/login'
}

// 登录账号
const signin = async () => {
  try {
    console.log('Sending sign-in request with:', input.username, input.password)
    // 登陆请求
    const response = await axios.post('/api/signin', {
      name: input.username,
      password: input.password
    })
    console.log('Response from sign-in:', response.data)
    if (response.data.error_code === 0) {
      window.location.href = 'http://localhost:5173/student'
    } else {
      alert('登陆失败: ' + response.data.msg)
    }
  } catch (error) {
    console.error('Error during sign-in:', error)
    // alert('登陆失败: ' + error.message)
  }
}
</script>

<style scoped>
.radio-label {
  margin-right: 10px;
  margin-left: 18px;
  font-size: 16px; /* 调整字体大小 */
}
/*为输入框设置统一的宽度和底部边距，确保输入框之间有间距。*/
.input-field {
  width: 340px;
  margin-bottom: 10px;
}
/* 为单选按钮组设置宽度和上边距，并使其与输入框左对齐。 */
.radio-group {
  margin-top: 2px;
  text-align: left;
  width: 340px;
  /* margin-left: 10px; */
}
.sign-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.sign-form {
  max-width: 400px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
