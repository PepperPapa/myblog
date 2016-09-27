// wait for all html load ready
window.onload = function() {
  // 注册失败返回error信息处理
  function regErrorCheck() {
    var error = window.location.search;
    var pattern = /\?error=(.*)/; // 不能附加g
    var match = pattern.exec(error);
    if (match) {
      var error_info = match[1];
      var $error_login = document.querySelector(".error-login");
      $error_login.innerText = error_info.replace(/%20/g, " ");
    }
  }
  regErrorCheck();
};
