function customMouseOver(event){
    event.target.classList.add('highlight')
}

function customMouseOut(event){
    event.target.classList.remove('highlight')
}

window.addEventListener('load', function(){
    document.getElementsByTagName('p')[0].addEventListener('mouseover', customMouseOver)
    document.getElementsByTagName('p')[0].addEventListener('mouseout', customMouseOut)
})