function updateDays(){
  today = new Date();
  for (i = 0; i < 6; i++){
    submission = document.getElementById("date[" + i + "]").innerHTML;
    dd = submission.substring(0,2);
    mm = submission.substring(3,5);
    yyyy = submission.substring(6,10);
    submissionDate = new Date(mm + "/" + dd + "/" + yyyy);
    diffTime = Math.abs(submissionDate.getTime() - today.getTime());
    diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    if (submissionDate.getTime() >= today.getTime()){
        days = "  days";
      }
    else{
        days = "  days overdue";
    }
    document.getElementById("dueDays[" + i + "]").innerHTML = diffDays + days;
  }
}
