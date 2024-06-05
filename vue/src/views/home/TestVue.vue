<!-- FaceScanner.vue -->
<template>
  <div class="face-scanner">
    <video ref="webcam" autoplay playsinline></video>
    <button @click="capturePhoto" class="capture-button">Capture</button>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'

const webcam = ref<HTMLVideoElement | null>(null)

const startWebcam = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true })
    if (webcam.value) {
      webcam.value.srcObject = stream
    }
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
    canvas.getContext('2d')?.drawImage(video, 0, 0, canvas.width, canvas.height)
    const photo = canvas.toDataURL('image/png')
    // Handle the photo (send it to the server for face recognition)
    console.log(photo)
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
</style>
