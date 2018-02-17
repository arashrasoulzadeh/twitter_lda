<script>
var ctx = document.getElementById("rtchart").getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [
            {% for item in rtChart %}
                    ["{{item.date}}"] ,
           {% endfor %}


        ],
        datasets: [{
            label: '# of RT',
            data: [

                 {% for item in rtChart %}
                    {{item.c}}   ,
           {% endfor %}
            ],

            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});
</script>


<script>
var ctx = document.getElementById("favchart").getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [
            {% for item in favsChart %}
                    ["{{item.date}}"] ,
           {% endfor %}


        ],
        datasets: [{
            label: '# of RT',
            data: [

                 {% for item in favsChart %}
                    {{item.c}}   ,
           {% endfor %}
            ],

            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});
</script>

