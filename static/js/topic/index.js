/**
 * for /topic/index.html
 */

function trim(str) {
  return str.replace(/(^\s+)|(\s+$)/g, "");
}


$(document).ready(function() {
    $('.ui.checkbox').checkbox();
});

/**
 * 显示修改当前话题的modal
 * @param topic_hashid
 */
function show_modify_topic_modal(topic_hashid) {
    $("#modify-topic-title").val($("#show-title").text());
    $("#modify-topic-abstract").val($("#show-abstract").text());
    if (trim($("#topic-top-status").text()) == "1") {
        $("#modify-topic-top-status").prop('checked', true);
    }
    $('#modify-topic-modal').modal('show');
}

/**
 * 修改当前话题
 * @param topic_hashid
 */
function modify_topic(topic_hashid) {
    var msg = $("#modify-topic-error-message");
//    msg.text("测试").show();
    var new_title = trim($("#modify-topic-title").val());
    var new_abstract = trim($("#modify-topic-abstract").val());
    var new_top_status = 0;
    if ($("#modify-topic-top-status").is(':checked')) {
        new_top_status = 1;
    }
    var _xsrf = $( "input[name='_xsrf']").val();
    if (new_title.length == 0) {
        msg.text("标题内容不能为空！").show();
        return;
    }
//    $("#show-title").text("asdasfd");
//    $("#show-abstract").text("asdasfdafdsdfsf");
    msg.text("更新中...").show();
    var new_topic = {"title": new_title,
        "abstract": new_abstract,
        "topic_hashid": topic_hashid,
        "top_status": new_top_status,
        "_xsrf": _xsrf}
//    alert(new_top_status);
    var post = $.post( "/modify/topic", new_topic, "json");
    post.success(function(data) {
            if (data.success === true) {
                $("#show-title").text(new_title);
                $("#show-abstract").text(new_abstract);
                $('#modify-topic-modal').modal('hide');
                $("#topic-top-status").text(new_top_status+"");
                msg.text("").hide();
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

/**
 * 显示添加链接的modal
 */
function show_add_link_modal() {
    $('#add-link-modal').modal('show');
}

/**
 * 为话题topic_hashid添加链接
 * @param topic_hashid
 */
function add_link(topic_hashid) {
    var msg = $("#add-link-error-message");
//    msg.text("测试").show();
    var url = trim($("#add-link-url").val());
    var title = trim($("#add-link-title").val());
    var abstract = trim($("#add-link-abstract").val());
    var top_status = 0;
    if ($("#add-link-top-status").is(':checked')) {
        top_status = 1;
    }
    var _xsrf = $( "input[name='_xsrf']").val();
    if (title.length == 0 || url.length == 0) {
        msg.text("url和标题都不能为空！").show();
        return;
    }
    msg.text("添加中...").show();
    var new_link = {"title": title,
        "url": url,
        "abstract": abstract,
        "topic_hashid": topic_hashid,
        "top_status": top_status,
        "_xsrf": _xsrf}
    var post = $.post( "/new/link", new_link, "json");
    post.success(function(data) {
            if (data.success === true) {
                window.location.href=data.redirect;
                $('#add-link-modal').modal('hide');
                msg.text("").hide();
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

/**
 * 显示修改链接的modal
 * @param link_hashid
 */
function show_modify_link_modal(link_hashid) {
    var old1 = $("#link-item-"+link_hashid);
    var old2 = $("#link-item-"+link_hashid+"-abstract");
    var old_url = trim(old1.attr("href"));
    var old_title = trim(old1.text());
    var old_abstract = trim(old2.text());
    var old_top_status = trim($("#link-item-"+link_hashid+"-top-status").text());
    console.log("#link-item-"+link_hashid+"-top-status");
    console.log(old_top_status);
//    alert(old_top_status);
    if (old_top_status == "1") {
        $("#modify-link-top-status").prop('checked', true);
    }

    if (old_top_status == "0") {
        $("#modify-link-top-status").prop('checked', false);
    }

    $("#modify-link-url").val(old_url);
    $("#modify-link-title").val(old_title);
    $("#modify-link-abstract").text(old_abstract);
    $("#modify-link").attr('onclick', "modify_link(\'"+link_hashid+"\')");
    $('#modify-link-modal').modal('show');
}

/**
 * 修改链接
 * @param link_hashid
 */
function modify_link(link_hashid) {
    var msg = $("#modify-link-error-message");
    var url =trim($("#modify-link-url").val());
    var title = trim($("#modify-link-title").val());
    var abstract = trim($("#modify-link-abstract").val());
//    msg.text(url+title+abstract).show();
    var _xsrf = $( "input[name='_xsrf']").val();
    if (title.length == 0 || url.length == 0) {
        msg.text("url和标题都不能为空！").show();
        return;
    }

//    if (url.indexof("http://") == -1 && url.indexof("https://") == -1 && url.indexof("ftp://") == -1) {
//
//    }

    var top_status = 0;
    if ($("#modify-link-top-status").is(':checked')) {
        top_status = 1;
    }

    msg.text("更新中...").show();
    var modified_link = {
        "title": title,
        "url": url,
        "abstract": abstract,
        "link_hashid": link_hashid,
        "top_status": top_status,
        "_xsrf": _xsrf}
    var post = $.post( "/modify/link", modified_link, "json");
    post.success(function(data) {
            if (data.success === true) {
                var old1 = $("#link-item-"+link_hashid);
                var old2 = $("#link-item-"+link_hashid+"-abstract");
                old1.attr("href", url);
                old1.text(title);
                old2.text(abstract);
                $("#link-item-"+link_hashid+"-top-status").text(top_status+"");

                var par = $("#link-item-"+link_hashid+"-top-status").parent();

                if (top_status == 1) {
                    par.children(".ui.label").remove();
                    par.prepend("<div class=\'ui label\'>置顶</div>");
                }
//                alert(top_status);
                if (top_status == 0) {
                    par.children(".ui.label").remove();
                }

                $('#modify-link-modal').modal('hide');
                msg.text("").hide();
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

/**
 * 删除链接
 * @param link_hashid
 */

function delete_link(link_hashid) {
    var title = trim($("#link-item-"+link_hashid).text());

    if (!confirm("确定删除\""+title+"\"？")) {
        return;
    }
    var _xsrf = $( "input[name='_xsrf']").val();
    var post = $.post( "/delete/link", {"link_hashid": link_hashid, "_xsrf": _xsrf}, "json");
    post.success(function(data) {
            if (data.success === true) {
                $('#div-item-'+link_hashid).hide();
                return;
            }
            if (data.success === false) {
            }
        });
    post.error(function(){

        });
}

/**
 * 删除话题
 */

function delete_topic(topic_hashid) {

    if (!confirm("确定删除当前话题？")) {
        return;
    }
    var _xsrf = $( "input[name='_xsrf']").val();
    var post = $.post( "/delete/topic", {"topic_hashid": topic_hashid, "_xsrf": _xsrf}, "json");
    post.success(function(data) {
            if (data.success === true) {
                window.location.href=data.redirect;
                return;
            }
            if (data.success === false) {
                alert(data.info);
            }
        });
    post.error(function(){

        });
}


/**
 * 收藏/取消收藏某话题
 * @param action
 * @param topic_hashid
 */
function star_topic(action, topic_hashid) {
    if (action != "unstar" && action!="star") {
        return;
    }
    var _xsrf = $( "input[name='_xsrf']").val();
    var post = $.post( "/star/topic",
        {"topic_hashid": topic_hashid, "action":action, "_xsrf": _xsrf},
        "json");
    post.success(function(data) {
            if (data.success === true) {
                if (action=="unstar") {
                    $("#star_topic").removeClass("orange");
                    $("#star_topic_a").attr("title", "收藏该话题");
                    $("#star_topic_a").attr("onclick", "star_topic('star', '"+topic_hashid+"')");
                    $("#star_num").text(parseInt($("#star_num").text())-1);
                } else {
                    $("#star_topic").addClass("orange");
                    $("#star_topic_a").attr("title", "取消收藏该话题")
                    $("#star_topic_a").attr("onclick", "star_topic('unstar', '"+topic_hashid+"')")
                    $("#star_num").text(parseInt($("#star_num").text())+1);
                }
                return;
            }
            if (data.success === false) {
                alert(data.info);
            }
        });
    post.error(function(){

        });

}