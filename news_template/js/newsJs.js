/*2018-02-07*/
var clou_slide = tclou_slide = 0, count_slide_l; //初始化轮播索引，间歇调用变量，轮播图片数量
$(function () {
    $(".newsTopBar_ul1 li").click(function () {
        var index = $(this).index();
        $(this).addClass("newsOn1").siblings().removeClass("newsOn1");
        $(".newsTopBar_txt ul").eq(index).show().siblings().hide();
    })

    //轮播图片
    var list_wh = $("#slide_main_ul").width() * -1;
    $("#slide_main_ul").css("margin-left", list_wh / 2);
    //首页banner轮播动画
    count_slide_l = $(".slide_main>div").length;
    $(".slide_main>div:not(:first-child)").hide();
    tclou_slide = setInterval("Cbanner_showImg()", 5000);
    $(".slide_main").parent().hover(function () {
        clearInterval(tclou_slide);
    }, function () {
        tclou_slide = setInterval("Cbanner_showImg()", 5000);
    });
    $(".slide_main_ul li").click(function (event) {
        event.stopPropagation();
        var li_index = $(this).index();
        var show_index = $(".slide_main>div").filter(":visible").index();
        if (li_index != show_index) {
            $(".slide_main>div").filter(":visible").fadeOut(500).parent().children().eq(li_index).fadeIn(600);
            $(this).addClass("slide_main_on").siblings().removeClass("slide_main_on");
            clou_slide = li_index;
        }
    });
})

//显示图片
function Cbanner_showImg() {
    clou_slide = clou_slide >= (count_slide_l - 1) ? 0 : ++clou_slide;  //n的值 0 ，1 ，2...
    $(".slide_main_ul li").eq(clou_slide).trigger("click");
}