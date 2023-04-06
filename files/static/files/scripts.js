
// Dynamically change the input letters to uppercase
function handleInput(e) {
    var ss = e.target.selectionStart;
    var se = e.target.selectionEnd;
    e.target.value = e.target.value.toUpperCase();
    e.target.selectionStart = ss;
    e.target.selectionEnd = se;
    }


function clicked(e)
{
    // create a list with values from inputs
    const valuesFromInputs = [];
    let total_forms = document.getElementById("id_form-TOTAL_FORMS").value;
    for (var x = 0; x < total_forms; x++) {
        var input_value = document.getElementById('id_form-' + x + '-tr').value;
        if (input_value.length > 0)
        {
            valuesFromInputs.push(input_value);
        } 
    }
    const trRegex = /^[A-Z]{1,3}\s[A-Z\d]{3,5}$|^[A-Z]\d\s[A-Z\d]{3,5}$/g;
    /* Display a confirmation window if any of values from inputs won't fit a pattern */
    for (let value of valuesFromInputs)
    {
        console.log(value + "|   |" + trRegex.test(value) + "|   |" + value.search(trRegex))
        if (value.search(trRegex) == -1) 
        {
            if(!confirm('Czy jesteś pewien, że numer rejestracyjny "' + value + '" jest poprawny?')) 
            {
                e.preventDefault();
            }
        }
    }
}


// Adding new fields to formset
let birdForm = document.querySelectorAll("#tr-div")
let container = document.querySelector("#form-container")
let addButton = document.querySelector("#add-form")
let totalForms = document.querySelector("#id_form-TOTAL_FORMS")

let formNum = birdForm.length-1
addButton.addEventListener('click', addForm)

function addForm(e){
    e.preventDefault()

    let newForm = birdForm[0].cloneNode(true)
    let formRegex = RegExp(`form-(\\d){1}-`,'g')

    formNum++
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
    container.insertBefore(newForm, addButton)

    var lp = 'id_form-'+formNum+'-lp'
    console.log(lp)
    document.getElementById(lp).innerHTML = formNum + 1
    
    totalForms.setAttribute('value', `${formNum+1}`)
}
