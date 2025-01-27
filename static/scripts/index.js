document.addEventListener('DOMContentLoaded', (event) => {
    function checkForValidName(name) {
      const pattern = /^[a-zA-Z][a-zA-Z0-9_]{2,15}$/;
      console.log(pattern.test(name))
      return pattern.test(name);
    }
  
    function onClickEvent() {
      const userLastNameBox = document.getElementById("lName");
      const userFirstNameBox = document.getElementById("fName");
      const userFirstName = userFirstNameBox.value;
      const userLastName = userLastNameBox.value;
      if (checkForValidName(userFirstName) && checkForValidName(userLastName)) {
        alert("Thanks for your application!");
      } else {
        alert("Something is wrong with the input fields");
      }
    }
  
    const submitBTN = document.getElementById("submit-btn");
    submitBTN.addEventListener("click", onClickEvent);
  });