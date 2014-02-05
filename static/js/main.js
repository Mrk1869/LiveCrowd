var canvasHeight = $(".floor-background").height();
var canvasWidth = $(".floor-background").width();
var last_froyer = 0
var last_showroom = 0

// param
var scale_param = 10.0
var timer_delay = 10.0;
var max_count = 15.0;

$(function(){
  canvasHeight = $(".floor-background").height();
  canvasWidth = $(".floor-background").width();
  $("#graph").attr({height:canvasHeight});
  $("#graph").attr({width:canvasWidth});
//  var url =location.href;
//  var param = url.substring(url.lastIndexOf("/")+1,param);
//  (param != "")? scale_param = param : 100;
});

var ws = new WebSocket('ws://192.168.31.215:8000/data/');
ws.onmessage = function(evt) {
  var json = JSON.parse(evt.data);
  var froyer = parseFloat(json.froyer);
  var showroom = parseFloat(json.showroom);

  (froyer > max_count)? froyer = max_count : froyer;
  (showroom > max_count)? showroom = max_count : showroom;

  var timer;
  var count = 0;
  var delta_froyer = (froyer - last_froyer)/(1000.0/timer_delay);
  var delta_showroom = (showroom - last_showroom)/(1000.0/timer_delay);
  var tmp_froyer = last_froyer;
  var tmp_showroom = last_showroom;
  last_froyer = froyer;
  last_showroom = showroom;

  if (delta_froyer != 0 || delta_showroom != 0){
    var loop = function(){
      tmp_froyer = tmp_froyer + delta_froyer
      tmp_showroom = tmp_showroom + delta_showroom
      clearCanvas();
      drawCircle(220, 160, Math.pow(tmp_froyer, (2/3))*2*scale_param);
      drawCircle(200, 350, Math.pow(tmp_showroom, (2/3))*2*scale_param);
      clearTimeout(timer);
      count += 1
      if (count < (1000.0/timer_delay)){
        timer = setTimeout(loop, timer_delay);
      }
    }
    loop();
  }
};

function clearCanvas(){
  var canvas = $("#graph")[0];
  var ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, 800, 600);
}

function drawCircle(x, y, r){
  var canvas = $("#graph")[0];
  var ctx = canvas.getContext('2d');
  ctx.beginPath();
  ctx.fillStyle = getColor(r);
  ctx.arc(x, y, r, 0, Math.PI*2, true);
  ctx.stroke();
  ctx.fill();
}

function getColor(r){
  h = 150 - 20 * (r/max_count - 1);
  s = 0.8;
  v = 0.7;
  rgb =  hsv2rgb(h, s, v);
  return "rgba("+rgb[0]+","+rgb[1]+","+rgb[2]+",0.7)"
}

function hsv2rgb(h, s, v){
  while (h < 0)
    h += 360;
  h %= 360;
  if (+s === 0) {
    v *= 255;
    return [ v, v, v ];
  }
  var hi = +(h / 60 >> 0);
  var f = h / 60 - hi;
  var p = v * (1 - s);
  var q = v * (1 - f * s);
  var t = v * (1 - (1 - f) * s);
  var rgb = [ 1, 1, 1 ];
  if (hi === 0)
    rgb = [ v, t, p ];
  else if (hi === 1)
    rgb = [ q, v, p ];
  else if (hi === 2)
    rgb = [ p, v, t ];
  else if (hi === 3)
    rgb = [ p, q, v ];
  else if (hi === 4)
    rgb = [ t, p, v ];
  else if (hi === 5)
    rgb = [ v, p, q ];
  rgb[0] = rgb[0] * 255 >> 0;
  rgb[1] = rgb[1] * 255 >> 0;
  rgb[2] = rgb[2] * 255 >> 0;
  return rgb;
};

