/**
 * for /link/index.html
 */

function trim(str) {
  return str.replace(/(^\s+)|(\s+$)/g, "");
}


/**
 * 收藏/取消收藏某链接
 * @param action
 * @param link_hashid
 */
function star_link(action, link_hashid) {
    if (action != "unstar" && action!="star") {
        return;
    }
    var _xsrf = $( "input[name='_xsrf']").val();
    var post = $.post( "/star/link",
        {"link_hashid": link_hashid, "action":action, "_xsrf": _xsrf},
        "json");
    post.success(function(data) {
            if (data.success === true) {
                if (action=="unstar") {
                    $("#star_link").removeClass("orange");
                    $("#star_link_a").attr("title", "收藏该链接");
                    $("#star_link_a").attr("onclick", "star_link('star', '"+link_hashid+"')");
                    $("#star_num").text(parseInt($("#star_num").text())-1);
                } else {
                    $("#star_link").addClass("orange");
                    $("#star_link_a").attr("title", "取消收藏该链接")
                    $("#star_link_a").attr("onclick", "star_link('unstar', '"+link_hashid+"')");
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