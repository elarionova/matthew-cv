function showImg(el)
{
	document.getElementById("photo_popup").style.display="block";
	var photo = document.getElementsByClassName("photo_large");
	if (el.parentNode.className == "item_img_hr")
		photo[0].innerHTML = "<div class='popup_img_hr'><img src='"+el.src+"'"+"'/></div>";
	else
		photo[0].innerHTML = "<img src='"+el.src+"'"+" class='"+"popup_img_vr"+"'/>";
	
}

function hideImg()
{
	document.getElementById("photo_popup").style.display="none";
}



jQuery(function ($) {
    function fix_size() {
        var images = $('.photo_large img');
        images.each(setsize);

        function setsize() {
            var img = $(this),
                img_dom = img.get(0),
                container = img.parents('.photo_large');
            if (img_dom.complete) {
                resize();
            } else img.one('load', resize);

            function resize() {
                if ((container.width() / container.height()) < (img_dom.width / img_dom.height)) {
                    img.width('100%');
                    img.height('auto');
                    return;
                }
                img.height('100%');
                img.width('auto');
            }
        }
    }
    $(window).on('resize', fix_size);
    fix_size();
});