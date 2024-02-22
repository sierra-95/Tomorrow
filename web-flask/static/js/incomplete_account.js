function confirmQuit(decision) {
  document.getElementById("confirmQuitModal").style.display = "none";
  if (decision === 'yes') {
    var form = document.getElementById("confirmationForm");
    form.elements["decision"].value = "yes";
    form.submit();
  }
}
document.addEventListener("DOMContentLoaded", function () {
  setTimeout(function() {
      document.getElementById("confirmQuitModal").style.display = "block";
  }, 1000); // Add a delay to ensure modal is displayed after a short delay
});
