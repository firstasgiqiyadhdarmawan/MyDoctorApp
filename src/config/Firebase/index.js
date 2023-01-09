import * as firebase from 'firebase';

const firebaseConfig = {
  apiKey: 'AIzaSyBjVGaZUCESkBfIUwIFdNLKxP30LaoYyxQ',
  authDomain: 'mydoctorapp-90fb0.firebaseapp.com',
  projectId: 'mydoctorapp-90fb0',
  storageBucket: 'mydoctorapp-90fb0.appspot.com',
  messagingSenderId: '346006783356',
  appId: '1:346006783356:web:003a37eb3bd880f74950f9',
};

// Initialize Firebase
let app;
if (firebase.apps.length === 0) {
  app = firebase.initializeApp(firebaseConfig);
} else {
  app = firebase.app();
}

const auth = firebase.auth();

export {auth};
