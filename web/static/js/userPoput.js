function popup()
{
    let popup = document.getElementById('works_popup'),
    popupToggle = document.getElementById('my_works'),
    popupClose = document.getElementById('.close');

    popupToggle.onclick = function()
    {
        popup.style.display="block";
    };

    popupClose.onclick = function () 
    {
        popup.style.display = "none";
    }

    window.onclick = function (e) 
    {
        if(e.target == popup) 
        {
            popup.style.display = 'none';
        }
    }
}