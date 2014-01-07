$(document).ready(  
    function() {
        $("#getURLContentBtn").bind('click',loadURLContent)
        $("#extractBtn").bind('click',extract)
        $("#previewBtn").bind('click',preview)
    }
);  
function loadURLContent()
{
    var url = $("#urlInput").val();
    $.get("http://127.0.0.1:8000/getURLContent/"+url, function(data){
        var str = unescape(data.replace(/\\u/gi, '%u'))
        str = str.replace('\'','\\\'')
        console.log(str)
        result = eval("\'"+str+"\'")
        console.log(result)
        $("#URLContentDIV").val(result.content)
        $("#encoding").val(result.encoding)
    });
}
function extract () {
    var data = {};
    data.global_pattern = $("#globalSearchPattern").val()
    data.item_pattern = $("#itemSearchPattern").val()
    data.urlContent = $("#URLContentDIV").val()
    $.post("http://127.0.0.1:8000/extractFeedEntry/",data,function(result){
        var list = eval(unescape(result.replace(/\\u/gi, '%u')))
        var str = ""
        for (var i = 0; i < list.length; i++) {
            var item = list[i];
            for (var j = 0; j < item.length; j++) {
                str+="{"+j+"}  " + item[j] + "\n";
            };
            str+="\n"
        };
        $("#clipedData").val(str)

    })
}
function preview () {
    var data = {};
    data.title = $("#titleInput").val()
    data.url = $("#urlInput").val()
    data.item_title = $("#itemTitleInput").val()
    data.item_link = $("#itemLinkInput").val()
    data.item_content = $("#itemContentInput").val()
    // data.

    $.post("http://127.0.0.1:8000/extractFeedEntry/",data,function (result) {


    })
}