let feedBackMessageID =  document.getElementById('feedBack1');
let feedBackMessagePassLength =  document.getElementById('feedBack2');
let feedBackMessagePasssMatch =  document.getElementById('feedBack3');

let userID = document.getElementById('userid');
let userPass1 = document.getElementById('password1');
let userPass2 = document.getElementById('password2');

let userCrentials = {

    userName:'',
    password:''

}

function setEmailTaken(){
    feedBackMessageID.classList.remove('d-none')
    userID.classList.add('is-invalid')
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
    if(userPass1.value.length>=8 && userPass1.value.length<=16){
        return true
    }

    else{
        setPasswordShort();
        return false
    }
}

function checkPassMatch(){
    if(userPass1.value==userPass2.value){
        return true
    }

    else{
        setPassMatch();
        return false
    }

}

//use this to verify credentials

function verifyCredentials(){

}

function setCredentials(){
    userCredentials.userName=userID.value;
    userCredentials.passowrd=userPass1.value;
}

$(function() {
    $('#signupForm').on('submit', function(e){
        lengthValid = checkPassLength();
        matchValid = checkPassMatch();
        if(!lengthValid || !matchValid) {
            e.preventDefault();
        }
    });

    $('#password1').on('input', function() {
        feedBackMessagePassLength.classList.remove('text-danger')
        feedBackMessagePasssMatch.classList.add('d-none')
        userPass1.classList.remove('is-invalid')
    })

    $('#password2').on('input', function() {
        feedBackMessagePassLength.classList.remove('text-danger')
        feedBackMessagePasssMatch.classList.add('d-none')
        userPass2.classList.remove('is-invalid')
    })

    $('#userid').on('input', function() {
        feedBackMessageID.classList.add('d-none')
    })
})

