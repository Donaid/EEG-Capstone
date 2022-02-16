let feedBackMessage =  document.getElementById('feedBack');
let userEmail = document.getElementById('emailAddress1');
let userPass = document.getElementById('password1');



let userCrentials = {

    userName:'',
    password:''

}

// use this function to verify user credentials and move user to next page

function verifyUserCredentials(email,password){


}


// call this function if credentials are Invalid


function setCredentialsInvalid(){
    userEmail.classList.add('is-invalid');
    userPass.classList.add('is-invalid');
    feedBackMessage.classList.remove('d-none');

}

function setCredentials(){
    userCredentials.userName=userEmail.value;
    userCredentials.passowrd=userPass.value;
}