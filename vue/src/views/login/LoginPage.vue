<!-- 注册 -->
<template>
  <div class="sign-container">
    <div class="sign-form">
      <h1>Welcome!</h1>
      <el-input v-model="username" class="input-field" placeholder="Please input username">
        <template #prepend>
          <el-icon :size="18"><User /></el-icon>
        </template>
      </el-input>
      <el-input
        v-model="password"
        class="input-field"
        type="password"
        placeholder="Please input password"
        show-password
        :rules="passwordRules"
      >
        <template #prepend>
          <el-icon :size="18"><Lock /></el-icon>
        </template>
      </el-input>
      <el-input
        v-model="checkPassword"
        class="input-field"
        type="password"
        placeholder="Please check password"
        show-password
      >
        <template #prepend>
          <el-icon :size="18"><Lock /></el-icon>
        </template>
      </el-input>
      <div class="radio-group">
        <label>身 份：</label>
        <el-radio-group v-model="role">
          <el-radio value="student">学生</el-radio>
          <el-radio value="admin">管理员</el-radio>
        </el-radio-group>
      </div>
      <div class="radio-group">
        <label>登记人脸信息？：</label>
        <el-radio-group v-model="faceLoginEnabled">
          <el-radio value="False">No</el-radio>
          <el-radio value="True">Yes</el-radio>
        </el-radio-group>
      </div>
      <a-button
        type="primary"
        style="background-color: cornflowerblue; width: 340px; margin-top: 10px"
        @click="handleSubmit"
      >
        注册
      </a-button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, toRefs } from 'vue'
import axios from 'axios'

// 响应式对象
const state = reactive({
  username: '',
  password: '',
  checkPassword: '',
  role: 'student',
  faceLoginEnabled: 'False'
})

// 解构响应式对象
const { username, password, checkPassword, role, faceLoginEnabled } = toRefs(state)

// 提交表单
const handleSubmit = async () => {
  if (password.value !== checkPassword.value) {
    alert('Passwords do not match')
    return
  }

  const formData = {
    name: username.value,
    password: password.value,
    role: role.value,
    face_login_enabled: faceLoginEnabled.value === 'True' // 转换为布尔值
    // face_image 可以从另一个字段或文件上传中获取
  }

  try {
    const response = await axios.post('/api/login', formData)
    console.log('Success:', response.data)
    alert('Registration successful')
  } catch (error) {
    console.error('Error:', error)
    alert('Registration failed')
  }
}
// 密码验证规则
const passwordRules = [
  { required: true, message: 'Please input your password', trigger: 'blur' },
  { pattern: /^.{6,20}$/, message: 'Password must be 6 to 20 characters', trigger: 'blur' }
]
</script>

<style scoped>
.radio-label {
  margin-right: 10px;
  font-size: 16px; /* 调整字体大小 */
}
.input-field {
  width: 340px;
  margin-bottom: 10px;
}
.radio-group {
  display: flex;
  align-items: center;
  margin-top: 2px;
  text-align: left;
  width: 340px;
  margin-left: 20px;
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
