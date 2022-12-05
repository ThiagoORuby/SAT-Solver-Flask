var cur_id;

function setId(id) {
    cur_id = id;
}

function addtext(text){
    console.log("to aqui po");
    input = document.getElementById(cur_id)
    input.value += text
    input.focus()

    console.log(document.activeElement)
}