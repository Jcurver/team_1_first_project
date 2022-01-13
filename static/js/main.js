function toggle_like(post_id, type) {
    let $a_like = $(`#${post_id} a.lecture-like[aria-label="heart"]`);
    let $i_like = $a_like.find("i");
    let $is_liked = $(`#${post_id} p.liked`);
    if ($i_like.hasClass("xi-heart")) {
        $.ajax({
            type: "POST",
            url:"/api/post/like",
            data: {
                post_id_give:post_id,
                type_give: type,
                action_give: "unlike"
            },
            success: function (response) {
                console.log("unlike");
                $i_like.addClass("xi-heart-o").removeClass("xi-heart");
                $is_liked.find("span").text(response["count"])
            }
        })
    } else {
        $.ajax({
            type: "POST",
            url:"/api/post/like",
            data: {
                post_id_give:post_id,
                type_give: type,
                action_give: "like"
            },
            success: function (response) {
                console.log("like");
                $i_like.addClass("xi-heart").removeClass("xi-heart-o");
                $is_liked.find("span").text(response["count"])
            }
        })
    }
}

function toggle_bookmark(post_id, type) {
    let $a_bookmark = $(`#${post_id} a.lecture-bookmark[aria-label="bookmark"]`);
    let $i_bookmark = $a_bookmark.find("i");
    if ($i_bookmark.hasClass("xi-bookmark")) {
        $.ajax({
            type: "POST",
            url:"/api/post/bookmark",
            data: {
                post_id_give:post_id,
                type_give: type,
                action_give: "unbookmark"
            },
            success: function () {
                console.log("unbookmark");
                $i_bookmark.addClass("xi-bookmark-o").removeClass("xi-bookmark");
            }
        })
    } else {
        $.ajax({
            type: "POST",
            url:"/api/post/bookmark",
            data: {
                post_id_give:post_id,
                type_give: type,
                action_give: "bookmark"
            },
            success: function () {
                console.log("bookmark");
                $i_bookmark.addClass("xi-bookmark").removeClass("xi-bookmark-o");
            }
        })
    }
}
function sign_out() {
    $.removeCookie('mytoken', { path: '/' });
    alert('로그아웃!')
    window.location.href = "/"
}

function toggle_sign_up() {
    $("#sign-up-box").toggleClass("is-hidden")
}