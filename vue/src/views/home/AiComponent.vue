<template>
  <!-- AI -->
  <!-- 弹出框整体位置 -->
  <div class="affix-container">
    <!-- 锚点 -->
    <el-affix position="bottom">
      <el-popover popper-style="height: 470px;" placement="top" :width="400" trigger="click">
        <!-- 弹出按钮 -->
        <template #reference>
          <div class="icon-button"></div>
        </template>

        <!-- 弹出框内部高度 -->

        <!-- 聊天展示界面 -->
        <el-row style="height: 400px; overflow-y: auto" ref="chatBox">
          <el-col>
            <!-- 初始消息 -->
            <div class="ai-message">
              <a-comment
                author="Wapiti"
                avatar="https://raw.githubusercontent.com/wapitil/SoftCup/main/ref/pets.png"
              >
                <template #content>
                  <div class="message-content">Hello, How can I help you today?</div>
                </template>
              </a-comment>
            </div>
            <!-- 动态消息 -->
            <div
              v-for="(message, index) in messages"
              :key="index"
              class="message"
              :class="{
                'user-message': message.sender === 'user',
                'ai-message': message.sender === 'ai'
              }"
            >
              <a-comment
                :author="message.sender === 'user' ? 'User' : 'Wapiti'"
                :avatar="message.sender === 'ai' ? aiAvatar : ''"
              >
                <template #content>
                  <div class="message-content">{{ message.text }}</div>
                </template>
              </a-comment>
            </div>
            <!-- AI 回复 -->
            <div v-if="typing" class="ai-message">
              <a-comment author="Wapiti" :avatar="aiAvatar">
                <template #content>
                  <div class="message-content">{{ currentReply }}</div>
                </template>
              </a-comment>
            </div>
          </el-col>
        </el-row>
        <!-- 输入框 -->
        <el-row style="height: 50px">
          <el-col>
            <el-input v-model="input" style="max-width: 380px" placeholder="Please input">
              <template #append>
                <el-button @click="handleEntry">Entry</el-button>
              </template>
            </el-input>
          </el-col>
        </el-row>
      </el-popover>
    </el-affix>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'

const input = ref('')
const messages = ref<{ sender: string; text: string }[]>([])
const chatBox = ref<HTMLElement | null>(null)
const typing = ref(false)
const currentReply = ref('')

const aiAvatar = 'https://raw.githubusercontent.com/wapitil/SoftCup/main/ref/pets.png'

const handleEntry = async () => {
  if (input.value.trim() === '') return

  // Add user's message
  messages.value.push({ sender: 'user', text: input.value })
  typing.value = true
  currentReply.value = ''

  try {
    const response = await axios.post('http://192.168.196.117:5001/spark_ai', {
      user_input: input.value
    })
    if (response.data && response.data.data && response.data.data.answer) {
      // 流式显示 AI 回复
      const answer = response.data.data.answer
      let index = 0
      const intervalId = setInterval(() => {
        if (index < answer.length) {
          currentReply.value += answer[index]
          index++
        } else {
          clearInterval(intervalId)
          messages.value.push({ sender: 'ai', text: currentReply.value })
          typing.value = false
        }
      }, 50)
    } else {
      messages.value.push({ sender: 'ai', text: 'Unexpected response format' })
      console.error('Unexpected response format:', response)
      typing.value = false
    }
  } catch (error) {
    console.error('Error:', error)
    messages.value.push({ sender: 'ai', text: 'Error communicating with AI' })
    typing.value = false
  }

  // 清空输入框
  input.value = ''

  // 滚动到底部
  nextTick(() => {
    if (chatBox.value) {
      chatBox.value.scrollTop = chatBox.value.scrollHeight
    }
  })
}

onMounted(() => {
  if (chatBox.value) {
    chatBox.value.scrollTop = chatBox.value.scrollHeight
  }
})
</script>

<style scoped>
/* 确保消息内容不超出聊天框 */
.message-content {
  max-width: 300px;
  word-wrap: break-word;
  white-space: pre-wrap; /* 允许文本换行 */
  background-color: #f0f0f0; /* 示例背景颜色 */
  padding: 10px; /* 内边距 */
  border-radius: 10px; /* 圆角 */
}

.el-popover__reference-wrapper {
  display: flex;
  justify-content: flex-end;
}

/* 用户消息和AI消息的容器 */
.user-message {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 10px;
  /* flex-direction: row; 将头像固定在右侧 */
}

.ai-message {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 10px;
}

/* 锚点图标 */
.icon-button {
  width: 50px; /* 设置按钮的宽度和高度 */
  height: 50px;
  background-image: url('@/assets/icons/pets.svg');
  background-size: cover;
  border-radius: 50%;
  cursor: pointer;
}

/* 锚点位置 */
.affix-container {
  position: fixed;
  bottom: 0;
  right: 0;
  margin-bottom: 50px; /* 为了让按钮不贴在屏幕边缘，可以添加一些 margin */
  margin-right: 50px; /* 为了让按钮不贴在屏幕边缘，可以添加一些 margin */
}
</style>
