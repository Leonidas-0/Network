document.addEventListener('DOMContentLoaded', function() {
    try {
        var allButtons = document.querySelector('#all').childElementCount;
        var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        var page=document.querySelector('#page').innerHTML
      }
      catch (error) {
        var allButtons = 0
      }
    var content = document.querySelectorAll('.name');
    try {
    var button = document.querySelectorAll('.heart');
    }
    catch (error) {
    }
    var edit = document.querySelectorAll('#edit');
    var subedit = document.querySelectorAll('#subedit');
    var editdiv = document.querySelectorAll('.editdiv');
    var post = document.querySelectorAll('.post');
    var textarea = document.querySelectorAll('.textarea');
    var editbutton=document.querySelectorAll('input[name="edit"]')
    var likenum = document.querySelectorAll('#likenum')
    for (i = 0; i < allButtons; i++) {
    function listen(i) {
        edit[i].addEventListener('click', () => {
            editdiv[i].style.display = 'block';
            editbutton[i].className="btn btn-info"
            post[i].style.display = 'none';
            subedit[i].addEventListener('click', () => {
            fetch(`/edit/${content[i].id}`,
            {
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                mode: 'same-origin',
                body: JSON.stringify({
                post: textarea[i].value,
                page: page             
                })}).then(() => {
                    editdiv[i].style.display = 'none';
                    post[i].style.display = 'block';
                })})})
        var heart = new Image();
        heart.id = "main";
        if (button[i]) {
    var requestPOST = new Request(
        `/Post/${content[i].id}`,
        {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin'
        }
    );}
    var requestGET = new Request(
        `/Post/${content[i].id}`,
        {
            method: 'GET',
        }
    );
    fetch(requestGET).then((response) => response.json()).then((data) => {
        if (data[0]=="like") {
            heart.src = "/static/network/like.png"
        }
        else {
            heart.src = "/static/network/nolike.png"
        }
        likenum[i].innerHTML=data[1]
        button[i].appendChild(heart);
    })


    if (button[i]) {
    button[i].addEventListener('click', () =>
    fetch(requestPOST).then((response) => response.json()).then((data) => {
        if (data[0]=="like") {
            heart.src = "/static/network/like.png"
        }
        else {
            heart.src = "/static/network/nolike.png"
        }
        likenum[i].innerHTML=data[1]
        button[i].appendChild(heart);
        heart.style.animationPlayState  = 'running';
        }
))
}}listen(i)}})

  