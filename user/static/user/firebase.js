
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  const firebaseConfig = {
    apiKey: "AIzaSyC67owy0RTYrLNzXUIwBFfA345ZeVrCXB0",
    authDomain: "autoinvoice-b6618.firebaseapp.com",
    projectId: "autoinvoice-b6618",
    storageBucket: "autoinvoice-b6618.appspot.com",
    messagingSenderId: "695287461030",
    appId: "1:695287461030:web:ce6669e7174d119beab067",
    measurementId: "G-1SDM9KTEKY"

};
  
  
// Initialize Firebase
firebase.initializeApp(firebaseConfig);

function logout(event){
    firebase.auth().currentUser.signOut();
    console.log(user);
}


function sendEmailVerification() {
  // [START auth_send_email_verification]
  firebase.auth().currentUser.sendEmailVerification()
    .then(() => {
      alert("Email sent successfully");
      window.location.href = "http://127.0.0.1:8000/ftoken/";
    });
  // [END auth_send_email_verification]
}

function sendPasswordReset(event) {
  event.preventDefault();
  const email = document.getElementById('email').value;
  // [START auth_send_password_reset]
  firebase.auth().sendPasswordResetEmail(email)
    .then(() => {
        alert("Password Reset mail has been sent successfully");
      // Password reset email sent!
      // ..
    })
    .catch((error) => {
      var errorCode = error.code;
      var errorMessage = error.message;
      // ..
    });
  // [END auth_send_password_reset]
}