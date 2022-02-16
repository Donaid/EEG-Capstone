let feedBackMessageEmail =  document.getElementById('feedBack1');
let feedBackMessagePassLength =  document.getElementById('feedBack2');
let feedBackMessagePasssMatch =  document.getElementById('feedBack3');

let userEmail = document.getElementById('emailAddress1');
let userPass1 = document.getElementById('password1');
let userPass2 = document.getElementById('password2');

let userCrentials = {

    userName:'',
    password:''

}

function setEmailTaken(){
    feedBackMessageEmail.classList.remove('d-none')
    userEmail.classList.add('is-invalid')
}


function setPasswordShort(){
    feedBackMessagePassLength.classList.add('text-danger')
    userPass1.classList.add('is-invalid')
    userPass2.classList.add('is-invalid')

}

function setPassMatch(){
    feedBackMessagePasssMatch.classList.remove('d-none')
    userPass1.classList.add('is-invalid')
    userPass2.classList.add('is-invalid')
}

function checkPassLength(){
    if(userPass1.innerHTML.length>=7 && userPass1.innerHTML.length<=19){
        return true
    }

    else{
        return false
    }
}

function checkPassMatch(){
    if(userPass1.innerHTML==userPass2.innerHTML){
        return true
    }

    else{
        return false
    }

}

//use this to verify credentials

function verifyCredentials(){

}

function setCredentials(){
    userCredentials.userName=userEmail1.value;
    userCredentials.passowrd=userPass1.value;
}

