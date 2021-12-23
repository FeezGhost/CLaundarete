/*global $, document, LINECHARTEXMPLE*/
$(document).ready(function () {

    'use strict';

    var brandPrimary = 'rgba(51, 179, 90, 1)';

    var PIECHARTEXMPLE    = $('#pieChartExample'),
        RADARCHARTEXMPLE  = $('#radarChartExample');



    var radarChartExample = new Chart(RADARCHARTEXMPLE, {
        type: 'radar',
        data: {
            labels: ["Eating", "Drinking", "Sleeping", "Designing", "Coding", "Cycling"],
            datasets: [
                {
                    label: "My First dataset",
                    backgroundColor: "rgba(179,181,198,0.2)",
                    borderWidth: 2,
                    borderColor: "rgba(179,181,198,1)",
                    pointBackgroundColor: "rgba(179,181,198,1)",
                    pointBorderColor: "#fff",
                    pointHoverBackgroundColor: "#fff",
                    pointHoverBorderColor: "rgba(179,181,198,1)",
                    data: [65, 59, 90, 81, 56, 55]
                },
                {
                    label: "My Second dataset",
                    backgroundColor: "rgba(51, 179, 90, 0.2)",
                    borderWidth: 2,
                    borderColor: "rgba(51, 179, 90, 1)",
                    pointBackgroundColor: "rgba(51, 179, 90, 1)",
                    pointBorderColor: "#fff",
                    pointHoverBackgroundColor: "#fff",
                    pointHoverBorderColor: "rgba(51, 179, 90, 1)",
                    data: [28, 48, 40, 19, 96, 27]
                }
            ]
        }
    });
    var radarChartExample = {
        responsive: true
    };



});
