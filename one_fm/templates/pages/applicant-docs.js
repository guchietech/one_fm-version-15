window.frappe = {};
frappe.ready_events = [];
frappe.ready = function (fn) {
    frappe.ready_events.push(fn);
}
window.dev_server = {{dev_server}};
window.socketio_port = {{frappe.socketio_port}};

var front_civil , back_civil, front_passport, back_passport;
var is_kuwaiti = 0;
function front_civil_extract(input){
    let file = input.files[0];

    let reader = new FileReader();

    reader.readAsDataURL(file);

    reader.onload = function() {
      front_civil = reader.result;
      front_civil = front_civil.replace(/^data:image\/\w+;base64,/, "");
    };

    reader.onerror = function() {
      console.log(reader.error);
    };

};

function back_civil_extract(input){
    let file = input.files[0];
    let reader = new FileReader();

    reader.readAsDataURL(file);

    reader.onload = function() {
      back_civil = reader.result;
      back_civil = back_civil.replace(/^data:image\/\w+;base64,/, "");
    };

    reader.onerror = function() {
      console.log(reader.error);
    };
};

function front_passport_extract(input){
  let file = input.files[0];
  let reader = new FileReader();

  reader.readAsDataURL(file);

  reader.onload = function() {
    front_passport = reader.result;
    front_passport = front_passport.replace(/^data:image\/\w+;base64,/, "");
  };

  reader.onerror = function() {
    console.log(reader.error);
  };
};

function back_passport_extract(input){
  let file = input.files[0];
  let reader = new FileReader();

  reader.readAsDataURL(file);

  reader.onload = function() {
    back_passport = reader.result;
    back_passport = back_passport.replace(/^data:image\/\w+;base64,/, "");
  };

  reader.onerror = function() {
    console.log(reader.error);
  };
};
function test(input){
var date = input.value;
console.log(date)
}

function populate_nationality(){
  frappe.call({
    type: "GET",
    method: "one_fm.templates.pages.applicant-docs.populate_nationality",
    callback: function(r) {

      langArray = r.message;
      var select = document.getElementById("nationality");
      for (let i=0; i<=langArray.length;i++) {
        select.options[select.options.length] = new Option(langArray[i], langArray[i]);
     }
    }
  }); 
}

function fetchNationality(code){
  frappe.call({
    type: "GET",
    method: "one_fm.templates.pages.applicant-docs.fetch_nationality",
    args: {code :code},
    callback: function(r) {
      console.log(r)
      document.getElementById("nationality").value = r.message;
    }
  }); 
}
function upload(){
  populate_nationality()
  civilid_check = document.getElementById("noCivilID").checked;
  //civilid_check = document.getElementById("noPassport").checked;
  //front_civil , back_civil, front_passport, back_passport
<<<<<<< HEAD
  {/*
=======

>>>>>>> 4129a86a (Resolve Conflicts)
  if(!civilid_check){
    if (front_civil && back_civil){
      image = {front_side:front_civil, back_side:back_civil};
      frappe.call({
        type: "GET",
<<<<<<< HEAD
        method: "one_fm.templates.pages.applicant-docs.fetch_text_for_kuwaiti_civilid",
        args: {image :JSON.stringify(image)},
=======
        method: "one_fm.templates.pages.applicant-docs.get_civil_id_text",
        args: {images :JSON.stringify(image), is_kuwaiti: is_kuwaiti},
>>>>>>> 4129a86a (Resolve Conflicts)
        callback: function(r) {
          console.log(r)
          if(r && r.message){
            document.getElementById("finalForm").style.display = "block"; 
            document.getElementById("output_message").innerHTML = "Have a look at the following form and correct if any mistakes!";
            fill_form(r.message)
            console.log(r.message)
          }
          else{
            console.log("Error");
          }
        }
      });  
    };
  }
  else{
    document.getElementById("finalForm").style.display = "block";   
    document.getElementById("output_message").innerHTML = "Kindly fill in the following form and correct if any mistakes!";
  }
  */}
  
  console.log("End");
};


function fill_form(data){
  {/* This Function fills the output form for user to view.
  The value is fetched from the api*/}
  if(data == "Error"){
    alert("Sorry! Some Error Occured!!");
  }
  else {
    document.getElementById("name").value = data['front_text']['Name'];
    document.getElementById("ar_name").value = data['front_text']['Arabic Name'];
    document.getElementById("gender").value = data['front_text']['Gender']
    document.getElementById("civilid").value = data['front_text']['Civil ID No.']
    document.getElementById("country_code").value = data['front_text']['Nationality']
    fetchNationality(data['front_text']['Nationality'])
    document.getElementById("dob").value = data['front_text']['Date Of Birth']
    document.getElementById("civil_expiry_date").value = data['front_text']['Expiry Date']
    document.getElementById("paci_no").value = data['back_text']['PACI No.'] 
  }
};