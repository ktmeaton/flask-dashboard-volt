"use strict";

var system_share = document.currentScript.getAttribute('system_share');
window.alert(system_share)
document.addEventListener("DOMContentLoaded", function(event) {

  if(document.querySelector('.ct-chart-system-share')) {
      var data = {
          series: [20,10,30,40]
        };

        var sum = function(a, b) { return a + b };

        new Chartist.Pie('.ct-chart-system-share', data, {
          labelInterpolationFnc: function(value) {
            return Math.round(value / data.series.reduce(sum) * 100) + '%';
          },
          low: 0,
          high: 8,
          donut: true,
          donutWidth: 20,
          donutSolid: true,
          fullWidth: false,
          showLabel: false,
          plugins: [
            Chartist.plugins.tooltip()
          ],
      });
  }

});
