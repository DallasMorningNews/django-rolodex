(function(){
    var werks = document.querySelectorAll(".chartWerk");

    for (var i = 0; i < werks.length; i++) {
        var werk = werks[i],
            id = werk.getAttribute("data-id"),
            single = werk.getAttribute("data-single"),
            double = werk.getAttribute("data-double"),
            size = werk.getAttribute("data-size"),
            screen = werk.parentElement.clientWidth;
        
            //Check if iframe already embedded.
            if(werk.querySelectorAll('iframe').length < 1){

                var iframe = document.createElement("iframe");
                iframe.setAttribute("scrolling","no");
                iframe.setAttribute("frameborder","0");
            
                //desktop
                if(size == 'responsive'){
                    if(screen > 700){
                        iframe.setAttribute("src","http://interactives.dallasnews.com/charts/"+id+".html");
                        iframe.setAttribute("style","margin:10px auto; display:block;");
                        iframe.setAttribute("height",double);
                        iframe.setAttribute("width",600);
                    }else{
                        iframe.setAttribute("src","http://interactives.dallasnews.com/charts/"+id+"_mobile.html");
                        iframe.setAttribute("height",single+"px");
                        iframe.setAttribute("width",290);
                        //float or center
                        if(screen > 480){
                            iframe.setAttribute("style","float:left; margin: 10px 20px 10px 0px;");
                        }else{
                            iframe.setAttribute("style","margin:10px auto; display:block;");
                        }
                    }
                //mobile
                }else{
                    iframe.setAttribute("src","http://interactives.dallasnews.com/charts/"+id+"_mobile.html");
                    iframe.setAttribute("style","margin:10px auto; display:block;");
                    iframe.setAttribute("height",single);
                    iframe.setAttribute("width",290)
                    //float or center
                    if(screen > 480){
                        iframe.setAttribute("style","float:left; margin: 10px 20px 10px 0px;");
                    }else{
                        iframe.setAttribute("style","margin:10px auto; display:block;");
                    }
                
                }

                werk.appendChild(iframe);
            }
    }
})();
