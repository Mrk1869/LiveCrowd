$(function(){

});

var ws = new WebSocket('ws://localhost:8000/data');
ws.onmessage = function(evt) {
  var json = JSON.parse(evt.data);
  var val_a = parseInt(json.val_a);
  var val_b = 60 - val_a;

  clearCanvas();
  drawCircle(480, 200, val_a);
  drawCircle(230, 270, val_b);

};

function clearCanvas(){
  var canvas = $("#graph")[0];
  var ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, 800, 400);
}

function drawCircle(x, y, r){
  var canvas = $("#graph")[0];
  var ctx = canvas.getContext('2d');
  ctx.beginPath();
  ctx.fillStyle = getColor(r);
  ctx.arc(x, y, r, 0, Math.PI*2, true);
  ctx.fill();
}

function getColor(r){
  return 'rgba('+r*4+', 80, 77, 0.7)';
}
