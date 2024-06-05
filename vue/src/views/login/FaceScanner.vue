<!-- FaceScanner.vue -->
<template>
  <div class="face-scanner">
    <video ref="webcam" autoplay playsinline></video>
    <button @click="capturePhoto" class="capture-button">Capture</button>
    <p v-if="feedback" :class="{ success: feedback.success, error: !feedback.success }">
      {{ feedback.message }}
    </p>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const webcam = ref<HTMLVideoElement | null>(null)
const feedback = ref<{ success: boolean; message: string } | null>(null)

const startWebcam = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true })
    if (webcam.value) {
      webcam.value.srcObject = stream
    }
    console.log('Webcam started')
  } catch (error) {
    console.error('Error accessing webcam: ', error)
  }
}

const capturePhoto = () => {
  if (webcam.value) {
    const video = webcam.value
    const canvas = document.createElement('canvas')
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    const context = canvas.getContext('2d')
    if (context) {
      context.drawImage(video, 0, 0, canvas.width, canvas.height)
      let photo = canvas.toDataURL('image/png') // 将图像转换为 base64 编码
      // 移除 data:image/png;base64, 前缀
      if (photo.startsWith('data:image/png;base64,')) {
        photo = photo.replace('data:image/png;base64,', '')
      }
      console.log('Captured Photo (base64):', photo) // 添加这行以调试输出 base64 编码的图像数据
      faceScan(photo)
    } else {
      console.error('Failed to get canvas context')
    }
  } else {
    console.error('Webcam is not available')
  }
}

const faceScan = async (photo: string) => {
  try {
    console.log('Sending photo to API:', photo) // 调试输出发送的图像数据
    const response = await axios.post('http://192.168.196.117:5001/face_scan', { image: photo })
    console.log('Response from FaceScan:', response.data)
    if (response.data.error_code === 0) {
      feedback.value = { success: true, message: 'FaceScan successful! Redirecting...' }
      setTimeout(() => {
        window.location.href = '/student'
      }, 1000)
    } else {
      feedback.value = { success: false, message: 'FaceScan failed: ' + response.data.error_msg }
    }
  } catch (error) {
    console.error('Error during face_scan:', error)
    feedback.value = { success: false, message: 'FaceScan failed: ' + error.message }
  }
}

onMounted(() => {
  startWebcam()
})
</script>

<style scoped>
.face-scanner {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}
video {
  width: 100%;
  max-width: 400px;
  border-radius: 8px;
  margin-bottom: 16px;
}
.capture-button {
  background-color: #a0522d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}
.capture-button:hover {
  background-color: #8b4513;
}
p {
  margin-top: 10px;
  font-size: 16px;
}
.success {
  color: green;
}
.error {
  color: red;
}
</style>
