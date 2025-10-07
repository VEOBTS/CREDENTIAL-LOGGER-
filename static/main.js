document.addEventListener("DOMContentLoaded", function(){
  const acceptBtn = document.getElementById("acceptBtn");
  const consentBox = document.getElementById("consentBox");
  const loginForm = document.getElementById("loginForm");
  const screenField = document.getElementById("screenField");
  const tzField = document.getElementById("tzField");
  const msgEl = document.getElementById("loginMessage");

  if(acceptBtn){
    acceptBtn.addEventListener("click", function(){
      consentBox.classList.add("hidden");
      if(loginForm) loginForm.classList.remove("hidden");
      if(screenField) screenField.value = screen.width + "x" + screen.height;
      if(tzField) tzField.value = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
    });
  }

  // optional: display small confirmation locally if element exists
  if(msgEl){
    setTimeout(()=> { msgEl.classList.remove("hidden"); }, 300);
  }
});
