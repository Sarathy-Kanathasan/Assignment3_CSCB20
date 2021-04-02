let button = document.getElementsById('sbmt');
let login = document.getElementById("login_box");
let err = document.getElementById("invalid");

loginButton.addEventListener("click",  {
    for result in results:
    if result[1]==request.form['username']:
        if result[2]==request.form['password']:
            session['username']=request.form['username']
            session['status']=result[3]
            return redirect(url_for('index'))
    return "Incorrect UserName/Password"
})