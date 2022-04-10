var socket = new WebSocket('ws://localhost:8000/ws/test1')
let deviceStatus = 0;
let tempDjangoData;
socket.onmessage = function(e) {
  tempDjangoData = JSON.parse(e.data).data;
  
  if(tempDjangoData.hasOwnProperty('Status')) {
    if(tempDjangoData.Status == "connected") {
      deviceStatus = 1;
      bluetoothIcon.src="https://img.icons8.com/material-rounded/96/000000/bluetooth.png";
      if(!isRecording) {
        unDisableStartButton();
      }
    }
    else if(tempDjangoData.Status == "disconnected") {
      deviceStatus = 0;
      bluetoothIcon.src="https://img.icons8.com/material-rounded/96/000000/bluetooth-off.png";
      if(isRecording) {
        featureDecider();
      }
      disableStartButton();
    }
  }

  if(isRecording && deviceStatus == 1) {
    updaterAll(tempDjangoData)
    saveAttention(tempDjangoData)
  }

  // if(tempDjangoData.Status == "disconnected") {
  //   bluetoothIcon.src="https://img.icons8.com/material-rounded/96/000000/bluetooth-off.png"
  //   if(!isRecording){
  //     disableStartButton()
  //   }
  //   if(isRecording){
  //     showDisconnectModal()
  //     featureDecider()
  //   }
    
    
  // }
  // else if (tempDjangoData.Status == "connected") {
  //   bluetoothIcon.src="https://img.icons8.com/material-rounded/96/000000/bluetooth.png"
  //   if(!isRecording){
  //     unDisableStartButton()
  //   }
  // }

}

//  --------------------------------  Music PLayer -----------------------------------------------
const playPauseBtn = document.getElementById('playPauseButton');
const music = document.getElementById('musicPlayer');
const alert1 = document.getElementById('alert');
let musicPlaying = false;

music.addEventListener('ended',nextSong)
let songNumber=0;

function playPauseSong(){
  if(musicPlaying){
    document.getElementById('playPauseCh').classList.add('fa-play');
    document.getElementById('playPauseCh').classList.remove('fa-pause');
    music.pause();
    musicPlaying=false;
  }
  else{
    document.getElementById('playPauseCh').classList.add('fa-pause');
    document.getElementById('playPauseCh').classList.remove('fa-play');
    music.play();
    music.volume=0.5;
    musicPlaying=true;
  }
}

function nextSong(){
  if(songNumber==3){
    songNumber=1;
  }
  else{
    songNumber++;
  }
  music.src='/static/media/song'+songNumber+'.mp3'
  if(musicPlaying){
    music.play();
  }
}

function prevSong(){
  if(songNumber==1){
    songNumber=3;
  }
  else{
    songNumber--;
  }
  music.src='/static/media/song'+songNumber+'.mp3';
  if(musicPlaying){
    music.play();
  }
}

//  -----------------------------------  Main Graph  -------------------------------------------------

const ctx = document.getElementById('mainChart').getContext('2d');
const chData={
  type:'line',
  data:{
    labels:['10s','10s','10s','10s','10s','10s'],
    datasets:[{
      label:'Attention Graph',
      data:[0,0,0,0,0,0],
      backgroundColor: [
        'rgba(255, 100, 130, 0.5)',
      ],
      borderColor:[
        'rgba(240, 95, 125, 1)',
        'rgba(48, 155, 230, 1)',
        'rgba(248, 198, 80, 1)',
        'rgba(68, 185, 180, 1)',
        'rgba(140, 90, 240, 1)',
        'rgba(240, 140, 50, 1)'
      ],
      borderWidth: 2
    }]
  },
  options:{
    scales:{
      y:{
        beginAtZero:true,
        max:100,
        title:{
          display:true,
          text:'Probability of High Attention %'
        }
      },
      x:{
        title:{
          display:true,
          text:'Time - 10 seconds Interval'
        }
      },
    }
  }
}
const mainChart = new Chart(ctx, chData);

//------------------------------------Updating Graph-------------------------------------------------

const readWriteBtn = document.getElementById('readWrite');
const auralVisualBtn = document.getElementById('auralVisual');
const recordingBtn = document.getElementById('record');
disableStartButton()
let summaryModal = new bootstrap.Modal(document.getElementById("modal1"), {});
let attentionModal = new bootstrap.Modal(document.getElementById("modal2"), {});
let disconnectModal = new bootstrap.Modal(document.getElementById("modal3"), {});
//const mUserName=document.getElementById('modalUserName');
const mLearningMode=document.getElementById('modalLearningMode');
const mSessionTime=document.getElementById('modalSessionTime');
const mAttentionLevel=document.getElementById('modelAttentionLevel');
const bluetoothIcon=document.getElementById('bluetoothIcon');
const alertIcon=document.getElementById('alertIcon');
let aIconPressed=true;
let isRecording=false;
let learningMode='Read/Write';
//let username='new user';  
//let date='';
let attentionValue=0;
let counter=0;
let totalAttentionTemp=0;
let averageAttention='';
// let timer1;
let startTime=0;
let endTime=0;
let elapsedTime='';
let dateCheck = new Date();
let tempConsecutiveHighAttention = 0;
let consecutiveHighAttention = 0;
//let currentTime=0;
//let highestConsecutive=0;
//let highestConsecutiveTemp=0;
let attentionValueSum=0;
let attentionValueCounter=0;

//this object will have all the data stored at end of the session
let userData = {
  learningType:'',
  sessionTime:0,
  attentionLevel:0,
  //date:'',
  //time:0,
  //highestConsecutiveTime:0,
  // userName:''
}

function featureDecider(){
  if(isRecording){
	  
    endTime=Date.now();
    elapsedTime=(calculateElapsedTime(startTime,endTime));
    recordingBtn.innerHTML='Start Recording';
    unDisableButtons();
    averageAttention=calculateAveAttention(totalAttentionTemp,counter)+'%';
    isRecording=false;
    updateLatestSession(consecutiveHighAttention, (learningMode=='Read/Write'? 'r':'w'));
    fillObject();
    updateModal();
    showModal();
    resetData();
    clearGraph(); 

    // clearInterval(timer1)
    //highestConsecutiveTime=0;
    /* send object to back-end here*/
	// socket.onclose = function (e) {
	// 	console.log('The connection has been closed successfully.');
	// };
	// socket.onclose()
  }
  
  else if(!isRecording){
    // timer1=setInterval(updateChart,1000);
    //currentTime=dateCheck.getHours();
    startTime=Date.now();//used to calculate elapsed time
    recordingBtn.innerHTML='Stop Recording';
    //date=dateCheck.getFullYear()+'-'+(dateCheck.getMonth()+1)+'-'+dateCheck.getDate();
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

function disableStartButton(){
  recordingBtn.classList.add('disabled');
}

function unDisableStartButton(){
  recordingBtn.classList.remove('disabled');
}

function updaterAll(tempDjangoData){
	
  let djangoData = tempDjangoData;
  attentionValue=djangoData.Attention;

  if(attentionValue >= 50) {
    tempConsecutiveHighAttention++;
    if (tempConsecutiveHighAttention > consecutiveHighAttention) {
      consecutiveHighAttention = tempConsecutiveHighAttention;
    }
  }
  else {
    tempConsecutiveHighAttention = 0;
  }

  updateChart();
  alertOneM();
  alerttenM();
  manageMusicPlay();
  
  counter++;
  totalAttentionTemp=totalAttentionTemp+attentionValue;
}

function updateChart(){
  chData.data.datasets[0].data.shift();
  chData.data.datasets[0].data.push(attentionValue);
  mainChart.update();
}
  
function alertOneM(){
  attentionValueSum=attentionValueSum+attentionValue;
  attentionValueCounter=attentionValueCounter+1;
  if((attentionValueCounter%6)==0){
    if((attentionValueSum/6)<50){
      attentionValueSum=0;
      playAlert();
    }
    if((attentionValueSum/6)>=50){
      attentionValueCounter=0;
      attentionValueSum=0;
    }
  }
}  
  
function alerttenM(){
  if(attentionValueCounter==60){
    attentionModal.show();
    playAlert();
    attentionValueCounter=0;
  }
}

function manageMusicPlay(){
  if(attentionValue>=50){
    if(musicPlaying){
      if(music.volume>0.19){
          music.volume=music.volume-0.1;
      }
    }
    //highestConsecutiveTemp=highestConsecutiveTemp+1;
  }
  else if(attentionValue<50){
    if(musicPlaying){
      let tempVolume = music.volume + 0.1;
      if(tempVolume > 1){
        music.volume = 1;
      }
      else if(music.volume<1){
        music.volume=music.volume+0.1;
      }
    }
    //if(highestConsecutiveTemp>highestConsecutive){
    //highestConsecutive=highestConsecutiveTemp;
    //}
    //highestConsecutiveTemp=0;
  }
}
  
function calculateAveAttention(attention,number){
  return(Math.round(attention/number));
} 

function calculateElapsedTime(startT,endT){
  let actualTime=Math.floor((endT-startT)/1000);
  let m=Math.floor(actualTime/ 60);
  let s=(actualTime % 60);
  return(m+":"+s);
}

function showModal () {
  summaryModal.show();
}

function fillObject(){
  userData.learningType=learningMode;
  userData.sessionTime=elapsedTime;
  userData.attentionLevel=averageAttention;
  //userData.date=date;
  //userData.time=currentTime;
  //userData.highestConsecutiveTime=highestConsecutive;
  // userData.userName=username;
}

function updateModal(){
  // mUserName.innerHTML='Username : ' + userData.userName;
  mLearningMode.innerHTML='Learning Mode : ' + userData.learningType;
  mSessionTime.innerHTML='Session Time : ' + userData.sessionTime;
  mAttentionLevel.innerHTML='Avg Attention Level : ' + userData.attentionLevel;
}  

function clearGraph(){
  mainChart.data.datasets[0].data=[0,0,0,0,0,0];
  mainChart.update();
}

function resetData(){
  counter=0;
  totalAttentionTemp=0;
  attentionValueCounter = 0;
  attentionValueSum = 0;
  music.volume=0.5;
  tempConsecutiveHighAttention = 0;
  consecutiveHighAttention = 0;
}

function learningModeReadWrite(){
  learningMode='Read/Write';
  readWriteBtn.classList.add('learningModeActiveButton');
  auralVisualBtn.classList.remove('learningModeActiveButton');
}
  
function learningModeAuralVisual(){
  learningMode='Aural/Visual';
  readWriteBtn.classList.remove('learningModeActiveButton');
  auralVisualBtn.classList.add('learningModeActiveButton');
}

function closeModal(){
  summaryModal.hide();
}

function playAlert(){
  alert1.play();
}

function changeAlertIcon(){
  if(aIconPressed){
    alert1.volume=0;
    alertIcon.src="https://img.icons8.com/external-kmg-design-glyph-kmg-design/64/000000/external-silent-calendar-date-kmg-design-glyph-kmg-design.png";
    aIconPressed=false;
  }

  else{
    alert1.volume=1;
    alertIcon.src="https://img.icons8.com/material-rounded/96/000000/bell--v1.png";
    aIconPressed=true;
  }
}

function closeModal2(){
  attentionModal.hide();
}

function closeModal3(){
  disconnectModal.hide();
}

function showDisconnectModal(){
  disconnectModal.show();
  setTimeout(closeModal3,1000);
}

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  function saveAttention(tempDjangoSaveData){
    $.ajax(
    {
      type:"POST",
      url: "/test1/saveattention/",
      mode: 'same-origin',
      headers: {
        "X-CSRFToken" : getCookie('csrftoken')
      },
      data: {
        attention: tempDjangoSaveData.Attention.toFixed(2),
        status: tempDjangoSaveData.Status,
        learningMethod: (learningMode=='Read/Write'? 'r':'w')

      },
      success: function(data) 
        {
          console.log("save success", data)
        }
    })
  }

  function updateLatestSession(consecutiveHigh, learningMethod) {
    $.ajax(
    {
      type:"POST",
      url: "/test1/updatelatestsession/",
      mode: 'same-origin',
      headers: {
        "X-CSRFToken" : getCookie('csrftoken')
      },
      data: {
        consecutiveHigh: consecutiveHigh,
        learningMethod: learningMethod
      },
      success: function(data) 
        {
          console.log("update success", data)
        }
    })
  }