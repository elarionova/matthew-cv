var imgs = ["img/main/00.jpg", "img/main/01.jpg", "img/main/02.jpg", "img/main/03.jpg",
"img/main/04.jpg", "img/main/05.jpg", "img/main/06.jpg", "img/main/07.jpg", "img/main/08.jpg", 
"img/main/09.jpg", "img/main/10.jpg", "img/main/11.jpg", "img/main/12.jpg", "img/main/13.jpg", "img/main/14.jpg",
"img/main/15.jpg", "img/main/16.jpg", "img/main/17.jpg", "img/main/18.jpg", "img/main/19.jpg", "img/main/20.jpg",
"img/main/21.jpg", "img/main/22.jpg", "img/main/23.jpg", "img/main/24.jpg",  ];

var n=0;
var next="";
$(document).ready(function(){go=setInterval("chgImg(0)", 7000);});

function chgImg(number) {
 if (number!=0) {
     clearInterval(go);
     $('[id^=slide_show]').stop();
     n=number-2;
     go=setInterval("chgImg(0)", 7000);
 }
 n++;
 if (n>=imgs.length) n=0;
 if (next=="") next=2;
 else next="";

 $('#slide_show'+next).attr('src',imgs[n]);
 $('[id^=slide_show]').fadeToggle(2000);
}