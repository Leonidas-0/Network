document.addEventListener('DOMContentLoaded', function() {
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    try {
    var followbutton = document.querySelector("#follow");
    }
    catch (error) {
        var followbutton = null
      }
var requestfollow = new Request(
    `/follows/${document.querySelector(".username").id}`,
    {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
    }
);
var requestfollowget = new Request(
    `/follows/${document.querySelector(".username").id}`,
    {
        method: 'GET',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
    }
);
fetch(requestfollowget).then((response) => response.json()).then((data) => {
    document.querySelector("#followers").innerHTML="Followers: " + data[1]
    document.querySelector("#following").innerHTML="Following: " + data[2]
    try {
    if (data[0] == "following") {
        followbutton.innerHTML="Unfollow"
        followbutton.className="btn btn-primary"
    }
    else {
        followbutton.innerHTML="Follow"
        followbutton.className="btn btn-secondary"
    }
}catch (error) {
}})
    
try { document.querySelector("#follow").addEventListener('click', () => {
fetch(requestfollow).then((response) => response.json()).then((data) => {
    if (data[0] == "following") {
        followbutton.innerHTML="Unfollow"
        followbutton.className="btn btn-primary"
    }
    else {
        followbutton.innerHTML="Follow"
        followbutton.className="btn btn-secondary"
    }
    document.querySelector("#followers").innerHTML="Followers: " + data[1]
    document.querySelector("#following").innerHTML="Following: " + data[2]})})}
    catch (error) {
    }
})