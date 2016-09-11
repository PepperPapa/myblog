// wait for all html load ready
window.onload = function() {
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
};
