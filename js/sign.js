// wait for all html load ready
window.onload = function() {
  // 两次输入密码是否相同验证
  var $btn_signup = document.getElementById("btn-signup");
  var $pwd_verify = document.querySelector("input[name=verify]");

  $btn_signup.addEventListener("click", function() {
    var $input_pwd = document.querySelectorAll("input[type=password]");
    if ($input_pwd[0].value !== $input_pwd[1].value) {
      $pwd_verify.setCustomValidity("两次输入的密码不一致");
    } else {
      $pwd_verify.setCustomValidity("");  // 取消错误提示
    }
  });

  // 注册失败返回error信息处理
  function regErrorCheck() {
    var error = window.location.search;
    var pattern = /\?error=user%20(.*)%20already%20exits./; // 不能附加g
    var match = pattern.exec(error);
    if (match) {
      var error_user = match[1];
      var $username = document.querySelector("input[name=username]");
      $username.value = error_user;
      var $error_username = document.querySelector(".error-username");
      $error_username.innerText = "用户名已经存在...";
    }
  }
  regErrorCheck();
};
