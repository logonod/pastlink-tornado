function trim(str) {
  return str.replace(/(^\s+)|(\s+$)/g, "");
}


$(document)
.ready(function() {

    function do_login() {
        var email = trim($("#email").val());
        var password = trim($("#password").val());
        var _xsrf = $( "input[name='_xsrf']").val();
        var msg = $("#error-message");
        if (email.length == 0 || password.length == 0) {
            msg.text("请检查输入内容").show();
            return;
        }
        msg.text("登录中...").show();
        var post = $.post( "/login", {"email": email, "password": password, "_xsrf": _xsrf} , "json");
        post.success(function(data) {
//                alert(data);
                if (data.success === true) {
                    window.location.href=data.redirect;
                    return;
                }
                if (data.success === false) {
                    msg.text(data.info).show();
                }
            });
        post.error(function(){
                msg.text("请求错误，请稍后再试.").show();
            });

    }
    $('#login').click(do_login);
});