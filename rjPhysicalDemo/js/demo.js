if (!String.prototype.format) {
  String.prototype.format = function(args) {
      if (arguments.length > 0) {
        var result = this;
        if (arguments.length == 1 && typeof(args) == "object") {
          for (var key in args) {
            var reg = new RegExp("({" + key + "})", "g");
            result = result.replace(reg, args[key]);
          }
        } else {
          for (var i = 0; i < arguments.length; i++) {
            if (arguments[i] == undefined) {
              return "";
            } else {
              var reg = new RegExp("({[" + i + "]})", "g");
              result = result.replace(reg, arguments[i]);
            }
          }
        }
        return result;
      } else {
        return this;
      }
  }
}

function stopPropagation(e) {  
  e = e || window.event;  
  if(e.stopPropagation) { //W3C阻止冒泡方法  
      e.stopPropagation();  
  } else {  
      e.cancelBubble = true; //IE阻止冒泡方法  
  }  
}

layui.use(['dropdown', 'util', 'layer', 'table'], function(){
  var dropdown = layui.dropdown
  ,util = layui.util
  ,layer = layui.layer
  ,table = layui.table
  ,$ = layui.jquery;

  var segment_data = {}

  function build_display(key, display, segments, parents, olabels){
      var format_data = {}
      segments.forEach(function(s){
          var slabel = JSON.parse(JSON.stringify(parents));
          var olabel = JSON.parse(JSON.stringify(olabels));
          slabel.push(s.label);
          var _class = ["segment"]

          var val = s.value
          var just_click_it = false;
          switch(s.type){
              case "TEXT":
                  val = '{0}<input type="text" class="defaultInput" value="{1}" />{2}'.format(s.freetextPrefix, val, s.freetextPostfix);
                  _class.push("input");
                  break;
              case "RADIO":
                  if (s.options.length == 2){
                    just_click_it = true;
                  }
              case "CHECKBOX":
                  if (Array.isArray(val)){
                      var display_val = []
                      s.options.forEach(function(o){
                          if(val.indexOf(o.value)>-1){
                              if (o.hasOwnProperty("addition") && o.addition){
                                olabel.push(o.label);
                                display_val.push('<span class="{0}">{1}</span>'.format(o.props.color, build_display(key, o.display, o.addition, slabel, olabel)))
                                olabel = JSON.parse(JSON.stringify(olabels));
                              } else{
                                display_val.push('<span class="{0}">{1}</span>'.format(o.props.color, o.display))
                              }
                          }
                      });
                      
                      val = display_val.join('、')
                  }
                  break;
          }
          format_data[s.label] = '<span key="{0}" label="{1}" olabel="{2}" type="{3}" class="{4}" {5}>{6}</span>'.format(key, slabel.join('__'), olabel.join('__'), s.type, _class.join(" "), just_click_it?"jci":"", val);

          segment_data[slabel.join('__')] = s
      });

      return display.format(format_data);
  }



  function build_selector(elemPanel, elem){
    var key = $(elem).attr("key");
    var label = $(elem).attr("label");
    var label_path = label.split('__');
    var olabel = $(elem).attr("olabel");
    var olabel_path = olabel.split('__');
    var type = segment_data[label].type;
    var options = segment_data[label].options;
    var vals = segment_data[label].value;

    var type_html='';
    switch(type){
      case "TEXT":

        break;
      case "RADIO":
        options.forEach(function(o){
          var is_checked = vals.indexOf(o.value)>-1?"checked":"";
          type_html+='<input type="radio" name="{0}" value="{1}" title="{2}" {3}>{2}'.format(label, o.value, o.label, is_checked)
        });
        break;
      case "CHECKBOX":
        options.forEach(function(o){
          var is_checked = vals.indexOf(o.value)>-1?"checked":"";
          type_html+='<input type="checkbox" lay-skin="primary" name="{0}" value="{1}" title="{2}" {3}>{2}'.format(label, o.value, o.label, is_checked)
        });
        break;
    }
    
    $(elemPanel).find('.selector').html([
      '<div class="selector-header">'
        , '<b>'+label_path[label_path.length-1]+'</b>'
      ,'</div>'
      ,'<div class="selector-content">'
        ,'<div>'
          ,type_html
        ,'</div>'
      ,'</div>'
      ,'<div class="selector-bottom">'
        ,'<button type="button" class="layui-btn layui-btn-sm layui-btn-normal submit-btn" style="float: right;">确认</button>'
      ,'</div>'].join('')
    );

    $(elemPanel).find('.submit-btn').unbind('click').click(function(){
      var segments = null;
      if (key.indexOf('custom__') == 0){
        key_split = key.split('__');
        segments = data[key_split[0]][key_split[1]].segments;
      } else{
        segments = data[key].segments;
      }
      for (var i=0;i<segments.length;i++){
        var plabel = segments[i].label;
        var ptype = segments[i].type;
        console.log(plabel, label);
        if (plabel == label || label_path[0] == plabel){
          switch(ptype){
            case "TEXT":
      
              break;
            case "RADIO":
            case "CHECKBOX":
              var pval = [];
              $(elemPanel).find('input:checked[name="'+ label +'"]').each(function(){
                pval.push(this.value);
              });
              if (label_path.length > 1){
                var option_index = -1;
                for (var o=0;o<segments[i].options.length;o++){
                  if (olabel_path[0] == segments[i].options[o].label){
                    option_index = o;
                    break;
                  }
                }

                var addtion_index = -1;
                for (var a=0;a<segments[i].options[option_index].addition.length;a++){
                  if (label_path[1] == segments[i].options[option_index].addition[a].label){
                    addtion_index = a;
                    break;
                  }
                }

                segments[i].options[option_index].addition[addtion_index].value = pval; //暂仅支持到第二层
              } else {
                segments[i].value = pval;
              }
              
              $(elemPanel).remove();
              render();
              break;
          }
          break;
        }  
      }
    });

  }

  function render(){
    var m_display = data.medical_history.display;
    var m_segments = data.medical_history.segments;
    var medical_history = build_display("medical_history", m_display, m_segments, [], []);
    $("#medical_history").html(medical_history);

    var p_display = data.physical.display;
    var p_segments = data.physical.segments;
    var physical = build_display("physical", p_display, p_segments, [], []);
    $("#physical").html(physical);

    for (var i=0; i<data.custom.length; i++){
      var custom_id = "custom__"+ i;
      var c_title = data.custom[i].title;
      var c_display = data.custom[i].display;
      var c_segments = data.custom[i].segments;
      $("body").append('<br><div>'+ c_title +'<p id="'+ custom_id +'"></p></div>');
      var custom = build_display(custom_id, c_display, c_segments, [], []);
      $("#"+custom_id).html(custom);
    }
    

    $("input").unbind('click').click(function(){
      stopPropagation();
    });

    dropdown.render({
      elem: '.segment:not(.input):not("[jci]")'
      ,content: '<div class="selector"></div>'
      ,style: 'padding: 5px 15px; box-shadow: 1px 1px 30px rgb(0 0 0 / 12%);'
      ,ready: function(elemPanel, elem){
        stopPropagation();
        build_selector(elemPanel, elem);
      }
    });

    $(".segment[jci]").unbind('click').click(function(){
      that = $(this);
      var key = that.attr("key");
      var label = that.attr("label");
      var label_path = label.split('__');
      var olabel = that.attr("olabel");
      var olabel_path = olabel.split('__');
      var type = segment_data[label].type;
      var options = segment_data[label].options;
      var vals = segment_data[label].value;

      var segments = null;
      if (key.indexOf('custom__') == 0){
        key_split = key.split('__');
        segments = data[key_split[0]][key_split[1]].segments;
      } else{
        segments = data[key].segments;
      }

      options.forEach(function(o){
        var is_checked = vals.indexOf(o.value)>-1;
        if (!is_checked){
          for (var i=0;i<segments.length;i++){
            var plabel = segments[i].label;
            var ptype = segments[i].type;
            console.log(plabel, label);
            if (plabel == label || label_path[0] == plabel){
              if (label_path.length > 1){
                var option_index = -1;
                for (var op=0;op<segments[i].options.length;op++){
                  if (olabel_path[0] == segments[i].options[op].label){
                    option_index = op;
                    break;
                  }
                }

                var addtion_index = -1;
                for (var a=0;a<segments[i].options[option_index].addition.length;a++){
                  if (label_path[1] == segments[i].options[option_index].addition[a].label){
                    addtion_index = a;
                    break;
                  }
                }

                segments[i].options[option_index].addition[addtion_index].value = [o.value]; //暂仅支持到第二层
              } else {
                segments[i].value = [o.value];
              }
            }
          }
          render();
        }
      });

    });
  }

  
  render();

});

