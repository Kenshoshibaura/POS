var img=new Array();
var cnt1=3;

img[0]=new Image();
img[0].src="img/menu1.jpg"
img[1]=new Image();
img[1].src="img/menu2.jpg"
img[2]=new Image();
img[2].src="img/menu3.jpg"
img[3]=new Image();
img[3].src="img/menu4.jpg"
img[4]=new Image();
img[4].src="img/menu5.jpg"

function add(num){
  var qt=document.getElementsByClassName('qt');
  var sum1=document.getElementById('sum1');
  var sum2=document.getElementById('sum2');
  qt[num].innerHTML++;
  sum1.innerHTML++;
  sum2.innerHTML=set3fig(parseInt(sum1.innerHTML)*50);
}
function sub(num){
  var qt=document.getElementsByClassName('qt');
  var sum1=document.getElementById('sum1');
  var sum2=document.getElementById('sum2');
  if(parseInt(qt[num].innerHTML)>0){
  qt[num].innerHTML--;
  sum1.innerHTML--;}
  sum2.innerHTML=set3fig(parseInt(sum1.innerHTML)*50);
}

function addqta(){for(var i=0;i<3;i++){add(i);}}
function subqta(){for(var i=0;i<3;i++){sub(i);}}
