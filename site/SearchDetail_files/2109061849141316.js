// getCookieMode获取政务服务网的cookie值，该函数应放在判断本页面是否为老年版前
function getCookieMode(callback, failCallback) {
  $.ajax({
    type: "get",
    url: "https://www.zjzwfw.gov.cn/zjservice/home/getcookie.do",
    dataType: "jsonp",
    async: true,
    jsonp: "callback",
    success: function (res) {
      typeof callback === "function" && callback(res);
    },
    error: function (err) {
      typeof failCallback === "function" && failCallback(err);
    }
  });
}
// 进入老年版同步状态给政务服务网创建cookie
function _setCookiemode() {
  $.ajax({
    type: "get",
    url: "https://www.zjzwfw.gov.cn/zjservice/home/setcookie.do?mode=2",
    dataType: "jsonp"
  });
}
// 退出老年版同步状态给政务服务网删除cookie
function _delCookiemode() {
  $.ajax({
    type: "get",
    url: "https://www.zjzwfw.gov.cn/zjservice/home/delcookie.do",
    dataType: "jsonp",
    jsonp: "jsonpCallback"
  });
}

$(function(){
  // 无障碍js
    var script = document.createElement("script");
    script.setAttribute("defer", "");
    script.setAttribute("async", "");
    script.type = "text/javascript";
    script.src = "//wza.zj.gov.cn/cniil/assist.js?sid=11963&pos=left&bar=0";
    $("body").append(script);
})
