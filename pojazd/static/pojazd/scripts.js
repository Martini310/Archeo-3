
// Dynamically change the input letters to uppercase
function handleInput(e) {
    var ss = e.target.selectionStart;
    var se = e.target.selectionEnd;
    e.target.value = e.target.value.toUpperCase();
    e.target.selectionStart = ss;
    e.target.selectionEnd = se;
    }

function peselToBirthDate(element) {
    // Function to create birth date based on provided pesel and insert it to appropriate field
    var pesel = element.value
    if (pesel.length == 11){
        if (pesel[2] > 1) {
            var month = pesel.slice(2,4) - 20;
            if (month < 10) {
                month = '0' + month;
            }
        }
        else {
            var month = pesel.slice(2,4);
        }
        if (pesel[2] > 1) {
            var year = 2000 + Number(pesel.slice(0,2));
        }
        else {
            var year = 1900 + Number(pesel.slice(0,2));
        }
        var day = pesel.slice(4,6);
        var birth_date = year + '-' + month + '-' + day;
        var birthDateID = element.id.slice(0,-5) + 'birth_date';
        document.getElementById(birthDateID).value = birth_date;
    }
}


function checkMyOrderValues(e){
    // Function to check if values provided in all tr inputs are consist with the tr pattern
    // create a list with values from inputs
    const valuesFromInputs = [];
    // number of all rows
    let total_forms = document.getElementById("id_form-TOTAL_FORMS").value;
    // insert values from inputs to the list
    for (var x = 0; x < total_forms; x++) {
        var input_value = document.getElementById('id_form-' + x + '-tr').value;
        if (input_value.length > 0)
        {
            valuesFromInputs.push(input_value);
        } 
    }
    // tr pattern
    const trRegex = /^[A-Z]{1,3}\s[A-Z\d]{3,5}$|^[A-Z]\d\s[A-Z\d]{3,5}$/g;
    // Display a confirmation window if any value from inputs won't fit the pattern
    for (let value of valuesFromInputs)
    {
        if (value.search(trRegex) == -1) 
        {
            if(!confirm('Czy jesteś pewien, że numer rejestracyjny "' + value + '" jest poprawny?')) 
            {
                e.preventDefault();
            }
        }
    }
}


function addForm(e){
    // Add new rows to formset
    e.preventDefault()

    let newForm = birdForm[0].cloneNode(true)
    let formRegex = RegExp(`form-(\\d){1}-`,'g')

    formNum++
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
    container.insertBefore(newForm, Buttons)

    var lp = 'id_form-'+formNum+'-lp'
    document.getElementById(lp).innerHTML = formNum + 1
    
    totalForms.setAttribute('value', `${formNum+1}`)
}
    