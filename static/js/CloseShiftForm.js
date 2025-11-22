let totalAmount = 0;
let main = document.querySelector("#printuser");

function mousehover(eles) {
    eles.style.backgroundColor = "rgb(254, 169, 78)";
    eles.style.padding = "6px";
    eles.style.fontWeight = "bold";
}

function mouseout(eles) {
    eles.style.backgroundColor = "#f39c12"; // Updated to match new CSS
    eles.style.padding = "10px 25px"; // Reset to CSS padding
    eles.style.fontWeight = "normal";
}

function emptyCashForm() {
    let elemA = document.querySelector("#amount");
    let elemF = document.querySelector("#moneyForm"); 
    
    document.getElementById("total").value = "$";
    document.getElementById("amount").style.display = "none";
    
    // Clear cash inputs
    let money = document.getElementsByName("cash");
    for (let i = 0; i < money.length; i++) {
        money[i].value = "0";
    }
    document.getElementById("totalCashOverride").value = "";
}

function toggleCashMode() {
    const mode = document.querySelector('input[name="cashMode"]:checked').value;
    const inputs = document.getElementsByName("cash");
    
    inputs.forEach(input => {
        const denom = input.getAttribute('data-denom');
        if (mode === 'value') {
            input.placeholder = `$ Value`;
        } else {
            input.placeholder = `Count`;
        }
    });
}

function Calculate() {
    let total = 0;
    const override = document.getElementById("totalCashOverride").value;
    
    if (override && parseFloat(override) > 0) {
        total = parseFloat(override);
    } else {
        const mode = document.querySelector('input[name="cashMode"]:checked').value;
        const inputs = document.getElementsByName("cash");
        
        inputs.forEach(input => {
            const val = parseFloat(input.value) || 0;
            const denom = parseFloat(input.getAttribute('data-denom'));
            
            if (val > 0) {
                if (mode === 'count') {
                    total += val * denom;
                } else {
                    // Mode is value, just add the number
                    total += val;
                }
            }
        });
    }
    
    totalAmount = total;
    document.getElementById("total").value = "$" + totalAmount.toFixed(2);
    document.getElementById("amount").style.display = "block";
}

function getShift() {
    let shiftInfo = document.getElementsByName("Shift");
    for (let i = 0; i < shiftInfo.length; i++) {
        if (shiftInfo[i].checked) {
            return shiftInfo[i].value;
        }
    }
    return "";
}

// Net Sales #1+#2=Gross Sales
function A() {
    let NS = document.getElementsByName("netSale");
    let num1 = parseFloat(NS[0].value) || 0;
    let num2 = parseFloat(NS[1].value) || 0;
    return num1 + num2;
}

// [i]+[ii]+[iii]
function B() {
    let DT = document.getElementById("DebitTotal").value || 0;
    let GCU = document.getElementById("GCU").value || 0;
    return parseFloat(DT) + parseFloat(GCU) + iii();
}

// total cash-$200float
function C() {
    return totalAmount - 200;
}

function D() {
    return B() + C();
}

function E() {
    return D() - A();
}

function F() {
    let dts = parseFloat(document.getElementById("DebitTips").value) || 0;
    return dts * 0.02;
}

function G() {
    return E() - F();
}

function H() {
    return G() * 0.4;
}

function I() {
    return C() - G();
}

// TB Payment #1+ #2
function iii() {
    let TB = document.getElementsByName("TB");
    let num1 = parseFloat(TB[0].value) || 0;
    let num2 = parseFloat(TB[1].value) || 0;
    return num1 + num2;
}

function resetForm() {
    document.getElementById("myForm").reset();
    totalAmount = 0;
    document.getElementById("amount").style.display = "none";
    document.getElementById("printuser").style.display = "none";
    document.getElementById("form-input-view").style.display = "block";
}


function ProcessForm() {
    Calculate();

    let name = document.getElementById("FirstName").value;
    let date = document.getElementById("today").value;

    document.querySelector("#shift").innerHTML = getShift() + " shift";
    document.querySelector("#date1").innerHTML = date;
    document.querySelector("#staff").innerHTML = name;
    document.querySelector("#GrossSales").innerHTML = A().toFixed(3);
    document.querySelector("#TBP").innerHTML = iii().toFixed(3);
    document.querySelector("#B").innerHTML = B().toFixed(3);
    document.querySelector("#C").innerHTML = C().toFixed(3);
    document.querySelector("#D").innerHTML = D().toFixed(3);
    document.querySelector("#E").innerHTML = E().toFixed(3);
    document.querySelector("#F").innerHTML = F().toFixed(3);
    document.querySelector("#G").innerHTML = G().toFixed(3);
    document.querySelector("#H").innerHTML = H().toFixed(3);
    
    let temp = G() - H();
    document.querySelector("#G-H").innerHTML = temp.toFixed(3);
    document.querySelector("#I").innerHTML = I().toFixed(3);
    
    let check = (Math.abs((I() + B()) - (A() + F())) < 0.01); // Float comparison
    document.querySelector("#check").innerHTML = check;
    
    document.getElementById("form-input-view").style.display = "none";
    document.getElementById("printuser").style.display = "flex";
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function editForm() {
    document.getElementById("printuser").style.display = "none";
    document.getElementById("form-input-view").style.display = "block";
}