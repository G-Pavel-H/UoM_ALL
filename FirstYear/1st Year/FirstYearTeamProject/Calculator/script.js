var op;
var preVal;
var postVal;
var calculation = false;
function updateRes(a){
  var result = document.getElementById('result');
  result.value = result.value  + a;
  if(calculation){
    postVal = result.value;
  }
  else{
    preVal = result.value;
  }
}

function clearRes(){
  result.value = "";
}

function operation(operand){
  op = operand;
  calculation = true;
  result.value = "";
}
function percentage(){
  result.value = result.value / 100;
  preVal = result.value;
}
function execute(){
  postVal = result.value;
  switch(op){
    case '+':
    result.value = Number(preVal) + Number(postVal);
    calculation = false;
    preVal = result.value;
    break;
    case '-':
    result.value = Number(preVal) - Number(postVal);
    calculation = false;
    preVal = result.value;
    break;
    case '*':
    result.value = Number(preVal) * Number(postVal);
    calculation = false;
    preVal = result.value;
    break;
    case '/':
    result.value = Number(preVal) / Number(postVal);
    calculation = false;
    preVal = result.value;
    break;
  }
}
