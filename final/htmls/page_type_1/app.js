var messages = ["Hi there!", "JavaScript is also working", "Even if this html was rendered by python"];
var msgBox = document.getElementById("msg-box");
var msgCount = 0;
function renderMessage(){
    if (msgCount<messages.length){
        msgBox.innerHTML=messages[msgCount];
        setTimeout(function(){
            renderMessage();
        }, 800);

        msgCount++;
        return;
    }
    msgCount = 0;
    renderMessage();
}
renderMessage();
