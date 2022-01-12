function toggle_like(post_id, type) {
    console.log(post_id,type)
    let $a_like = $(`#${post_id} a.lecture_like`);
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