
// if (checker == 0){
//     document.write(<p>{{checker}}</p>);
// }
// if (checker == 1){
//     e.preventDefault();
//     document.write('<p>Invalid Username/Password</p>');
//     }

// switch(checker){
//     case(1):
//         document.write(<p>{{checker}}</p>);
//         break;

//     case(0):
//         e.preventDefault();
//         document.write('<p>Invalid Username/Password</p>');
//         break;
// }

var checker = document.getElementById("hidden").innerHTML
var mpty = document.getElementById("hidden2").innerHTML
console.log(checker)

// if (checker == 0){
//     document.write('<p>Valid Username/Password</p>');
// }

if (checker == 1){
    document.write('<p>Sorry that Username is already taken</p>');
    event.preventDefault();
}

if (mpty == 1){
    document.write('<p>One or More Fields are Empty</p>');
    event.preventDefault();
}

