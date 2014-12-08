//This code is a bit wiffy. Could probably use a healthy refactor and definitely needs better comments...



function chartNetwork(links){


var nodes = {},
    nodeCount = {},
    bilinks = [],
    drawLinks = [],
    relations = [],
    parent_hierarchies = [];

var i = 0;
links.forEach(function(link) {
  
  var match = link.source+"_"+link.target,
      rematch = link.target+"_"+link.source;


  //Flip them so we avoid the marker-start property which doesn't track well with the curved path.
  if(link.source_hierarchy=='parent'){
    parent_hierarchies.push(link.source+link.target);
  }else if(link.source_hierarchy=='child'){
    parent_hierarchies.push(link.target+link.source);
  }

  

  //Check to see if we've already made the match...
  if( relations.indexOf(match) == -1 & relations.indexOf(rematch) == -1 ){


      relations.push(link.source+"_"+link.target)

      nodeCount[link.source] = 1;
      nodeCount[link.target] = 1;

      link.source = nodes[link.source] || (nodes[link.source] = {name:link.source_name,type:link.source_type,id:link.source,});
      link.target = nodes[link.target] || (nodes[link.target] = {name:link.target_name,type:link.target_type,id:link.target,});

      


      i+=1
      var iID = i.toString(),
          fake = {name:"fake"+iID,type:"fake",id:"fake"+iID,};
      
      nodes["fake"+i.toString()]=fake;

      drawLinks.push({
          source:link.source,
          target:fake
        },{
          source:fake,
          target:link.target
        });

      //Flip them
      if(link.source_hierarchy!=='child'){
        bilinks.push([link.source,fake,link.target]);
      }else{
        bilinks.push([link.target,fake,link.source]);
      }
  }

});



//Some scaling for large numbers of nodes...
var nodeCount = Object.keys(nodeCount).length;

linkLength = d3.scale.log().base(10)
  .clamp(true)
  .domain([1,250])
  .range([-150,-10]);

if(nodeCount > 150){
  window.defaultRadius = 4,
  window.scaleRadius = 3,
  window.stroke = .1;
}else if(nodeCount > 75){
  window.defaultRadius = 6,
  window.scaleRadius = 5,
  window.stroke = .5;
}else{
  window.defaultRadius = 8,
  window.scaleRadius = 6,
  window.stroke = 1;
}




var width = graphWidth,
    height = graphHeight;

var color = d3.scale.ordinal().domain(['org','person']).range(['#5F9F9F','#FF8C69']);

var tickI = 0;

var force = d3.layout.force()
    .nodes(d3.values(nodes))
    .links(drawLinks)
    .size([width, height])
    .linkDistance(10)
    .charge(linkLength(nodeCount))
    .on("tick", function(){
      /*Tick limiter*/
      if(tickI%4==0){tick();};
      tickI+=1;
    })
    .start();

var svg = d3.select("#networkCanvas").append("svg")
    .attr("class","nodeCanvas")
    .attr("width", width)
    .attr("height", height);

svg.append("defs").append("svg:marker")
  .attr("id","arrowEnd")
  .attr("viewBox", "0 -5 10 10")
    .attr("refX", 22)
    .attr("refY", 0)
    .attr("markerWidth", 8)
    .attr("markerHeight", 8)
    .attr("orient", "auto")
    .attr("fill","#666")
  .append("svg:path")
    .attr("d", "M0,-5L10,0L0,5");
svg.append("defs").append("svg:marker")
  .attr("id","arrowStart")
  .attr("viewBox", "0 -5 10 10")
    .attr("refX", 22)
    .attr("refY", 0)
    .attr("markerWidth", 8)
    .attr("markerHeight", 8)
    .attr("orient", "auto")
    .attr("fill","#666")
  .append("svg:path")
    .attr("d", "M0,-5L10,0L0,5");
svg.append("defs").append("svg:marker")
  .attr("id","arrowKey")
  .attr("viewBox", "0 -5 10 10")
    .attr("refX", 0)
    .attr("refY", 0)
    .attr("markerWidth", 8)
    .attr("markerHeight", 8)
    .attr("orient", "auto")
    .attr("fill","#666")
  .append("svg:path")
    .attr("d", "M0,-5L10,0L0,5");

var link = svg.selectAll(".link")
    .data(bilinks)
  .enter().append("path")
    .attr("class",
      function(d){
        if((d[0].name==nodePRIME && d[2].name==nodeID)||(d[2].name==nodePRIME && d[0].name==nodeID)){
          return "primary link";
        }else{
          return "link";
        }
      })
    .attr("marker-end", function(d){
      return $.inArray(d[0].id + d[2].id, parent_hierarchies) > -1 ? "url(#arrowEnd)" : "";
    })
    .style("stroke-width",window.stroke);

var node = svg.selectAll(".node")
    .data(force.nodes())
  .enter().append("g")
    .attr("class",function(d) { return d.name==nodeID ?  d.id+" node primary" : d.id+ " node"; })
    .call(force.drag);

node.append("circle")
    .attr("r", defaultRadius)
    .attr("class",function(d) { return d.name==nodeID ?  d.id+" circ primary "+d.type : d.id+ " circ "+d.type; })
    .style("visibility",function(d){return d.type=="fake" ? "hidden":"visible" })
    /*.style("fill", function(d) { return color(d.type); })*/
    .on("mouseenter",visible)
    .on("mouseout",invisible);

node.append("text")
  .attr("class",function(d) { return d.name===nodeID ? d.id + " lab primary":d.id+" lab"; })
    .attr("x", function(d){ return d.type==="org" ? 12:10;})
    .attr("dy", ".35em")
    .attr("opacity",function(d) { return d.name===nodeID ?1:0;})
    .attr("pointer-events","none")
    .text(function(d) { return d.name; })
    .on("click",function(d){
      var id = d.id.substring(1);
      if(d.name===nodeID){}else{
      if(d.type==='person'){
        var url = replaceP.replace('foobarbaz',id);
      }else{
        var url = replaceO.replace('foobarbaz',id);
      }
      window.location = url;
      }
    })
    .on("mouseenter", mouseover)
    .on("mouseout", mouseout);


//Key
svg.append("circle")
  .attr("r",4)
  .attr("cx",width-60)
  .attr("cy",height-40)
  .attr("class","key org");
svg.append("text")
  .attr("class","key keyText")
  .attr("x",width-53)
  .attr("y",height-37)
  .text("Organization");
svg.append("circle")
  .attr("r",4)
  .attr("cx",width-60)
  .attr("cy",height-30)
  .attr("class","key person");
svg.append("text")
  .attr("class","key keyText")
  .attr("x",width-53)
  .attr("y",height-27)
  .text("Person");
svg.append("text")
  .attr("class","key keyText title")
  .attr("x",width-55)
  .attr("y",height-16)
  .text("Hierarchy");
svg.append("line")
  .attr("x1",width-60)
  .attr("x2",width-45)
  .attr("y1",height-10)
  .attr("y2",height-10)
  .attr("class","key link")
  .attr("marker-end", "url(#arrowKey)");
svg.append("text")
  .attr("class","key keyText")
  .attr("x",width-35)
  .attr("y",height-7)
  .text("child");


function visible(){
  if($(this).attr('class').split(' ')[3]!=='primary'){
    var selector = $(this).attr('class').split(' ')[0];
    var lab = d3.selectAll("."+selector+".lab");
    lab.transition().attr("opacity",1)
    .attr("pointer-events","all");
  }
}
function invisible(){
  if($(this).attr('class').split(' ')[3]!=='primary'){
    var selector = $(this).attr('class').split(' ')[0];
    var lab = d3.selectAll("."+selector+".lab");
    lab.transition().delay(3000).duration(500).attr("opacity",0).attr("pointer-events","none");
  }
}

function tick() {
  link.attr("d", function(d) {
      return "M" + d[0].x + "," + d[0].y
          + "S" + d[1].x + "," + d[1].y
          + " " + d[2].x + "," + d[2].y;
    });

  node
      .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
}

function mouseover() {
  d3.select(this).transition()
      .duration(250)
      .style("fill","#880000");
}

function mouseout() {
  d3.select(this).transition()
      .duration(250)
      .style("fill","#888888");
}

};


function nodeCentrality(measure){
  var data = graphData.centrality;
  
  var colors = ['#fcc5c0','#f768a1','#7a0177',],
      decimal = d3.format("0.2f");

  var color = d3.scale.linear()
                .domain([0,.5,1.0])
                .range(colors),
      c = d3.scale.linear()
                .domain(d3.extent( d3.values(data), function(d){return d[measure]} ) )
                .range([0,1]),
      sizeFactor = $(".slider").slider( "value" ),
      size = d3.scale.pow().exponent(sizeFactor)
                .domain(d3.extent( d3.values(data), function(d){return d[measure]} ) )
                .range([window.scaleRadius,13]);

  d3.selectAll(".lab").style("fill","#666");



  if( d3.selectAll('.colorKey')[0].length == 0){
      svg = d3.select('svg')
      var legend = svg.append("defs").append("svg:linearGradient").attr("id", "gradient").attr("x1", "0%").attr("x2", "100%").attr("spreadMethod", "pad");
      
      legend.append("stop")
        .attr("offset", "0%")
        .attr("stop-color", colors[0])
        .attr("stop-opacity", 1);
      legend.append("stop")
        .attr("offset", "50%")
        .attr("stop-color", colors[1])
        .attr("stop-opacity", 1);
      legend.append("stop")
        .attr("offset", "100%")
        .attr("stop-color", colors[2])
        .attr("stop-opacity", 1);
      svg.append("rect")
      .attr("class","colorKey")
      .attr("width",99)
      .attr("height",12)
      .attr("fill","url(#gradient)")
      .attr("x",graphWidth-114)
      .attr("y",15 );
      svg.append("text")
        .attr("class","colorKey")
        .attr("x",graphWidth-37)
        .attr("y",25)
        .style("fill","white")
        .style("font-weight","bold")
        .text("Max");
      svg.append("text")
        .attr("class","colorKey title")
        .attr("x",graphWidth-115)
        .attr("y",12)
        .text("Centrality");
      svg.append("text")
        .attr("class","centralityData degree")
        .attr("x",graphWidth-15)
        .attr("y",38)
        .attr("text-anchor","end")
        .text("");
      svg.append("text")
        .attr("class","centralityData betweenness")
        .attr("x",graphWidth-15)
        .attr("y",48)
        .attr("text-anchor","end")
        .text("");
      svg.append("text")
        .attr("class","centralityData closeness")
        .attr("x",graphWidth-15)
        .attr("y",58)
        .attr("text-anchor","end")
        .text("");
      
  }else{
    d3.selectAll(".colorKey")
    .style("opacity",1);
    
  }


  d3.selectAll(".key")
    .style("opacity",0);

  d3.selectAll('circle.circ')
    .on("mouseover",function(d){
      d3.select(".centralityData.degree").text(     "Degree: "+decimal(data[d.id].degree))
      d3.select(".centralityData.betweenness").text("Betweenness: "+decimal(data[d.id].betweenness))
      d3.select(".centralityData.closeness").text(  "Closeness: "+decimal(data[d.id].closeness))
    })
    .on("mouseleave",function(){
      d3.selectAll(".centralityData").text("")
    })
    .transition().duration(1500)
    .style("fill",function(d){return d.id.substring(0,4) == 'fake' ? '' : color(c(data[d.id][measure]))  })
    .attr("r",function(d){return d.id.substring(0,4) == 'fake' ? '' : size(data[d.id][measure])  });

}

function nodeDefault(){

  d3.selectAll('circle.circ')
    .on("mouseover","")
    .on("mouseleave","")
    .transition().duration(1500)
    .style("fill","")
    .attr("r", window.defaultRadius);
  d3.selectAll(".colorKey")
    .style("opacity",0);
  d3.selectAll(".key")
    .style("opacity",1);
}

function changeSize(factor,measure){

    var data = graphData.centrality;
    var size = d3.scale.pow().exponent(factor)
                .domain(d3.extent( d3.values(data), function(d){return d[measure]} ) )
                .range([window.scaleRadius,13]);
  
    d3.selectAll('circle.circ')
      .transition().duration(1000)
      .attr("r",function(d){return d.id.substring(0,4) == 'fake' ? '' : size(data[d.id][measure])  });
}