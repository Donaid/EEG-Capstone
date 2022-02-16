var socket = new WebSocket('ws://localhost:8000/ws/test1')

//  --------------------------------  Music PLayer -----------------------------------------------

const nextBtn = document.getElementById('nextButton');
const prevBtn = document.getElementById('prevButton');
const playPauseBtn = document.getElementById('playPauseButton');
const music = document.getElementById('musicPlayer');
const alert1 = document.getElementById('alert');
let musicPlaying = false;


music.addEventListener('ended',nextSong)

const musicList = ['song1','song2','song3'];
let songNumber=0;

function playPauseSong(){
  if (musicPlaying){
    music.pause();
    playPauseBtn.getElementsByClassName('fas')[0].classList.add('fa-play');
    playPauseBtn.getElementsByClassName('fas')[0].classList.remove('fa-pause');
    musicPlaying=false;
  }
  else{
    music.play();
    playPauseBtn.getElementsByClassName('fas')[0].classList.add('fa-pause');
    playPauseBtn.getElementsByClassName('fas')[0].classList.remove('fa-play');
    music.volume=0.5
    musicPlaying=true;

  }



}

function nextSong(){
  if(songNumber==2){
    songNumber=0;
  }
  else{
    songNumber++
  }
  music.src='media/'+musicList[songNumber]+'.mp3'

  if(musicPlaying){
    music.play();
  }
  

}

function prevSong(){
  if(songNumber==0){
    songNumber=2;
  }
  else{
    songNumber--
  }
  music.src='media/'+musicList[songNumber]+'.mp3';

  if(musicPlaying){
    music.play();
  }
  
 
}


//  -----------------------------------  Main Graph  -------------------------------------------------

const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['15s','15s','15s','15s','15s','15s'],
        datasets: [{
            label: 'Attention Graph',
            data: [0,0,0,0,0,0],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 2
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                max:100,
                title: {
                  display: true,
                  text: 'Probability of High Attention %'
                }
            },
            x: {
              title: {
                display: true,
                text: 'Time - 10 seconds Interval'
              }
          },
        }

    }
});
const myChart = new Chart(ctx, dataObj);
//------------------------------------Updating Graph-------------------------------------------------


const loginBtn = document.getElementById('login');
const profileBtn = document.getElementById('profile');
const readWriteBtn = document.getElementById('readWrite');
const auralVisualBtn = document.getElementById('auralVisual');
const recordingBtn = document.getElementById('record')
var myModal = new bootstrap.Modal(document.getElementById("modal1"), {});
var myModal2 = new bootstrap.Modal(document.getElementById("modal2"), {});
const mUserName=document.getElementById('modalUserName')
const mLearningMode=document.getElementById('modalLearningMode')
const mSessionTime=document.getElementById('modalSessionTime')
const mAttentionLevel=document.getElementById('modelAttentionLevel')
const bluetoothIcon=document.getElementById('bluetoothIcon')
const alertIcon=document.getElementById('alertIcon')

let bIconPressed=true;
let aIconPressed=true;


let isRecording=false;
let learningMode='Read/Write';
let username='new user';        //import from back-end
let date='';
let attentionValue=0;
let counter=0;
let totalAttentionTemp=0;
let averageAttention=''
let timer1;
let startTime=0;
let endTime=0;
let elapsedTime='';
let dateCheck = new Date();
let currentTime=0;
let highestConsecutive=0;
let highestConsecutiveTemp=0;
let attentionValueSum=0;
let attentionValueCounter=0;

//this object will have all the data stored in this at the end of the session

let userData = {
  userName:'',
  learningType:'',
  sessionTime:0,
  attentionLevel:0,
  date:'',
  time:0,
  highestConsecutiveTime:0
}

function featureDecider(){
  if(isRecording){
    clearInterval(timer1)

    endTime=Date.now();
    

    elapsedTime=(calculateElapsedTime(startTime,endTime))

    recordingBtn.innerHTML='Start Recording';

    unDisableButtons()

    averageAttention=calculateAveAttention(totalAttentionTemp,counter)+'%'

    isRecording=false;

    fillObject();

    

    //Send object to back end here

    

    updateModal();

    showModal();

    resetData();

    clearGraph(); 

    highestConsecutiveTime=0;
    
    music.volume=0.5
    
    /* send object to back-end here*/

  }
  else if(!isRecording){

    timer1=setInterval(updateChart,1000);

    currentTime=dateCheck.getHours();
    
    startTime=Date.now();//used to calculate elapsed time
    

    recordingBtn.innerHTML='Stop Recording';

    date=dateCheck.getFullYear()+'-'+(dateCheck.getMonth()+1)+'-'+dateCheck.getDate();

    disableButtons();

    isRecording=true;


  }
}

function disableButtons(){

  const elementsChange = document.getElementsByClassName("contr1");
  for (let i = 0; i < elementsChange.length; i++) {
    elementsChange[i].classList.add('disabled');
}

}

function unDisableButtons(){
  const elementsChange = document.getElementsByClassName("contr1");
  for (let i = 0; i < elementsChange.length; i++) {
    elementsChange[i].classList.remove('disabled');
}

}




function updateChart(){
	
	
	
	socket.onmessage = function(e){
	previousValue=false;
	var djangoData = JSON.parse(e.data);
	console.log(djangoData);
	
	dataObj.data.datasets[0].data.shift();
	dataObj.data.datasets[0].data.push(djangoData.Attention);
	
  /*Fetch attentionValue here*/

  attentionValue=djangoData.Attention
  attentionValueSum=attentionValueSum+attentionValue;
  attentionValueCounter=attentionValueCounter+1;

  if((attentionValueCounter%6)==0){ //this will play alert every 60 seconds if average attention was low
    if((attentionValueSum/6)<50){
      playAlert();
      attentionValueSum=0
    }
    if((attentionValueSum/6)>=50){
      attentionValueCounter=0
    }
    
    if(attentionValueCounter==60){ //this will display modal if attention was consecutively low for 10 minutes
      myModal2.show()
      attentionValueCounter=0
    }

  }

  if(attentionValue>=50){
    reduceVolume()
    highestConsecutiveTemp=highestConsecutiveTemp+1;
  }
  else if(attentionValue<50){
    increaseVolume()
    if(highestConsecutiveTemp>highestConsecutive){
    highestConsecutive=highestConsecutiveTemp;
    }
    highestConsecutiveTemp=0;
  }
  myChart.update();
  counter++
  totalAttentionTemp=totalAttentionTemp+attentionValue

  }
  }
  
  
  
  
  
  
  
  
  
 function calculateAveAttention(attention,number){
  return(Math.round(attention/number))
 } 

function calculateElapsedTime(startT,endT){
  let actualTime=endT-startT
  actualTime=Math.floor(actualTime/1000);
  var minutes = Math.floor(actualTime/ 60);
  var seconds = (actualTime % 60)
  return(minutes + ":" + seconds);
}


function showModal () {
  myModal.show();

}
  

function fillObject(){
  userData.userName=username;
  userData.learningType=learningMode;
  userData.sessionTime=elapsedTime
  userData.attentionLevel=averageAttention
  userData.date=date
  userData.time=currentTime;
  userData.highestConsecutiveTime=highestConsecutive;
  }


function updateModal(){
  mUserName.innerHTML='Username : ' + userData.userName;
  mLearningMode.innerHTML='Learning Mode : ' + userData.learningType;
  mSessionTime.innerHTML='Session Time : ' + userData.sessionTime
  mAttentionLevel.innerHTML='Attention Level : ' + userData.attentionLevel;
}  

function clearGraph(){
  myChart.data.datasets[0].data=[0,0,0,0,0,0]
  myChart.update()
  }

function resetData(){
  counter=0;
  totalAttentionTemp=0;
}


function learningModeReadWrite(){
    learningMode='Read/Write'
    readWriteBtn.classList.add('learningModeActiveButton')
    auralVisualBtn.classList.remove('learningModeActiveButton')

  }
  
  function learningModeAuralVisual(){
    learningMode='Aural/Visual'
    readWriteBtn.classList.remove('learningModeActiveButton')
    auralVisualBtn.classList.add('learningModeActiveButton')
  }

  function closeModal(){
    myModal.hide()
  }

  function reduceVolume(){
    if(musicPlaying){
    if(music.volume>=0.1){
      music.volume=music.volume-0.1
    }
  }
  }

  function increaseVolume(){
    if(musicPlaying){
    if(music.volume<1){
      music.volume=music.volume+0.1
    }
  }
  }


  function playAlert(){
    alert1.play()
  }

  function changeBluetoothIcon(){
    if(bIconPressed){
      bluetoothIcon.src="https://img.icons8.com/material-rounded/96/000000/bluetooth-off.png"
      bIconPressed=false;
    }
    else{
      bluetoothIcon.src="https://img.icons8.com/material-rounded/96/000000/bluetooth.png"
      bIconPressed=true;
    }
  }

  function changeAlertIcon(){
    if(aIconPressed){
      alert1.volume=0
      alertIcon.src="https://img.icons8.com/external-kmg-design-glyph-kmg-design/64/000000/external-silent-calendar-date-kmg-design-glyph-kmg-design.png"
      aIconPressed=false;
    }
    else{
      alert1.volume=1
      alertIcon.src="https://img.icons8.com/material-rounded/96/000000/bell--v1.png"
      aIconPressed=true;
    }

  }

  function closeModal2(){
    myModal2.hide()
  }