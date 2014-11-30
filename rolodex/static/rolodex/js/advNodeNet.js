function chartNetwork(links){

var nodes = {},
    bilinks = [],
    drawLinks = [],
    relations = [];

var i = 0;
links.forEach(function(link) {
  
  var match = link.source+"_"+link.target,
      rematch = link.target+"_"+link.source;

  //Check to see if we've already made the match...
  if( relations.indexOf(match) == -1 & relations.indexOf(rematch) == -1 ){

      relations.push(link.source+"_"+link.target)

      link.source = nodes[link.source] || (nodes[link.source] = {name:link.source_name,type:link.source_type,id:link.source});
      link.target = nodes[link.target] || (nodes[link.target] = {name:link.target_name,type:link.target_type,id:link.target});


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

      bilinks.push([link.source,fake,link.target]);
  }

});

//Some scaling for large numbers of nodes...
linkLength = d3.scale.linear()
  .domain([1,150])
  .range([-125,-30]);

var width = graphWidth,
    height = graphHeight;

var color = d3.scale.ordinal().domain(['org','person']).range(['#5F9F9F','#FF8C69']);

var tickI = 0;

var force = d3.layout.force()
    .nodes(d3.values(nodes))
    .links(drawLinks)
    .size([width, height])
    .linkDistance(10)
    .charge(linkLength(drawLinks.length))
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
      });

var node = svg.selectAll(".node")
    .data(force.nodes())
  .enter().append("g")
    .attr("class",function(d) { return d.name==nodeID ?  d.id+" node primary" : d.id+ " node"; })
    .call(force.drag);

node.append("circle")
    .attr("r", function(d){ return d.type==="org" ? 10:8;})
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
  
  var colors = ['#fcc5c0','#f768a1','#7a0177',];

  var color = d3.scale.linear()
                .domain([0,.5,1.0])
                .range(colors),
      c = d3.scale.linear()
                .domain(d3.extent( d3.values(data), function(d){return d[measure]} ) )
                .range([0,1]),
      size = d3.scale.pow().exponent(10)
                .domain(d3.extent( d3.values(data), function(d){return d[measure]} ) )
                .range([6,13]);

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
      .attr("width",97)
      .attr("height",12)
      .attr("fill","url(#gradient)")
      .attr("x",graphWidth-160)
      .attr("y",10 );
      svg.append("text")
        .attr("class","colorKey")
        .attr("x",graphWidth-180)
        .attr("y",20)
        .text("Min");
      svg.append("text")
        .attr("class","colorKey")
        .attr("x",graphWidth-60)
        .attr("y",20)
        .text("Max");

  }else{
    d3.selectAll(".colorKey")
    .style("opacity",1);
  }


  d3.selectAll('circle.circ')
    .transition().duration(1500)
    .style("fill",function(d){ return d.id.substring(0,4) == 'fake' ? '' : color(c(data[d.id][measure]))  })
    .attr("r",function(d){return d.id.substring(0,4) == 'fake' ? '' : size(data[d.id][measure])  });

}

function nodeDefault(){
  d3.selectAll('circle.circ')
    .transition().duration(1500)
    .style("fill","")
    .attr("r", function(d){ return d.type==="org" ? 10:8;});
  d3.selectAll(".colorKey")
    .style("opacity",0);
}