//modified from http://bl.ocks.org/peterbsmith2/a37f2b733a75a6f348c2


function calDraw(data){

  Date.prototype.toJSONLocal = function() {
    function addZ(n) {
      return (n<10? '0' : '') + n;
    }
    return this.getFullYear() + '-' +
           addZ(this.getMonth() + 1) + '-' +
           addZ(this.getDate());
  }; // From : http://stackoverflow.com/questions/11382606/javascript-date-tojson-dont-get-the-timezone-offset

  function makeUTCDate(dateString){
    var d = new Date(dateString);
    return new Date(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate(),  d.getUTCHours(), d.getUTCMinutes());
  }

  function addDays(date, days) {
      var result = new Date(date);
      result.setDate(date.getDate() + days);
      return result;
  } // From: http://stackoverflow.com/questions/563406/add-days-to-datetime


  var calendarDays = window.innerWidth > 420 ? 365/2 : 31*3 ;

  //calendar array
  var calendar = [];

  //yAxis array to store which column month labels will go on
  var yAxis = [];

  //todays date
  var today = new Date();

  //last Years date
  var lastYear = addDays(today,(-calendarDays));

  //initialize column to 0
  var col = 0;

  //get the month of a year ago
  var month = lastYear.getMonth();

  //boolean for first sunday
  var first = true;

  //formatters for yaxis and tool tip
  var yAxisFormatter = d3.time.format("%b");
  var tipFormatter = d3.time.format("%m/%d/%Y");

  //for 365 days
  for (i=0; i <= (calendarDays); i++){

    //get date as a string
    dateString = lastYear.toJSONLocal();

    //make a UTC (no timezone offset) date
    var date = makeUTCDate(dateString);

    //c is current day of week
    var c = date.getDay();

    //if sunday, if january, and it's the first sunday
    if (c === 0 && date.getMonth() === 0 && first){
      //set month to -1 to allow following if block to run
      month = -1;
      //only do this for the first Sunday
      first = !first;
    }

    //if its sunday and a new month
    if (c === 0 && date.getMonth() > month){
        //add a new object to yAxis indicating the position and month for labeling
        yAxis.push({
          col: col,
          month: yAxisFormatter(date)
        });
        month++;
    }
    //add datum to calendar array including the date, initialized count, and column for positioning
    calendar.push({
      date: date,
      count: 0,
      col: col,
    });

    //add next time through the loop, use the next day and if its a saturday start a new column
    lastYear = addDays(lastYear,1);
    if (c === 6){ col++; }
  }

  var margin = {top: 20, right: 45, bottom: 25, left: 45}; //margins
  var width = 9 + ((calendarDays/7)*11); // 1 square + 53 squares with 2px padding
  var height = 9 + 6*11; //1 square + 6 squares with 2px padding
  var legendX = 18; //x Position for legend
  var legendY = height + 5; //y position for legend

  //append svg with a g object accounting for margins
  var svg = d3.select('#SearchCalendar').append('svg')
        .attr('width',width + margin.left + margin.right)
        .attr('height',height + margin.top + margin.bottom)
      .append('g')
        .attr('transform','translate('+margin.left+','+margin.top+')');

  //Lazy y-axis from GitHub's commit calendar
  svg.append('text')
    .text('M')
    .style('fill','#ccc')
    .attr('text-anchor','middle')
    .attr('dx','-10')
    .attr('dy','19');

  svg.append('text')
    .text('W')
    .style('fill','#ccc')
    .attr('text-anchor','middle')
    .attr('dx','-10')
    .attr('dy','41');

  svg.append('text')
    .text('F')
    .attr('text-anchor','middle')
    .style('fill','#ccc')
    .attr('dx','-10')
    .attr('dy','63');

  //Prepare Calendar
  svg.selectAll('.cal')
      .data(calendar)
      .enter()
    .append('rect')
      .attr('class','cal')
      .attr('width',9)
      .attr('height',9)
      .attr('x',function(d,i){return d.col*11;})
      .attr('y',function(d,i){return d.date.getDay() * 11;})
      .attr('fill','#eeeeee');

  var colorScale = d3.scale.threshold() //based on http://www.perbang.dk/rgbgradient/ from #eee to #FF8C00
        .range(['#eeeeee','#F2D5B2','#F6BD77','#FAA43B','#FF8C00']);

  //Prepare y Axis
  svg.selectAll('.y')
      .data(yAxis)
      .enter()
    .append('text')
      .text(function(d){ return d.month;})
      .attr('dy',-5)
      .attr('dx',function(d){
        return d.col*11;
      })
      .attr('fill','#ccc');

  //Prepare Legend
  svg.selectAll('.legend')
      .data(colorScale.range())
      .enter()
    .append('rect')
      .attr('class','legend')
      .attr('width',11)
      .attr('height',11)
      .attr('x',function(d,i){ return legendX + i*12; })
      .attr('y',legendY)
      .attr('fill',function(d){ return d; });

  svg.append('text')
    .attr('class','legend')
    .attr('x', legendX - 30)
    .attr('y',legendY + 10)
    .text('Fewer');

  svg.append('text')
    .attr('class','legend')
    .attr('x', legendX + 5*12)
    .attr('y',legendY + 10)
    .text('More');



  //instantiate events object
  var events = {};

  //for each item in array, starting with the last
  var l = data.length;
  while(l--){
    //get the day of the event
    var eventDate = data[l].date.substr(0,10);
    //if the events object doesn't have the current event's day as a key, create a key and give it a value 0
    if(!events[eventDate]){
      events[eventDate] = 0;
    }

    //+1 to event's value
    events[eventDate]++;
  }

  //for every day in the calendar (365)
  for (var i = 0; i < calendar.length; i++) {
    //if current calendars day matches a day key in the events object
    if (events[calendar[i].date.toJSONLocal()]){
      //calendar's count = events count
      calendar[i].count = events[calendar[i].date.toJSONLocal()];
    }
  }

  //calculate min, max excluding 0
  var extent = d3.extent(calendar, function(d){ return d.count === 0 ? null : d.count; });

  //Default this to .1, so zero is always null
  extent[0] = extent[0] == 1 ? 0.1 : extent[0];

  //calculate a range of 4 values, starting with min, stopping with max, spaced evenly
  var range = d3.range(extent[0],extent[1],((extent[1]-extent[0])/4));


  //use range as domain
  colorScale.domain(range);


  //Give calendar color based on # events and add tooltip events
  svg.selectAll('.cal')
    .attr('fill',function(d,i){
      return colorScale(d.count);
    })
    .on('mouseover',function(d){
      var xPosition = parseFloat(d3.select(this).attr("x"));
      var yPosition = parseFloat(d3.select(this).attr("y"));

      xPosition = xPosition < 90 ? 100 : xPosition;
      xPosition = xPosition > width + margin.left + margin.right - 140 ? width + margin.left + margin.right - 140 : xPosition;

      svg.append('rect')
        .attr('class','tip')
        .attr('x',xPosition - 90)
        .attr('y',yPosition - 20)
        .attr('rx',3)
        .attr('ry',3)
        .attr('width',140)
        .attr('height',20)
        .style({
          'fill': 'rgba(0,0,0,0.6)',
          'border': '2px solid #FFF'
        });


      svg.append('text')
        .text(d.count + " searches " + tipFormatter(d.date))
        .attr('x',xPosition - 85)
        .attr('y',yPosition -6)
        .style({
            fill: "#FFF",
            'font-weight': 'bold',
        })
        .attr('class','tip');

    })
    .on('mouseout',function(d){
      svg.selectAll('.tip').remove();
    });

};