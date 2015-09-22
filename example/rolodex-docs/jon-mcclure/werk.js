var Werk = (function(){

    var werk = { chart:{ } };


    ///////////////////////////////////////
    // DATA PARSERS ///////////////////////////////
    //////////////////////////////////
    ///////////////////////////////////////////

    //This function parses data pasted into the window
    //Parser expects TSV data at this point
    function parseData(){
        var pasteVal = $('#data-paste').val(),
            info = pasteVal.replace(/['"]/g,''),
            lines = info.split('\n'),
            header = lines.shift().split('\t'),
            json = [];


        //Helper function to remove quotes and parse numeric values
        function removeQuotes(string){
                                        string = string.replace(/(['"])/g, "\\$1");
                                        if (!isNaN(string)){
                                            string = isNaN(parseFloat(string)) ? undefined : parseFloat(string);
                                        };
                                        return string;
                                    };


        //Creates table to preview parsed data
        function previewTable(json){
                                        var element = $("#data-rendered");

                                        element.empty();

                                        var header_data = Object.keys(json[0]);

                                        $("<table class='previewTable' data-toggle='table'><thead></thead><tbody></tbody></table>").appendTo(element);
                                        var tablehead = $("table.previewTable thead");
                                        var tablebody = $("table.previewTable tbody");
                                        $("<tr></tr>").appendTo(tablehead);

                                        header_data.forEach(function(e){
                                            var tr = $("table.previewTable tr").last();
                                            $("<th data-field='"+e+"'>"+e+"</th>").appendTo(tr);
                                        });

                                        $("table.previewTable").bootstrapTable({
                                            data: json,
                                        });
                                    };


        $.each(lines, function(index, item){
            //No blank lines
            if(item != ""){
                var lineItem = item.split('\t'),
                    jsonLineEntry = {};

                $.each(lineItem, function(index, item){
                    jsonLineEntry[header[index]] = removeQuotes(item);
                });
                json.push(jsonLineEntry);
            };
        });


        previewTable(json);

        return json;
    };

    //Returns all the unique values at a given key in an array of objects
    function valsAtKey(dataArray,key){
        var valueArray = [];
        for(var obj in dataArray){
            valueArray.push(dataArray[obj][key]);
        }
        //unique array
        return _.uniq(valueArray)
    };


    ///////////////////////////////////////
    // DATA GETTERS ///////////////////////////////
    //////////////////////////////////
    ///////////////////////////////////////////

    //These functions get data from UI elements

    //Data column mapped to data types
    function getDatamap(){
        var columns = {},
            series = [],
            annotations = [],
            ignore = [];

        $("select.column-classify").each(function(){
            if( $(this).val() ==='base'){
                columns['base'] = $(this).attr("name")
                $("#baseName").html( $(this).attr("name") );
            }else if($(this).val()==='group'){
                columns['group'] = $(this).attr("name")
            }else if($(this).val()==='series'){
                series.push($(this).attr("name"))
            }else if($(this).val()==='annotation'){
                annotations.push($(this).attr("name"))
            }else if($(this).val()==='ignore'){
                ignore.push($(this).attr("name"))
            }

        });

        columns['series'] = series
        columns['annotations'] = annotations
        columns['ignore'] = ignore

        return columns;
    };

    //Get color range and domain
    function getColorData(){
        var seriesColors = {},
        colorRange = [],
        seriesRange = [],
        ramp = false;
        $("select.colorpicker-series").each(function(){
            seriesRange.push($(this).attr("data-column"));
            colorRange.push($(this).val());
        });

        //If colorRamp is selected, swap out colorRange for a color ramp
        if( $("input.colorRamp-select").is(":checked") ){
            var primaryPick = $("select.colorpicker-series")[0],
                pickers = $(".simplecolorpicker.icon"),
                primaryColor = $(primaryPick).val(),
                colorRange = $("i#colorRampDirect").hasClass("fa-arrow-circle-up") ? chartUtils.colorRamp(primaryColor, pickers.length) : chartUtils.colorRamp(primaryColor, pickers.length).reverse();
            //set ramp to primary color
            ramp = primaryColor;
            seriesColors['rampReverse'] = $("i#colorRampDirect").hasClass("fa-arrow-circle-down") ? true : false;
        }

        seriesColors['domain'] = seriesRange;
        seriesColors['range'] = colorRange;
        seriesColors['ramp'] = ramp;
        return seriesColors;
    };

    //Axis config from Axis Tab
    function getAxisData(){
        var baseObject = {},
        valueObject = {},

        numArray = function(commaString){
            return commaString != "" ? commaString.split(",").map(Number) : "";
        };

        $(".baseAxis-opt").each(function(){
            baseObject[$(this).attr("name")] = $(this).val();
        });
        $(".valueAxis-opt").each(function(){
            valueObject[$(this).attr("name")] = $(this).val();
        });

        //Annotations
        var baseNotes = [],
            valueNotes = [];
        $("#base-annotate .annotation").each(function(){
            noteObject ={};
            noteObject.label  = $(".annote-label", $(this) ).val();
            //Two annotation points are split by a colon.
            noteObject.points = $(".annote-axis",  $(this) ).val().split(":");
            baseNotes.push(noteObject);
        });
        $("#value-annotate .annotation").each(function(){
            noteObject ={};
            noteObject.label = $(".annote-label",$(this)).val();
            noteObject.points = $(".annote-axis",$(this)).val().split(":");
            valueNotes.push(noteObject);
        });

        baseObject.annotations = baseNotes
        valueObject.annotations = valueNotes

        baseObject.customTicks = numArray(baseObject.customTicks)
        valueObject.customTicks = numArray(valueObject.customTicks)

        return {'base':baseObject, 'value':valueObject}
    };

    //Get margin settings
    function getMarginsData(){
        marginsObject = {};
        $(".marginInput").each(function(){
            //name attr is top, bottom, left or right
            marginsObject[$(this).attr("name")] = parseInt($(this).val());
        });
        return marginsObject;
    };

    //Get custom schema data from alpaca form
    function getSchemaData(){
        var schemaData = {};
        $("#alpacaForm").serializeArray().forEach(function(e){
            schemaData[e.name] = e.value
        });
        return schemaData;
    };

    //Get key grid alignment
    function getAlignments(){
        var align = {};
        align['key'] = $("input[name='keyGrid']:checked").attr("value");
        align['stackMobile'] = $("input[name='keyStackMobile']").is(":checked")
        align['stackDesktop'] = $("input[name='keyStackDesktop']").is(":checked")
        //Disable key align checkbox if we're stacking keys on Desktop
        if($("input[name='keyStackDesktop']").is(":checked")){
            $("#radioKeyGrid").addClass("disabled");
        }else{
            $("#radioKeyGrid").removeClass("disabled");
        }
        return align;
    };

    //Get size of browser target
    function getSize(){
        if($("#size-desktop").is(":checked")){
            $("#previewWindow p.wrapText").show();
            $("#chart-logo img.desktop").show();
            $("#chart-logo img.mobile").hide();
            $("#chart").removeClass("mobile");
            $("#chart").addClass("desktop");
            return "desktop"
        }else{
            $("#previewWindow p.wrapText").show();
            $("#chart-logo img.mobile").show();
            $("#chart-logo img.desktop").hide();
            $("#chart").addClass("mobile");
            $("#chart").removeClass("desktop");
            return "mobile"
        }
    };



    //Builds the config object
    werk.buildConfig = function(){

                                werk.config = {
                                    data: parseData(),
                                    rawData: $('#data-paste').val(),
                                    datamap: getDatamap(),
                                    color : getColorData(),
                                    axes: getAxisData(),
                                    margin: getMarginsData(),
                                    schema: getSchemaData(),
                                    align: getAlignments(),
                                    size: getSize()
                                };

                                //Reset and redraw.
                                $("#d3-canvas").empty();
                                $("#preview-alerts .alert").hide();

                                // PUBLISH ----->
                                PubSub.publish('builtConfig', werk.config);

                                //Assign global draw func to private chart func
                                werk.chart.draw = draw

                                werk.chart.draw(werk.config.data, werk.config);

                        };



    ///////////////////////////////////////
    // UI ////////////////////////////////////////
    //////////////////////////////////
    ///////////////////////////////////////////

    //These functions set UI elements based on entered data.


    //UI public funcs are called as subscriptions
    werk.UI = {


        //A function to make single values in a series of dropdowns exclusive, ie,
        //if that opt is selected in one dropdown, it becomes unavailable in all others
        //Using this for Base Axis and Grouping Column.
        singleSelect: function(selector, value){
                                                    var flag = false;
                                                    $(selector).each(function(){
                                                        if($(this).val() === value){ flag = true };
                                                    });

                                                    //If there is one with value selected, disable value on all others
                                                    if( flag === true){
                                                        $(selector).each(function(){
                                                            if($(this).val() !== 'base' && $(this).val() !== 'group'){ 
                                                                $(this).children("option[value='"+value+"']").prop('disabled', true);
                                                            };
                                                        });
                                                    }
                                                    //else make opt available to every column
                                                    else{
                                                        $(selector).each(function(){
                                                            $(this).children("option[value='"+value+"']").prop('disabled', false);
                                                        });
                                                    };
                                                },

        //Creates dropdowns for mapping data columns to data types
        dataMapDrops: function(msg, config){

                                            var that = this;

                                            var json = parseData(),
                                                header_data = Object.keys(json[0]);

                                            var optsTable = $("#column-classify-options");

                                            optsTable.empty();

                                            $("#classify-cont").show();

                                            header_data.forEach(function(e, i){

                                                optsTable.append("<tr></tr>");

                                                var tr = optsTable.find("tr").last();

                                                tr.append("<td>"+e+"</td>");
                                                tr.append("<td><select name='"+e+"' data-column='"+e+"' class='form-control column-classify rebuild'></select></td>");
                                                tr.append("<td class='color-select' data-column='"+e+"'></td>");

                                                var select = optsTable.find("select").last();



                                                select.append(partialClassify)

                                                //Default to "base axis" for first column
                                                //"data series" to the rest.
                                                if(i > 0){
                                                    select.children("option").eq(1).prop('selected', true);
                                                    select.children("option").eq(0).prop('disabled', true);
                                                }

                                                //Change to allow for only one base and grouping axis
                                                select.change(function(){
                                                    that.singleSelect($(".column-classify"),"base");
                                                    that.singleSelect($(".column-classify"),"group");
                                                    that.addRemoveColor($(this));
                                                    that.colorRampSelect();

                                                    // PUBLISH ----->
                                                    PubSub.publish('dataMap.select');
                                                    PubSub.publish('rebuild.resetEvents');
                                                });


                                                //initial add remove colors
                                                $('select.column-classify').each(function(){ that.addRemoveColor($(this)); });


                                                //Color ramp select
                                                that.colorRampSelect();
                                                


                                                // PUBLISH ----->
                                                PubSub.publish('rebuild.resetEvents');

                                            })

                                        },


        //Adds or removes color pickers for data series columns only
        //Also adds check box for group to color by group
        addRemoveColor: function(select){
                                            var that = this;

                                            series = select.attr("data-column");
                                            td = $("td.color-select[data-column='"+series+"']");
                                            td.empty();


                                            if(select.val() === 'series'){
                                                td.append('<select data-column="'+series+'" class="colorpicker-series selected-color rebuild"></select>');
                                                
                                                var select = $('select.colorpicker-series[data-column="'+series+'"]');
                                                select.append(partialColor);
                                                select.simplecolorpicker({picker: true, theme: 'glyphicons'});
                                                select.change(function(){ getColorData(); that.colorRampSet(); werk.buildConfig(); });

                                            //If group add color by group opt
                                            }else if(select.val() === 'group'){
                                                
                                                td.append("<label> Color by groups? <input type='checkbox' data-column='"+series+"' class='colorByGroup-select rebuild'></label>");
                                                $(".colorByGroup-select").change(function(){ that.groupColors(); that.colorRampSet(); werk.buildConfig(); });

                                            };

                                        },

        //Creates color pickers when coloring by group.
        groupColors: function(){

                                    var that = this;

                                    var group = $(".colorByGroup-select").attr("data-column");
                                    $("#colorGroups").empty();

                                    if($(".colorByGroup-select").is(":checked")){

                                        $("#colorGroup-cont").show();
                                        $(".colorpicker-series").parent("td").empty();

                                        var json = parseData(),
                                        series = valsAtKey(json,group);
                                        

                                        $.each(series,function(i){
                                            var group = series[i];

                                            if(i===0){
                                                $("#colorGroups")
                                                    .append('<select data-column="'+group+'" class="colorpicker-series selected-color rebuild"></select><label class="control-label">'+group+'</label><label id="colorRampOpt">Gradient? <input type="checkbox" class="colorRamp-select"></label> <i id="colorRampDirect" class="fa fa-arrow-circle-up"></i><br>');
                                            }else{
                                                $("#colorGroups")
                                                    .append('<select data-column="'+group+'" class="colorpicker-series selected-color rebuild"></select><label class="control-label">'+group+'</label><br>');
                                            }
                                            
                                            var select = $('select.colorpicker-series[data-column="'+group+'"]');
                                            select.append(partialColor);
                                            select.simplecolorpicker({picker: true, theme: 'glyphicons'});
                                            select.change(function(){ that.colorRampSet(); });
                                            PubSub.publish('rebuild.resetEvents');
                                            

                                        });
                                    }else{
                                        $("#colorGroup-cont").hide();
                                        $('select.column-classify').each(function(){ that.addRemoveColor($(this)); });
                                    }


                                    $("i#colorRampDirect").click(function(){
                                        if($(this).hasClass("fa-arrow-circle-up")){
                                            $(this).removeClass("fa-arrow-circle-up").addClass("fa-arrow-circle-down");
                                        }else{
                                            $(this).removeClass("fa-arrow-circle-down").addClass("fa-arrow-circle-up");
                                        }
                                        that.colorRampSet();
                                        PubSub.publish('rebuild.resetEvents');
                                    });
                                    
                                    //Check ramp func
                                    $("input.colorRamp-select").change(function(){
                                        that.colorRampSet();
                                    });
                                    that.colorRampSet();

                                    // PUBLISH ----->
                                    PubSub.publish('rebuild.resetEvents');
                                },

        //
        colorRampSelect: function(){
                                        var that = this;
                                       
                                        $("label#colorRampOpt, i#colorRampDirect").remove();
                                        if( $(".simplecolorpicker.icon").length > 1 ){
                                            var firstPicker = $(".simplecolorpicker.icon")[0],
                                                pickerParent = $(firstPicker).parent("td");
                                                $(pickerParent).append("<label id='colorRampOpt'>Gradient? <input type='checkbox' class='colorRamp-select'></label> <i id='colorRampDirect' class='fa fa-arrow-circle-up'></i>");
                                        } 

                                        $("i#colorRampDirect").click(function(){
                                            if($(this).hasClass("fa-arrow-circle-up")){
                                                $(this).removeClass("fa-arrow-circle-up").addClass("fa-arrow-circle-down");
                                            }else{
                                                $(this).removeClass("fa-arrow-circle-down").addClass("fa-arrow-circle-up");
                                            }
                                            that.colorRampSet();
                                            PubSub.publish('rebuild.resetEvents');
                                        });

                                        //Check ramp func
                                        $("input.colorRamp-select").change(function(){
                                            that.colorRampSet();
                                        });
                                        that.colorRampSet();


                                    },

        //sets the picker span background colors according to values in color ramp
        //does not set the actual color ramp values, which happens in the config build getColorData 
        colorRampSet: function(){
                                    var primaryPick = $("select.colorpicker-series")[0],
                                        pickers = $(".simplecolorpicker.icon"),
                                        primaryColor = $(primaryPick).val(),
                                        pickerRamp = $("i#colorRampDirect").hasClass("fa-arrow-circle-up") ? chartUtils.colorRamp(primaryColor, pickers.length) : chartUtils.colorRamp(primaryColor, pickers.length).reverse();

                                    if( $("input.colorRamp-select").is(":checked") ){
                                        $("i#colorRampDirect").show();
                                        $("select.colorpicker-series").each(function(i,e){
                                            var picker = $(pickers[i]),
                                                color = pickerRamp[i];

                                            picker.css("background-color",color);
                                            
                                            if(i > 0){ 
                                                picker.css("pointer-events","none"); 
                                            };
                                        })

                                    }else{
                                        $("i#colorRampDirect").hide();
                                        $("select.colorpicker-series").each(function(i,e){
                                            var picker = $(pickers[i]),
                                                color = $(e).val();
                                            picker.css("background-color",color);
                                        });
                                        pickers.css("pointer-events","auto");
                                        
                                    }
                                    PubSub.publish('rebuild');

                                },


        //Shows/hides keyGrid UI opts if color domain/range > 1
        keyGrid:     function(){
                                    if(werk.config.color.domain.length > 1){
                                        $("#keyGrid").show();
                                    }else{
                                        $("#keyGrid").hide();
                                    }
                                },

        //Sets rebuild event on newly created UI elements
        resetEvents: function(){

                                    // unbind all the rebuild calls so we don't duplicate events
                                    $(".rebuild").off("change.rebuild");

                                    $(".rebuild").on("change.rebuild",function(){ 

                                        // PUBLISH ----->
                                        PubSub.publish('rebuild'); 

                                    });
                                },



    };



    ///////////////////////////////////////
    // Subscriptions /////////////////////////////
    //////////////////////////////////
    ///////////////////////////////////////////

    // Sets subscriptions on init
    (function(){
        PubSub.subscribe( 'rebuild', werk.buildConfig );
        PubSub.subscribe( 'rebuild.resetEvents', werk.UI.resetEvents );
        PubSub.subscribe( 'builtConfig', werk.UI.keyGrid );
    })();



    return werk;

});
