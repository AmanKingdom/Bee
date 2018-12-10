KindEditor.ready(function(K) {
    window.editor = K.create('#id_article_html',{
        width:'100%',
        height:'500px',
        minHeight: 100,
        uploadJson:'/uploads/',
        items:[
            'preview', 'undo', 'redo', 'formatblock', 'fontname', 'fontsize', 'forecolor', 'hilitecolor', 'bold', 'italic', 'underline', 'strikethrough', 'justifyleft',
            'justifycenter', 'justifyright', 'insertorderedlist', 'insertunorderedlist', 'subscript', 'superscript', 'removeformat', '|',
            'image', 'flash', 'media', 'table', 'hr', 'emoticons', 'baidumap', 'link', 'fullscreen'],
        themeType : 'simple',
        minChangeSize:1,    // undo/redo文字输入最小变化长度
        afterBlur:function (){this.sync();}
        }
    );
});
//
// KindEditor.ready(function(K) {
//     window.editor = K.create('#id_cover_img',{
//         width:'100%',
//         height:'200px',
//         minHeight: 100,
//         uploadJson:'/uploads/',
//         items:['image'],
//         themeType : 'simple',
//         afterBlur:function (){this.sync();}
//         }
//     );
// });