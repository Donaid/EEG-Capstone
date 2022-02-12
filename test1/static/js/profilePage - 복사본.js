var socket = new WebSocket('ws://localhost:8000/ws/test1')

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
const readWriteHighAttention=document.getElementById('consecutiveLowAttentionRW');

const sessionsCompletedAV=document.getElementById('sessionsCompletedAV')
const sessionsCompletedRW=document.getElementById('sessionsCompletedRW')
const highToTotalAV=document.getElementById('highToTotalAV')
const highToTotalRW=document.getElementById('highToTotalRW')


//fill up userData object using back-end
let userData={
userName:33,
idealStudyTime:33,
audioVideoHighAttention:33,
readWriteHighAttention:33,

sessionsCompletedAV:33,
sessionsCompletedRW:33,
highToTotalAV:33,
highToTotalRW:33,
graphHighAttention:33,
graphLowAttention:33,
}


//this function will update the graph using userData object

function updateChart(){
    hLChart.data.datasets[0].data[0]=userData.graphHighAttention;
    hLChart.data.datasets[0].data[1]=userData.graphLowAttention;
    hLChart.update();

}


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
updateData();
updateChart();
//----------------------Daily Sessions Chart---------------------------------------------

const ctx2 = document.getElementById('dailySessionsChart').getContext('2d');

var dSChart = new Chart(ctx2, {
    type: 'bar',
    data: {
        labels: [["session 1",'0900-1000'], ["session 2",'0900-1000'], ["session 3",'0900-1000'], ["session 4",'0900-1000']],
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
     plugins: [{
    beforeInit: function (chart) {
      chart.data.labels.forEach(function (e, i, a) {
        if (/\n/.test(e)) {
          a[i] = e.split(/\n/)
        }
      })
    }
  }]
});

//----------------------Daily Chart---------------------------------------------

const ctx3 = document.getElementById('dailyChart').getContext('2d');

var dChart = new Chart(ctx3, {
    type: 'bar',
    data: {
        labels: ['High Attention', 'Low Attention','High Attention','Low Attention'],
        datasets: [{
            label:['Aural/Visual'],
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
     plugins: [{
    beforeInit: function (chart) {
      chart.data.labels.forEach(function (e, i, a) {
        if (/\n/.test(e)) {
          a[i] = e.split(/\n/)
        }
      })
    }
  }]
});

//----------------------Weekly Chart---------------------------------------------

const ctx4 = document.getElementById('weeklyChart').getContext('2d');

var wChart = new Chart(ctx4, {
    type: 'bar',
    data: {
        labels: ['High Attention', 'Low Attention','High Attention','Low Attention'],
        datasets: [{
            label:['Aural/Visual'],
            data: [12, 19, 3, 5],
            backgroundColor: [
                'rgba(255,0,0,0.5)',
                'rgba(0,0,255, 0.5)',
                'rgba(255,0,0,.5)',
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
     plugins: [{
    beforeInit: function (chart) {
      chart.data.labels.forEach(function (e, i, a) {
        if (/\n/.test(e)) {
          a[i] = e.split(/\n/)
        }
      })
    }
  }]
});

//----------------------Updating the Bottom 3 Graphs---------------------------------------------

const date1=document.getElementById('dateSelected1')

//fill this object using date1 with userData
let graphData1={
  dailySessionTiming:[['session 1','09-12'],['session 2','12-01'],['session 3','09-12']],//in this array fill up the attention value and the time of the session
  dailySessionData:[30,40,50],
  daily:[12,12,4,5],//the attention values for the overall day
  weekly:[1,1,4,5]//the attention values for the overall week

}



function fillDailySessionsGraph(){//fills daily sessions graph
  dSChart.data.labels=graphData1.dailySessionTiming;
  dSChart.data.datasets[0].backgroundColor=[]
  dSChart.data.datasets[0].data=[]
  for(i=0;i<graphData1.dailySessionData.length;i++){
    
   dSChart.data.datasets[0].data.push(graphData1.dailySessionData[i])
    
    

    if(graphData1.dailySessionData[i]>=50){
      dSChart.data.datasets[0].backgroundColor.push('rgba(0,0,255,0.5)')
   


    }
    else{
      dSChart.data.datasets[0].backgroundColor.push('rgba(255,0,0,0.5)');
    }
 
  }
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

function updateData(){//called when submit button is pressed and calls all the graph functions and fills the graphs
  fillDailySessionsGraph()
 


}
