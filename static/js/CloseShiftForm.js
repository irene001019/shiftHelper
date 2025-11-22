let totalAmount=0;
let main= document.querySelector("#printuser");

function mousehover(eles){
eles.style.backgroundColor= "rgb(254, 169, 78)";
eles.style.padding= "6px";
eles.style.fontWeight="bold";    
}

function mouseout(eles){
eles.style.backgroundColor= "rgb(253, 220, 178)";
eles.style.padding= "5px";
eles.style.fontWeight="normal";
}

function emptyCashForm(){
document.getElementById("myForm").reset();
let elemA= document.querySelector("#amount");
let elemF= document.querySelector("#moneyForm");
totalAmount=0;
elemF.style.display="";
elemA.style.display="none";
}

function Calculate()
{
    let elemA= document.querySelector("#amount");
    let elemF= document.querySelector("#moneyForm");
    elemF.style.display="none";
    elemA.style.display="";
    let money= document.getElementsByName("cash");
    for(let i = 0; i< money.length; i++){
        let num= parseInt(money[i].value, 10)
        if(num!==0){
            if(i===0){
                totalAmount+= 100*num;
            }else if(i===1){
                totalAmount+= 50*num;
            }else if(i===2){
                totalAmount+= 20*num;
            }else if(i===3){
                totalAmount+= 10*num;
            }else if(i===4){
                totalAmount+= 5*num;
            }else if(i===5){
                totalAmount+= 2*num;
            }else if(i===6){
                totalAmount+= num;
            }else if(i===7){
                totalAmount+= 0.25*num;
            }else if(i===8){
                totalAmount+= 0.10*num;
            }else if(i===9){
                totalAmount+= 0.05*num;
            }
        }
    }
    document.getElementById("total").value="$"+totalAmount.toFixed(2);
}

function getShift(){
    let shiftInfo= document.getElementsByName("Shift");
    let shift="";
    for(let i=0;i<shiftInfo.length;i++)
    {
        if(shiftInfo[i].checked)
        {
            return shiftInfo[i].value;
        }
    }
}

//Net Sales #1+#2=Gross Sales
function A(){
    let NS= document.getElementsByName("netSale");
    let num1= parseFloat(NS[0].value, 10);
    let num2= parseFloat(NS[1].value, 10);
    return num1+num2;
}

//[i]+[ii]+[iii]
function B(){
    let DT= document.getElementsByName("DebitTotal");
    let GCU= document.getElementsByName("GCU");
    let i = parseFloat(DT[0].value, 10); 
    let ii = parseFloat(GCU[0].value, 10); 
    return i+ ii+ iii();
}

//total cash-$200float
function C(){
    return totalAmount-200;
}

function D(){
    return B()+C();
}

function E(){
    return D()-A();
}

function F(){
    let DTs= document.getElementsByName("DebitTips");
    let dts= parseFloat(DTs[0].value, 10);
    return dts*0.02;
}

function G()
{
    return E()-F();
}

function H()
{
    return G()*0.4;
}

function I(){
    return C()-parseFloat(G(), 10);
}

//TB Payment #1+ #2
function iii(){
    let TB= document.getElementsByName("TB");
    let num1= parseFloat(TB[0].value, 10);
    let num2= parseFloat(TB[1].value, 10);
    return num1+num2;
}

function resetForm(){
    document.getElementById("myForm").reset();
    totalAmount=0;
    let elemA= document.querySelector("#amount");
    let elemF= document.querySelector("#moneyForm");
    elemF.style.display="";
    elemA.style.display="none";

    let elem1= document.querySelector("#formArea");
    elem1.style.display="";
    main.style.display="none";

    let sub= document.querySelector("#sub");
    sub.style.display= "";
}


function ProcessForm(){
     main.style.display="";
    let nameElem= document.getElementsByName('name');
    let date= document.getElementById("today").value;
    const fn= nameElem[0].value;

    document.querySelector("#shift").innerHTML=getShift()+" shift";
    document.querySelector("#date1").innerHTML=date;
    document.querySelector("#staff").innerHTML= fn;
    document.querySelector("#GrossSales").innerHTML=A().toFixed(3);
    document.querySelector("#TBP").innerHTML= iii().toFixed(3);
    document.querySelector("#B").innerHTML= B().toFixed(3);
    document.querySelector("#C").innerHTML= C().toFixed(3);
    document.querySelector("#D").innerHTML= D().toFixed(3);
    document.querySelector("#E").innerHTML= E().toFixed(3);
    document.querySelector("#F").innerHTML= F().toFixed(3);
    document.querySelector("#G").innerHTML= G().toFixed(3);
    document.querySelector("#H").innerHTML= H().toFixed(3);
    let temp=G()-H();
    document.querySelector("#G-H").innerHTML= temp.toFixed(3);
    document.querySelector("#I").innerHTML= I().toFixed(3);
    document.querySelector("#check").innerHTML= ((I()+B())==(A()+F()));  
}