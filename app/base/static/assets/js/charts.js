"use strict";
const d = document;
d.addEventListener("DOMContentLoaded", function(event) {

    //Chartist

    if(d.querySelector('.ct-chart-test1')) {
        //Chart 5
          new Chartist.Line('.ct-chart-test1', {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'RANDOM'],
            series: [
                [0, 10, 30, 40, 80, 60, 300]
            ]
          }, {
            low: 0,
            showArea: true,
            fullWidth: true,
            plugins: [
              Chartist.plugins.tooltip()
            ],
            axisX: {
                // On the x-axis start means top and end means bottom
                position: 'end',
                showGrid: true
            },
            axisY: {
                // On the y-axis start means left and end means right
                showGrid: false,
                showLabel: false,
                labelInterpolationFnc: function(value) {
                    return '$' + (value / 1) + 'k';
                }
            }
        });
    }
});
