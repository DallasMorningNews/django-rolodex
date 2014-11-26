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
    .attr("class",function(d) { return d.name==nodeID ?  d.id+" circ primary" : d.id+ " circ"; })
    .style("visibility",function(d){return d.type=="fake" ? "hidden":"visible" })
    .style("fill", function(d) { return color(d.type); })
    .on("mouseenter",visible)
    .on("mouseout",invisible);

node.append("text")
	.attr("class",function(d) { return d.name===nodeID ? d.id + " lab primary":d.id+" lab"; })
    .attr("x", function(d){ return d.type==="org" ? 12:10;})
    .attr("dy", ".35em")
    .style("fill","#888888")
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