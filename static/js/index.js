/**
 * Created by CQ on 14-9-14.
 */
var username,password,remember;
$(".jobChoose").click(function(){
    switch (this.value){
        case "1":
            $("#jobChose").val(1);
            $("#introduce").text("学神，让你学得笑，笑出声。");
            break;
        case "2":
            $("#jobChose").val(2);
            $("#introduce").text("大牛，比大神更大，岂止于大。");
            break;
        case "3":
            $("#jobChose").val(3);
            $("#introduce").text("弱菜，自己的大事，大块所有人心的大好事。");
            break;
        default :
            break;
    }
})
function msgAdd(msg){
    $("#information").append("<p>"+msg+"</p>");
    document.getElementById("information").scrollTop = document.getElementById("information").scrollHeight;
}
$("#applyAction").click(function(){
    var command =$("#actions").val();
    msgAdd(command+"<br>");
    $("#actions").val("");
    $.post('/main',{orderContent:command}, function(data, textStatus){
        msgAdd(data+"<br>");
    });
});