var checker = document.getElementById("hidden").innerHTML

console.log(checker)


if (checker == 1){
    document.write('<p>Invalid Username/Password. Please Try Again.</p>');
    event.preventDefault();
}

