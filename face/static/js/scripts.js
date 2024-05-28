document.addEventListener("DOMContentLoaded", function () {
  const registerForm = document.getElementById("registerForm");
  const loginForm = document.getElementById("loginForm");

  registerForm.addEventListener("submit", function (event) {
    event.preventDefault();

    var username = document.getElementById("registerUsername").value;
    var password = document.getElementById("registerPassword").value;
    var confirmpassword = document.getElementById("confirmPassword").value;
    var role = document.getElementById("registerRole").value;

    var usernameLimit = /^[a-zA-Z0-9]{6,10}$/;
    var passwordLimit = /^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d.!?]{6,16}$/;
    var nameerror = document.getElementById("registernameerror");
    var passerror = document.getElementById("registerpasserror");
    var confirmpasserror = document.getElementById("confirmpasserror");

    if (!usernameLimit.test(username)) {
      nameerror.style.display = "block";
      nameerror.innerHTML =
        "<p>用户名长度应在6-10位字符,且应包含字母和阿拉伯数字</p>";
      return;
    } else {
      nameerror.style.display = "none";
    }

    if (!passwordLimit.test(password)) {
      passerror.style.display = "block";
      passerror.innerHTML =
        "<p>密码长度应在6-16位字符,且应包含字母和阿拉伯数字</p>";
      return;
    } else {
      passerror.style.display = "none";
    }

    if (password !== confirmpassword) {
      confirmpasserror.style.display = "block";
      confirmpasserror.innerHTML = "<p>两次输入的密码不一致，请重新输入</p>";
      return;
    } else {
      confirmpasserror.style.display = "none";
    }

    fetch("/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password,
        confirmpassword: confirmpassword,
        role: role,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        alert(data.message);
        if (data.message === "注册成功") {
          toggleForms();
        }
      });
  });

  loginForm.addEventListener("submit", function (event) {
    event.preventDefault();

    var username = document.getElementById("loginUsername").value;
    var password = document.getElementById("loginPassword").value;
    var role = document.getElementById("loginRole").value;

    fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password,
        role: role,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        alert(data.message);
      });
  });
});

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

// 其他人脸识别相关的函数
function startFaceRecognition() {
  document.getElementById("face-Recognition-modal").style.display = "flex";
  document.getElementsByClassName("get-face")[0].style.display = "block";
  document.getElementsByClassName("reget-face")[0].style.display = "none";
  document.getElementsByClassName("submitFaceButton")[0].style.display = "none";
  startVideo();
}

function closeModal() {
  document.getElementById("face-Recognition-modal").style.display = "none";
  video.style.visibility = "visible";
  canvas.style.visibility = "hidden";
  stopVideo();
}

function regetFace() {
  closeModal();
  startFaceRecognition();
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

  if (video.readyState === 4) {
    video.style.visibility = "hidden";
    canvas.style.visibility = "visible";
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    document.getElementsByClassName("get-face")[0].style.display = "none";
    document.getElementsByClassName("reget-face")[0].style.display =
      "inline-block";
    document.getElementsByClassName("submitFaceButton")[0].style.display =
      "inline-block";
  } else {
    console.error("视频还未准备好，无法捕获帧。");
  }
}

function submitFaceData() {
  const canvas = document.getElementById("canvas");
  const faceData = canvas.toDataURL("image/png");
  alert("人脸数据已提交");
  if (!registerOrLogin) {
    closeModal();
    document.getElementById("submitFaceButton").style.display = "none";
    toggleForms();
  } else {
    closeModal();
    document.getElementById("submitFaceButton").style.display = "none";
    alert("登录成功");
  }
}
