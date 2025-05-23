function isNumber(evt) {
  var charCode = (evt.which) ? evt.which : evt.keyCode;
  if (charCode < 48 || charCode > 57)
      return false;
  return true;
}
function convertCaps(evt) {
  var inp = evt.target;
  inp.value = inp.value.toUpperCase();
  }


// submit-reg form
const form_ = document.getElementById("form1");
if(form_ && form_.id==='form1'){
form_.addEventListener('submit', async function(event) {
  event.preventDefault();
  const form = event.target;
  const formData = new FormData(form);
  const responseDiv = document.getElementById('response');
  try {
    const response = await fetch('/submit', {
        method: 'POST',
        body: formData
    });
    if (!response.ok) {
        throw new Error('ROLL NO. EXISTS ALREADY!');
    }
    const data = await response.json();
    responseDiv.style.boxShadow = "inset 0 0 0 5px teal";
    responseDiv.textContent = `Success: ${data.message}`;
    alert(`${data.message}`)
} catch (error) {
     log(`${error.message}`)
}
});
}

// search roll and delete record
const form2 = document.getElementById("form2");
if (form2 && form2.id === 'form2') {
      form2.addEventListener('submit', async function(event) {
          event.preventDefault();
          const formData_2 = new FormData(form2);
        
          try {
              const response = await fetch('/rollvalidate_and_delete', {
                  method: 'POST',
                  body: formData_2
              });
              if (!response.ok) {
                  throw new Error('DB ERROR');
              }
              const data = await response.json();
              if (data.flag === 1) {
                // elem1 = document.getElementById('edit-section')
                // document.getElementById('selected').innerHTML="CURRENT ROLLNUM SELECTED :" + data.rnum
                  // elem1.classList.remove('hidden')
                alert(`RECORD ${data.rnum} DELETED`);
              
              } else {
                  alert('ROLL NUM NOT FOUND');
              }
          } catch (error) {
              alert(`${error.message}`);
          }
      });
  }


// in edit-section rnum -guide indicating record availabilty
function insertrnum(){
    const elem = document.getElementById('r-edit');
    let val = elem.value;
    e1 = document.getElementById('rnum');
    e1.innerHTML = val;} 

document.getElementById('r-edit').addEventListener('keyup', async (event) => {
    insertrnum();
    const elem = event.target;
    if(elem.value===""){hideSection();
    }
    else{
    const exists = await rollExist(event);
    if (exists) {
        showSection();
    } else {
        hideSection();
    }
}
});
async function rollExist(e) {
    const val = document.getElementById('r-edit').value;
    const response = await fetch('/search-roll', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
      },
        body: JSON.stringify({ value: val })
    });
    const data = await response.json();
    if(data.flag===1){
        return true;
    }
    {
        return false;
    }
}


// searchRecord and view-individually or view-entirely
async function searchRecord() {
    const val = document.getElementById('val').value;
    const response = await fetch('/search-record', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
      },
        body: JSON.stringify({ value: val })
    });

    const data = await response.json();
    displayResults(data,`RESULTS FOR "${val}"`);
}

async function viewAllRecords() {
    const response = await fetch('/view-all-records', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const data = await response.json();
    displayResults(data,'RESULTS FOR "ALL RECORDS:"');
}

function displayResults(data,title) {
  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = `${title}`;    //overwriting the div
  for (const className in data) {
      let sectionTable = `<h2>Class ${className}</h2>
              <table border="1">
                  <thead>
                      <tr>
                          <th>Name</th>
                          <th>Roll Number</th>
                          <th>Section</th>
                          <th></th>
                      </tr>
                  </thead>
                  <tbody>`;
      for (const section in data[className]) {
          sectionTable += `
                      ${data[className][section].map(student => 
                        ` <tr>
                              <td>${student.name}</td>
                              <td>${student.roll}</td>
                              <td>${section}</td>
                              <td><a href="/edit?roll=${student.roll}" id="a-load">EDIT</a></td>
                          </tr>
                          <br>
                      `).join('')}`;
      }
       sectionTable += `</tbody> </table>`;
      resultsDiv.innerHTML += (sectionTable);
  }
}
// preload with rollnum on redirection-to-edit
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}
document.addEventListener('DOMContentLoaded', () => {
    const roll = getQueryParam('roll');
    if (roll) {
        document.getElementById('r-edit').value = roll;
        showSection();
        insertrnum();
    }
});



// update-records
document.getElementById('up-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const roll = document.getElementById('roll-section').value.trim();
    const name = document.getElementById('name-section').value.trim();
    const studClass = document.getElementById('section-section').value.trim();
    const section = document.getElementById('section-section').value.trim();

    if (!roll && !name && !studClass && !section) {
        alert('Please fill at least one field to update.');
        return;
    }
    const formData = new FormData(e.target);
    fetch('/update-record', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        
        if (data.success) {
            alert(data.message);
            window.location.href = '/edit'

        }
        else{
            alert('ROll num exists already...');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('ROll num exists already...');
    });
});




// show and hide sections of edit by clicking radio
function showSection() {   
    let section = document.getElementById("hid")
      section.classList.remove('hidden');
  }
function hideSection() {  
    
    let section = document.getElementById("hid")
      section.classList.add('hidden');
  }