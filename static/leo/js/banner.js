var imgs = ["img/01.jpg", "img/02.jpg", "img/03.png", "img/04.jpg", "img/05.png", "img/06.jpg" ];
/*var timer = null;
var ind = 0;

var id_name = "banner";

function invisBanner(id_name)
{
	var img = document.getElementById(id_name);
	img.className="banner_stop";	
}

function visBanner(id_name)
{
	var img = document.getElementById(id_name);
	img.className="banner_start";	
}

function changeSrc (id_name)
{
	var img = document.getElementById(id_name);
	if(ind  >= img_arr.length)
        ind = 0;
	var time=3000;
 $(id_name).fadeOut(time, function() {    //для картинок
  $(this).attr('src', img_arr[ind]).fadeIn(time);
 });
	//img.src="img/"+img_arr[ind];
	ind++;
	
	
}




 function showBanner (id_name)
 {
 	
 	timer = setInterval("changeSrc(id_name)", 6000);
 	
 }


showBanner("banner");


*/

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