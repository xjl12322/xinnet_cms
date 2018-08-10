$(function () {
    FastClick.attach(document.body);  //解决zeptoJs点透问题
    $(".mobNewscon3_ul li a").on("tap", function () {
        var index = $(this).parent().index();
        $(this).addClass("newOn").parent().siblings().find("a").removeClass("newOn");
        $(this).parents("ul").next().find("div").eq(index).show().siblings().hide();
    })
    //mob轮播
    var slide = $(".slide_main");
    var li_index = $(".slide_index li");
    var width1 = $("body").width();
    var len1 = $(".slide_main li").length;
    $(".slide_main li").width(width1);
    slide.width(width1 * len1);
    var lists = "";
    for (var i = 0; i < len1; i++) {
        lists += "<li></li>";
    }
    $(".slide_index").append(lists).find("li").eq(0).addClass("on");
    var index_on = 0;
    var aniSlide = function () {
        if (index_on > len1 - 1) {
            index_on = 0;
        }
        else if (index_on < 0) {
            index_on = len1 - 1;
        }
        slide.animate({"transform": "translate(" + (index_on * width1 * -1) + "px)"}, 300, "ease", function () {
            $(".slide_index li").removeClass("on").eq(index_on).addClass('on');
            //判断timeId的值如果为undefined说明我们干掉了计时器这是要重新开启定时器
            if (timeId == undefined) {
                timeId = setInterval(function () {
                    index_on++;
                    aniSlide();
                }, 3000);
            }
        })
    }
    //定时器自动轮播
    var timeId = setInterval(function () {
        //对index进行累加  
        index_on++;
        //调用移动ul的方法  
        aniSlide();
    }, 3000);
    //左右滑动的右滑动  
    slide.swipeRight(function () {
        clearInterval(timeId);
        //这里要记住尽管计时器清楚了但是timeId一直都在  
        timeId = undefined;
        index_on--;
        //调用移动ul的方法  
        aniSlide();
    });
    slide.swipeLeft(function () {
        clearInterval(timeId);
        //这里要记住尽管计时器清楚了但是timeId一直都在  
        timeId = undefined;
        index_on++;
        //调用移动ul的方法  
        aniSlide();
    });
    //mob轮播 end
})