// script.js
const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const startCameraButton = document.getElementById("startCamera");
const snapButton = document.getElementById("snap");
const retakeButton = document.getElementById("retake");
const confirmButton = document.getElementById("confirm");
const stopCameraButton = document.getElementById("stopCamera");
const registerForm = document.getElementById("register-form");
const loginForm = document.getElementById("login-form");
let imageBase64 = "";
let useFaceLogin = false;
let stream = null;

// 打开摄像头
function startCamera() {
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((s) => {
      stream = s;
      video.srcObject = stream;
      document.querySelector(".video-container").style.display = "block";
      snapButton.style.display = "inline-block";
      retakeButton.style.display = "none";
      confirmButton.style.display = "none";
    })
    .catch((err) => {
      console.error("Error accessing the camera: ", err);
    });
}

// 关闭摄像头
function stopCamera() {
  if (stream) {
    stream.getTracks().forEach((track) => track.stop());
    document.querySelector(".video-container").style.display = "none";
  }
}

// 拍照
snapButton.addEventListener("click", () => {
  const context = canvas.getContext("2d");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  imageBase64 = canvas
    .toDataURL("image/png")
    .replace(/^data:image\/(png|jpg);base64,/, "");
  console.log("拍照成功！");
  snapButton.style.display = "none";
  retakeButton.style.display = "inline-block";
  confirmButton.style.display = "inline-block";
});

// 重拍
retakeButton.addEventListener("click", () => {
  snapButton.style.display = "inline-block";
  retakeButton.style.display = "none";
  confirmButton.style.display = "none";
});

// 确认使用拍照
confirmButton.addEventListener("click", () => {
  if (imageBase64) {
    const username = document.getElementById("register-username").value;
    const password = document.getElementById("register-password").value;
    const role = document.querySelector('input[name="role"]:checked').value;

    const requestData = {
      name: username,
      password: password,
      role: role,
      face_login_enabled: 1,
      face_image_base64: imageBase64,
    };
    sendRegisterRequest(requestData);
    stopCamera();
  } else {
    alert("请先拍照");
  }
});

// 注册表单提交
registerForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const username = document.getElementById("register-username").value;
  const password = document.getElementById("register-password").value;
  const role = document.querySelector('input[name="role"]:checked').value;
  useFaceLogin = confirm("是否录入人脸信息？");

  if (!username || !password || !role) {
    alert("信息不完整，请重试！");
    return;
  }

  if (useFaceLogin) {
    startCamera();
  } else {
    const requestData = {
      name: username,
      password: password,
      role: role,
      face_login_enabled: 0,
      face_image_base64: "",
    };
    sendRegisterRequest(requestData);
  }
});

function sendRegisterRequest(data) {
  fetch("/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.msg) {
        alert(data.msg);
      } else {
        alert("注册成功");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("注册过程中发生错误");
    });
}

// 登录表单提交
loginForm.addEventListener("submit", (e) => {
  e.preventDefault();
  useFaceLogin = confirm("是否使用人脸信息进行登录？");

  if (useFaceLogin) {
    startCamera();
    snapButton.style.display = "inline-block";
    snapButton.addEventListener(
      "click",
      () => {
        fetch("/face_login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ image_base64: imageBase64 }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.msg) {
              alert(data.msg);
            } else {
              alert("登录成功");
            }
            stopCamera();
          })
          .catch((error) => {
            console.error("Error:", error);
            alert("登录过程中发生错误");
            stopCamera();
          });
      },
      { once: true }
    );
  } else {
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;
    if (!username || !password) {
      alert("信息不完整，请重试！");
      return;
    }
    fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: username, password: password }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.msg) {
          alert(data.msg);
        } else {
          alert("登录成功");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("登录过程中发生错误");
      });
  }
});

startCameraButton.addEventListener("click", startCamera);
stopCameraButton.addEventListener("click", stopCamera);
