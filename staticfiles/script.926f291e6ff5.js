// (function changeSizeOfDiv() {
//     var pageContentHeight = document.getElementById('body').clientHeight;
//     var content = document.querySelector('.page-content').clientHeight;
//     document.querySelector(".left-div").style.height =
//              parseInt(pageContentHeight+content)+"px";
//     console.log(pageContentHeight)
// })();




 function changeSizeOfPic(click_id) {
     
     var image = document.getElementById(click_id);
     image.style.height = "360px";
     image.style.width = "572px";
     
        
     
     
         
 }

function originalSize(click_id){
    
    var image = document.getElementById(click_id)
    image.style.height = "317px";
    image.style.width = "249px";
    
}
