function chartNetwork(links){




var nodes = {};

// Compute the distinct nodes from the links.
links.forEach(function(link) {
  link.source = nodes[link.source] || (nodes[link.source] = {name:link.source_name,type:link.source_type,id:link.source});
  link.target = nodes[link.target] || (nodes[link.target] = {name:link.target_name,type:link.target_type,id:link.target});
});

var width = 500,
    height = 250;

var color = d3.scale.ordinal().domain(['org','person']).range(['#5F9F9F','#FF8C69']);

var tickI = 0;

var force = d3.layout.force()
    .nodes(d3.values(nodes))
    .links(links)
    .size([width, height])
    .linkDistance(30)
    .charge(-600)
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
    .data(force.links())
  .enter().append("line")
    .attr("class", function(d){
      if((d.source.name==nodePRIME && d.target.name==nodeID)||(d.target.name==nodePRIME && d.source.name==nodeID)){
        return "primary link";
      }else{
        return "link";
      }});
var node = svg.selectAll(".node")
    .data(force.nodes())
  .enter().append("g")
    .attr("class",function(d) { return d.name==nodeID ?  d.id+" node primary" : d.id+ " node"; })
    .call(force.drag);

node.append("circle")
    .attr("r", function(d){ return d.type==="org" ? 10:8;})
    .attr("class",function(d) { return d.name==nodeID ?  d.id+" circ primary" : d.id+ " circ"; })
    .style("fill", function(d) { return color(d.type); })
    .on("mouseover",visible)
    .on("mouseout",invisible)
    ;



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
    .on("mouseover", mouseover)
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
  link
      .attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

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