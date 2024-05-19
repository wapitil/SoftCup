// document.addEventListener("DOMContentLoaded", function () {
//   const registerForm = document.getElementById("registerForm");
//   registerForm.addEventListener("submit", function (event) {
//     event.preventDefault();
//     // 处理注册逻辑
//     alert("注册成功");
//     toggleForms();
//   });

//   const loginForm = document.getElementById("loginForm");
//   loginForm.addEventListener("submit", function (event) {
//     event.preventDefault();
//     // 处理登录逻辑（例如验证用户名和密码）
//     // 如果登录成功，将用户重定向到主界面
//     window.location.href = "index.html";
//   });
// });

function toggleForms() {
  const formContainer = document.querySelector(".form-container");
  const registerForm = document.getElementById("register-form");
  const loginForm = document.getElementById("login-form");

  if (registerForm.classList.contains("active")) {
    formContainer.style.transform = "translateX(-50%)";
    registerForm.classList.remove("active");
    loginForm.classList.add("active");
  } else {
    formContainer.style.transform = "translateX(0%)";
    loginForm.classList.remove("active");
    registerForm.classList.add("active");
  }
}

function startFaceRecognitionLogin() {
  document.getElementById("face-recognition-modal").style.display = "flex";
  startVideo();
}

function startFaceRecognitionRegister() {
  document.getElementById("face-recognition-modal").style.display = "flex";
  startVideo();
}

function closeModal() {
  document.getElementById("face-recognition-modal").style.display = "none";
  stopVideo();
}

function startVideo() {
  const video = document.getElementById("video");
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((stream) => {
      video.srcObject = stream;
    })
    .catch((err) => {
      console.error("Error accessing the camera: " + err);
    });
}

function stopVideo() {
  const video = document.getElementById("video");
  const stream = video.srcObject;
  const tracks = stream.getTracks();

  tracks.forEach((track) => {
    track.stop();
  });

  video.srcObject = null;
}

function captureFace() {
  const video = document.getElementById("video");
  const canvas = document.getElementById("canvas");
  const context = canvas.getContext("2d");
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  document.getElementById("submitFaceButton").style.display = "block";
}

function submitFaceData() {
  const canvas = document.getElementById("canvas");
  const faceData = canvas.toDataURL("image/png");
  // 在这里将 faceData 发送到服务器以保存人脸数据
  alert("人脸数据已提交");
  closeModal();
  toggleForms(); // 在成功提交人脸数据后切换到登录表单
}

document
  .getElementById("registerForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // 阻止表单默认提交行为

    let userData = {
      name: document.getElementById("name").value,
      password: document.getElementById("password").value,
      role: document.getElementById("role").value,
      face_image_enabled: document.getElementById("face_image_enabled").checked,
      face: "", // 人脸数据，如果启用了人脸识别并已通过其他方式收集
    };

    // TODO: 这里添加获取人脸图像数据的逻辑，如果启用了人脸识别功能

    // 发送数据到后端
    fetch("http://127.0.0.1:5001/register", {
      // 确保路径正确
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userData),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
