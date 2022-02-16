//-------------------------------------------Pie Chart Graph------------------------------------------------

const ctx = document.getElementById('pieChart1').getContext('2d');

const hLChart = new Chart(ctx, {
    type: 'pie',
    data: {


  labels: [
    'High Attention',
    'Low Attention'
  ],
  datasets: [{
    label: 'Total Attention High/Low',
    data: [80,10],
    backgroundColor: [
      'rgb(0, 0, 255)',
      'rgb(255, 0, 0)'
    ],
    hoverOffset: 4
  }]
      
    },

    options: {
        title: {
            display: true,
            text: 'Total Attention Hi',
        },
    }
   
});





//--------------------------------------Updating Pie Chart Graph and Data on top row-----------------------------------------------------

const userName=document.getElementById('userName');
const idealStudyTime=document.getElementById('idealStudyTime');
const audioVideoHighAttention=document.getElementById('consecutiveHighAttentionAV');
const readWriteHighAttention=document.getElementById('consecutiveHighAttentionRW');

const sessionsCompletedAV=document.getElementById('sessionsCompletedAV');
const sessionsCompletedRW=document.getElementById('sessionsCompletedRW');
const highToTotalAV=document.getElementById('highToTotalAV');
const highToTotalRW=document.getElementById('highToTotalRW');

let userData={
 userName:'Andy',
idealStudyTime:'0300',
audioVideoHighAttention:9,
readWriteHighAttention:7,

sessionsCompletedAV:37,
sessionsCompletedRW:30,
highToTotalAV:72,
highToTotalRW:53,
graphHighAttention:68,
graphLowAttention:32,
}

//fill up userData object using back-end


//this function will update the graph using userData object

function updateChart(){
    hLChart.data.datasets[0].data[0]=userData.graphHighAttention;
    hLChart.data.datasets[0].data[1]=userData.graphLowAttention;
    hLChart.update();

};


//this function will update the profile summary and learning summray using the userData object

function updateData(){

  userName.innerHTML='Username : ' + userData.userName;
  idealStudyTime.innerHTML='Ideal Study Time : ' + userData.idealStudyTime;
  audioVideoHighAttention.innerHTML='Aural/Visual : ' + userData.audioVideoHighAttention
  readWriteHighAttention.innerHTML='Read/Write : ' + userData.readWriteHighAttention

  sessionsCompletedAV.innerHTML='Aural/Visual : ' + userData.sessionsCompletedAV
  sessionsCompletedRW.innerHTML='Read/Write : ' + userData.sessionsCompletedRW
  highToTotalAV.innerHTML='Aural/Visual : ' + userData.highToTotalAV
  highToTotalRW.innerHTML='Read/Write : ' + userData.highToTotalRW
};


//----------------------Daily Sessions Chart---------------------------------------------

const ctx2 = document.getElementById('dailySessionsChart').getContext('2d');

var dSChart = new Chart(ctx2, {
    type: 'bar',
    data: {
        labels: [["session 1"], ["session 2"], ["session 3"], ["session 4"]],
        datasets: [{
            label:[''],
            data: [12, 19, 3, 5],
            backgroundColor: [
                'rgba(255,0,0,.5)',
                'rgba(0,0,255, 0.5)',
                'rgba(255,0,0,.5)',
                'rgba(0,0,255, 0.5)',
            ],
            borderWidth: 1
        }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          max:100,
          title: {
            display: true,
            text: 'Attention Level'
          }
      },
        
    },
      maintainAspectRatio:false,
      responsiveness:true,
      plugins: {
          legend: {
              display:false,
          }
      }
  
     
  },
});

//----------------------Daily Chart---------------------------------------------

const ctx3 = document.getElementById('dailyChart').getContext('2d');

var dChart = new Chart(ctx3, {
    type: 'bar',
    data: {
        labels: ['High Attention', 'Low Attention','High Attention','Low Attention'],
        datasets: [{
            label:[''],
            data: [12, 19, 3, 5],
            backgroundColor: [
                'rgba(255,0,0,.5)',
                'rgba(255,0,0,.5)',
                'rgba(0,0,255, 0.5)',
                'rgba(0,0,255, 0.5)',
            ],
            borderWidth: 1
        }]
    },
    options: {

      maintainAspectRatio:false,
      responsiveness:true,
      plugins: {
          legend: {
              display:false,
          }
      },
      y: {
        beginAtZero: true,
        max:100,
        title: {
          display: true,
          text: 'Attention Level'
        }
    },
      
  
     
  },
});

//----------------------Weekly Chart---------------------------------------------

const ctx4 = document.getElementById('weeklyChart').getContext('2d');

var wChart = new Chart(ctx4, {
    type: 'bar',
    data: {
        labels: ['High Attention', 'Low Attention','High Attention','Low Attention'],
        datasets: [{
            label:[''],
            data: [12, 19, 3, 5],
            backgroundColor: [
                'rgba(255,0,0,0.5)',
                'rgba(255,0,0,.5)',
                'rgba(0,0,255, 0.5)',
                'rgba(0,0,255, 0.5)',
            ],
            borderWidth: 1
        }]
    },
    options: {
      y: {
        beginAtZero: true,
        max:100,
        title: {
          display: true,
          text: 'Attention Level'
        }
    },
      maintainAspectRatio:false,
      responsiveness:true,
      plugins: {
          legend: {
              display:false,
          }
      }
  
     
  },
});

//----------------------Updating the Bottom 3 Graphs---------------------------------------------

const date1=document.getElementById('dateSelected1');
var errorModal = new bootstrap.Modal(document.getElementById("errorModal"), {});




//fill this object using date1 with userData
let graphData1={
  learningMode:['r','w','r','r'],
  dailySessionData:[76,41,89,17],//the attention values for daily sessions
  daily:[70,30,80,20],//the attention values for the overall day
  weekly:[15,85,28,72]//the attention values for the overall week

}





function fillDailySessionsGraph(){//fills daily sessions graph
  chartLabelsTemp=[]
  
  dSChart.data.datasets[0].backgroundColor=[]
  dSChart.data.datasets[0].data=[]
  for(i=0;i<graphData1.dailySessionData.length;i++){

   chartLabelsTemp.push('session ' + (i+1));
    
   dSChart.data.datasets[0].data.push(graphData1.dailySessionData[i])
    
    

    if(graphData1.learningMode[i]==='r'){
      dSChart.data.datasets[0].backgroundColor.push('rgba(0,0,255,0.5)')
   


    }
    else{
      dSChart.data.datasets[0].backgroundColor.push('rgba(255,0,0,0.5)');
    }
 
  }
  dSChart.data.labels=chartLabelsTemp;
  dSChart.update()
}

function fillDailyGraph(){//fills daily Graph
  dChart.data.datasets[0].data=[]
  
  for(i=0;i<graphData1.daily.length;i++){
    dChart.data.datasets[0].data.push(graphData1.daily[i])
  

  }
  dChart.update()
}





function fillWeeklyGraph(){//fills weekly graph
  wChart.data.datasets[0].data=[]
  
  for(i=0;i<graphData1.weekly.length;i++){
    wChart.data.datasets[0].data.push(graphData1.weekly[i])
  

  }
  wChart.update()

}

function updateAll(){//updates all the graphs
  updateData()
  fillDailySessionsGraph()
  fillDailyGraph()
  fillWeeklyGraph()
 
}

function timer1(){
  setTimeout(updateAll,1000)
}


function changeData(){//this function is for when the user selects Date
  dateFound = true;
  date1.value

  if(dateFound){

  
  //update this object with new date
  graphData1={
    learningMode:['r','w','r','w'],
    dailySessionData:[10,10,10,10],//the attention values for daily sessions
    daily:[10,10,10,10],//the attention values for the overall day
    weekly:[10,10,10,10]//the attention values for the overall week
  
  }

  updateAll()

}

else{
  errorModal.show()
}

}


function closeErrorModal(){
  errorModal.hide()
}